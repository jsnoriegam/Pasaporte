"""Una sola instancia: la segunda reenvía su orden a la primera."""

from __future__ import annotations

import json
import os
import sys
import tempfile
import time
import unittest
import uuid
from pathlib import Path
from unittest.mock import patch

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

_XDG = tempfile.TemporaryDirectory()
os.environ.setdefault("XDG_CONFIG_HOME", str(Path(_XDG.name) / "xdg"))

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

import shiboken6  # noqa: E402
from PySide6.QtCore import QCoreApplication, QDir, QEvent  # noqa: E402
from PySide6.QtWidgets import QApplication, QSystemTrayIcon  # noqa: E402

import pasaporte.ui as ui  # noqa: E402
from pasaporte.single_instance import SingleInstance  # noqa: E402


def _wait(predicate, timeout: float) -> bool:
    deadline = time.time() + timeout
    while time.time() < deadline:
        QCoreApplication.processEvents()
        if predicate():
            return True
        time.sleep(0.02)
    QCoreApplication.processEvents()
    return predicate()


class SingleInstanceTests(unittest.TestCase):
    app = None

    @classmethod
    def setUpClass(cls) -> None:
        cls.app = QApplication.instance() or QApplication([])

    def setUp(self) -> None:
        self.key = f"pasaporte-test-{uuid.uuid4().hex}"
        self.received: list[str] = []

    def test_forward_without_running_instance_is_false(self) -> None:
        self.assertFalse(SingleInstance(self.key, self.app).forward("show", 200))

    def test_second_instance_forwards_its_message(self) -> None:
        first = SingleInstance(self.key, self.app)
        self.assertTrue(first.listen())
        first.received.connect(self.received.append)

        second = SingleInstance(self.key, self.app)
        self.assertTrue(second.forward("connect:UTB"))
        self.assertTrue(_wait(lambda: self.received, 3), self.received)
        self.assertEqual(self.received, ["connect:UTB"])

    def test_stale_socket_file_is_replaced(self) -> None:
        stale = Path(QDir.tempPath()) / self.key
        stale.write_text("huérfano", encoding="utf-8")
        try:
            instance = SingleInstance(self.key, self.app)
            self.assertTrue(instance.listen())
        finally:
            QCoreApplication.processEvents()
            stale.unlink(missing_ok=True)

    def test_show_request_shows_hidden_window(self) -> None:
        tmp = tempfile.TemporaryDirectory()
        config = Path(tmp.name) / "hosts.json"
        config.write_text(json.dumps([]), encoding="utf-8")
        with patch.object(
            QSystemTrayIcon, "isSystemTrayAvailable", return_value=True
        ):
            window = ui.MainWindow(config)
        window.hide()
        self.app.processEvents()
        self.assertFalse(window.isVisible())

        window.handle_external_request("show")
        self.app.processEvents()
        self.assertTrue(window.isVisible())

        window.hide()
        window.handle_external_request("background")
        self.app.processEvents()
        self.assertFalse(window.isVisible())

        shiboken6.delete(window)
        tmp.cleanup()


if __name__ == "__main__":
    unittest.main()
