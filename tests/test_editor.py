"""Tests del diálogo de edición de conexiones."""

from __future__ import annotations

import os
import sys
import unittest
from pathlib import Path

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from PySide6.QtWidgets import QApplication  # noqa: E402

from pasaporte.config import VPNServer, validate_server  # noqa: E402
from pasaporte.editor import ConnectionDialog  # noqa: E402


class EditorTests(unittest.TestCase):
    app = None

    @classmethod
    def setUpClass(cls) -> None:
        cls.app = QApplication.instance() or QApplication([])

    def test_new_saml_without_username(self) -> None:
        dialog = ConnectionDialog()
        dialog.name_edit.setText("UTB")
        dialog.host_edit.setText("vpn3.utb.edu.co")
        dialog.username_edit.setText("")
        dialog._set_protocol("gp")
        dialog.saml_check.setChecked(True)
        dialog._update_saml_state()
        dialog.accept()

        server = dialog.result_server
        self.assertIsNotNone(server)
        assert server is not None
        self.assertEqual(server.username, "")
        self.assertTrue(server.requires_saml)
        self.assertEqual(server.os, "win")
        self.assertEqual(server.clientos, "Windows")

    def test_edit_existing(self) -> None:
        existing = VPNServer(
            name="Tempo",
            host="1.2.3.4:443",
            username="u",
            protocol="fortinet",
        )
        dialog = ConnectionDialog(
            server=existing, existing=[existing], index=0
        )
        dialog.name_edit.setText("Tempo 2")
        dialog.accept()

        server = dialog.result_server
        self.assertIsNotNone(server)
        assert server is not None
        self.assertEqual(server.name, "Tempo 2")
        self.assertEqual(server.protocol, "fortinet")

    def test_non_saml_requires_username(self) -> None:
        server = VPNServer(
            name="x",
            host="vpn.example.com",
            username="",
            protocol="fortinet",
        )
        self.assertTrue(validate_server(server))

    def test_saml_requires_protocol_gp(self) -> None:
        server = VPNServer(
            name="x",
            host="vpn.example.com",
            username="",
            protocol="fortinet",
            saml=True,
        )
        errors = validate_server(server)
        self.assertTrue(any("saml" in error.lower() for error in errors))

    def test_sync_os_from_clientos(self) -> None:
        dialog = ConnectionDialog()
        dialog.name_edit.setText("UTB")
        dialog.host_edit.setText("vpn3.utb.edu.co")
        dialog._set_protocol("gp")
        dialog.saml_check.setChecked(True)
        dialog._update_saml_state()

        self.assertTrue(dialog.sync_os_check.isChecked())
        self.assertEqual(dialog.os_combo.currentText(), "win")
        self.assertEqual(dialog.clientos_combo.currentText(), "Windows")
        self.assertFalse(dialog.os_combo.isEnabled())

        dialog.clientos_combo.setCurrentText("Linux")
        self.assertEqual(dialog.os_combo.currentText(), "linux-64")

        dialog.clientos_combo.setCurrentText("Mac")
        self.assertEqual(dialog.os_combo.currentText(), "mac-intel")

        # Al desactivar la sincronización, --os vuelve a ser editable.
        dialog.sync_os_check.setChecked(False)
        self.assertTrue(dialog.os_combo.isEnabled())
        dialog.os_combo.setCurrentText("win")
        dialog.clientos_combo.setCurrentText("Windows")
        self.assertEqual(dialog.os_combo.currentText(), "win")

        dialog.sync_os_check.setChecked(True)
        self.assertEqual(dialog.os_combo.currentText(), "win")
        self.assertFalse(dialog.os_combo.isEnabled())

        dialog.accept()
        server = dialog.result_server
        self.assertIsNotNone(server)
        assert server is not None
        self.assertEqual(server.os, "win")
        self.assertEqual(server.clientos, "Windows")

    def test_sync_preserves_mismatch(self) -> None:
        server = VPNServer(
            name="UTB",
            host="vpn3.utb.edu.co",
            username="",
            protocol="gp",
            saml=True,
            os="linux-64",
            clientos="Windows",
        )
        dialog = ConnectionDialog(
            server=server, existing=[server], index=0
        )
        self.assertFalse(dialog.sync_os_check.isChecked())
        self.assertEqual(dialog.os_combo.currentText(), "linux-64")
        self.assertTrue(dialog.os_combo.isEnabled())

        dialog.accept()
        result = dialog.result_server
        self.assertIsNotNone(result)
        assert result is not None
        self.assertEqual(result.os, "linux-64")
        self.assertEqual(result.clientos, "Windows")

    def test_sync_consistent_existing(self) -> None:
        server = VPNServer(
            name="UTB",
            host="vpn3.utb.edu.co",
            username="",
            protocol="gp",
            saml=True,
            os="linux-64",
            clientos="Linux",
        )
        dialog = ConnectionDialog(
            server=server, existing=[server], index=0
        )
        self.assertTrue(dialog.sync_os_check.isChecked())
        self.assertFalse(dialog.os_combo.isEnabled())

        dialog.accept()
        result = dialog.result_server
        self.assertIsNotNone(result)
        assert result is not None
        self.assertEqual(result.os, "linux-64")
        self.assertEqual(result.clientos, "Linux")


if __name__ == "__main__":
    unittest.main()
