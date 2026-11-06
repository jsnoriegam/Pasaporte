"""Tests de la migración guiada al arrancar."""

from __future__ import annotations

import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from PySide6.QtWidgets import QApplication  # noqa: E402

import pasaporte.ui as ui  # noqa: E402
from pasaporte.paths import ConfigTarget  # noqa: E402


class MigrationTests(unittest.TestCase):
    app = None

    @classmethod
    def setUpClass(cls) -> None:
        cls.app = QApplication.instance() or QApplication([])

    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.xdg = self.root / "xdg"
        self.env = patch.dict(
            os.environ,
            {
                "XDG_CONFIG_HOME": str(self.xdg),
                "VPN_CONFIG": "",
            },
        )
        self.env.start()

        self.legacy = self.xdg / "vpn" / "hosts.json"
        self.legacy.parent.mkdir(parents=True, exist_ok=True)
        self.legacy.write_text(
            json.dumps(
                [
                    {
                        "name": "Legacy",
                        "host": "legacy.example.com",
                        "username": "u",
                    }
                ]
            ),
            encoding="utf-8",
        )
        self.canonical = self.xdg / "pasaporte" / "hosts.json"
        self.window = None

    def tearDown(self) -> None:
        if self.window is not None:
            self.window.close()
            self.window.deleteLater()
            self.app.processEvents()
        self.env.stop()
        self.tmp.cleanup()

    def _make_window(self, choice: str):
        target = ConfigTarget(
            self.canonical, explicit=False, canonical=True
        )
        with patch.object(
            ui.MainWindow, "_ask_migration", return_value=choice
        ):
            self.window = ui.MainWindow(target)
        self.window.show()
        self.app.processEvents()
        return self.window

    def test_import_migrates(self) -> None:
        window = self._make_window("import")

        self.assertTrue(self.canonical.exists())
        self.assertEqual(window.config_path, self.canonical)
        self.assertFalse(window._read_only)
        self.assertEqual(len(window.servers), 1)
        self.assertEqual(window.servers[0].name, "Legacy")
        self.assertTrue(window.add_button.isEnabled())
        self.assertTrue(window.readonly_banner.isHidden())

    def test_session_is_read_only(self) -> None:
        window = self._make_window("session")

        self.assertFalse(self.canonical.exists())
        self.assertEqual(window.config_path, self.legacy)
        self.assertTrue(window._read_only)
        self.assertEqual(len(window.servers), 1)
        self.assertFalse(window.add_button.isEnabled())
        self.assertFalse(window.migrate_button.isHidden())
        self.assertFalse(window.readonly_banner.isHidden())
        tip = window.add_button.toolTip().lower()
        self.assertTrue(
            "read-only" in tip or "solo lectura" in tip
        )

    def test_migrate_now(self) -> None:
        window = self._make_window("session")
        self.assertTrue(window._read_only)
        self.assertFalse(window.readonly_banner.isHidden())

        window.migrate_now()
        self.app.processEvents()

        self.assertTrue(self.canonical.exists())
        self.assertFalse(window._read_only)
        self.assertEqual(window.config_path, self.canonical)
        self.assertTrue(window.add_button.isEnabled())
        self.assertTrue(window.migrate_button.isHidden())
        self.assertTrue(window.readonly_banner.isHidden())


if __name__ == "__main__":
    unittest.main()
