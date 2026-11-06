"""Construcción de la línea de comandos de openconnect y elevación."""

from __future__ import annotations

import os
import shutil
from pathlib import Path

from PySide6.QtCore import QCoreApplication

from .config import VPNServer
from .gp import SamlResult

DEFAULT_GP_USER_AGENT = "PAN GlobalProtect"


class PrivilegeError(RuntimeError):
    pass


def openconnect_binary() -> str:
    """Localiza openconnect sin asumir una ruta fija.

    Prioridad:
      1. $OPENCONNECT_BIN (ruta o nombre de comando)
      2. shutil.which("openconnect")
    """
    override = os.environ.get("OPENCONNECT_BIN", "").strip()
    if override:
        candidate = Path(override).expanduser()
        if candidate.is_file() and os.access(candidate, os.X_OK):
            return str(candidate.resolve())
        found = shutil.which(override)
        if found:
            return found
        raise PrivilegeError(
            QCoreApplication.translate(
                "OpenConnect",
                "OPENCONNECT_BIN points to '{path}', but it is not an "
                "executable file.",
            ).format(path=override)
        )

    path = shutil.which("openconnect")
    if path:
        return path

    raise PrivilegeError(
        QCoreApplication.translate(
            "OpenConnect",
            "'openconnect' was not found. Install it or set "
            "OPENCONNECT_BIN to its path.",
        )
    )


def privilege_prefix(server: VPNServer) -> list[str]:
    """Devuelve el prefijo para ejecutar openconnect como root.

    ``pkexec`` es lo recomendado en escritorio: muestra el diálogo de
    Polkit y conserva stdin (necesario para --passwd-on-stdin).
    ``sudo -n`` requiere sudoers sin contraseña.
    """
    mode = (
        server.privilege
        or os.environ.get("VPN_GUI_PRIVILEGE")
        or ""
    ).strip().lower()

    if not mode:
        mode = "pkexec" if shutil.which("pkexec") else "sudo"

    binary = openconnect_binary()

    if mode == "pkexec":
        if not shutil.which("pkexec"):
            raise PrivilegeError(
                QCoreApplication.translate(
                    "OpenConnect",
                    "'pkexec' was not found. Install polkit or use "
                    "VPN_GUI_PRIVILEGE=sudo.",
                )
            )
        return ["pkexec", binary]

    if mode == "sudo":
        if not shutil.which("sudo"):
            raise PrivilegeError(
                QCoreApplication.translate(
                    "OpenConnect", "'sudo' was not found."
                )
            )
        return ["sudo", "-n", binary]

    raise PrivilegeError(
        QCoreApplication.translate(
            "OpenConnect",
            "Unknown privilege mode: {mode!r} (use 'pkexec' or 'sudo')",
        ).format(mode=mode)
    )


def build_connection(
    server: VPNServer,
    *,
    password: str | None = None,
    saml_result: SamlResult | None = None,
) -> tuple[list[str], str | None]:
    """Devuelve (argumentos de openconnect, secreto para stdin)."""
    args: list[str] = ["--protocol=" + server.protocol]

    username = saml_result.username if saml_result else server.username
    if not username:
        raise ValueError(
            QCoreApplication.translate(
                "OpenConnect",
                "No username for openconnect. The ACS did not return "
                "'saml-username' and the connection has no fallback "
                "'username'. Add one in the configuration.",
            )
        )
    args.append("--user=" + username)

    if server.servercert:
        args.append("--servercert=" + server.servercert)
    if server.allow_insecure_crypto:
        args.append("--allow-insecure-crypto")

    host = server.host
    secret: str | None = password

    if saml_result is not None:
        secret = saml_result.cookie
        if not server.ignore_redirects and saml_result.server:
            host = saml_result.server

        args.append("--os=" + (server.os or "win"))

        usergroup = (
            server.usergroup
            or f"{saml_result.interface}:{saml_result.cookie_field}"
        )
        args.append("--usergroup=" + usergroup)

        useragent = server.useragent or DEFAULT_GP_USER_AGENT
        if useragent:
            args.append("--useragent=" + useragent)

    elif server.protocol == "gp":
        if server.usergroup:
            args.append("--usergroup=" + server.usergroup)
        if server.os:
            args.append("--os=" + server.os)
        if server.useragent:
            args.append("--useragent=" + server.useragent)

    # En un GUI no hay terminal para responder prompts.
    args.append("--non-inter")

    if secret is not None:
        args.append("--passwd-on-stdin")

    args.extend(server.extra_args)
    args.append(host)
    return args, secret
