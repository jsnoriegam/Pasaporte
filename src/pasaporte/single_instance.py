"""Una sola instancia de Pasaporte: la segunda reenvía su orden a la primera."""

from __future__ import annotations

import sys

from PySide6.QtCore import QObject, Signal
from PySide6.QtNetwork import QLocalServer, QLocalSocket


class SingleInstance(QObject):
    received = Signal(str)

    def __init__(self, key: str, parent: QObject | None = None) -> None:
        super().__init__(parent)
        self.key = key
        self._server: QLocalServer | None = None

    def forward(self, message: str, timeout_ms: int = 1000) -> bool:
        """Envía `message` a la instancia en marcha; False si no hay ninguna."""
        socket = QLocalSocket(self)
        socket.connectToServer(self.key)
        if not socket.waitForConnected(timeout_ms):
            socket.abort()
            return False
        socket.write(message.encode("utf-8"))
        socket.flush()
        socket.waitForBytesWritten(timeout_ms)
        socket.disconnectFromServer()
        return True

    def listen(self) -> bool:
        server = QLocalServer(self)
        server.setSocketOptions(QLocalServer.UserAccessOption)
        if not server.listen(self.key):
            # Socket huérfano de una sesión que murió sin cerrarlo: como
            # forward() no obtuvo respuesta, es seguro reemplazarlo.
            QLocalServer.removeServer(self.key)
            if not server.listen(self.key):
                print(
                    f"aviso: no se pudo abrir {self.key}: {server.errorString()}",
                    file=sys.stderr,
                )
                return False
        server.newConnection.connect(self._on_new_connection)
        self._server = server
        return True

    def _on_new_connection(self) -> None:
        if self._server is None:
            return
        socket = self._server.nextPendingConnection()
        if socket is None:
            return
        # Propiedad de Qt (padre = este objeto): así deleteLater() no
        # provoca un segundo borrado desde Python al finalizar.
        socket.setParent(self)
        message = ""
        if socket.waitForReadyRead(1000):
            message = bytes(socket.readAll()).decode("utf-8", "replace")
        socket.disconnectFromServer()
        socket.deleteLater()
        if message.strip():
            self.received.emit(message.strip())
