#!/usr/bin/env bash
# Construye Pasaporte-<version>-x86_64.AppImage.
# Pensado para ejecutarse dentro del contenedor de packaging/Containerfile.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

VENV="${BUILD_VENV:-/tmp/pasaporte-build-venv}"
export PIP_CACHE_DIR="${PIP_CACHE_DIR:-/tmp/pasaporte-pip-cache}"
export HOME="${HOME:-/tmp}"

python3 -m venv "$VENV"
"$VENV/bin/pip" install --upgrade pip
"$VENV/bin/pip" install -r requirements.txt pyinstaller

VERSION="$("$VENV/bin/python" - <<'PY'
import sys
sys.path.insert(0, "src")
from pasaporte.constants import APP_VERSION
print(APP_VERSION)
PY
)"

rm -rf build dist
"$VENV/bin/pyinstaller" --noconfirm --clean packaging/pasaporte.spec

APPDIR="$ROOT/build/AppDir"
rm -rf "$APPDIR"
mkdir -p \
    "$APPDIR/usr/bin" \
    "$APPDIR/usr/share/applications" \
    "$APPDIR/usr/share/icons/hicolor/scalable/apps" \
    "$APPDIR/usr/share/icons/hicolor/256x256/apps" \
    "$APPDIR/usr/share/metainfo"

cp -a "$ROOT/dist/pasaporte/." "$APPDIR/usr/bin/"
find "$APPDIR/usr/bin" -name QtWebEngineProcess -exec chmod +x {} \;

cp packaging/io.github.jsnoriegam.pasaporte.desktop \
    "$APPDIR/usr/share/applications/"
cp packaging/io.github.jsnoriegam.pasaporte.appdata.xml \
    "$APPDIR/usr/share/metainfo/"
cp packaging/pasaporte.svg \
    "$APPDIR/usr/share/icons/hicolor/scalable/apps/io.github.jsnoriegam.pasaporte.svg"
cp packaging/io.github.jsnoriegam.pasaporte.png \
    "$APPDIR/usr/share/icons/hicolor/256x256/apps/io.github.jsnoriegam.pasaporte.png"

cp packaging/AppRun "$APPDIR/AppRun"
chmod +x "$APPDIR/AppRun"
cp packaging/io.github.jsnoriegam.pasaporte.desktop \
    "$APPDIR/io.github.jsnoriegam.pasaporte.desktop"
cp packaging/pasaporte.svg "$APPDIR/io.github.jsnoriegam.pasaporte.svg"
cp packaging/io.github.jsnoriegam.pasaporte.png \
    "$APPDIR/io.github.jsnoriegam.pasaporte.png"

export ARCH=x86_64
export APPIMAGE_EXTRACT_AND_RUN=1

appimagetool --no-appstream "$APPDIR" \
    "$ROOT/dist/Pasaporte-${VERSION}-x86_64.AppImage"

echo
echo "AppImage: dist/Pasaporte-${VERSION}-x86_64.AppImage"
