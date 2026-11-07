"""Arranque de Pasaporte con la sesión (entrada XDG autostart)."""

from __future__ import annotations

import os
from pathlib import Path

from .constants import APP_ID, APP_NAME, PROJECT_DIR, xdg_config_home


def autostart_path() -> Path:
    return xdg_config_home() / "autostart" / f"{APP_ID}.desktop"


def is_enabled() -> bool:
    return autostart_path().is_file()


def launch_command() -> str:
    # El AppImage exporta la ruta de su propio archivo en APPIMAGE.
    appimage = os.environ.get("APPIMAGE")
    if appimage:
        return appimage
    return str(PROJECT_DIR / "pasaporte")


def _quote(value: str) -> str:
    """Cita un argumento según la especificación de Exec de Desktop Entry."""
    escaped = (
        value.replace("\\", "\\\\")
        .replace('"', '\\"')
        .replace("`", "\\`")
        .replace("$", "\\$")
        .replace("%", "%%")
    )
    return f'"{escaped}"'


def desktop_entry(command: str) -> str:
    return (
        "[Desktop Entry]\n"
        "Type=Application\n"
        f"Name={APP_NAME}\n"
        "Comment=Start Pasaporte in the tray at login\n"
        f"Exec={_quote(command)} --start-hidden\n"
        f"Icon={APP_ID}\n"
        "Terminal=false\n"
        "X-GNOME-Autostart-enabled=true\n"
    )


def enable(command: str | None = None) -> Path:
    path = autostart_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(desktop_entry(command or launch_command()), encoding="utf-8")
    path.chmod(0o644)
    return path


def disable() -> None:
    autostart_path().unlink(missing_ok=True)
