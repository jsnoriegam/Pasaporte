"""La ventana solo se cierra cuando openconnect ya terminó."""

from __future__ import annotations

import json
import os
import stat
import sys
import tempfile
import time
import unittest
from pathlib import Path
from unittest.mock import patch

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

_XDG = tempfile.TemporaryDirectory()
os.environ["XDG_CONFIG_HOME"] = str(Path(_XDG.name) / "xdg")

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from PySide6.QtCore import QCoreApplication  # noqa: E402
from PySide6.QtWidgets import QApplication, QMessageBox  # noqa: E402

import pasaporte.ui as ui  # noqa: E402

FAKE_OPENCONNECT = """#!/bin/bash
echo "Configurado como 172.16.0.2, con SSL desconectado y ESP establecida"
trap 'echo "Cerrando sesión..."; sleep 1; exit 0' TERM INT
while true; do sleep 1; done
"""

FAKE_PKEXEC_EXEC = """#!/bin/bash
exec "$@"
"""


def _wait(predicate, timeout: float) -> bool:
    deadline = time.time() + timeout
    while time.time() < deadline:
        QCoreApplication.processEvents()
        if predicate():
            return True
        time.sleep(0.05)
    QCoreApplication.processEvents()
    return predicate()


class CloseWhileConnectedTests(unittest.TestCase):
    app = None

    @classmethod
    def setUpClass(cls) -> None:
        cls.app = QApplication.instance() or QApplication([])

    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        root = Path(self.tmp.name)

        self.openconnect = root / "openconnect"
        self.openconnect.write_text(FAKE_OPENCONNECT, encoding="utf-8")
        self.pkexec = root / "pkexec"
        self.pkexec.write_text(FAKE_PKEXEC_EXEC, encoding="utf-8")
        for path in (self.openconnect, self.pkexec):
            path.chmod(path.stat().st_mode | stat.S_IEXEC)

        config = root / "hosts.json"
        config.write_text(
            json.dumps(
                [
                    {
                        "name": "Fake",
                        "host": "vpn.example.com",
                        "username": "u",
                    }
                ]
            ),
            encoding="utf-8",
        )
        self.window = ui.MainWindow(config)
        self.window.show()
        self.app.processEvents()

    def tearDown(self) -> None:
        if self.window.runner.is_running():
            self.window.runner.process.kill()
            self.window.runner.process.waitForFinished(3000)
        self.window.deleteLater()
        self.app.processEvents()
        self.tmp.cleanup()

    def test_close_disconnects_before_quitting(self) -> None:
        window = self.window
        window.runner.start(
            [str(self.pkexec), str(self.openconnect)], [], None
        )
        self.assertTrue(
            _wait(lambda: window.runner.state == "connected", 8),
            window.runner.state,
        )
        self.assertTrue(window.disconnect_button.isEnabled())

        with patch.object(
            QMessageBox, "question", return_value=QMessageBox.Yes
        ):
            window.close()

        self.assertTrue(
            _wait(lambda: not window.runner.is_running(), 15),
            "openconnect sigue activo tras cerrar la ventana",
        )
        self.assertTrue(
            _wait(lambda: not window.isVisible(), 3),
            "la ventana no se cerró tras desconectar",
        )


if __name__ == "__main__":
    unittest.main()
