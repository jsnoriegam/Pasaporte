"""Reconexión automática tras una caída, y desconexión pedida por el usuario."""

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
os.environ.setdefault("XDG_CONFIG_HOME", str(Path(_XDG.name) / "xdg"))

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from PySide6.QtCore import QCoreApplication  # noqa: E402
from PySide6.QtWidgets import QApplication  # noqa: E402

import pasaporte.ui as ui  # noqa: E402

FAKE_OPENCONNECT = """#!/bin/bash
echo "Configurado como 172.16.0.2, con SSL desconectado y ESP establecida"
trap 'exit 0' TERM INT
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


class _Base(unittest.TestCase):
    app = None

    @classmethod
    def setUpClass(cls) -> None:
        cls.app = QApplication.instance() or QApplication([])

    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        root = Path(self.tmp.name)
        self.config = root / "hosts.json"
        self.config.write_text(
            json.dumps(
                [{"name": "Fake", "host": "vpn.example.com", "username": "u"}]
            ),
            encoding="utf-8",
        )
        self.window = ui.MainWindow(self.config)
        self.window.show()
        self.app.processEvents()
        self.window.settings.setValue("auto_reconnect", True)
        self.window.reconnect_action.setChecked(True)
        self.server = self.window.servers[0]

    def tearDown(self) -> None:
        window = self.window
        if window.runner.is_running():
            window.runner.process.kill()
            window.runner.process.waitForFinished(3000)
        window.settings.setValue("auto_reconnect", False)
        window._update_thread = None
        window.deleteLater()
        self.app.processEvents()
        self.tmp.cleanup()

    def _simulate_session(self, password: str | None = "pw") -> None:
        window = self.window
        window._was_connected = True
        window._session_server = self.server
        window._session_password = password


class ReconnectDecisionTests(_Base):
    def test_drop_with_password_schedules_reconnect(self) -> None:
        window = self.window
        self._simulate_session()
        window._schedule_reconnect(1)
        self.assertTrue(window._reconnect_active)
        self.assertTrue(window._reconnect_timer.isActive())
        self.assertEqual(window._reconnect_attempt, 1)
        self.assertEqual(window._session_password, "pw")

    def test_saml_session_is_not_reconnected(self) -> None:
        window = self.window
        self._simulate_session(password=None)
        window._schedule_reconnect(1)
        self.assertFalse(window._reconnect_active)
        self.assertFalse(window._reconnect_timer.isActive())
        self.assertIsNone(window._session_server)

    def test_gives_up_after_all_attempts(self) -> None:
        window = self.window
        self._simulate_session()
        window._reconnect_attempt = len(window.RECONNECT_DELAYS_MS)
        window._schedule_reconnect(1)
        self.assertFalse(window._reconnect_active)
        self.assertIsNone(window._session_password)

    def test_cancelled_authorization_stops(self) -> None:
        window = self.window
        self._simulate_session()
        window._schedule_reconnect(126)
        self.assertFalse(window._reconnect_active)
        self.assertIsNone(window._session_password)

    def test_disabled_preference_never_reconnects(self) -> None:
        window = self.window
        self._simulate_session()
        window.reconnect_action.setChecked(False)
        window._schedule_reconnect(1)
        self.assertFalse(window._reconnect_active)
        self.assertIsNone(window._session_password)

    def test_user_stop_is_not_a_drop(self) -> None:
        window = self.window
        self._simulate_session()
        window.runner.stop_requested = True
        window.on_finished(0)
        self.assertFalse(window._reconnect_active)
        self.assertIsNone(window._session_password)

    def test_unexpected_exit_is_a_drop(self) -> None:
        window = self.window
        self._simulate_session()
        window.runner.stop_requested = False
        window.on_finished(0)
        self.assertTrue(window._reconnect_active)

    def test_password_is_kept_only_when_preference_is_on(self) -> None:
        window = self.window
        window.reconnect_action.setChecked(False)
        with patch.object(ui, "privilege_prefix", return_value=["true"]), patch.object(
            ui, "build_connection", return_value=([], None)
        ), patch.object(window.runner, "start"):
            window._start_openconnect(self.server, password="pw")
        self.assertIsNone(window._session_password)
        self.assertIs(window._session_server, self.server)


class ReconnectIntegrationTests(_Base):
    def setUp(self) -> None:
        super().setUp()
        root = Path(self.tmp.name)
        self.openconnect = root / "openconnect"
        self.openconnect.write_text(FAKE_OPENCONNECT, encoding="utf-8")
        self.pkexec = root / "pkexec"
        self.pkexec.write_text(FAKE_PKEXEC_EXEC, encoding="utf-8")
        for path in (self.openconnect, self.pkexec):
            path.chmod(path.stat().st_mode | stat.S_IEXEC)
        # Esperas cortas para que el test sea rápido.
        self.window.RECONNECT_DELAYS_MS = (50,)

        self.patches = [
            patch.object(
                ui,
                "privilege_prefix",
                return_value=[str(self.pkexec), str(self.openconnect)],
            ),
            patch.object(ui, "build_connection", return_value=([], "pw")),
        ]
        for p in self.patches:
            p.start()

    def tearDown(self) -> None:
        for p in self.patches:
            p.stop()
        super().tearDown()

    def test_real_drop_reconnects(self) -> None:
        window = self.window
        window._start_openconnect(self.server, password="pw")
        self.assertTrue(
            _wait(lambda: window.runner.state == "connected", 10),
            window.runner.state,
        )

        window.runner.process.kill()
        self.assertTrue(
            _wait(lambda: window._reconnect_active, 10),
            "la caída no programó la reconexión",
        )
        self.assertTrue(
            _wait(
                lambda: window.runner.state == "connected"
                and not window._reconnect_active,
                15,
            ),
            "no se reconectó tras la caída",
        )

    def test_user_disconnect_does_not_reconnect(self) -> None:
        window = self.window
        window._start_openconnect(self.server, password="pw")
        self.assertTrue(
            _wait(lambda: window.runner.state == "connected", 10),
            window.runner.state,
        )

        window.runner.stop()
        self.assertTrue(
            _wait(lambda: not window.runner.is_running(), 15),
            "openconnect sigue activo tras desconectar",
        )
        # Margen para que llegue cualquier reconexión programada.
        deadline = time.time() + 0.5
        while time.time() < deadline:
            QCoreApplication.processEvents()
            time.sleep(0.05)
        self.assertFalse(window._reconnect_active)
        self.assertIsNone(window._session_password)
        self.assertFalse(window.runner.is_running())


if __name__ == "__main__":
    unittest.main()
