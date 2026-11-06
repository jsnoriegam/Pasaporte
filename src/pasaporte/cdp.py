"""Cliente mínimo del protocolo DevTools (CDP) de QtWebEngine.

QtWebEngine no expone las cabeceras HTTP de las respuestas. Para capturar
las cabeceras ``saml-*`` y ``prelogin-cookie`` que devuelve el ACS de
GlobalProtect usamos el servidor DevTools que QtWebEngine abre cuando se
define ``QTWEBENGINE_REMOTE_DEBUGGING`` antes de crear QApplication.
"""

from __future__ import annotations

import json
from typing import Callable

from PySide6.QtCore import QObject, QTimer, QUrl, Signal
from PySide6.QtNetwork import QNetworkAccessManager, QNetworkReply, QNetworkRequest
from PySide6.QtWebSockets import QWebSocket, QWebSocketProtocol

Callback = Callable[[dict, dict | None], None]


class CdpClient(QObject):
    event = Signal(dict)
    ready = Signal()
    error = Signal(str)

    def __init__(
        self,
        port: int,
        target_id: str | None = None,
        parent: QObject | None = None,
    ) -> None:
        super().__init__(parent)
        self._port = port
        self._target_id = target_id or None
        self._nam = QNetworkAccessManager(self)
        self._ws = QWebSocket(
            "", QWebSocketProtocol.VersionLatest, self
        )
        self._ws.connected.connect(self._on_connected)
        self._ws.textMessageReceived.connect(self._on_text)
        self._ws.errorOccurred.connect(self._on_ws_error)

        self._next_id = 1
        self._callbacks: dict[int, Callback] = {}
        self._attempts = 0
        self._started = False
        self._closed = False

    def start(self) -> None:
        if self._started:
            return
        self._started = True
        self._fetch_targets()

    def stop(self) -> None:
        self._closed = True
        self._callbacks.clear()
        try:
            self._ws.close()
        except RuntimeError:
            pass

    def send(
        self,
        method: str,
        params: dict | None = None,
        callback: Callback | None = None,
    ) -> int:
        message_id = self._next_id
        self._next_id += 1
        if callback is not None:
            self._callbacks[message_id] = callback
        payload = {"id": message_id, "method": method}
        if params:
            payload["params"] = params
        self._ws.sendTextMessage(json.dumps(payload))
        return message_id

    def _fetch_targets(self) -> None:
        if self._closed:
            return
        request = QNetworkRequest(
            QUrl(f"http://127.0.0.1:{self._port}/json")
        )
        reply = self._nam.get(request)
        reply.finished.connect(lambda: self._on_targets(reply))

    def _on_targets(self, reply: QNetworkReply) -> None:
        try:
            if reply.error() != QNetworkReply.NetworkError.NoError:
                self._retry(
                    self.tr("DevTools unavailable: {error}").format(
                        error=reply.errorString()
                    )
                )
                return

            targets = json.loads(bytes(reply.readAll()).decode("utf-8"))
            pages = [item for item in targets if item.get("type") == "page"]
            if not pages:
                self._retry(self.tr("no WebEngine page yet"))
                return

            target = None
            if self._target_id:
                target = next(
                    (
                        item
                        for item in pages
                        if item.get("id") == self._target_id
                    ),
                    None,
                )

            if target is None:
                # Fallback: la ventana SAML suele ser la única página. Si
                # hubiera varias, preferimos about:blank (la recién creada).
                target = next(
                    (
                        item
                        for item in pages
                        if item.get("url") in ("", "about:blank")
                    ),
                    pages[-1],
                )

            self._ws.open(QUrl(target["webSocketDebuggerUrl"]))
        finally:
            reply.deleteLater()

    def _retry(self, reason: str) -> None:
        self._attempts += 1
        if self._attempts >= 25:
            self.error.emit(reason)
            return
        QTimer.singleShot(200, self._fetch_targets)

    def _on_connected(self) -> None:
        self.send("Network.enable", callback=self._on_network_enabled)

    def _on_network_enabled(self, _result: dict, error: dict | None) -> None:
        if error:
            self.error.emit(f"Network.enable: {error}")
        else:
            self.ready.emit()

    def _on_text(self, message: str) -> None:
        try:
            data = json.loads(message)
        except json.JSONDecodeError:
            return

        if "id" in data:
            callback = self._callbacks.pop(data["id"], None)
            if callback is not None:
                try:
                    callback(data.get("result") or {}, data.get("error"))
                except Exception as exc:  # no romper el bucle de Qt
                    self.error.emit(
                        self.tr(
                            "error processing CDP: {error}"
                        ).format(error=exc)
                    )
            return

        method = data.get("method")
        if method:
            self.event.emit(data)

    def _on_ws_error(self, _error) -> None:
        if not self._closed:
            self.error.emit(
                self.tr("lost connection to DevTools")
            )
