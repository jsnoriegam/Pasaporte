"""Configuración JSON de conexiones VPN: lectura, validación y escritura."""

from __future__ import annotations

import json
import os
import shutil
import tempfile
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from PySide6.QtCore import QCoreApplication

KNOWN_PROTOCOLS = {
    "fortinet",
    "gp",
    "anyconnect",
    "pulse",
    "nc",
    "f5",
    "array",
}

SERVERCERT_PREFIXES = ("pin-sha256:", "sha256:", "sha1:")


class ConfigConflictError(RuntimeError):
    """El archivo cambió en disco desde que se cargó."""


def default_config_path() -> Path:
    """Ruta canónica, salvo que $VPN_CONFIG la sobrescriba."""
    from .paths import resolve_config_path

    return resolve_config_path(None).path


def _as_bool(value: Any, default: bool = False) -> bool:
    if value is None:
        return default
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.strip().lower() in {"1", "true", "yes", "si", "sí", "on"}
    return bool(value)


def _as_str_list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, str):
        return value.split()
    if isinstance(value, (list, tuple)):
        return [str(item) for item in value]
    raise ValueError(
        QCoreApplication.translate(
            "Config", "'extra_args' must be a list of strings."
        )
    )


@dataclass
class VPNServer:
    name: str
    host: str
    username: str
    protocol: str = "fortinet"
    servercert: str | None = None

    # GlobalProtect / SAML
    saml: bool = False
    gateway: bool = False
    usergroup: str | None = None
    os: str | None = None
    clientos: str | None = None
    useragent: str | None = None
    browser_useragent: str | None = None
    ignore_redirects: bool = False

    # Seguridad / comportamiento
    no_verify: bool = False
    allow_insecure_crypto: bool = False
    privilege: str | None = None

    # Extras
    extra_args: list[str] = field(default_factory=list)
    description: str | None = None

    @property
    def requires_saml(self) -> bool:
        return self.protocol == "gp" and self.saml

    @property
    def display_name(self) -> str:
        return self.name or self.host

    @property
    def subtitle(self) -> str:
        if self.username:
            return f"{self.protocol} · {self.username} · {self.host}"
        return f"{self.protocol} · {self.host}"


def validate_host(host: str) -> str | None:
    if not host.strip():
        return QCoreApplication.translate(
            "Config", "Host is required."
        )
    if "://" in host:
        return QCoreApplication.translate(
            "Config", "Host must not include http:// or https://."
        )
    if "/" in host:
        return QCoreApplication.translate(
            "Config", "Host must not include a path; use host:port."
        )
    if any(char.isspace() for char in host):
        return QCoreApplication.translate(
            "Config", "Host must not contain spaces."
        )
    return None


def validate_server(server: VPNServer) -> list[str]:
    errors: list[str] = []

    host_error = validate_host(server.host)
    if host_error:
        errors.append(host_error)

    if server.protocol not in KNOWN_PROTOCOLS:
        errors.append(
            QCoreApplication.translate(
                "Config", "Unknown protocol: {protocol!r}."
            ).format(protocol=server.protocol)
        )

    if server.saml and server.protocol != "gp":
        errors.append(
            QCoreApplication.translate(
                "Config",
                "'saml' is only supported with protocol 'gp'.",
            )
        )

    if not server.username and not server.requires_saml:
        errors.append(
            QCoreApplication.translate(
                "Config",
                "Username is required (except for GlobalProtect with SAML).",
            )
        )

    if server.servercert and not server.servercert.startswith(
        SERVERCERT_PREFIXES
    ):
        errors.append(
            QCoreApplication.translate(
                "Config",
                "servercert must start with pin-sha256:, sha256: or sha1:.",
            )
        )

    if server.privilege and server.privilege not in {"pkexec", "sudo"}:
        errors.append(
            QCoreApplication.translate(
                "Config",
                "privilege must be 'pkexec', 'sudo' or empty.",
            )
        )

    if not isinstance(server.extra_args, list) or any(
        not isinstance(arg, str) for arg in server.extra_args
    ):
        errors.append(
            QCoreApplication.translate(
                "Config", "extra_args must be a list of strings."
            )
        )

    return errors


def find_duplicate(
    server: VPNServer,
    existing: list[VPNServer],
    skip_index: int | None = None,
) -> int | None:
    for index, other in enumerate(existing):
        if skip_index is not None and index == skip_index:
            continue
        if (
            other.protocol == server.protocol
            and other.host.lower() == server.host.lower()
            and other.username.lower() == server.username.lower()
        ):
            return index
    return None


def _parse_server(item: dict[str, Any], number: int) -> VPNServer:
    host = str(item.get("host") or "").strip()
    username = str(item.get("username") or "").strip()
    name = str(item.get("name") or host).strip()
    protocol = str(item.get("protocol") or "fortinet").strip().lower()
    saml = _as_bool(item.get("saml"))

    server = VPNServer(
        name=name or host,
        host=host,
        username=username,
        protocol=protocol,
        servercert=(
            str(item["servercert"]).strip()
            if item.get("servercert")
            else None
        ),
        saml=saml,
        gateway=_as_bool(item.get("gateway")),
        usergroup=(
            str(item["usergroup"]).strip()
            if item.get("usergroup")
            else None
        ),
        os=str(item["os"]).strip() if item.get("os") else None,
        clientos=(
            str(item["clientos"]).strip()
            if item.get("clientos")
            else None
        ),
        useragent=(
            str(item["useragent"]).strip()
            if item.get("useragent")
            else None
        ),
        browser_useragent=(
            str(item["browser_useragent"]).strip()
            if item.get("browser_useragent")
            else None
        ),
        ignore_redirects=_as_bool(item.get("ignore_redirects")),
        no_verify=_as_bool(item.get("no_verify")),
        allow_insecure_crypto=_as_bool(
            item.get("allow_insecure_crypto")
        ),
        privilege=(
            str(item["privilege"]).strip().lower()
            if item.get("privilege")
            else None
        ),
        extra_args=_as_str_list(
            item.get("extra_args") or item.get("extra")
        ),
        description=(
            str(item["description"]).strip()
            if item.get("description")
            else None
        ),
    )

    errors = validate_server(server)
    if errors:
        raise ValueError(
            QCoreApplication.translate(
                "Config", "Entry #{number} ({name}): {error}"
            ).format(
                number=number,
                name=server.display_name,
                error=errors[0],
            )
        )

    return server


def parse_servers(raw: Any) -> list[VPNServer]:
    if not isinstance(raw, list):
        raise ValueError(
            QCoreApplication.translate(
                "Config", "The JSON must be an array of connections."
            )
        )

    servers: list[VPNServer] = []
    for index, item in enumerate(raw):
        number = index + 1
        if not isinstance(item, dict):
            raise ValueError(
                QCoreApplication.translate(
                    "Config", "Entry #{number} is not a JSON object."
                ).format(number=number)
            )
        servers.append(_parse_server(item, number))
    return servers


def apply_server_to_dict(base: dict[str, Any], server: VPNServer) -> dict:
    """Actualiza un dict preservando campos desconocidos."""
    data = dict(base)

    data["name"] = server.name or server.host
    data["host"] = server.host

    if server.protocol == "fortinet":
        data.pop("protocol", None)
    else:
        data["protocol"] = server.protocol

    if server.username:
        data["username"] = server.username
    else:
        data.pop("username", None)

    optional = {
        "servercert": server.servercert,
        "usergroup": server.usergroup,
        "os": server.os,
        "clientos": server.clientos,
        "useragent": server.useragent,
        "browser_useragent": server.browser_useragent,
        "privilege": server.privilege,
        "description": server.description,
    }
    for key, value in optional.items():
        if value:
            data[key] = value
        else:
            data.pop(key, None)

    booleans = {
        "saml": server.saml,
        "gateway": server.gateway,
        "ignore_redirects": server.ignore_redirects,
        "no_verify": server.no_verify,
        "allow_insecure_crypto": server.allow_insecure_crypto,
    }
    for key, value in booleans.items():
        if value:
            data[key] = True
        else:
            data.pop(key, None)

    if server.extra_args:
        data["extra_args"] = list(server.extra_args)
        data.pop("extra", None)
    else:
        data.pop("extra_args", None)
        data.pop("extra", None)

    return data


def server_to_dict(server: VPNServer) -> dict:
    return apply_server_to_dict({}, server)


def load_raw(path: Path, *, missing_ok: bool = True) -> list[dict]:
    config_path = path.expanduser()
    if not config_path.exists():
        if missing_ok:
            return []
        raise FileNotFoundError(
            QCoreApplication.translate(
                "Config",
                "Configuration file does not exist: {path}",
            ).format(path=config_path)
        )

    text = config_path.read_text(encoding="utf-8")
    if not text.strip():
        return []

    try:
        raw = json.loads(text)
    except json.JSONDecodeError as exc:
        raise ValueError(
            QCoreApplication.translate(
                "Config", "Invalid JSON in {path}: {error}"
            ).format(path=config_path, error=exc)
        ) from exc

    if not isinstance(raw, list):
        raise ValueError(
            QCoreApplication.translate(
                "Config", "{path} must contain a JSON array."
            ).format(path=config_path)
        )
    return raw


def save_raw(path: Path, raw: list[dict]) -> None:
    """Escribe el JSON de forma atómica, con backup y permisos 0600."""
    config_path = path.expanduser()
    target = (
        config_path.resolve()
        if config_path.is_symlink()
        else config_path
    )

    parent = target.parent
    parent_existed = parent.exists()
    parent.mkdir(parents=True, exist_ok=True)
    if not parent_existed:
        try:
            os.chmod(parent, 0o700)
        except OSError:
            pass

    if target.exists():
        backup = target.with_name(target.name + ".bak")
        shutil.copy2(target, backup)
        try:
            os.chmod(backup, 0o600)
        except OSError:
            pass

    temp_name: str | None = None
    try:
        with tempfile.NamedTemporaryFile(
            "w",
            dir=target.parent,
            prefix=f".{target.name}.",
            suffix=".tmp",
            delete=False,
            encoding="utf-8",
        ) as handle:
            temp_name = handle.name
            json.dump(raw, handle, indent=2, ensure_ascii=False)
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())

        os.chmod(temp_name, 0o600)
        os.replace(temp_name, target)
        temp_name = None

        # Durabilidad del renombrado (mejor esfuerzo).
        try:
            dir_fd = os.open(str(target.parent), os.O_DIRECTORY)
            try:
                os.fsync(dir_fd)
            finally:
                os.close(dir_fd)
        except OSError:
            pass
    finally:
        if temp_name is not None:
            try:
                os.unlink(temp_name)
            except OSError:
                pass


class ConfigStore:
    """Mantiene el JSON crudo y la lista validada de conexiones."""

    def __init__(self, path: Path, *, load: bool = True) -> None:
        self.path = path.expanduser()
        self.raw: list[dict] = []
        self.servers: list[VPNServer] = []
        self._mtime: int | None = None
        if load:
            self.reload()

    def _file_mtime(self) -> int | None:
        try:
            return self.path.stat().st_mtime_ns
        except FileNotFoundError:
            return None

    def changed_on_disk(self) -> bool:
        return self._file_mtime() != self._mtime

    def reload(self) -> None:
        raw = load_raw(self.path)
        servers = parse_servers(raw)
        self.raw = raw
        self.servers = servers
        self._mtime = self._file_mtime()

    def save(self, *, force: bool = False) -> None:
        if not force and self.changed_on_disk():
            raise ConfigConflictError(
                QCoreApplication.translate(
                    "Config", "{path} changed outside Pasaporte."
                ).format(path=self.path)
            )
        save_raw(self.path, self.raw)
        self._mtime = self._file_mtime()

    def add(self, server: VPNServer) -> int:
        self.raw.append(server_to_dict(server))
        self._refresh()
        return len(self.servers) - 1

    def update(self, index: int, server: VPNServer) -> None:
        if not 0 <= index < len(self.raw):
            raise IndexError(
                QCoreApplication.translate(
                    "Config", "Index out of range: {index}"
                ).format(index=index)
            )
        self.raw[index] = apply_server_to_dict(
            self.raw[index], server
        )
        self._refresh()

    def replace(self, raw: list[dict]) -> None:
        """Reemplaza todo el contenido (importar/reemplazar)."""
        servers = parse_servers(raw)
        self.raw = [dict(item) for item in raw]
        self.servers = servers

    def delete(self, index: int) -> None:
        if not 0 <= index < len(self.raw):
            raise IndexError(
                QCoreApplication.translate(
                    "Config", "Index out of range: {index}"
                ).format(index=index)
            )
        del self.raw[index]
        self._refresh()

    def _refresh(self) -> None:
        self.servers = parse_servers(self.raw)


def load_config(path: Path | None = None) -> list[VPNServer]:
    if path is not None:
        return ConfigStore(path).servers

    from .paths import find_legacy_config, resolve_config_path

    target = resolve_config_path(None)
    config_path = target.path
    if target.canonical and not config_path.exists():
        legacy = find_legacy_config()
        if legacy is not None:
            config_path = legacy
    return ConfigStore(config_path).servers
