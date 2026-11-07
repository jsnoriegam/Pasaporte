"""Entrada XDG de arranque con la sesión."""

from __future__ import annotations

import os
import shutil
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

_TMP = tempfile.TemporaryDirectory()
os.environ["XDG_CONFIG_HOME"] = str(Path(_TMP.name) / "xdg")

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from pasaporte import autostart  # noqa: E402
from pasaporte.constants import APP_ID  # noqa: E402


class AutostartTests(unittest.TestCase):
    def setUp(self) -> None:
        shutil.rmtree(Path(_TMP.name) / "xdg", ignore_errors=True)

    def test_enable_writes_entry_and_disable_removes_it(self) -> None:
        self.assertFalse(autostart.is_enabled())
        path = autostart.enable("/opt/pasaporte/pasaporte")
        self.assertEqual(path.name, f"{APP_ID}.desktop")
        self.assertEqual(path.parent.name, "autostart")
        self.assertTrue(autostart.is_enabled())

        text = path.read_text(encoding="utf-8")
        self.assertIn("Type=Application\n", text)
        self.assertIn(f"Icon={APP_ID}\n", text)
        self.assertIn('Exec="/opt/pasaporte/pasaporte" --start-hidden\n', text)

        autostart.disable()
        self.assertFalse(autostart.is_enabled())
        autostart.disable()  # idempotente

    def test_exec_quotes_paths_with_spaces_and_specials(self) -> None:
        entry = autostart.desktop_entry('/home/ana/Mis Apps/"x" $1%')
        line = next(l for l in entry.splitlines() if l.startswith("Exec="))
        self.assertEqual(
            line,
            'Exec="/home/ana/Mis Apps/\\"x\\" \\$1%%" --start-hidden',
        )

    def test_appimage_path_wins(self) -> None:
        with patch.dict(os.environ, {"APPIMAGE": "/home/ana/Pasaporte.AppImage"}):
            self.assertEqual(
                autostart.launch_command(), "/home/ana/Pasaporte.AppImage"
            )

    def test_source_launcher_without_appimage(self) -> None:
        env = {k: v for k, v in os.environ.items() if k != "APPIMAGE"}
        with patch.dict(os.environ, env, clear=True):
            command = autostart.launch_command()
        self.assertTrue(command.endswith("pasaporte"))


if __name__ == "__main__":
    unittest.main()
