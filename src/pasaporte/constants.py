"""Identidad y rutas centralizadas de Pasaporte."""

from __future__ import annotations

import os
from pathlib import Path

APP_NAME = "Pasaporte"
APP_SLUG = "pasaporte"
APP_ID = "io.github.jsnoriegam.pasaporte"
APP_VERSION = "0.2.0"

PROJECT_DIR = Path(__file__).resolve().parents[2]


def xdg_config_home() -> Path:
    value = os.environ.get("XDG_CONFIG_HOME")
    if value:
        return Path(value).expanduser()
    return Path.home() / ".config"


def config_dir() -> Path:
    return xdg_config_home() / APP_SLUG


def config_path() -> Path:
    return config_dir() / "hosts.json"


def legacy_config_paths() -> list[Path]:
    """Rutas antiguas desde las que se puede migrar."""
    return [
        xdg_config_home() / "vpn" / "hosts.json",
        PROJECT_DIR / "vpn.json",
    ]
