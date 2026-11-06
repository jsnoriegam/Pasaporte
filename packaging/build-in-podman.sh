#!/usr/bin/env bash
# Construye el AppImage usando Podman (por defecto) o Docker.
#
#   ./packaging/build-in-podman.sh
#   CONTAINER_ENGINE=docker ./packaging/build-in-podman.sh
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ENGINE="${CONTAINER_ENGINE:-podman}"
IMAGE="${IMAGE:-pasaporte-appimage:latest}"

if ! command -v "$ENGINE" >/dev/null 2>&1; then
    echo "Error: no se encontró '$ENGINE'." >&2
    exit 1
fi

"$ENGINE" build -t "$IMAGE" -f "$ROOT/packaging/Containerfile" "$ROOT"

if [[ "$ENGINE" == "podman" ]]; then
    USER_ARGS=(--userns=keep-id)
    VOLUME="$ROOT:/src:Z"
else
    USER_ARGS=(--user "$(id -u):$(id -g)")
    VOLUME="$ROOT:/src"
fi

"$ENGINE" run --rm "${USER_ARGS[@]}" \
    -e HOME=/tmp \
    -e BUILD_VENV=/src/.build-venv \
    -e PIP_CACHE_DIR=/src/.build-cache/pip \
    -v "$VOLUME" \
    -w /src \
    "$IMAGE" \
    bash packaging/build-appimage.sh
