"""Tests de resolución de idioma, traducción y cambio en caliente."""

from __future__ import annotations

import json
import os
import sys
import tempfile
import unittest
from pathlib import Path

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

_XDG = tempfile.TemporaryDirectory()
os.environ["XDG_CONFIG_HOME"] = str(Path(_XDG.name) / "xdg")

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from PySide6.QtCore import QCoreApplication  # noqa: E402
from PySide6.QtWidgets import QApplication  # noqa: E402

from pasaporte.i18n import (  # noqa: E402
    TRANSLATIONS_DIR,
    get_language_manager,
    resolve_language,
)
from pasaporte.ui import MainWindow  # noqa: E402


class I18nTests(unittest.TestCase):
    app = None
    manager = None

    @classmethod
    def setUpClass(cls) -> None:
        cls.app = QApplication.instance() or QApplication([])
        cls.manager = get_language_manager()

    @classmethod
    def tearDownClass(cls) -> None:
        _XDG.cleanup()

    def test_resolve_language(self) -> None:
        self.assertEqual(resolve_language("auto", "es_ES"), "es")
        self.assertEqual(resolve_language("auto", "es_CO"), "es")
        self.assertEqual(resolve_language("auto", "en_US"), "en")
        self.assertEqual(resolve_language("auto", "fr_FR"), "en")
        self.assertEqual(resolve_language("es", "en_US"), "es")
        self.assertEqual(resolve_language("en", "es_ES"), "en")
        self.assertEqual(resolve_language("pt_BR", "es_ES"), "en")

    def test_translation_file_exists(self) -> None:
        self.assertTrue(
            (TRANSLATIONS_DIR / "pasaporte_es.qm").exists()
        )

    def test_manager_translates(self) -> None:
        manager = self.manager
        manager.set_language("es")
        self.assertEqual(manager.current, "es")
        self.assertEqual(
            QCoreApplication.translate("MainWindow", "Add"),
            "Añadir",
        )

        manager.set_language("en")
        self.assertEqual(manager.current, "en")
        self.assertEqual(
            QCoreApplication.translate("MainWindow", "Add"),
            "Add",
        )

    def test_main_window_retranslates(self) -> None:
        tmp = tempfile.TemporaryDirectory()
        config = Path(tmp.name) / "hosts.json"
        config.write_text(
            json.dumps(
                [
                    {
                        "name": "UTB",
                        "host": "vpn.example.com",
                        "username": "u",
                        "protocol": "gp",
                        "saml": True,
                    }
                ]
            ),
            encoding="utf-8",
        )

        window = MainWindow(
            config, language_manager=self.manager
        )
        window.show()
        self.app.processEvents()

        window.language_manager.set_language("en")
        self.app.processEvents()
        self.assertEqual(window.add_button.text(), "Add")
        self.assertEqual(window.file_menu.title(), "File")
        self.assertEqual(window.status_label.text(), "Disconnected")
        self.assertTrue(window.language_actions["en"].isChecked())

        window.language_manager.set_language("es")
        self.app.processEvents()
        self.assertEqual(window.add_button.text(), "Añadir")
        self.assertEqual(window.file_menu.title(), "Archivo")
        self.assertEqual(window.status_label.text(), "Sin conexión")
        self.assertTrue(window.language_actions["es"].isChecked())

        window.close()
        window.deleteLater()
        self.app.processEvents()
        tmp.cleanup()


if __name__ == "__main__":
    unittest.main()
