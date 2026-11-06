# -*- mode: python ; coding: utf-8 -*-
"""Receta de PyInstaller para el AppImage de Pasaporte."""

from pathlib import Path

from PyInstaller.utils.hooks import collect_data_files

ROOT = Path(SPECPATH).resolve().parent
SRC = ROOT / "src"

datas = [
    (
        str(SRC / "pasaporte" / "translations"),
        "pasaporte/translations",
    ),
]

# QtWebEngine y las traducciones de Qt que no siempre recoge el hook.
datas += collect_data_files(
    "PySide6",
    includes=[
        "Qt/libexec/QtWebEngineProcess",
        "Qt/resources/*",
        "Qt/translations/qtbase_es.qm",
        "Qt/translations/qtwebengine_locales/*",
    ],
)

hiddenimports = [
    "PySide6.QtWebEngineWidgets",
    "PySide6.QtWebEngineCore",
    "PySide6.QtWebChannel",
    "PySide6.QtWebSockets",
    "PySide6.QtNetwork",
    "PySide6.QtPrintSupport",
]

a = Analysis(
    [str(ROOT / "packaging" / "entry.py")],
    pathex=[str(SRC)],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)

# Usar el stack de fuentes del host evita warnings de fontconfig cuando
# el AppImage se ejecuta en una distro más nueva que el contenedor.
SYSTEM_LIBS = {
    "libfontconfig.so.1",
    "libfreetype.so.6",
    "libharfbuzz.so.0",
    "libgbm.so.1",
    "libstdc++.so.6",
    "libgcc_s.so.1",
}
a.binaries = [
    entry
    for entry in a.binaries
    if Path(entry[0]).name not in SYSTEM_LIBS
]

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="pasaporte",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=False,
    upx_exclude=[],
    name="pasaporte",
)
