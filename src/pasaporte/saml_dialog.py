"""Ventana embebida para completar el login SAML de GlobalProtect."""

from __future__ import annotations

import base64
import html
import re
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from urllib.parse import unquote, urlparse

from PySide6.QtCore import Qt, QTimer, QUrl
from PySide6.QtWidgets import (
    QApplication,
    QDialog,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QProgressBar,
    QPushButton,
    QSizePolicy,
    QVBoxLayout,
)
from PySide6.QtWebEngineCore import QWebEnginePage, QWebEngineProfile
from PySide6.QtWebEngineWidgets import QWebEngineView

from .cdp import CdpClient
from .config import VPNServer
from .gp import COOKIE_FIELDS, SamlRequest, SamlResult


class _CommentParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.comments: list[str] = []

    def handle_comment(self, data: str) -> None:
        self.comments.append(data)


class SamlLoginDialog(QDialog):
    """Muestra el IdP en un WebView y captura el resultado del ACS.

    El ACS de GlobalProtect devuelve las cabeceras ``saml-username``,
    ``saml-auth-status`` y ``prelogin-cookie`` / ``portal-userauthcookie``.
    QtWebEngine no permite leer cabeceras de respuesta, así que usamos el
    protocolo DevTools para escucharlas.
    """

    _shared_profile = None
    _default_user_agent: str | None = None

    @classmethod
    def _get_profile(cls, user_agent: str | None) -> QWebEngineProfile:
        if cls._shared_profile is None:
            # Perfil off-the-record, pero con vida ligada a la aplicación
            # para que sobreviva a la página y no escriba nada en disco.
            cls._shared_profile = QWebEngineProfile(
                QApplication.instance()
            )
            raw_ua = cls._shared_profile.httpUserAgent()
            # Quitar el token "QtWebEngine/x.y" para que algunos IdP no
            # bloqueen el navegador embebido.
            cls._default_user_agent = re.sub(
                r"\s*QtWebEngine/[\d.]+", "", raw_ua
            )

        cls._shared_profile.setHttpUserAgent(
            user_agent or cls._default_user_agent or ""
        )
        return cls._shared_profile

    def __init__(
        self,
        server: VPNServer,
        saml: SamlRequest,
        devtools_port: int,
        parent=None,
    ) -> None:
        super().__init__(parent)
        self.server = server
        self.saml = saml
        self.devtools_port = devtools_port
        self.result_data: SamlResult | None = None

        self._values: dict[str, str] = {}
        self._responses: dict[str, str] = {}
        self._body_requests = 0
        self._closed = False
        self._loaded = False

        self.setWindowTitle(
            self.tr("SAML · {name}").format(name=server.display_name)
        )
        self.setModal(True)

        # Tamaño inicial razonable y acotado a la pantalla disponible.
        screen = QApplication.primaryScreen()
        if screen is not None:
            available = screen.availableGeometry()
            width = max(640, min(1000, available.width() - 80))
            height = max(480, min(800, available.height() - 80))
        else:
            width, height = 900, 700
        self.resize(width, height)
        self.setMinimumSize(min(640, width), min(480, height))

        layout = QVBoxLayout(self)

        header = QLabel(
            self.tr(
                "<b>{name}</b><br>Complete the SSO login. When finished, "
                "the VPN will connect automatically."
            ).format(name=html.escape(server.display_name))
        )
        header.setTextFormat(Qt.RichText)
        header.setWordWrap(True)
        layout.addWidget(header)

        # Perfil efímero compartido: no persistimos cookies del IdP en disco.
        self.profile = self._get_profile(server.browser_useragent)

        self.page = QWebEnginePage(self.profile, self)
        self.page.certificateError.connect(self._on_certificate_error)

        self.view = QWebEngineView(self)
        self.view.setPage(self.page)
        layout.addWidget(self.view, 1)

        self.status = QLabel(self.tr("Preparing browser…"))
        self.status.setWordWrap(True)
        self.status.setTextFormat(Qt.PlainText)
        # Que una URL larga no dicte el ancho del diálogo.
        self.status.setSizePolicy(
            QSizePolicy.Policy.Ignored,
            QSizePolicy.Policy.Preferred,
        )
        layout.addWidget(self.status)

        bottom = QHBoxLayout()
        self.progress = QProgressBar()
        self.progress.setRange(0, 0)
        self.progress.setTextVisible(False)
        bottom.addWidget(self.progress, 1)

        cancel_button = QPushButton(self.tr("Cancel"))
        cancel_button.clicked.connect(self.reject)
        bottom.addWidget(cancel_button)
        layout.addLayout(bottom)

        self.view.loadStarted.connect(lambda: self._set_status(self.tr("Loading…")))
        self.view.loadProgress.connect(self._on_progress)
        self.view.loadFinished.connect(self._on_load_finished)

        self.cdp = CdpClient(
            devtools_port, self.page.devToolsId(), self
        )
        self.cdp.event.connect(self._on_cdp_event)
        self.cdp.ready.connect(self._load_saml_once)
        self.cdp.error.connect(
            lambda message: self._set_status(
                self.tr("DevTools: {message}").format(message=message)
            )
        )
        self.cdp.start()

        self._timeout = QTimer(self)
        self._timeout.setSingleShot(True)
        self._timeout.timeout.connect(self._on_timeout)
        self._timeout.start(5 * 60 * 1000)

        # Cargar cuando Network.enable esté activo. Si DevTools falla,
        # cargamos igualmente a los 2 segundos para no dejar la ventana en
        # blanco (aunque no se puedan capturar cabeceras).
        QTimer.singleShot(2000, self._load_saml_once)

    # ------------------------------------------------------------------ UI

    def _set_status(self, text: str) -> None:
        self.status.setText(text)

    @staticmethod
    def _short_url(url: str, limit: int = 80) -> str:
        """Acorta una URL para mostrarla sin romper el layout."""
        parsed = urlparse(url)
        if parsed.netloc:
            path = parsed.path
            if len(path) > 36:
                path = path[:33] + "…"
            short = f"{parsed.scheme}://{parsed.netloc}{path}"
        else:
            short = url
        if len(short) > limit:
            short = short[: limit - 1] + "…"
        return short

    def _on_progress(self, value: int) -> None:
        if value < 100:
            self._set_status(
                self.tr("Loading… {value}%").format(value=value)
            )

    def _on_load_finished(self, ok: bool) -> None:
        url = self.view.url().toString()
        if not ok:
            self._set_status(
                self.tr("Could not load: {url}").format(
                    url=self._short_url(url)
                )
            )
            return

        self._set_status(
            self.tr("Loaded: {url}").format(
                url=self._short_url(url)
            )
        )

        # Algunos ACS devuelven el resultado dentro de un comentario HTML
        # en lugar de cabeceras. Lo revisamos también desde el DOM.
        self.page.runJavaScript(
            "document.documentElement ? "
            "document.documentElement.outerHTML : ''",
            lambda html_text: self._parse_html_result(
                html_text, url
            ),
        )

    def _on_certificate_error(self, error) -> None:
        if self.server.no_verify:
            error.acceptCertificate()
        else:
            self._set_status(
                self.tr("Certificate rejected: {error}").format(
                    error=error.description()
                )
            )
            error.rejectCertificate()

    # -------------------------------------------------------------- SAML

    def _load_saml(self) -> None:
        if self.saml.method == "POST":
            # El HTML contiene el formulario que el IdP espera recibir.
            base = QUrl(f"https://{self.saml.host}/")
            self.view.setHtml(self.saml.payload, base)
        else:
            self.view.load(QUrl(self.saml.payload))

    def _load_saml_once(self) -> None:
        if self._loaded or self._closed:
            return
        self._loaded = True
        self._set_status(self.tr("Waiting for SSO login…"))
        self._load_saml()

    def _on_cdp_event(self, event: dict) -> None:
        method = event.get("method")
        params = event.get("params") or {}

        if method == "Network.responseReceived":
            response = params.get("response") or {}
            url = response.get("url") or ""
            headers = {
                str(key).lower(): str(value)
                for key, value in (response.get("headers") or {}).items()
            }
            interesting = {
                key: value
                for key, value in headers.items()
                if key.startswith("saml-") or key in COOKIE_FIELDS
            }

            # Algunos portales devuelven la cookie en Set-Cookie en vez de
            # en una cabecera propia.
            set_cookie = headers.get("set-cookie", "")
            for field in COOKIE_FIELDS:
                match = re.search(
                    rf"(?:^|[;,]\s*){re.escape(field)}=([^;,\s]+)",
                    set_cookie,
                )
                if match:
                    interesting.setdefault(field, match.group(1))

            if interesting:
                self._merge(interesting, url)
            self._responses[params.get("requestId", "")] = url

        elif method == "Network.loadingFinished":
            request_id = params.get("requestId", "")
            url = self._responses.get(request_id, "")
            if not self._should_fetch_body(url):
                return
            self._body_requests += 1
            if self._body_requests > 50:
                return
            self.cdp.send(
                "Network.getResponseBody",
                {"requestId": request_id},
                self._on_response_body,
            )

    def _should_fetch_body(self, url: str) -> bool:
        lowered = url.lower()
        return (
            "/saml20/sp/acs" in lowered
            or "/acs" in lowered
            or "saml" in lowered
        )

    def _on_response_body(self, result: dict, error: dict | None) -> None:
        if error:
            return
        body = result.get("body") or ""
        if result.get("base64Encoded"):
            try:
                body = base64.b64decode(body).decode("utf-8", "replace")
            except Exception:
                return
        if body:
            self._parse_html_result(body, self.view.url().toString())

    def _parse_html_result(self, text: str, url: str) -> None:
        if not text:
            return

        # Caso 1: el cuerpo es XML (por ejemplo <prelogin-response>).
        xml_values = self._scan_xml(text)
        if xml_values:
            self._merge(xml_values, url)

        # Caso 2: el cuerpo es HTML y los datos están en un comentario.
        parser = _CommentParser()
        try:
            parser.feed(text)
        except Exception:
            return

        for comment in parser.comments:
            if not comment.strip():
                continue
            values = self._scan_xml(
                f"<fakexmlroot>{comment}</fakexmlroot>"
            )
            if values:
                self._merge(values, url)

    def _scan_xml(self, text: str) -> dict[str, str]:
        text = text.strip()
        if not text.startswith("<"):
            return {}
        try:
            root = ET.fromstring(text)
        except ET.ParseError:
            return {}

        values: dict[str, str] = {}
        for element in root.iter():
            tag = element.tag
            if not isinstance(tag, str):
                continue
            if tag.startswith("saml-") or tag in COOKIE_FIELDS:
                if element.text:
                    values[tag] = element.text.strip()
        return values

    def _merge(self, values: dict[str, str], url: str) -> None:
        self._values.update(values)
        if url:
            host = urlparse(url).netloc
            if host:
                self._values.setdefault("server", host)
        self._check_done()

    def _check_done(self) -> bool:
        status = (self._values.get("saml-auth-status") or "").strip()
        if status == "0":
            self._set_status(self.tr("The SAML provider rejected authentication."))
            return False

        cookie_field = next(
            (field for field in COOKIE_FIELDS if self._values.get(field)),
            None,
        )
        if not cookie_field:
            return False

        saml_username = self._values.get("saml-username")
        if not saml_username and not self.server.username:
            self._set_status(
                self.tr(
                    "The ACS did not return 'saml-username'. Cancel and "
                    "add a fallback username in the configuration."
                )
            )
            return False

        if saml_username:
            username = unquote(saml_username)
        else:
            username = self.server.username

        if self.server.ignore_redirects:
            host = self.server.host
        else:
            host = self._values.get("server") or self.server.host

        # La interfaz es la que se pidió en el prelogin (portal o gateway),
        # no la que sugiere el nombre de la cookie. Igual que gp-saml-gui.
        interface = "gateway" if self.server.gateway else "portal"

        self.result_data = SamlResult(
            username=username,
            cookie=self._values[cookie_field],
            cookie_field=cookie_field,
            server=host,
            interface=interface,
        )
        self._set_status(self.tr("SAML complete. Connecting…"))
        self.accept()
        return True

    def _on_timeout(self) -> None:
        if self._closed:
            return
        QMessageBox.warning(
            self,
            "SAML",
            self.tr("SAML login took too long. Try again."),
        )
        self.reject()

    # ------------------------------------------------------------ cierre

    def accept(self) -> None:
        self._closed = True
        self._timeout.stop()
        self.cdp.stop()
        super().accept()

    def reject(self) -> None:
        self._closed = True
        self._timeout.stop()
        self.cdp.stop()
        super().reject()

    def closeEvent(self, event) -> None:
        self._closed = True
        self._timeout.stop()
        self.cdp.stop()
        super().closeEvent(event)
