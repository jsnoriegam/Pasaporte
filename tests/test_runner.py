"""Tests del ciclo conectar/desconectar del runner, con openconnect falso."""

from __future__ import annotations

import os
import subprocess
import stat
import sys
import tempfile
import time
import unittest
from pathlib import Path

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from PySide6.QtCore import QCoreApplication  # noqa: E402
from PySide6.QtWidgets import QApplication  # noqa: E402

from pasaporte.runner import OpenConnectRunner  # noqa: E402

FAKE_OPENCONNECT = """#!/bin/bash
echo "POST https://vpn.example.com/ssl-vpn/login.esp"
echo "Configurado como 172.16.0.2, con SSL desconectado y ESP establecida"
echo "Sesión ESP establecida con el servidor"
echo "$$" > "{pid_file}"
trap 'echo "Cerrando sesión..."; sleep 1; echo "Sesión cerrada"; exit 0' TERM INT
while true; do sleep 1; done
"""

# Imita a pkexec que crea un proceso hijo para el programa.
FAKE_PKEXEC_FORK = """#!/bin/bash
"$@"
"""

# Imita a pkexec real, que sustituye su proceso por el programa (mismo PID).
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


def _alive(pid: int) -> bool:
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return False
    except PermissionError:
        return True
    return True


class RunnerLifecycleTests(unittest.TestCase):
    app = None
    stub_text = FAKE_PKEXEC_FORK

    @classmethod
    def setUpClass(cls) -> None:
        cls.app = QApplication.instance() or QApplication([])

    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        root = Path(self.tmp.name)
        self.pid_file = root / "openconnect.pid"

        self.openconnect = root / "openconnect"
        self.openconnect.write_text(
            FAKE_OPENCONNECT.format(pid_file=self.pid_file),
            encoding="utf-8",
        )
        self.pkexec = root / "pkexec"
        self.pkexec.write_text(self.stub_text, encoding="utf-8")
        for path in (self.openconnect, self.pkexec):
            path.chmod(path.stat().st_mode | stat.S_IEXEC)

        self.runner = OpenConnectRunner()
        self.states: list[str] = []
        self.logs: list[str] = []
        self.runner.state_changed.connect(self.states.append)
        self.runner.log.connect(self.logs.append)

    def tearDown(self) -> None:
        if self.runner.is_running():
            self.runner.process.kill()
            self.runner.process.waitForFinished(3000)
        if self.pid_file.exists():
            pid = int(self.pid_file.read_text().strip() or 0)
            if pid and _alive(pid):
                os.kill(pid, 9)
        self.tmp.cleanup()

    def test_spanish_success_marks_connected(self) -> None:
        self.runner.start([str(self.pkexec), str(self.openconnect)], [], None)
        connected = _wait(lambda: "connected" in self.states, 8)
        self.assertTrue(connected, f"estados: {self.states}")

    def test_disconnect_stops_openconnect(self) -> None:
        self.runner.start([str(self.pkexec), str(self.openconnect)], [], None)
        self.assertTrue(_wait(lambda: "connected" in self.states, 8))

        pid = int(self.pid_file.read_text().strip())
        self.assertTrue(_alive(pid))

        self.runner.stop()
        finished = _wait(lambda: not self.runner.is_running(), 15)

        self.assertTrue(finished, f"estados: {self.states}")
        self.assertEqual(self.states[-1], "idle")
        self.assertFalse(_alive(pid), "openconnect sigue vivo")
        self.assertTrue(
            any(
                "Signal TERM sent" in line
                or "Señal TERM enviada" in line
                for line in self.logs
            ),
            self.logs,
        )


@unittest.skipUnless(
    os.environ.get("PASAPORTE_ISOLATED"),
    "se ejecuta en su propio proceso desde RunnerIsolationTests",
)
class RunnerWithForkingPkexecTests(RunnerLifecycleTests):
    stub_text = FAKE_PKEXEC_FORK


@unittest.skipUnless(
    os.environ.get("PASAPORTE_ISOLATED"),
    "se ejecuta en su propio proceso desde RunnerIsolationTests",
)
class RunnerWithExecingPkexecTests(RunnerLifecycleTests):
    """Como pkexec real: openconnect ocupa el PID del proceso lanzado."""

    stub_text = FAKE_PKEXEC_EXEC


del RunnerLifecycleTests



class RunnerIsolationTests(unittest.TestCase):
    """Cada variante de pkexec corre en su propio intérprete.

    Ejecutadas juntas en el mismo proceso, la finalización de Python aborta
    (double free) cuando quedan QProcess vivos; cada una por separado pasa.
    """

    def test_each_variant_in_its_own_interpreter(self) -> None:
        env = dict(os.environ, PASAPORTE_ISOLATED="1")
        for name in (
            "RunnerWithForkingPkexecTests",
            "RunnerWithExecingPkexecTests",
        ):
            with self.subTest(variant=name):
                result = subprocess.run(
                    [
                        sys.executable,
                        "-m",
                        "unittest",
                        f"tests.test_runner.{name}",
                    ],
                    cwd=ROOT,
                    env=env,
                    capture_output=True,
                    text=True,
                    timeout=180,
                    check=False,
                )
                self.assertEqual(
                    result.returncode,
                    0,
                    result.stderr[-2000:],
                )


if __name__ == "__main__":
    unittest.main()
