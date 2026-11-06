"""Smoke tests de la ventana principal y el CRUD."""

from __future__ import annotations

import json
import os
import sys
import tempfile
import unittest
from pathlib import Path

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

_XDG = tempfile.TemporaryDirectory()
os.environ["XDG_CONFIG_HOME"] = str(Path(_XDG.name) / "xdg")

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from PySide6.QtWidgets import (  # noqa: E402
    QApplication,
    QDialog,
    QMessageBox,
)

import pasaporte.ui as ui  # noqa: E402
from pasaporte.config import VPNServer  # noqa: E402


class FakeDialog:
    server_to_return: VPNServer | None = None

    def __init__(self, server=None, existing=None, index=None, parent=None):
        self.result_server = FakeDialog.server_to_return

    def exec(self):
        return QDialog.Accepted


class MainWindowCrudTests(unittest.TestCase):
    app = None
    original_dialog = None
    original_question = None
    original_warning = None
    original_critical = None
    original_information = None

    @classmethod
    def setUpClass(cls) -> None:
        cls.app = QApplication.instance() or QApplication([])
        cls.original_dialog = ui.ConnectionDialog
        cls.original_question = QMessageBox.question
        cls.original_warning = QMessageBox.warning
        cls.original_critical = QMessageBox.critical
        cls.original_information = QMessageBox.information

        ui.ConnectionDialog = FakeDialog
        QMessageBox.question = staticmethod(
            lambda *a, **k: QMessageBox.Yes
        )
        QMessageBox.warning = staticmethod(
            lambda *a, **k: QMessageBox.Ok
        )
        QMessageBox.critical = staticmethod(
            lambda *a, **k: QMessageBox.Ok
        )
        QMessageBox.information = staticmethod(
            lambda *a, **k: QMessageBox.Ok
        )

    @classmethod
    def tearDownClass(cls) -> None:
        ui.ConnectionDialog = cls.original_dialog
        QMessageBox.question = cls.original_question
        QMessageBox.warning = cls.original_warning
        QMessageBox.critical = cls.original_critical
        QMessageBox.information = cls.original_information
        _XDG.cleanup()

    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.config_path = Path(self.tmp.name) / "hosts.json"
        self.config_path.write_text(
            json.dumps(
                [
                    {
                        "name": "UTB",
                        "host": "vpn3.utb.edu.co",
                        "protocol": "gp",
                        "saml": True,
                    },
                    {
                        "name": "Tempo",
                        "host": "1.2.3.4:443",
                        "username": "u",
                    },
                ]
            ),
            encoding="utf-8",
        )
        self.window = ui.MainWindow(self.config_path)
        self.window.show()
        self.app.processEvents()

    def tearDown(self) -> None:
        self.window.close()
        self.window.deleteLater()
        self.app.processEvents()
        self.tmp.cleanup()

    def test_load(self) -> None:
        self.assertEqual(len(self.window.servers), 2)
        self.assertTrue(self.window._config_ok)
        self.assertIs(
            self.window.stack.currentWidget(), self.window.list
        )

    def test_add_edit_delete(self) -> None:
        FakeDialog.server_to_return = VPNServer(
            name="Nueva",
            host="nueva.example.com",
            username="nuevo",
            protocol="fortinet",
        )
        self.window.add_server()
        self.app.processEvents()
        self.assertEqual(len(self.window.servers), 3)
        self.assertTrue(
            any(s.name == "Nueva" for s in self.window.servers)
        )
        self.assertTrue(
            self.config_path.with_name(
                self.config_path.name + ".bak"
            ).exists()
        )

        FakeDialog.server_to_return = VPNServer(
            name="UTB editada",
            host="vpn3.utb.edu.co",
            username="respaldo@utb.edu.co",
            protocol="gp",
            saml=True,
        )
        self.window.list.setCurrentRow(0)
        self.window.edit_server()
        self.app.processEvents()
        self.assertEqual(self.window.servers[0].name, "UTB editada")

        raw = json.loads(
            self.config_path.read_text(encoding="utf-8")
        )
        self.assertEqual(raw[0]["name"], "UTB editada")
        self.assertEqual(
            raw[0]["username"], "respaldo@utb.edu.co"
        )

        self.window.list.setCurrentRow(0)
        self.window.delete_server()
        self.app.processEvents()
        self.assertEqual(len(self.window.servers), 2)

    def test_empty_state(self) -> None:
        while self.window.servers:
            self.window.list.setCurrentRow(0)
            self.window.delete_server()
            self.app.processEvents()

        self.assertEqual(self.window.servers, [])
        self.assertIs(
            self.window.stack.currentWidget(), self.window.empty_widget
        )
        raw = json.loads(
            self.config_path.read_text(encoding="utf-8")
        )
        self.assertEqual(raw, [])

    def test_connect_by_name(self) -> None:
        called = []
        self.window.connect_selected = lambda: called.append(True)

        self.window.connect_by_name("UTB")
        self.assertEqual(self.window.current_server().name, "UTB")
        self.assertEqual(called, [True])

        # Un nombre inexistente no debe lanzar excepción.
        self.window.connect_by_name("No existe")
        self.assertEqual(called, [True])


if __name__ == "__main__":
    unittest.main()
