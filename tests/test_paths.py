"""Tests de rutas, migración e importación/merge."""

from __future__ import annotations

import json
import os
import stat
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from pasaporte import constants  # noqa: E402
from pasaporte.paths import (  # noqa: E402
    canonical_config_path,
    find_legacy_config,
    merge_connections,
    migrate_config,
    resolve_config_path,
)


class PathsTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.xdg = self.root / "xdg"
        self.env = patch.dict(
            os.environ,
            {
                "XDG_CONFIG_HOME": str(self.xdg),
                "VPN_CONFIG": "",
            },
        )
        self.env.start()

    def tearDown(self) -> None:
        self.env.stop()
        self.tmp.cleanup()

    def _write(self, path: Path, data) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            json.dumps(data, indent=2) + "\n", encoding="utf-8"
        )

    def test_default_is_canonical(self) -> None:
        target = resolve_config_path(None)
        self.assertTrue(target.canonical)
        self.assertFalse(target.explicit)
        self.assertEqual(
            target.path, self.xdg / "pasaporte" / "hosts.json"
        )

    def test_env_overrides_canonical(self) -> None:
        custom = self.root / "custom.json"
        with patch.dict(os.environ, {"VPN_CONFIG": str(custom)}):
            target = resolve_config_path(None)
        self.assertTrue(target.explicit)
        self.assertFalse(target.canonical)
        self.assertEqual(target.path, custom)

    def test_cli_overrides_env(self) -> None:
        cli = self.root / "cli.json"
        env = self.root / "env.json"
        with patch.dict(os.environ, {"VPN_CONFIG": str(env)}):
            target = resolve_config_path(cli)
        self.assertEqual(target.path, cli)
        self.assertTrue(target.explicit)

    def test_find_legacy_order(self) -> None:
        project = self.root / "project"
        project.mkdir()
        user_legacy = self.xdg / "vpn" / "hosts.json"
        project_legacy = project / "vpn.json"
        self._write(
            user_legacy,
            [{"name": "user", "host": "u", "username": "u"}],
        )
        self._write(
            project_legacy,
            [{"name": "project", "host": "p", "username": "p"}],
        )

        with patch.object(constants, "PROJECT_DIR", project):
            self.assertEqual(find_legacy_config(), user_legacy)
            user_legacy.unlink()
            self.assertEqual(find_legacy_config(), project_legacy)
            project_legacy.unlink()
            self.assertIsNone(find_legacy_config())

    def test_migrate_config(self) -> None:
        source = self.xdg / "vpn" / "hosts.json"
        target = self.xdg / "pasaporte" / "hosts.json"
        self._write(
            source,
            [
                {
                    "name": "UTB",
                    "host": "vpn3.utb.edu.co",
                    "protocol": "gp",
                    "saml": True,
                }
            ],
        )

        count = migrate_config(source, target)
        self.assertEqual(count, 1)
        self.assertTrue(target.exists())
        self.assertTrue(source.exists())
        self.assertEqual(
            stat.S_IMODE(target.stat().st_mode), 0o600
        )

        raw = json.loads(target.read_text(encoding="utf-8"))
        self.assertEqual(raw[0]["name"], "UTB")

        # Segunda migración: debe crear backup.
        migrate_config(source, target)
        backup = target.with_name(target.name + ".bak")
        self.assertTrue(backup.exists())

    def test_migrate_invalid(self) -> None:
        source = self.xdg / "vpn" / "hosts.json"
        target = self.xdg / "pasaporte" / "hosts.json"
        source.parent.mkdir(parents=True, exist_ok=True)
        source.write_text("{no es json", encoding="utf-8")

        with self.assertRaises(ValueError):
            migrate_config(source, target)
        self.assertFalse(target.exists())

    def test_merge_connections(self) -> None:
        current = [
            {"name": "A", "host": "a", "username": "u"},
        ]
        incoming = [
            {"name": "a", "host": "a2", "username": "u"},
            {
                "name": "B",
                "host": "b",
                "username": "u",
                "custom": "keep",
            },
        ]

        merged, added, skipped = merge_connections(current, incoming)
        self.assertEqual(added, 1)
        self.assertEqual(skipped, 1)
        self.assertEqual([item["name"] for item in merged], ["A", "B"])
        self.assertEqual(merged[1]["custom"], "keep")

    def test_canonical_path_uses_xdg(self) -> None:
        self.assertEqual(
            canonical_config_path(),
            self.xdg / "pasaporte" / "hosts.json",
        )


if __name__ == "__main__":
    unittest.main()
