"""Ejecución y control del proceso openconnect."""

from __future__ import annotations

import subprocess

from PySide6.QtCore import QObject, QProcess, QTimer, Signal

OPENCONNECT_NAME = "openconnect"
GRACE_MS = 20000
KILL_GRACE_MS = 10000


def _process_name(pid: int) -> str | None:
    try:
        with open(f"/proc/{pid}/comm", encoding="utf-8") as handle:
            return handle.read().strip()
    except OSError:
        return None


CONNECTED_MARKERS = (
    "configured as",
    "configurado como",
    "esp session established",
    "sesión esp establecida",
    "connected as",
    "conectado como",
)


class OpenConnectRunner(QObject):
    log = Signal(str)
    state_changed = Signal(str)
    finished = Signal(int)

    def __init__(self, parent: QObject | None = None) -> None:
        super().__init__(parent)

        self.process = QProcess(self)
        self.process.setProcessChannelMode(QProcess.SeparateChannels)
        self.process.started.connect(self._on_started)
        self.process.readyReadStandardOutput.connect(self._read_stdout)
        self.process.readyReadStandardError.connect(self._read_stderr)
        self.process.finished.connect(self._on_finished)
        self.process.errorOccurred.connect(self._on_error)

        self._prefix: list[str] = []
        self._killer: QProcess | None = None
        self._secret: str | None = None
        self._state = "idle"
        self._stopping = False
        self.stop_requested = False
        self._stop_stage = 0
        self._hinted_512 = False

        self._kill_timer = QTimer(self)
        self._kill_timer.setSingleShot(True)
        self._kill_timer.timeout.connect(self._escalate)

    @property
    def state(self) -> str:
        return self._state

    def is_running(self) -> bool:
        return self.process.state() != QProcess.NotRunning

    def start(
        self,
        prefix: list[str],
        args: list[str],
        secret: str | None,
    ) -> None:
        if self.is_running():
            self.log.emit(
                self.tr("An openconnect process is already running.")
            )
            return

        self._prefix = list(prefix)
        self._secret = secret
        self._stopping = False
        self.stop_requested = False
        self._stop_stage = 0
        self._hinted_512 = False
        self._set_state("connecting")

        self.log.emit("$ " + " ".join(prefix + args))
        self.process.start(prefix[0], prefix[1:] + args)

    def stop(self) -> None:
        if not self.is_running() or self._stopping:
            return
        self._stopping = True
        self.stop_requested = True
        self._stop_stage = 0
        self._set_state("disconnecting")
        self.log.emit(
            self.tr("Closing the openconnect session…")
        )
        self._send_signal("TERM")
        self._kill_timer.start(GRACE_MS)

    def _openconnect_pid(self) -> int | None:
        """PID del openconnect real.

        pkexec y sudo normalmente sustituyen su proceso por openconnect (mismo
        PID); en ese caso el PID del QProcess ya es el correcto. Si no, se
        busca el hijo. openconnect corre como root, así que la señal se pide
        con la misma elevación (pkexec/sudo).
        """
        parent = self.process.processId()
        if not parent:
            return None
        if _process_name(parent) == OPENCONNECT_NAME:
            return int(parent)
        try:
            result = subprocess.run(
                [
                    "pgrep",
                    "-P",
                    str(parent),
                    "-x",
                    OPENCONNECT_NAME,
                ],
                capture_output=True,
                text=True,
                timeout=5,
                check=False,
            )
        except (OSError, subprocess.TimeoutExpired):
            return None
        for token in result.stdout.split():
            if token.isdigit():
                return int(token)
        return None

    def _send_signal(self, sig: str) -> None:
        child = self._openconnect_pid()
        if child is None:
            self.log.emit(
                self.tr(
                    "The openconnect process was not found; the session "
                    "cannot be closed from here."
                )
            )
            return

        # Usa el mismo prefijo de elevación (pkexec/sudo) que se usó al
        # arrancar; por ejemplo ["pkexec"] o ["sudo", "-n"].
        command = self._prefix[:-1] + ["kill", f"-{sig}", str(child)]
        self._killer = QProcess(self)
        self._killer.errorOccurred.connect(
            lambda _error, s=sig: self.log.emit(
                self.tr(
                    "Could not run kill -{signal} "
                    "(did you cancel authorization?)"
                ).format(signal=s)
            )
        )
        self._killer.finished.connect(
            lambda code, _status, s=sig: self._on_killer_finished(code, s)
        )
        self._killer.start(command[0], command[1:])

    def _on_killer_finished(self, code: int, sig: str) -> None:
        if code == 0:
            self.log.emit(
                self.tr("Signal {signal} sent to openconnect.").format(
                    signal=sig
                )
            )
        else:
            self.log.emit(
                self.tr(
                    "Could not send {signal} to openconnect (code {code}). "
                    "Did you cancel authorization?"
                ).format(signal=sig, code=code)
            )

    def _escalate(self) -> None:
        if not self.is_running():
            return
        self._stop_stage += 1
        if self._stop_stage == 1:
            self.log.emit(
                self.tr("openconnect did not exit in time; sending KILL.")
            )
            self._send_signal("KILL")
            self._kill_timer.start(KILL_GRACE_MS)
            return
        # openconnect sigue activo: no lo damos por desconectado.
        self._stopping = False
        self._set_state("connected")
        self.log.emit(
            self.tr(
                "Could not close openconnect; the VPN is still active as "
                "root. Press “Disconnect” again or close it with: "
                "pkexec pkill -x openconnect"
            )
        )

    def _on_started(self) -> None:
        if self._secret is not None:
            self.process.write((self._secret + "\n").encode("utf-8"))
            self.process.closeWriteChannel()
            self._secret = None
        self.log.emit(
            self.tr("openconnect started; waiting for authentication…")
        )

    def _read_stdout(self) -> None:
        data = bytes(self.process.readAllStandardOutput()).decode(
            "utf-8", "replace"
        )
        self._handle_output(data)

    def _read_stderr(self) -> None:
        data = bytes(self.process.readAllStandardError()).decode(
            "utf-8", "replace"
        )
        self._handle_output(data)

    def _handle_output(self, text: str) -> None:
        for line in text.splitlines():
            line = line.rstrip()
            if not line:
                continue
            self.log.emit(line)
            lowered = line.lower()
            if "resultado 512" in lowered or "status code 512" in lowered:
                if not self._hinted_512:
                    self._hinted_512 = True
                    self.log.emit(
                        self.tr(
                            "Hint: the portal rejected the SAML cookie "
                            "(512). Check that “gateway” matches the "
                            "interface where you started SAML, or "
                            "reconnect: the cookie expires quickly."
                        )
                    )
            if not self._stopping and any(
                marker in lowered for marker in CONNECTED_MARKERS
            ):
                self._set_state("connected")

    def _on_finished(self, exit_code: int, _exit_status) -> None:
        self._kill_timer.stop()
        self._secret = None

        if self._stopping:
            self._set_state("idle")
        elif exit_code == 0:
            self._set_state("idle")
        elif exit_code in (126, 127):
            self._set_state("error")
            self.log.emit(
                self.tr(
                    "openconnect could not run. If using pkexec, cancel or "
                    "authorize the Polkit dialog; if using sudo, configure "
                    "passwordless sudoers."
                )
            )
        else:
            self._set_state("error")

        self._stopping = False
        self.finished.emit(exit_code)

    def _on_error(self, error) -> None:
        if error == QProcess.FailedToStart:
            self._set_state("error")
            self.log.emit(
                self.tr(
                    "Could not start the process. Is openconnect installed?"
                )
            )
        elif error == QProcess.Crashed:
            self.log.emit(
                self.tr("openconnect terminated abnormally.")
            )

    def _set_state(self, state: str) -> None:
        if state != self._state:
            self._state = state
            self.state_changed.emit(state)
