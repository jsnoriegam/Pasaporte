"""Regresión: cancelar un diálogo no debe dejar los botones desactivados."""

from __future__ import annotations

import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

_XDG = tempfile.TemporaryDirectory()
os.environ.setdefault("XDG_CONFIG_HOME", str(Path(_XDG.name) / "xdg"))

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from PySide6.QtWidgets import QApplication, QDialog  # noqa: E402

import pasaporte.ui as ui  # noqa: E402


class _RejectingDialog:
    def __init__(self, *args, **kwargs):
        self.result_server = None
        self.result_data = None

    def exec(self):
        return QDialog.Rejected

    def deleteLater(self):
        pass


class CancelTests(unittest.TestCase):
    app = None

    @classmethod
    def setUpClass(cls) -> None:
        cls.app = QApplication.instance() or QApplication([])

    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.config = Path(self.tmp.name) / "hosts.json"
        self.config.write_text(
            json.dumps(
                [
                    {
                        "name": "Fortinet",
                        "host": "vpn.example.com",
                        "username": "u",
                        "servercert": "pin-sha256:abc",
                    },
                    {
                        "name": "SAMLP",
                        "host": "gp.example.com",
                        "username": "u",
                        "protocol": "gp",
                        "saml": True,
                    },
                ]
            ),
            encoding="utf-8",
        )
        self.window = ui.MainWindow(self.config)
        self.window.show()
        self.app.processEvents()

    def tearDown(self) -> None:
        self.window.close()
        self.window.deleteLater()
        self.app.processEvents()
        self.tmp.cleanup()

    def _assert_editing_enabled(self) -> None:
        self.assertTrue(self.window.add_button.isEnabled())
        self.assertTrue(self.window.edit_button.isEnabled())
        self.assertTrue(self.window.delete_button.isEnabled())
        self.assertTrue(self.window.connect_button.isEnabled())

    def test_password_cancel(self) -> None:
        self.window.list.setCurrentRow(0)
        with patch.object(ui, "PasswordDialog", _RejectingDialog):
            self.window.connect_selected()
        self.app.processEvents()
        self._assert_editing_enabled()

    def test_saml_cancel(self) -> None:
        self.window.list.setCurrentRow(1)
        self.window._pending_server = self.window.servers[1]
        with patch.object(ui, "SamlLoginDialog", _RejectingDialog):
            self.window._on_prelogin_done(object())
        self.app.processEvents()
        self._assert_editing_enabled()

    def test_editor_cancel(self) -> None:
        with patch.object(ui, "ConnectionDialog", _RejectingDialog):
            self.window.add_server()
        self.app.processEvents()
        self._assert_editing_enabled()


if __name__ == "__main__":
    unittest.main()
