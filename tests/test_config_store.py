"""Tests de configuración, validación y persistencia."""

from __future__ import annotations

import json
import stat
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from pasaporte.config import (  # noqa: E402
    ConfigConflictError,
    ConfigStore,
    VPNServer,
    find_duplicate,
    parse_servers,
    validate_server,
)


class ConfigStoreTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.path = Path(self.tmp.name) / "config" / "hosts.json"

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def test_empty_store(self) -> None:
        store = ConfigStore(self.path)
        self.assertEqual(store.servers, [])
        self.assertEqual(store.raw, [])

    def test_add_saml_without_username(self) -> None:
        store = ConfigStore(self.path)
        server = VPNServer(
            name="Work VPN",
            host="gp.example.com",
            username="",
            protocol="gp",
            saml=True,
        )
        self.assertEqual(validate_server(server), [])
        store.add(server)
        store.save()

        raw = json.loads(self.path.read_text(encoding="utf-8"))
        self.assertEqual(raw[0]["name"], "Work VPN")
        self.assertNotIn("username", raw[0])
        self.assertTrue(raw[0]["saml"])

        reloaded = ConfigStore(self.path)
        self.assertEqual(len(reloaded.servers), 1)
        self.assertTrue(reloaded.servers[0].requires_saml)
        self.assertEqual(reloaded.servers[0].username, "")

    def test_permissions_and_backup(self) -> None:
        store = ConfigStore(self.path)
        store.add(
            VPNServer(
                name="Tempo",
                host="1.2.3.4:443",
                username="u",
                protocol="fortinet",
            )
        )
        store.save()

        mode = stat.S_IMODE(self.path.stat().st_mode)
        self.assertEqual(mode, 0o600)

        store.add(
            VPNServer(
                name="Otra",
                host="5.6.7.8:443",
                username="u",
                protocol="fortinet",
            )
        )
        store.save()

        backup = self.path.with_name(self.path.name + ".bak")
        self.assertTrue(backup.exists())
        self.assertEqual(
            stat.S_IMODE(backup.stat().st_mode), 0o600
        )

    def test_preserve_unknown_fields(self) -> None:
        self.path.parent.mkdir(parents=True)
        self.path.write_text(
            json.dumps(
                [
                    {
                        "name": "Work VPN",
                        "host": "gp.example.com",
                        "protocol": "gp",
                        "saml": True,
                        "custom_field": "keep-me",
                    }
                ]
            ),
            encoding="utf-8",
        )

        store = ConfigStore(self.path)
        server = store.servers[0]
        server.name = "Work VPN editada"
        store.update(0, server)
        store.save()

        raw = json.loads(self.path.read_text(encoding="utf-8"))
        self.assertEqual(raw[0]["custom_field"], "keep-me")
        self.assertEqual(raw[0]["name"], "Work VPN editada")

    def test_conflict_detection(self) -> None:
        store = ConfigStore(self.path)
        store.add(
            VPNServer(
                name="Work VPN",
                host="gp.example.com",
                username="",
                protocol="gp",
                saml=True,
            )
        )
        store.save()

        other = ConfigStore(self.path)
        self.path.write_text(
            self.path.read_text(encoding="utf-8") + "\n",
            encoding="utf-8",
        )
        with self.assertRaises(ConfigConflictError):
            other.save()

        other.save(force=True)

    def test_empty_list_allowed(self) -> None:
        self.path.parent.mkdir(parents=True)
        self.path.write_text("[]\n", encoding="utf-8")
        store = ConfigStore(self.path)
        self.assertEqual(store.servers, [])

    def test_replace(self) -> None:
        store = ConfigStore(self.path)
        store.add(
            VPNServer(
                name="Original",
                host="old.example.com",
                username="u",
            )
        )
        store.save()

        store.replace(
            [
                {
                    "name": "Nueva",
                    "host": "new.example.com",
                    "username": "u",
                    "custom": "keep",
                }
            ]
        )
        store.save()

        raw = json.loads(self.path.read_text(encoding="utf-8"))
        self.assertEqual(len(raw), 1)
        self.assertEqual(raw[0]["name"], "Nueva")
        self.assertEqual(raw[0]["custom"], "keep")
        self.assertEqual(len(store.servers), 1)

    def test_duplicate_detection(self) -> None:
        a = VPNServer(
            name="A", host="vpn.example.com", username="u", protocol="gp"
        )
        b = VPNServer(
            name="B", host="VPN.EXAMPLE.COM", username="U", protocol="gp"
        )
        self.assertEqual(find_duplicate(b, [a]), 0)
        self.assertIsNone(find_duplicate(b, [a], skip_index=0))

    def test_validation(self) -> None:
        invalid_host = VPNServer(
            name="x",
            host="https://vpn.example.com",
            username="u",
        )
        self.assertTrue(validate_server(invalid_host))

        no_user = VPNServer(
            name="x",
            host="vpn.example.com",
            username="",
            protocol="fortinet",
        )
        self.assertTrue(validate_server(no_user))

        saml_no_user = VPNServer(
            name="x",
            host="vpn.example.com",
            username="",
            protocol="gp",
            saml=True,
        )
        self.assertEqual(validate_server(saml_no_user), [])

        bad_cert = VPNServer(
            name="x",
            host="vpn.example.com",
            username="u",
            servercert="malo",
        )
        self.assertTrue(validate_server(bad_cert))

    def test_parse_servers_rejects_non_list(self) -> None:
        with self.assertRaises(ValueError):
            parse_servers({"host": "x"})


if __name__ == "__main__":
    unittest.main()
