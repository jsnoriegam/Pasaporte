"""Configuración común de los tests (Qt en modo offscreen)."""

from __future__ import annotations

import os
import socket

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
os.environ.setdefault("QTWEBENGINE_DISABLE_SANDBOX", "1")

if "QTWEBENGINE_REMOTE_DEBUGGING" not in os.environ:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as _sock:
        _sock.bind(("127.0.0.1", 0))
        _port = _sock.getsockname()[1]
    os.environ["QTWEBENGINE_REMOTE_DEBUGGING"] = str(_port)
