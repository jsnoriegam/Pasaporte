"""Test del flujo SAML embebido con un ACS simulado."""

from __future__ import annotations

import os
import socket
import sys
import threading
import unittest
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
os.environ.setdefault("QTWEBENGINE_DISABLE_SANDBOX", "1")
if "QTWEBENGINE_REMOTE_DEBUGGING" not in os.environ:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as _sock:
        _sock.bind(("127.0.0.1", 0))
        _port = _sock.getsockname()[1]
    os.environ["QTWEBENGINE_REMOTE_DEBUGGING"] = str(_port)

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from PySide6.QtCore import QEventLoop, QTimer  # noqa: E402
from PySide6.QtWidgets import QApplication  # noqa: E402

from pasaporte.config import VPNServer  # noqa: E402
from pasaporte.gp import SamlRequest, SamlResult  # noqa: E402
from pasaporte.openconnect import build_connection  # noqa: E402
from pasaporte.saml_dialog import SamlLoginDialog  # noqa: E402

IDP_HTML = b"""<!doctype html><html><body><h1>IdP mock</h1>
<script>setTimeout(function(){location.href='/SAML20/SP/ACS'}, 400);</script>
</body></html>"""

ACS_HTML = b"<html><body>login ok</body></html>"


class _Handler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        if self.path.startswith("/SAML20/SP/ACS"):
            self.send_header("saml-username", "mock.user@example.com")
            self.send_header("saml-auth-status", "1")
            self.send_header("prelogin-cookie", "MOCK-COOKIE-123")
            body = ACS_HTML
        else:
            body = IDP_HTML
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *_args) -> None:
        pass


class SamlDialogTests(unittest.TestCase):
    app = None
    httpd = None
    port = 0

    @classmethod
    def setUpClass(cls) -> None:
        cls.app = QApplication.instance() or QApplication([])

        with socket.socket() as sock:
            sock.bind(("127.0.0.1", 0))
            cls.port = sock.getsockname()[1]

        cls.httpd = HTTPServer(("127.0.0.1", cls.port), _Handler)
        threading.Thread(
            target=cls.httpd.serve_forever, daemon=True
        ).start()

    @classmethod
    def tearDownClass(cls) -> None:
        if cls.httpd is not None:
            cls.httpd.shutdown()
            cls.httpd.server_close()

    def _run_dialog(self, gateway: bool) -> SamlResult | None:
        devtools_port = int(os.environ["QTWEBENGINE_REMOTE_DEBUGGING"])
        server = VPNServer(
            name="Mock GP",
            host=f"127.0.0.1:{self.port}",
            username="",
            protocol="gp",
            saml=True,
            gateway=gateway,
        )
        request = SamlRequest(
            method="REDIRECT",
            payload=f"http://127.0.0.1:{self.port}/idp",
            host=server.host,
            endpoint=f"http://127.0.0.1:{self.port}/prelogin.esp",
        )

        dialog = SamlLoginDialog(server, request, devtools_port)
        loop = QEventLoop()
        dialog.accepted.connect(loop.quit)
        dialog.rejected.connect(loop.quit)
        QTimer.singleShot(10000, loop.quit)

        dialog.show()
        loop.exec()

        result = dialog.result_data
        dialog.close()
        self.app.processEvents()
        return result

    def test_captures_acs_headers_for_gateway(self) -> None:
        result = self._run_dialog(gateway=True)

        self.assertIsNotNone(
            result, "el diálogo no capturó las cabeceras SAML"
        )
        assert result is not None
        self.assertEqual(result.username, "mock.user@example.com")
        self.assertEqual(result.cookie, "MOCK-COOKIE-123")
        self.assertEqual(result.cookie_field, "prelogin-cookie")
        self.assertEqual(result.interface, "gateway")
        self.assertEqual(result.server, f"127.0.0.1:{self.port}")

    def test_usergroup_follows_requested_interface(self) -> None:
        # El ACS devuelve prelogin-cookie aunque se pidiera el portal.
        # El usergroup debe seguir al portal, no al nombre de la cookie.
        result = self._run_dialog(gateway=False)

        self.assertIsNotNone(result)
        assert result is not None
        self.assertEqual(result.interface, "portal")
        self.assertEqual(result.cookie_field, "prelogin-cookie")

        server = VPNServer(
            name="Mock GP",
            host=result.server,
            username="",
            protocol="gp",
            saml=True,
            gateway=False,
        )
        args, _secret = build_connection(server, saml_result=result)
        self.assertIn("--usergroup=portal:prelogin-cookie", args)



if __name__ == "__main__":
    unittest.main()
