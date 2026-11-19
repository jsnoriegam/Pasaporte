"""Tests de split DNS: dominios, envoltorio y argumentos de openconnect."""

from __future__ import annotations

import os
import stat
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from PySide6.QtWidgets import QApplication  # noqa: E402

from pasaporte.config import (  # noqa: E402
    VPNServer,
    parse_servers,
    server_to_dict,
    validate_server,
)
from pasaporte.editor import ConnectionDialog  # noqa: E402
from pasaporte.openconnect import build_connection  # noqa: E402
from pasaporte.split_dns import (  # noqa: E402
    has_custom_script,
    normalize_domains,
    validate_domains,
    write_wrapper,
)


class DomainTests(unittest.TestCase):
    def test_normalize_string(self) -> None:
        self.assertEqual(
            normalize_domains(
                "UTB.edu.co, ~corp.example.com.  utb.edu.co"
            ),
            ["utb.edu.co", "corp.example.com"],
        )

    def test_normalize_list(self) -> None:
        self.assertEqual(
            normalize_domains(
                ["utb.edu.co", " corp.example.com ", ""]
            ),
            ["utb.edu.co", "corp.example.com"],
        )

    def test_validate_valid(self) -> None:
        self.assertEqual(
            validate_domains(
                ["utb.edu.co", "example.internal", "localhost"]
            ),
            [],
        )

    def test_validate_invalid(self) -> None:
        for domain in (
            "bad_domain",
            "-bad.example.com",
            "bad-.example.com",
            "a..b",
            "x" * 64 + ".example.com",
            "bad;rm",
            "bad domain",
        ):
            with self.subTest(domain=domain):
                self.assertTrue(validate_domains([domain]))

    def test_custom_script_detection(self) -> None:
        self.assertTrue(has_custom_script(["--script=/tmp/x"]))
        self.assertTrue(has_custom_script(["--script", "/tmp/x"]))
        self.assertTrue(has_custom_script(["-s", "/tmp/x"]))
        self.assertFalse(has_custom_script(["--no-dtls"]))


class WrapperTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.runtime = self.root / "run"
        self.runtime.mkdir()
        self.base = self.root / "vpnc-script"
        self.base.write_text(
            "#!/bin/sh\n"
            "printf '%s\\n' \"$CISCO_SPLIT_DNS\" > \"$OUT\"\n",
            encoding="utf-8",
        )
        self.base.chmod(0o755)

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def _write(self, domains: list[str]) -> Path:
        with patch.dict(
            os.environ, {"XDG_RUNTIME_DIR": str(self.runtime)}
        ), patch(
            "pasaporte.split_dns.vpnc_script_path",
            return_value=self.base,
        ), patch(
            "pasaporte.split_dns.resolvectl_path",
            return_value=Path("/bin/true"),
        ):
            return write_wrapper(domains)

    def test_wrapper_content_and_mode(self) -> None:
        path = self._write(["utb.edu.co", "corp.example.com"])
        self.assertTrue(path.is_file())
        self.assertEqual(
            stat.S_IMODE(path.stat().st_mode), 0o700
        )
        content = path.read_text(encoding="utf-8")
        self.assertIn("#!/bin/sh", content)
        self.assertIn(
            "PASAPORTE_SPLIT_DNS=utb.edu.co,corp.example.com",
            content,
        )
        self.assertIn(str(self.base), content)
        self.assertIn("'~utb.edu.co' '~corp.example.com'", content)

    def test_wrapper_runs_and_exports_domains(self) -> None:
        path = self._write(["utb.edu.co", "corp.example.com"])
        out = self.root / "out"
        env = dict(
            os.environ,
            OUT=str(out),
            reason="connect",
            TUNDEV="tun0",
            CISCO_SPLIT_DNS="",
        )
        subprocess.run([str(path)], env=env, check=True)
        self.assertEqual(
            out.read_text(encoding="utf-8").strip(),
            "utb.edu.co,corp.example.com",
        )

    def test_wrapper_appends_to_existing_domains(self) -> None:
        path = self._write(["utb.edu.co"])
        out = self.root / "out"
        env = dict(
            os.environ,
            OUT=str(out),
            reason="connect",
            TUNDEV="tun0",
            CISCO_SPLIT_DNS="server.example.com",
        )
        subprocess.run([str(path)], env=env, check=True)
        self.assertEqual(
            out.read_text(encoding="utf-8").strip(),
            "server.example.com,utb.edu.co",
        )

    def test_falls_back_to_resolvectl_when_script_ignores_it(self) -> None:
        resolver = self.root / "resolvectl"
        resolver.write_text(
            "#!/bin/sh\n"
            "printf '%s\\n' \"$*\" >> \"$LOG\"\n"
            "if [ \"$1\" = \"domain\" ] && [ $# -eq 2 ]; then\n"
            "    printf 'Link 5 (tun0):\\n'\n"
            "fi\n",
            encoding="utf-8",
        )
        resolver.chmod(0o755)

        with patch.dict(
            os.environ, {"XDG_RUNTIME_DIR": str(self.runtime)}
        ), patch(
            "pasaporte.split_dns.vpnc_script_path",
            return_value=self.base,
        ), patch(
            "pasaporte.split_dns.resolvectl_path",
            return_value=resolver,
        ):
            path = write_wrapper(["utb.edu.co"])

        log = self.root / "resolver.log"
        out = self.root / "out"
        env = dict(
            os.environ,
            OUT=str(out),
            LOG=str(log),
            reason="connect",
            TUNDEV="tun0",
            CISCO_SPLIT_DNS="",
        )
        subprocess.run([str(path)], env=env, check=True)

        lines = log.read_text(encoding="utf-8").splitlines()
        self.assertIn("domain tun0", lines)
        self.assertIn("domain tun0 ~utb.edu.co", lines)
        self.assertIn("flush-caches", lines)
        self.assertEqual(
            out.read_text(encoding="utf-8").strip(), "utb.edu.co"
        )

    def test_missing_vpnc_script(self) -> None:
        with patch(
            "pasaporte.split_dns.vpnc_script_path", return_value=None
        ), patch(
            "pasaporte.split_dns.resolvectl_path",
            return_value=Path("/bin/true"),
        ):
            with self.assertRaises(ValueError):
                write_wrapper(["utb.edu.co"])

    def test_missing_resolvectl(self) -> None:
        with patch(
            "pasaporte.split_dns.vpnc_script_path",
            return_value=self.base,
        ), patch(
            "pasaporte.split_dns.resolvectl_path", return_value=None
        ):
            with self.assertRaises(ValueError):
                write_wrapper(["utb.edu.co"])

    def test_invalid_domain(self) -> None:
        with self.assertRaises(ValueError):
            self._write(["bad_domain"])


class ConfigSplitDnsTests(unittest.TestCase):
    def test_parse_and_serialize(self) -> None:
        servers = parse_servers(
            [
                {
                    "name": "Work VPN",
                    "host": "vpn.example.com",
                    "username": "u",
                    "dns_domains": ["UTB.edu.co", "corp.example.com"],
                }
            ]
        )
        self.assertEqual(
            servers[0].dns_domains,
            ["utb.edu.co", "corp.example.com"],
        )
        raw = server_to_dict(servers[0])
        self.assertEqual(
            raw["dns_domains"], ["utb.edu.co", "corp.example.com"]
        )

        empty = VPNServer(
            name="x", host="vpn.example.com", username="u"
        )
        self.assertNotIn("dns_domains", server_to_dict(empty))

    def test_conflict_with_custom_script(self) -> None:
        server = VPNServer(
            name="x",
            host="vpn.example.com",
            username="u",
            dns_domains=["utb.edu.co"],
            extra_args=["--script=/tmp/other.sh"],
        )
        errors = validate_server(server)
        self.assertTrue(
            any("--script" in error for error in errors)
        )

    def test_invalid_domain_in_config(self) -> None:
        with self.assertRaises(ValueError):
            parse_servers(
                [
                    {
                        "name": "x",
                        "host": "vpn.example.com",
                        "username": "u",
                        "dns_domains": ["bad_domain"],
                    }
                ]
            )


class BuildConnectionTests(unittest.TestCase):
    def test_adds_generated_script(self) -> None:
        server = VPNServer(
            name="x",
            host="vpn.example.com",
            username="u",
            dns_domains=["utb.edu.co"],
        )
        with patch(
            "pasaporte.openconnect.write_wrapper",
            return_value=Path("/tmp/pasaporte-script.sh"),
        ) as write:
            args, secret = build_connection(server)
        write.assert_called_once_with(["utb.edu.co"])
        self.assertIn(
            "--script=/tmp/pasaporte-script.sh", args
        )
        self.assertIsNone(secret)

    def test_no_script_without_domains(self) -> None:
        server = VPNServer(
            name="x", host="vpn.example.com", username="u"
        )
        args, _secret = build_connection(server)
        self.assertFalse(
            any(arg.startswith("--script") for arg in args)
        )

    def test_rejects_custom_script_conflict(self) -> None:
        server = VPNServer(
            name="x",
            host="vpn.example.com",
            username="u",
            dns_domains=["utb.edu.co"],
            extra_args=["--script=/tmp/other.sh"],
        )
        with self.assertRaises(ValueError):
            build_connection(server)


class EditorSplitDnsTests(unittest.TestCase):
    app = None

    @classmethod
    def setUpClass(cls) -> None:
        cls.app = QApplication.instance() or QApplication([])

    def test_load_and_save_domains(self) -> None:
        server = VPNServer(
            name="Work VPN",
            host="gp.example.com",
            username="u",
            protocol="gp",
            dns_domains=["utb.edu.co", "corp.example.com"],
        )
        dialog = ConnectionDialog(
            server=server, existing=[server], index=0
        )
        self.assertEqual(
            dialog.dns_domains_edit.text(),
            "utb.edu.co, corp.example.com",
        )

        dialog.dns_domains_edit.setText(
            "new.example.com, other.example.com"
        )
        dialog.accept()
        result = dialog.result_server
        self.assertIsNotNone(result)
        assert result is not None
        self.assertEqual(
            result.dns_domains,
            ["new.example.com", "other.example.com"],
        )


if __name__ == "__main__":
    unittest.main()
