"""Acción Conectar de la bandeja: qué conexión usa y cómo avisa."""

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

import shiboken6  # noqa: E402
from PySide6.QtWidgets import QApplication, QMessageBox, QSystemTrayIcon  # noqa: E402

import pasaporte.ui as ui  # noqa: E402


class TrayConnectTests(unittest.TestCase):
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
                    {"name": "Alpha", "host": "a.example.com", "username": "u"},
                    {"name": "Beta", "host": "b.example.com", "username": "u"},
                ]
            ),
            encoding="utf-8",
        )
        with patch.object(
            QSystemTrayIcon, "isSystemTrayAvailable", return_value=True
        ):
            self.window = ui.MainWindow(self.config)
        self.window.show()
        self.app.processEvents()

    def tearDown(self) -> None:
        self.window._update_thread = None
        shiboken6.delete(self.window)
        self.app.processEvents()
        self.tmp.cleanup()

    def _submenu_names(self) -> list[str]:
        return [a.text() for a in self.window.tray_connect_menu.actions()]

    def test_submenu_lists_every_connection(self) -> None:
        self.assertEqual(self._submenu_names(), ["Alpha", "Beta"])

    def test_top_action_names_the_selected_connection(self) -> None:
        self.window.list.setCurrentRow(1)
        self.assertEqual(
            self.window.tray_connect_action.text(),
            self.window.tr("Connect: {name}").format(name="Beta"),
        )
        self.assertTrue(self.window.tray_connect_action.isEnabled())

    def test_no_selection_disables_connect(self) -> None:
        self.window.list.setCurrentRow(-1)
        self.assertEqual(
            self.window.tray_connect_action.text(), self.window.tr("Connect")
        )
        self.assertFalse(self.window.tray_connect_action.isEnabled())

    def test_submenu_entry_connects_that_connection(self) -> None:
        window = self.window
        window.list.setCurrentRow(0)
        with patch.object(window, "connect_selected") as connect:
            window.tray_connect_menu.actions()[1].trigger()
        connect.assert_called_once()
        self.assertEqual(window.current_server().name, "Beta")

    def test_hidden_window_notifies_instead_of_dialog(self) -> None:
        window = self.window
        window.list.setCurrentRow(-1)
        window.hide()
        self.app.processEvents()
        with patch.object(QMessageBox, "information") as info, patch.object(
            window.tray, "showMessage"
        ) as notify:
            window.connect_selected()
        info.assert_not_called()
        notify.assert_called_once()

    def test_visible_window_uses_dialog(self) -> None:
        window = self.window
        window.list.setCurrentRow(-1)
        with patch.object(QMessageBox, "information") as info:
            window.connect_selected()
        info.assert_called_once()

    def test_submenu_follows_config_reload(self) -> None:
        self.config.write_text(
            json.dumps(
                [
                    {"name": "Gamma", "host": "g.example.com", "username": "u"},
                ]
            ),
            encoding="utf-8",
        )
        self.window.reload_config()
        self.assertEqual(self._submenu_names(), ["Gamma"])


if __name__ == "__main__":
    unittest.main()
