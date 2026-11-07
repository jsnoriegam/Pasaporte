"""Minimizar a la bandeja: cerrar/minimizar oculta, salir cierra de verdad."""

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

from PySide6.QtWidgets import QApplication, QSystemTrayIcon  # noqa: E402

import pasaporte.ui as ui  # noqa: E402


class TrayTests(unittest.TestCase):
    app = None

    @classmethod
    def setUpClass(cls) -> None:
        cls.app = QApplication.instance() or QApplication([])

    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.config = Path(self.tmp.name) / "hosts.json"
        self.config.write_text(json.dumps([]), encoding="utf-8")

    def tearDown(self) -> None:
        window = getattr(self, "window", None)
        if window is not None:
            window.deleteLater()
            self.app.processEvents()
        self.tmp.cleanup()

    def _window(self, tray_available: bool) -> ui.MainWindow:
        with patch.object(
            QSystemTrayIcon,
            "isSystemTrayAvailable",
            return_value=tray_available,
        ):
            self.window = ui.MainWindow(self.config)
        self.window.show()
        self.app.processEvents()
        return self.window

    def test_close_hides_to_tray_when_enabled(self) -> None:
        window = self._window(tray_available=True)
        window.minimize_tray_action.setChecked(True)
        with patch.object(window, "_save_geometry") as save:
            self.assertFalse(window.close())
        self.assertFalse(window.isVisible())
        save.assert_not_called()

    def test_quit_action_really_quits(self) -> None:
        window = self._window(tray_available=True)
        window.minimize_tray_action.setChecked(True)
        with patch.object(window, "_save_geometry") as save:
            window.quit_action.trigger()
        save.assert_called_once()

    def test_tray_quit_really_quits(self) -> None:
        window = self._window(tray_available=True)
        window.minimize_tray_action.setChecked(True)
        with patch.object(window, "_save_geometry") as save:
            window.tray_quit_action.trigger()
        save.assert_called_once()

    def test_close_quits_when_disabled(self) -> None:
        window = self._window(tray_available=True)
        window.minimize_tray_action.setChecked(False)
        with patch.object(window, "_save_geometry") as save:
            self.assertTrue(window.close())
        save.assert_called_once()

    def test_no_tray_means_close_quits(self) -> None:
        window = self._window(tray_available=False)
        self.assertIsNone(window.tray)
        self.assertFalse(window.minimize_tray_action.isEnabled())
        with patch.object(window, "_save_geometry") as save:
            self.assertTrue(window.close())
        save.assert_called_once()

    def test_pending_vpn_stop_is_not_hidden(self) -> None:
        window = self._window(tray_available=True)
        window.minimize_tray_action.setChecked(True)
        window._quit_after_stop = True
        self.assertFalse(window._hides_to_tray())

    def test_session_saving_is_not_hidden(self) -> None:
        window = self._window(tray_available=True)
        window.minimize_tray_action.setChecked(True)
        with patch(
            "PySide6.QtGui.QGuiApplication.isSavingSession",
            return_value=True,
        ):
            self.assertFalse(window._hides_to_tray())

    def test_minimized_window_goes_to_tray(self) -> None:
        window = self._window(tray_available=True)
        window.minimize_tray_action.setChecked(True)
        window.showMinimized()
        for _ in range(3):
            self.app.processEvents()
        self.assertFalse(window.isVisible())

    def test_preference_is_remembered(self) -> None:
        window = self._window(tray_available=True)
        window.minimize_tray_action.setChecked(False)
        self.assertFalse(window._tray_preference())
        window.minimize_tray_action.setChecked(True)
        self.assertTrue(window._tray_preference())


if __name__ == "__main__":
    unittest.main()
