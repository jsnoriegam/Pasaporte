"""Tests de detección de openconnect y OPENCONNECT_BIN."""

from __future__ import annotations

import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from pasaporte.openconnect import (  # noqa: E402
    PrivilegeError,
    openconnect_binary,
)


class OpenconnectBinaryTests(unittest.TestCase):
    def test_openconnect_bin_override(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            binary = Path(tmp) / "openconnect"
            binary.write_text("#!/bin/sh\n", encoding="utf-8")
            binary.chmod(0o755)

            with patch.dict(
                os.environ, {"OPENCONNECT_BIN": str(binary)}
            ):
                self.assertEqual(
                    openconnect_binary(), str(binary.resolve())
                )

    def test_openconnect_bin_invalid(self) -> None:
        with patch.dict(
            os.environ,
            {"OPENCONNECT_BIN": "/no/existe/openconnect"},
        ):
            with self.assertRaises(PrivilegeError):
                openconnect_binary()

    def test_which_fallback(self) -> None:
        with patch.dict(os.environ, {"OPENCONNECT_BIN": ""}):
            with patch(
                "pasaporte.openconnect.shutil.which",
                return_value="/opt/openconnect",
            ):
                self.assertEqual(
                    openconnect_binary(), "/opt/openconnect"
                )

    def test_not_found_message_mentions_env(self) -> None:
        with patch.dict(os.environ, {"OPENCONNECT_BIN": ""}):
            with patch(
                "pasaporte.openconnect.shutil.which",
                return_value=None,
            ):
                with self.assertRaises(PrivilegeError) as ctx:
                    openconnect_binary()
        self.assertIn("OPENCONNECT_BIN", str(ctx.exception))


if __name__ == "__main__":
    unittest.main()
