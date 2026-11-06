"""Infraestructura de traducción de Pasaporte (Qt Linguist)."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from PySide6.QtCore import (
    QCoreApplication,
    QLibraryInfo,
    QLocale,
    QObject,
    QSettings,
    QTranslator,
    Signal,
)

from .constants import APP_SLUG

TRANSLATIONS_DIR = Path(__file__).resolve().parent / "translations"


@dataclass(frozen=True)
class Language:
    code: str
    name: str
    filename: str | None


LANGUAGES: tuple[Language, ...] = (
    Language("en", "English", None),
    Language("es", "Español", "pasaporte_es"),
)


def available_languages() -> list[Language]:
    return list(LANGUAGES)


def _base_code(value: str) -> str:
    return value.replace("-", "_").lower().split("_")[0]


def resolve_language(
    setting: str | None,
    locale_name: str | None = None,
) -> str:
    """Resuelve el ajuste (auto/en/es) a un código de idioma disponible."""
    codes = {lang.code for lang in LANGUAGES}
    if setting and setting != "auto":
        base = _base_code(setting)
        return base if base in codes else "en"

    locale = _base_code(locale_name or QLocale.system().name())
    return locale if locale in codes else "en"


class LanguageManager(QObject):
    language_changed = Signal(str)

    def __init__(self, parent: QObject | None = None) -> None:
        super().__init__(parent)
        self.settings = QSettings(APP_SLUG, APP_SLUG)
        self._app_translator = QTranslator(self)
        self._qt_translator = QTranslator(self)
        self._setting = str(
            self.settings.value("language", "auto") or "auto"
        )
        self._current = "en"
        self.apply_saved()

    @property
    def setting(self) -> str:
        return self._setting

    @property
    def current(self) -> str:
        return self._current

    def language_name(self, code: str) -> str:
        for language in LANGUAGES:
            if language.code == code:
                return language.name
        return code

    def apply_saved(self) -> None:
        self._apply(self._setting, emit=False)

    def set_language(self, setting: str) -> None:
        self._setting = setting or "auto"
        self.settings.setValue("language", self._setting)
        self._apply(self._setting, emit=True)

    def _apply(self, setting: str, *, emit: bool) -> None:
        code = resolve_language(setting)
        self._install(code)
        changed = code != self._current
        self._current = code
        if emit and changed:
            self.language_changed.emit(code)

    def _install(self, code: str) -> None:
        QCoreApplication.removeTranslator(self._app_translator)
        QCoreApplication.removeTranslator(self._qt_translator)

        language = next(
            (item for item in LANGUAGES if item.code == code), None
        )
        if language is None or language.filename is None:
            return

        if self._app_translator.load(
            language.filename, str(TRANSLATIONS_DIR)
        ):
            QCoreApplication.installTranslator(self._app_translator)

        # Botones y diálogos estándar de Qt (Yes/No/Ok/Cancel...).
        qt_path = QLibraryInfo.path(
            QLibraryInfo.LibraryPath.TranslationsPath
        )
        if self._qt_translator.load(f"qtbase_{code}", qt_path):
            QCoreApplication.installTranslator(self._qt_translator)


_manager: LanguageManager | None = None


def get_language_manager() -> LanguageManager:
    """Devuelve el gestor único de la aplicación (y lo crea si hace falta)."""
    global _manager
    if _manager is None:
        app = QCoreApplication.instance()
        if app is None:
            raise RuntimeError(
                "get_language_manager() requires a QCoreApplication"
            )
        _manager = LanguageManager(app)
    return _manager
