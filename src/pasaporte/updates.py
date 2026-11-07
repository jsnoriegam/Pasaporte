"""Comprobación manual de nuevas versiones de Pasaporte.

Solo se consulta la API pública de GitHub cuando el usuario lo pide; no hay
comprobaciones automáticas en segundo plano.
"""

from __future__ import annotations

import json
import re
import urllib.error
import urllib.request
from dataclasses import dataclass

from .constants import APP_VERSION

RELEASES_API = (
    "https://api.github.com/repos/jsnoriegam/Pasaporte/releases?per_page=10"
)
RELEASES_PAGE = "https://github.com/jsnoriegam/Pasaporte/releases"

_VERSION_RE = re.compile(
    r"^v?(\d+)\.(\d+)\.(\d+)(?:-([0-9A-Za-z.-]+))?$"
)


class UpdateError(RuntimeError):
    """No se pudo consultar la lista de releases."""


@dataclass(frozen=True)
class ReleaseInfo:
    version: str
    url: str


def parse_version(text: str) -> tuple[tuple[int, int, int], tuple | None]:
    """Devuelve (núcleo, identificadores de pre-release) según SemVer.

    Un pre-release tiene identificadores; una versión estable no tiene
    ninguno y, a igualdad de núcleo, va después de cualquier pre-release.
    """
    match = _VERSION_RE.match(text.strip())
    if match is None:
        raise ValueError(f"versión no válida: {text!r}")
    core = (int(match[1]), int(match[2]), int(match[3]))
    if match[4] is None:
        return core, None
    identifiers = tuple(
        (0, int(part), "") if part.isdigit() else (1, 0, part)
        for part in match[4].split(".")
    )
    return core, identifiers


def is_newer(candidate: str, current: str = APP_VERSION) -> bool:
    cand_core, cand_pre = parse_version(candidate)
    cur_core, cur_pre = parse_version(current)
    if cand_core != cur_core:
        return cand_core > cur_core
    if cand_pre is None:
        return cur_pre is not None
    if cur_pre is None:
        return False
    return cand_pre > cur_pre


def latest_release(
    url: str = RELEASES_API,
    timeout: float = 10,
    include_prereleases: bool = True,
) -> ReleaseInfo | None:
    """Devuelve la release más reciente o None si no hay ninguna."""
    request = urllib.request.Request(
        url,
        headers={
            "Accept": "application/vnd.github+json",
            "User-Agent": "Pasaporte-update-check",
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            releases = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        exc.close()
        raise UpdateError(f"HTTP {exc.code}") from exc
    except (OSError, ValueError) as exc:
        raise UpdateError(str(exc)) from exc

    if not isinstance(releases, list):
        raise UpdateError("respuesta inesperada de GitHub")

    for release in releases:
        if release.get("draft"):
            continue
        if release.get("prerelease") and not include_prereleases:
            continue
        tag = str(release.get("tag_name", ""))
        try:
            parse_version(tag)
        except ValueError:
            continue
        return ReleaseInfo(
            version=tag.lstrip("v"),
            url=str(release.get("html_url") or RELEASES_PAGE),
        )
    return None
