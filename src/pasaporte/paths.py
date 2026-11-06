"""Resolución de rutas de configuración y migración a ~/.config/pasaporte."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from .config import load_raw, parse_servers, save_raw
from .constants import config_path, legacy_config_paths


@dataclass
class ConfigTarget:
    """Ruta activa y por qué se eligió."""

    path: Path
    explicit: bool = False
    canonical: bool = False

    def __post_init__(self) -> None:
        self.path = self.path.expanduser()


def canonical_config_path() -> Path:
    return config_path()


def resolve_config_path(cli_path: str | Path | None = None) -> ConfigTarget:
    """Prioridad: --config > $VPN_CONFIG > ~/.config/pasaporte/hosts.json."""
    if cli_path:
        return ConfigTarget(Path(cli_path), explicit=True, canonical=False)

    env = os.environ.get("VPN_CONFIG")
    if env:
        return ConfigTarget(Path(env), explicit=True, canonical=False)

    return ConfigTarget(
        canonical_config_path(), explicit=False, canonical=True
    )


def find_legacy_config() -> Path | None:
    """Devuelve la primera configuración legacy existente, si hay."""
    canonical = canonical_config_path().absolute()
    for candidate in legacy_config_paths():
        candidate = candidate.expanduser()
        if candidate.absolute() == canonical:
            continue
        if candidate.exists():
            return candidate
    return None


def migrate_config(source: Path, target: Path | None = None) -> int:
    """Copia y valida una configuración legacy en la ruta canónica.

    No borra el archivo de origen. Devuelve el número de conexiones.
    """
    source = source.expanduser()
    target = (target or canonical_config_path()).expanduser()

    if source.absolute() == target.absolute():
        return 0

    raw = load_raw(source, missing_ok=False)
    parse_servers(raw)
    save_raw(target, raw)
    return len(raw)


def connection_key(item: dict) -> str:
    return str(item.get("name") or item.get("host") or "").strip().casefold()


def merge_connections(
    current: list[dict],
    incoming: list[dict],
) -> tuple[list[dict], int, int]:
    """Fusiona por nombre, preservando los dicts originales.

    Devuelve (lista_fusionada, añadidas, omitidas).
    """
    merged = list(current)
    seen = {connection_key(item) for item in current}
    added = 0
    skipped = 0

    for item in incoming:
        key = connection_key(item)
        if key and key in seen:
            skipped += 1
            continue
        merged.append(dict(item))
        if key:
            seen.add(key)
        added += 1

    return merged, added, skipped
