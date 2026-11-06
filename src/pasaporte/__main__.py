"""Punto de entrada de la GUI."""

from __future__ import annotations

import argparse
import os
import socket
import sys
from pathlib import Path


def _free_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(("127.0.0.1", 0))
        return int(sock.getsockname()[1])


def _configure_devtools() -> int:
    """Configura el puerto DevTools antes de inicializar QtWebEngine.

    QtWebEngine solo abre el servidor DevTools si la variable de entorno
    existe antes de crear QApplication. El puerto es aleatorio y local.
    """
    value = os.environ.get("QTWEBENGINE_REMOTE_DEBUGGING")
    if value:
        port_text = value.rsplit(":", 1)[-1]
        try:
            port = int(port_text)
        except ValueError:
            port = 0
        if port > 0:
            os.environ["VPN_GUI_DEVTOOLS_PORT"] = str(port)
            return port

    port = _free_port()
    os.environ["QTWEBENGINE_REMOTE_DEBUGGING"] = str(port)
    os.environ["VPN_GUI_DEVTOOLS_PORT"] = str(port)
    return port


DEVTOOLS_PORT = _configure_devtools()

# Importar Qt DESPUÉS de configurar DevTools.
from PySide6.QtCore import QTimer  # noqa: E402
from PySide6.QtGui import QIcon  # noqa: E402
from PySide6.QtWidgets import QApplication  # noqa: E402

from .constants import APP_ID, APP_NAME, APP_SLUG  # noqa: E402
from .paths import resolve_config_path  # noqa: E402
from .ui import MainWindow  # noqa: E402


def _desktop_file_installed(app_id: str) -> bool:
    candidates = [
        Path.home() / ".local/share/applications" / f"{app_id}.desktop",
        Path("/usr/local/share/applications") / f"{app_id}.desktop",
        Path("/usr/share/applications") / f"{app_id}.desktop",
    ]
    return any(path.exists() for path in candidates)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            f"{APP_NAME}: graphical interface for openconnect "
            "(Fortinet, GlobalProtect/SAML, …)"
        )
    )
    parser.add_argument(
        "-c",
        "--config",
        help=(
            "path to the connections JSON "
            "(default: ~/.config/pasaporte/hosts.json)"
        ),
    )
    parser.add_argument(
        "--connect",
        metavar="NAME",
        help="connect to the named connection on startup",
    )
    args = parser.parse_args(argv)

    app = QApplication([sys.argv[0]])
    app.setApplicationName(APP_SLUG)
    app.setApplicationDisplayName(APP_NAME)
    app.setOrganizationName(APP_SLUG)

    is_appimage = bool(os.environ.get("APPDIR"))
    if is_appimage:
        app.setDesktopFileName(APP_ID)
    elif _desktop_file_installed(APP_SLUG):
        app.setDesktopFileName(APP_SLUG)

    icon = QIcon.fromTheme(APP_ID)
    if icon.isNull():
        icon = QIcon.fromTheme("network-vpn")
    app.setWindowIcon(icon)

    app.setProperty("pasaporte_devtools_port", DEVTOOLS_PORT)

    config_target = resolve_config_path(args.config)
    window = MainWindow(config_target)
    window.show()
    if args.connect:
        QTimer.singleShot(
            0, lambda: window.connect_by_name(args.connect)
        )
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
