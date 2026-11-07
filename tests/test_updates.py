"""Comparación de versiones y consulta de releases (sin red real)."""

from __future__ import annotations

import json
import os
import sys
import tempfile
import threading
import unittest
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from unittest.mock import patch

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

_XDG = tempfile.TemporaryDirectory()
os.environ.setdefault("XDG_CONFIG_HOME", str(Path(_XDG.name) / "xdg"))

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from PySide6.QtGui import QDesktopServices  # noqa: E402
from PySide6.QtWidgets import QApplication, QMessageBox  # noqa: E402

import pasaporte.ui as ui  # noqa: E402
from pasaporte.constants import APP_VERSION  # noqa: E402
from pasaporte.updates import (  # noqa: E402
    UpdateError,
    is_newer,
    latest_release,
    parse_version,
)


class VersionOrderTests(unittest.TestCase):
    def test_newer_beta(self) -> None:
        self.assertTrue(is_newer("0.1.0-beta.2", "0.1.0-beta.1"))
        self.assertFalse(is_newer("0.1.0-beta.1", "0.1.0-beta.2"))

    def test_numeric_identifiers_compare_as_numbers(self) -> None:
        self.assertTrue(is_newer("0.1.0-beta.10", "0.1.0-beta.9"))

    def test_stable_beats_its_prerelease(self) -> None:
        self.assertTrue(is_newer("0.1.0", "0.1.0-beta.1"))
        self.assertFalse(is_newer("0.1.0-beta.1", "0.1.0"))

    def test_higher_core_beats_prerelease(self) -> None:
        self.assertTrue(is_newer("0.2.0", "0.1.0-beta.1"))
        self.assertTrue(is_newer("1.0.0-rc.1", "0.9.9"))

    def test_same_version_is_not_newer(self) -> None:
        self.assertFalse(is_newer("0.1.0-beta.1", "0.1.0-beta.1"))

    def test_v_prefix_accepted(self) -> None:
        self.assertEqual(
            parse_version("v0.1.0-beta.1"), parse_version("0.1.0-beta.1")
        )

    def test_invalid_version_rejected(self) -> None:
        with self.assertRaises(ValueError):
            parse_version("latest")


_RELEASES = [
    {"tag_name": "v0.3.0", "draft": True, "prerelease": False,
     "html_url": "https://example.test/draft"},
    {"tag_name": "v0.2.0-beta.1", "draft": False, "prerelease": True,
     "html_url": "https://example.test/beta"},
    {"tag_name": "v0.1.0", "draft": False, "prerelease": False,
     "html_url": "https://example.test/stable"},
]


class _Handler(BaseHTTPRequestHandler):
    status = 200
    body = b""

    def do_GET(self) -> None:  # noqa: N802
        self.send_response(type(self).status)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(type(self).body)

    def log_message(self, *args) -> None:
        pass


class LatestReleaseTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.httpd = HTTPServer(("127.0.0.1", 0), _Handler)
        cls.url = f"http://127.0.0.1:{cls.httpd.server_port}/releases"
        threading.Thread(target=cls.httpd.serve_forever, daemon=True).start()

    @classmethod
    def tearDownClass(cls) -> None:
        cls.httpd.shutdown()
        cls.httpd.server_close()

    def _serve(self, status: int, payload) -> None:
        _Handler.status = status
        _Handler.body = json.dumps(payload).encode("utf-8")

    def test_skips_drafts_and_returns_newest_prerelease(self) -> None:
        self._serve(200, _RELEASES)
        info = latest_release(self.url, include_prereleases=True)
        self.assertEqual(info.version, "0.2.0-beta.1")
        self.assertEqual(info.url, "https://example.test/beta")

    def test_stable_only_skips_prereleases(self) -> None:
        self._serve(200, _RELEASES)
        info = latest_release(self.url, include_prereleases=False)
        self.assertEqual(info.version, "0.1.0")

    def test_empty_list_returns_none(self) -> None:
        self._serve(200, [])
        self.assertIsNone(latest_release(self.url))

    def test_http_error_raises(self) -> None:
        self._serve(500, {"message": "boom"})
        with self.assertRaises(UpdateError):
            latest_release(self.url)

    def test_unexpected_payload_raises(self) -> None:
        self._serve(200, {"message": "rate limit"})
        with self.assertRaises(UpdateError):
            latest_release(self.url)


class UpdateMenuTests(unittest.TestCase):
    app = None

    @classmethod
    def setUpClass(cls) -> None:
        cls.app = QApplication.instance() or QApplication([])

    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        config = Path(self.tmp.name) / "hosts.json"
        config.write_text("[]", encoding="utf-8")
        self.window = ui.MainWindow(config)
        self.window.show()
        self.app.processEvents()

    def tearDown(self) -> None:
        self.window.close()
        self.window.deleteLater()
        self.app.processEvents()
        self.tmp.cleanup()

    def test_error_shows_warning(self) -> None:
        with patch.object(ui.QMessageBox, "warning") as warning:
            self.window._on_update_result("", "", "HTTP 500")
        warning.assert_called_once()
        self.assertIn("HTTP 500", warning.call_args.args[2])

    def test_no_newer_version_shows_information(self) -> None:
        with patch.object(ui.QMessageBox, "information") as info:
            self.window._on_update_result(APP_VERSION, "", "")
        info.assert_called_once()

    def test_newer_version_offers_download(self) -> None:
        with patch.object(
            ui.QMessageBox, "exec", return_value=0
        ), patch.object(ui.QDesktopServices, "openUrl") as open_url:
            self.window._on_update_result("9.9.9", "https://example.test", "")
        # Sin clic en el botón de descarga no se abre el navegador.
        open_url.assert_not_called()
        self.assertTrue(self.window.update_action.isEnabled())

    def test_check_is_ignored_while_running(self) -> None:
        started = []

        class _Running:
            def isRunning(self) -> bool:
                return True

            def start(self) -> None:
                started.append(True)

        self.window._update_thread = _Running()
        try:
            self.window.check_for_updates()
            self.assertEqual(started, [])
        finally:
            self.window._update_thread = None


if __name__ == "__main__":
    unittest.main()
