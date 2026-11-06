"""Cliente mínimo del protocolo de autenticación de GlobalProtect.

Solo se encarga de la fase previa al SAML: pide a ``prelogin.esp`` la
petición SAML y la devuelve para que la muestre un WebView.
"""

from __future__ import annotations

import base64
import gzip
import os
import ssl
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from pathlib import Path

from PySide6.QtCore import QCoreApplication

from .config import VPNServer

COOKIE_FIELDS = ("prelogin-cookie", "portal-userauthcookie")
DEFAULT_USER_AGENT = "PAN GlobalProtect"


class GlobalProtectError(RuntimeError):
    """Error contactando el portal/gateway de GlobalProtect."""


class SamlNotAvailable(GlobalProtectError):
    """El servidor no anuncia SAML en la interfaz elegida."""


@dataclass
class SamlRequest:
    method: str      # POST o REDIRECT
    payload: str     # HTML (POST) o URL (REDIRECT)
    host: str
    endpoint: str


@dataclass
class SamlResult:
    """Resultado del login SAML, listo para pasárselo a openconnect."""

    username: str
    cookie: str
    cookie_field: str      # prelogin-cookie | portal-userauthcookie
    server: str            # host:puerto donde responderá el gateway
    interface: str         # portal | gateway


def _ssl_context(no_verify: bool) -> ssl.SSLContext:
    # create_default_context() carga el almacén de CAs del sistema.
    # SSLContext(PROTOCOL_TLS_CLIENT) NO lo hace por sí solo.
    context = ssl.create_default_context()

    # En un AppImage, el OpenSSL empaquetado puede tener rutas de CA
    # distintas a las del host. Cargamos explícitamente el bundle del
    # sistema si existe.
    if not no_verify:
        candidates = (
            os.environ.get("SSL_CERT_FILE"),
            "/etc/pki/tls/certs/ca-bundle.crt",
            "/etc/ssl/certs/ca-certificates.crt",
            "/etc/ssl/cert.pem",
        )
        for candidate in candidates:
            if candidate and Path(candidate).is_file():
                try:
                    context.load_verify_locations(cafile=candidate)
                    break
                except ssl.SSLError:
                    continue

    # Muchos portales GlobalProtect antiguos usan cifrados débiles.
    try:
        context.set_ciphers("DEFAULT:@SECLEVEL=1")
    except ssl.SSLError:
        pass

    # OpenSSL: SSL_OP_LEGACY_SERVER_CONNECT
    context.options |= getattr(ssl, "OP_LEGACY_SERVER_CONNECT", 1 << 2)

    if no_verify:
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE

    return context


def request_saml(server: VPNServer, timeout: int = 30) -> SamlRequest:
    """Pide a GlobalProtect la petición SAML y la devuelve.

    Lanza ``SamlNotAvailable`` si el servidor no usa SAML.
    """
    interface = "gateway" if server.gateway else "portal"
    path = (
        "ssl-vpn/prelogin.esp"
        if interface == "gateway"
        else "global-protect/prelogin.esp"
    )
    endpoint = f"https://{server.host}/{path}"
    clientos = server.clientos or "Windows"
    useragent = server.useragent or DEFAULT_USER_AGENT

    data = {
        "tmp": "tmp",
        "kerberos-support": "yes",
        "ipv6-support": "yes",
        "clientVer": "4100",
        "clientos": clientos,
    }

    request = urllib.request.Request(
        endpoint,
        data=urllib.parse.urlencode(data).encode("utf-8"),
        headers={
            "User-Agent": useragent,
            "Content-Type": "application/x-www-form-urlencoded",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(
            request,
            context=_ssl_context(server.no_verify),
            timeout=timeout,
        ) as response:
            content = response.read()
            if response.headers.get("Content-Encoding", "").lower() == "gzip":
                content = gzip.decompress(content)
    except urllib.error.HTTPError as exc:
        raise GlobalProtectError(
            QCoreApplication.translate(
                "GlobalProtect", "{endpoint} returned HTTP {code}"
            ).format(endpoint=endpoint, code=exc.code)
        ) from exc
    except Exception as exc:
        raise GlobalProtectError(
            QCoreApplication.translate(
                "GlobalProtect", "Could not contact {endpoint}: {error}"
            ).format(endpoint=endpoint, error=exc)
        ) from exc

    try:
        root = ET.fromstring(content)
    except ET.ParseError as exc:
        raise GlobalProtectError(
            QCoreApplication.translate(
                "GlobalProtect",
                "Invalid response from {endpoint}: {error}",
            ).format(endpoint=endpoint, error=exc)
        ) from exc

    if root.tag != "prelogin-response":
        raise GlobalProtectError(
            QCoreApplication.translate(
                "GlobalProtect",
                "{host} does not appear to be a GlobalProtect "
                "{interface} (response <{tag}>)",
            ).format(
                host=server.host,
                interface=interface,
                tag=root.tag,
            )
        )

    status = (root.findtext("status") or "").strip()
    if status and status != "Success":
        message = (root.findtext("msg") or "").strip()
        detail = f"{status}: {message}" if message else status
        raise GlobalProtectError(
            QCoreApplication.translate(
                "GlobalProtect",
                "GlobalProtect returned an error: {detail}",
            ).format(detail=detail)
        )

    method = (root.findtext("saml-auth-method") or "").strip()
    encoded = (root.findtext("saml-request") or "").strip()

    if not method or not encoded:
        other = "portal" if interface == "gateway" else "gateway"
        raise SamlNotAvailable(
            QCoreApplication.translate(
                "GlobalProtect",
                "{host} does not advertise SAML on the {interface} "
                "interface. Try 'gateway': {gateway} or disable 'saml'.",
            ).format(
                host=server.host,
                interface=interface,
                gateway="true" if other == "gateway" else "false",
            )
        )

    try:
        payload = base64.b64decode(encoded).decode("utf-8")
    except Exception as exc:
        raise GlobalProtectError(
            QCoreApplication.translate(
                "GlobalProtect",
                "Could not decode the SAML request: {error}",
            ).format(error=exc)
        ) from exc

    if method not in ("POST", "REDIRECT"):
        raise GlobalProtectError(
            QCoreApplication.translate(
                "GlobalProtect", "Unknown SAML method: {method}"
            ).format(method=method)
        )

    return SamlRequest(
        method=method,
        payload=payload,
        host=server.host,
        endpoint=endpoint,
    )
