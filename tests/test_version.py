"""Consistencia de la versión de Pasaporte."""

from __future__ import annotations

import sys
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from pasaporte.constants import APP_VERSION  # noqa: E402

APPDATA = (
    ROOT / "packaging" / "io.github.jsnoriegam.pasaporte.appdata.xml"
)


class VersionTests(unittest.TestCase):
    def test_semver_shape(self) -> None:
        self.assertRegex(
            APP_VERSION,
            r"^\d+\.\d+\.\d+(-[0-9A-Za-z]+(\.[0-9A-Za-z]+)*)?$",
        )

    def test_appstream_release_matches(self) -> None:
        root = ET.parse(APPDATA).getroot()
        releases = root.findall(".//release")
        self.assertTrue(releases, "appdata must declare a release")
        self.assertEqual(releases[0].get("version"), APP_VERSION)

    def test_pyside_612_is_excluded_on_old_python(self) -> None:
        # PySide6 6.12.0 aborta con none_dealloc en Python <3.12.
        text = (ROOT / "requirements.txt").read_text(encoding="utf-8")
        lines = [
            line for line in text.splitlines()
            if line.startswith("PySide6") and "python_version <" in line
        ]
        self.assertTrue(lines)
        self.assertIn("<6.12", lines[0])
        self.assertIn('python_version < "3.12"', lines[0])


if __name__ == "__main__":
    unittest.main()
