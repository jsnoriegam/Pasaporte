"""Ventana principal de Pasaporte."""

from __future__ import annotations

import html
import re
from pathlib import Path

from PySide6.QtCore import (
    QElapsedTimer,
    QEvent,
    QSettings,
    QSize,
    Qt,
    QThread,
    QTimer,
    QUrl,
    Signal,
)
from PySide6.QtGui import (
    QAction,
    QActionGroup,
    QDesktopServices,
    QFontDatabase,
    QIcon,
)
from PySide6.QtWidgets import (
    QApplication,
    QCheckBox,
    QDialog,
    QDialogButtonBox,
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QMainWindow,
    QMenu,
    QMessageBox,
    QPlainTextEdit,
    QPushButton,
    QSplitter,
    QStackedWidget,
    QStyle,
    QSystemTrayIcon,
    QVBoxLayout,
    QWidget,
)

from .config import (
    ConfigConflictError,
    ConfigStore,
    VPNServer,
    load_raw,
    parse_servers,
    save_raw,
)
from .constants import APP_NAME, APP_SLUG
from .editor import ConnectionDialog
from .gp import SamlResult
from .i18n import LanguageManager, get_language_manager
from .openconnect import build_connection, privilege_prefix
from .paths import (
    ConfigTarget,
    canonical_config_path,
    find_legacy_config,
    merge_connections,
    migrate_config,
)
from .runner import OpenConnectRunner
from .saml_dialog import SamlLoginDialog

_ANSI_RE = re.compile(r"\x1b\[[0-9;]*[A-Za-z]")
_EDITABLE_STATES = ("idle", "error")


class PreloginWorker(QThread):
    """Consulta ``prelogin.esp`` sin bloquear la interfaz."""

    done = Signal(object)
    failed = Signal(str)

    def __init__(self, server: VPNServer, parent=None) -> None:
        super().__init__(parent)
        self.server = server

    def run(self) -> None:
        try:
            from .gp import request_saml

            result = request_saml(self.server)
        except Exception as exc:
            self.failed.emit(str(exc))
        else:
            self.done.emit(result)


class PasswordDialog(QDialog):
    def __init__(self, server: VPNServer, parent=None) -> None:
        super().__init__(parent)
        self.setWindowTitle(
            self.tr("Password · {name}").format(
                name=server.display_name
            )
        )
        self.setModal(True)
        self.resize(420, 180)

        layout = QVBoxLayout(self)

        identity = (
            f"{server.username} · {server.host}"
            if server.username
            else server.host
        )
        label = QLabel(
            f"<b>{html.escape(server.display_name)}</b><br>"
            f"{html.escape(identity)}"
        )
        label.setTextFormat(Qt.RichText)
        label.setWordWrap(True)
        layout.addWidget(label)

        self.edit = QLineEdit(self)
        self.edit.setEchoMode(QLineEdit.Password)
        self.edit.setPlaceholderText(self.tr("VPN password"))
        layout.addWidget(self.edit)

        show = QCheckBox(self.tr("Show password"), self)
        show.toggled.connect(
            lambda checked: self.edit.setEchoMode(
                QLineEdit.Normal if checked else QLineEdit.Password
            )
        )
        layout.addWidget(show)

        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

        self.edit.returnPressed.connect(self.accept)
        self.edit.setFocus()

    @property
    def password(self) -> str:
        return self.edit.text()


class MainWindow(QMainWindow):
    def __init__(
        self,
        config: Path | ConfigTarget,
        parent=None,
        language_manager: LanguageManager | None = None,
    ) -> None:
        super().__init__(parent)

        if isinstance(config, ConfigTarget):
            self.config_target = config
        else:
            self.config_target = ConfigTarget(
                Path(config).expanduser(),
                explicit=True,
                canonical=False,
            )

        self.config_path = self.config_target.path
        self.settings = self._make_settings()
        self.language_manager = (
            language_manager or get_language_manager()
        )
        self.language_manager.language_changed.connect(
            self._on_language_changed
        )
        self._config_ok = False
        self._read_only = False

        self.store = ConfigStore(self.config_path, load=False)
        self.servers: list[VPNServer] = []

        self._worker: PreloginWorker | None = None
        self._pending_server: VPNServer | None = None
        self._quit_after_stop = False
        self._state = "idle"

        self.runner = OpenConnectRunner(self)
        self.runner.log.connect(self.append_log)
        self.runner.state_changed.connect(self.on_state_changed)
        self.runner.finished.connect(self.on_finished)

        self._elapsed = QElapsedTimer()
        self._tick = QTimer(self)
        self._tick.setInterval(1000)
        self._tick.timeout.connect(self.update_elapsed)

        self._devtools_port = int(
            QApplication.instance().property(
                "pasaporte_devtools_port"
            )
            or 0
        )

        self._build_ui()
        self._restore_geometry()
        self._maybe_migrate()
        self.reload_config()

    def _make_settings(self) -> QSettings:
        settings = QSettings(APP_SLUG, APP_SLUG)
        # Migrar una sola vez la geometría de la versión antigua.
        if not settings.contains("geometry"):
            old = QSettings("vpn-gui", "vpn-gui")
            geometry = old.value("geometry")
            if geometry:
                settings.setValue("geometry", geometry)
        return settings

    # ------------------------------------------------------------------ UI

    def _build_ui(self) -> None:
        self.setWindowTitle(APP_NAME)
        self.resize(960, 760)

        central = QWidget(self)
        self.setCentralWidget(central)

        root = QVBoxLayout(central)
        root.setContentsMargins(18, 18, 18, 14)
        root.setSpacing(12)

        # Cabecera
        header = QHBoxLayout()

        titles = QVBoxLayout()
        titles.setSpacing(2)

        title = QLabel(APP_NAME, self)
        title_font = title.font()
        title_font.setPointSize(20)
        title_font.setBold(True)
        title.setFont(title_font)
        titles.addWidget(title)
        self.title_label = title

        subtitle = QLabel(
            "openconnect · Fortinet · GlobalProtect/SAML", self
        )
        subtitle.setStyleSheet("color: palette(mid);")
        titles.addWidget(subtitle)
        self.subtitle_label = subtitle

        header.addLayout(titles, 1)

        reload_button = QPushButton(self.tr("Reload"), self)
        reload_button.setToolTip(self.tr("Re-read the connections JSON"))
        reload_button.clicked.connect(self.reload_config)
        header.addWidget(reload_button, 0, Qt.AlignTop)
        self.reload_button = reload_button

        root.addLayout(header)

        # Aviso de configuración de solo lectura
        self.readonly_banner = QWidget(self)
        self.readonly_banner.setStyleSheet(
            "background: palette(alternate-base); "
            "border: 1px solid palette(mid); border-radius: 6px;"
        )
        banner_layout = QHBoxLayout(self.readonly_banner)
        banner_layout.setContentsMargins(10, 8, 10, 8)
        self.readonly_label = QLabel(self.readonly_banner)
        self.readonly_label.setWordWrap(True)
        self.readonly_label.setTextFormat(Qt.RichText)
        banner_layout.addWidget(self.readonly_label, 1)
        self.readonly_migrate_button = QPushButton(
            self.tr("Migrate now"), self.readonly_banner
        )
        self.readonly_migrate_button.clicked.connect(self.migrate_now)
        banner_layout.addWidget(self.readonly_migrate_button)
        self.readonly_banner.setVisible(False)
        root.addWidget(self.readonly_banner)

        # Gestión de conexiones
        manage = QHBoxLayout()
        self.connections_label = QLabel(self.tr("Connections"), self)
        manage.addWidget(self.connections_label, 0)
        manage.addStretch(1)

        self.add_button = QPushButton(self.tr("Add"), self)
        self.add_button.clicked.connect(self.add_server)
        manage.addWidget(self.add_button)

        self.edit_button = QPushButton(self.tr("Edit"), self)
        self.edit_button.clicked.connect(self.edit_server)
        manage.addWidget(self.edit_button)

        self.delete_button = QPushButton(self.tr("Delete"), self)
        self.delete_button.clicked.connect(self.delete_server)
        manage.addWidget(self.delete_button)

        self.migrate_button = QPushButton(self.tr("Migrate configuration"), self)
        self.migrate_button.setToolTip(
            self.tr(
                "Copy the legacy configuration to "
                "~/.config/pasaporte/hosts.json and switch to editable mode"
            )
        )
        self.migrate_button.clicked.connect(self.migrate_now)
        self.migrate_button.setVisible(False)
        manage.addWidget(self.migrate_button)

        root.addLayout(manage)

        # Lista + estado vacío + registro
        splitter = QSplitter(Qt.Vertical, self)

        self.list = QListWidget(self)
        self.list.setSelectionMode(QListWidget.SingleSelection)
        self.list.setSpacing(2)
        self.list.setStyleSheet(
            "QListWidget::item { border-radius: 8px; }"
            "QListWidget::item:selected { "
            "background: rgba(42, 130, 218, 55); "
            "}"
        )
        self.list.itemDoubleClicked.connect(
            lambda _item: self.connect_selected()
        )
        self.list.currentRowChanged.connect(
            lambda _row: self._update_buttons(self._state)
        )
        self.list.setContextMenuPolicy(Qt.CustomContextMenu)
        self.list.customContextMenuRequested.connect(
            self._show_list_menu
        )

        self.empty_widget = QWidget(self)
        empty_layout = QVBoxLayout(self.empty_widget)
        empty_layout.setContentsMargins(24, 24, 24, 24)
        empty_layout.addStretch(1)

        empty_title = QLabel(self.tr("No connections yet"), self.empty_widget)
        empty_title.setAlignment(Qt.AlignCenter)
        empty_font = empty_title.font()
        empty_font.setPointSize(14)
        empty_font.setBold(True)
        empty_title.setFont(empty_font)
        empty_layout.addWidget(empty_title)
        self.empty_title = empty_title

        empty_hint = QLabel(
            self.tr("Press “Add” to create the first connection."),
            self.empty_widget,
        )
        empty_hint.setAlignment(Qt.AlignCenter)
        empty_hint.setStyleSheet("color: palette(mid);")
        empty_layout.addWidget(empty_hint)
        self.empty_hint = empty_hint

        empty_row = QHBoxLayout()
        empty_row.addStretch(1)
        self.empty_add_button = QPushButton(
            self.tr("Add connection"), self.empty_widget
        )
        self.empty_add_button.clicked.connect(self.add_server)
        empty_row.addWidget(self.empty_add_button)
        empty_row.addStretch(1)
        empty_layout.addLayout(empty_row)
        empty_layout.addStretch(1)

        self.stack = QStackedWidget(self)
        self.stack.addWidget(self.list)
        self.stack.addWidget(self.empty_widget)
        splitter.addWidget(self.stack)

        log_container = QWidget(self)
        log_layout = QVBoxLayout(log_container)
        log_layout.setContentsMargins(0, 0, 0, 0)
        log_layout.setSpacing(6)

        log_header = QHBoxLayout()
        self.log_label = QLabel(self.tr("Log"), log_container)
        log_header.addWidget(self.log_label, 0)
        log_header.addStretch(1)

        clear_button = QPushButton(self.tr("Clear"), log_container)
        clear_button.clicked.connect(self.clear_log)
        log_header.addWidget(clear_button)
        self.clear_button = clear_button
        log_layout.addLayout(log_header)

        self.log_view = QPlainTextEdit(log_container)
        self.log_view.setReadOnly(True)
        self.log_view.setMaximumBlockCount(5000)
        self.log_view.setFont(
            QFontDatabase.systemFont(QFontDatabase.FixedFont)
        )
        self.log_view.setPlaceholderText(
            self.tr("openconnect output will appear here.")
        )
        log_layout.addWidget(self.log_view)

        splitter.addWidget(log_container)
        splitter.setStretchFactor(0, 3)
        splitter.setStretchFactor(1, 2)
        root.addWidget(splitter, 1)

        # Acciones de conexión
        actions = QHBoxLayout()

        self.connect_button = QPushButton(self.tr("Connect"), self)
        self.connect_button.setDefault(True)
        self.connect_button.clicked.connect(self.connect_selected)
        actions.addWidget(self.connect_button)

        self.disconnect_button = QPushButton(self.tr("Disconnect"), self)
        self.disconnect_button.setEnabled(False)
        self.disconnect_button.clicked.connect(self.runner.stop)
        actions.addWidget(self.disconnect_button)

        actions.addStretch(1)

        config_button = QPushButton(self.tr("Open configuration"), self)
        config_button.clicked.connect(self.open_config)
        actions.addWidget(config_button)
        self.config_button = config_button

        root.addLayout(actions)

        # Estado
        status_row = QHBoxLayout()

        self.status_label = QLabel(self.tr("Disconnected"), self)
        self.status_label.setStyleSheet("font-weight: 600;")
        status_row.addWidget(self.status_label, 1)

        self.elapsed_label = QLabel("", self)
        self.elapsed_label.setStyleSheet("color: palette(mid);")
        status_row.addWidget(self.elapsed_label, 0)

        root.addLayout(status_row)

        self.statusBar().showMessage(str(self.config_path))

        self._build_menu()
        self._build_tray()
        self._update_empty_state()

    def _build_menu(self) -> None:
        self.file_menu = self.menuBar().addMenu(self.tr("File"))
        file_menu = self.file_menu

        self.new_action = QAction(self.tr("New connection"), self)
        self.new_action.setShortcut("Ctrl+N")
        self.new_action.triggered.connect(self.add_server)
        file_menu.addAction(self.new_action)
        self.addAction(self.new_action)

        self.edit_action = QAction(self.tr("Edit connection"), self)
        self.edit_action.setShortcut("Ctrl+E")
        self.edit_action.triggered.connect(self.edit_server)
        file_menu.addAction(self.edit_action)
        self.addAction(self.edit_action)

        self.delete_action = QAction(self.tr("Delete connection"), self)
        self.delete_action.setShortcut("Delete")
        self.delete_action.triggered.connect(self.delete_server)
        file_menu.addAction(self.delete_action)
        self.addAction(self.delete_action)

        file_menu.addSeparator()

        self.import_action = QAction(
            self.tr("Import configuration…"), self
        )
        self.import_action.triggered.connect(self.import_config)
        file_menu.addAction(self.import_action)

        self.export_action = QAction(
            self.tr("Export configuration…"), self
        )
        self.export_action.triggered.connect(self.export_config)
        file_menu.addAction(self.export_action)

        self.folder_action = QAction(
            self.tr("Open configuration folder"), self
        )
        self.folder_action.triggered.connect(self.open_config_folder)
        file_menu.addAction(self.folder_action)

        file_menu.addSeparator()

        self.migrate_action = QAction(
            self.tr("Migrate configuration…"), self
        )
        self.migrate_action.triggered.connect(self.migrate_now)
        self.migrate_action.setEnabled(False)
        file_menu.addAction(self.migrate_action)

        file_menu.addSeparator()

        self.reload_action = QAction(
            self.tr("Reload configuration"), self
        )
        self.reload_action.setShortcut("F5")
        self.reload_action.triggered.connect(self.reload_config)
        file_menu.addAction(self.reload_action)

        self.open_action = QAction(self.tr("Open configuration…"), self)
        self.open_action.triggered.connect(self.open_config)
        file_menu.addAction(self.open_action)

        self.language_menu = file_menu.addMenu(self.tr("Language"))
        self.language_group = QActionGroup(self)
        self.language_group.setExclusive(True)
        self.language_actions: dict[str, QAction] = {}

        language_choices = (
            ("auto", self.tr("Automatic (system)")),
            ("en", "English"),
            ("es", "Español"),
        )
        for code, label in language_choices:
            action = QAction(label, self)
            action.setCheckable(True)
            action.setData(code)
            action.triggered.connect(
                lambda _checked=False, c=code: self._change_language(c)
            )
            self.language_group.addAction(action)
            self.language_menu.addAction(action)
            self.language_actions[code] = action
            if code == self.language_manager.setting:
                action.setChecked(True)

        file_menu.addSeparator()

        self.quit_action = QAction(self.tr("Quit"), self)
        self.quit_action.setShortcut("Ctrl+Q")
        self.quit_action.triggered.connect(self.close)
        file_menu.addAction(self.quit_action)

        self.help_menu = self.menuBar().addMenu(self.tr("Help"))
        self.about_action = QAction(self.tr("About…"), self)
        self.about_action.triggered.connect(self.show_about)
        self.help_menu.addAction(self.about_action)

    def _build_tray(self) -> None:
        self.tray: QSystemTrayIcon | None = None
        if not QSystemTrayIcon.isSystemTrayAvailable():
            return

        tray = QSystemTrayIcon(self)
        fallback = self.style().standardIcon(
            QStyle.StandardPixmap.SP_ComputerIcon
        )
        tray.setIcon(QIcon.fromTheme("network-vpn", fallback))
        tray.setToolTip(APP_NAME)

        menu = QMenu(self)
        self.tray_menu = menu
        self.tray_show_action = menu.addAction(
            self.tr("Show"), self.showNormal
        )
        self.tray_connect_action = menu.addAction(
            self.tr("Connect"), self.connect_selected
        )
        self.tray_disconnect_action = menu.addAction(
            self.tr("Disconnect"), self.runner.stop
        )
        menu.addSeparator()
        self.tray_quit_action = menu.addAction(
            self.tr("Quit"), self.close
        )
        tray.setContextMenu(menu)

        tray.activated.connect(self._on_tray_activated)
        tray.show()
        self.tray = tray

    def _on_tray_activated(self, reason) -> None:
        if reason == QSystemTrayIcon.Trigger:
            self.showNormal()
            self.raise_()
            self.activateWindow()

    # ------------------------------------------------------------- idioma

    def _change_language(self, code: str) -> None:
        self.language_manager.set_language(code)

    def _on_language_changed(self, _code: str) -> None:
        action = getattr(self, "language_actions", {}).get(
            self.language_manager.setting
        )
        if action is not None:
            action.setChecked(True)

    def changeEvent(self, event) -> None:
        if event.type() == QEvent.Type.LanguageChange:
            self._retranslate_ui()
        super().changeEvent(event)

    def _retranslate_ui(self) -> None:
        self.setWindowTitle(APP_NAME)
        self.title_label.setText(APP_NAME)
        self.subtitle_label.setText(
            "openconnect · Fortinet · GlobalProtect/SAML"
        )
        self.reload_button.setText(self.tr("Reload"))
        self.reload_button.setToolTip(
            self.tr("Re-read the connections JSON")
        )
        self.readonly_migrate_button.setText(self.tr("Migrate now"))
        self.connections_label.setText(self.tr("Connections"))
        self.add_button.setText(self.tr("Add"))
        self.edit_button.setText(self.tr("Edit"))
        self.delete_button.setText(self.tr("Delete"))
        self.migrate_button.setText(self.tr("Migrate configuration"))
        self.migrate_button.setToolTip(
            self.tr(
                "Copy the legacy configuration to "
                "~/.config/pasaporte/hosts.json and switch to editable mode"
            )
        )
        self.empty_title.setText(self.tr("No connections yet"))
        self.empty_hint.setText(
            self.tr("Press “Add” to create the first connection.")
        )
        self.empty_add_button.setText(self.tr("Add connection"))
        self.log_label.setText(self.tr("Log"))
        self.clear_button.setText(self.tr("Clear"))
        self.log_view.setPlaceholderText(
            self.tr("openconnect output will appear here.")
        )
        self.connect_button.setText(self.tr("Connect"))
        self.disconnect_button.setText(self.tr("Disconnect"))
        self.config_button.setText(self.tr("Open configuration"))

        self.file_menu.setTitle(self.tr("File"))
        self.help_menu.setTitle(self.tr("Help"))
        self.new_action.setText(self.tr("New connection"))
        self.edit_action.setText(self.tr("Edit connection"))
        self.delete_action.setText(self.tr("Delete connection"))
        self.import_action.setText(self.tr("Import configuration…"))
        self.export_action.setText(self.tr("Export configuration…"))
        self.folder_action.setText(self.tr("Open configuration folder"))
        self.migrate_action.setText(self.tr("Migrate configuration…"))
        self.reload_action.setText(self.tr("Reload configuration"))
        self.open_action.setText(self.tr("Open configuration…"))
        self.quit_action.setText(self.tr("Quit"))
        self.about_action.setText(self.tr("About…"))
        self.language_menu.setTitle(self.tr("Language"))
        if "auto" in self.language_actions:
            self.language_actions["auto"].setText(
                self.tr("Automatic (system)")
            )

        if self.tray is not None:
            self.tray_show_action.setText(self.tr("Show"))
            self.tray_connect_action.setText(self.tr("Connect"))
            self.tray_disconnect_action.setText(self.tr("Disconnect"))
            self.tray_quit_action.setText(self.tr("Quit"))

        self._update_status_text()
        self._update_buttons(self._state)
        self.statusBar().showMessage(self._config_status_text())

    def _show_list_menu(self, pos) -> None:
        item = self.list.itemAt(pos)
        if item is not None:
            self.list.setCurrentItem(item)

        editable = (
            self._config_ok and self._state in _EDITABLE_STATES
        )
        has_selection = item is not None

        menu = QMenu(self)

        connect_action = menu.addAction(
            self.tr("Connect"), self.connect_selected
        )
        connect_action.setEnabled(
            has_selection and self._state in _EDITABLE_STATES
        )

        edit_action = menu.addAction(self.tr("Edit…"), self.edit_server)
        edit_action.setEnabled(editable and has_selection)

        delete_action = menu.addAction(self.tr("Delete"), self.delete_server)
        delete_action.setEnabled(editable and has_selection)

        menu.addSeparator()
        add_action = menu.addAction(
            self.tr("Add connection…"), self.add_server
        )
        add_action.setEnabled(editable)

        menu.exec(self.list.mapToGlobal(pos))

    # ---------------------------------------------------------- configuración

    def _update_empty_state(self) -> None:
        self.stack.setCurrentWidget(
            self.list if self.servers else self.empty_widget
        )

    def reload_config(
        self,
        select_index: int | None = None,
        select_name: str | None = None,
    ) -> None:
        current = self.current_server()
        current_name = current.name if current is not None else None

        try:
            self.store.reload()
        except Exception as exc:
            self._config_ok = False
            self.servers = self.store.servers
            QMessageBox.critical(self, self.tr("Configuration"), str(exc))
            self.append_log(
                self.tr("Configuration error: {error}").format(error=exc)
            )
            self._update_empty_state()
            self.statusBar().showMessage(self._config_status_text())
            self._update_buttons(self._state)
            return

        self._config_ok = True
        self.servers = self.store.servers

        selected_row = 0
        if (
            select_index is not None
            and 0 <= select_index < len(self.servers)
        ):
            selected_row = select_index
        elif select_name:
            for index, server in enumerate(self.servers):
                if server.name == select_name:
                    selected_row = index
                    break
        elif current_name:
            for index, server in enumerate(self.servers):
                if server.name == current_name:
                    selected_row = index
                    break

        self.list.blockSignals(True)
        self.list.clear()
        for server in self.servers:
            item = QListWidgetItem()
            item.setData(Qt.UserRole, server)
            item.setSizeHint(
                QSize(0, 76 if server.description else 64)
            )
            self.list.addItem(item)
            self.list.setItemWidget(item, self._make_item_widget(server))

        if self.servers:
            self.list.setCurrentRow(selected_row)
        self.list.blockSignals(False)

        self._update_empty_state()
        self.statusBar().showMessage(self._config_status_text())
        self.append_log(
            self.tr(
                "Configuration loaded: {count} connection(s) from {path}"
            ).format(
                count=len(self.servers),
                path=self._config_status_text(),
            )
        )
        self._update_buttons(self._state)

    def _make_item_widget(self, server: VPNServer) -> QWidget:
        widget = QWidget(self)
        widget.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)

        layout = QHBoxLayout(widget)
        layout.setContentsMargins(10, 8, 10, 8)
        layout.setSpacing(12)

        texts = QVBoxLayout()
        texts.setSpacing(2)

        name = QLabel(html.escape(server.display_name), widget)
        name.setStyleSheet("font-weight: 600; font-size: 11pt;")
        texts.addWidget(name)

        subtitle = QLabel(html.escape(server.subtitle), widget)
        subtitle.setStyleSheet("color: palette(mid);")
        texts.addWidget(subtitle)

        if server.description:
            description = QLabel(
                html.escape(server.description), widget
            )
            description.setStyleSheet("color: palette(mid);")
            texts.addWidget(description)

        layout.addLayout(texts, 1)

        badge = QLabel(server.protocol.upper(), widget)
        badge.setStyleSheet(
            "padding: 2px 8px; border-radius: 6px; "
            "background: palette(button); color: palette(button-text); "
            "font-weight: 600;"
        )
        layout.addWidget(badge, 0, Qt.AlignVCenter)

        if server.requires_saml:
            saml_badge = QLabel("SAML", widget)
            saml_badge.setStyleSheet(
                "padding: 2px 8px; border-radius: 6px; "
                "background: palette(highlight); "
                "color: palette(highlighted-text); font-weight: 600;"
            )
            layout.addWidget(saml_badge, 0, Qt.AlignVCenter)

        return widget

    def current_server(self) -> VPNServer | None:
        item = self.list.currentItem()
        if item is None:
            return None
        return item.data(Qt.UserRole)

    def current_index(self) -> int:
        return self.list.currentRow()

    def _config_status_text(self) -> str:
        suffix = self.tr(" (read-only)") if self._read_only else ""
        return f"{self.config_path}{suffix}"

    def open_config(self) -> None:
        target = self.config_path
        if not target.exists():
            target = target.parent
            try:
                target.mkdir(parents=True, exist_ok=True)
            except OSError as exc:
                QMessageBox.critical(
                    self,
                    APP_NAME,
                    self.tr(
                        "Could not open the folder:\n{error}"
                    ).format(error=exc),
                )
                return
        QDesktopServices.openUrl(QUrl.fromLocalFile(str(target)))

    def open_config_folder(self) -> None:
        folder = self.config_path.parent
        try:
            folder.mkdir(parents=True, exist_ok=True)
        except OSError as exc:
            QMessageBox.critical(
                self,
                APP_NAME,
                self.tr(
                    "Could not open the folder:\n{error}"
                ).format(error=exc),
            )
            return
        QDesktopServices.openUrl(QUrl.fromLocalFile(str(folder)))

    # ------------------------------------------------------------ migración

    def _maybe_migrate(self) -> None:
        if not self.config_target.canonical:
            return
        if self.config_path.exists():
            return

        legacy = find_legacy_config()
        if legacy is None:
            return

        choice = self._ask_migration(legacy, self.config_path)
        if choice == "import":
            try:
                count = migrate_config(legacy, self.config_path)
            except Exception as exc:
                QMessageBox.critical(
                    self,
                    self.tr("Migration"),
                    self.tr(
                        "Could not migrate the configuration:\n{error}"
                    ).format(error=exc),
                )
                self._use_legacy_read_only(legacy)
            else:
                self.append_log(
                    self.tr(
                        "Configuration migrated ({count} connections): "
                        "{source} → {target}"
                    ).format(
                        count=count,
                        source=legacy,
                        target=self.config_path,
                    )
                )
        else:
            self._use_legacy_read_only(legacy)

    def _ask_migration(self, source: Path, target: Path) -> str:
        box = QMessageBox(self)
        box.setWindowTitle(APP_NAME)
        box.setIcon(QMessageBox.Question)
        box.setText(self.tr("An existing configuration was found."))
        box.setInformativeText(
            self.tr(
                "{source}\n\n"
                "Do you want to copy it to the new location?\n\n"
                "{target}\n\n"
                "If you choose “Continue without migrating”, it will be "
                "used in read-only mode and you will see a notice to "
                "migrate it whenever you want."
            ).format(source=source, target=target)
        )
        import_button = box.addButton(
            self.tr("Import"), QMessageBox.AcceptRole
        )
        box.addButton(
            self.tr("Continue without migrating (read-only)"),
            QMessageBox.DestructiveRole,
        )
        box.setDefaultButton(import_button)
        box.exec()

        if box.clickedButton() is import_button:
            return "import"
        return "session"

    def _use_legacy_read_only(self, legacy: Path) -> None:
        self.config_path = legacy
        self.config_target = ConfigTarget(
            legacy, explicit=False, canonical=False
        )
        self.store = ConfigStore(legacy, load=False)
        self._read_only = True
        self.append_log(
            self.tr(
                "Using legacy configuration in read-only mode: {path}. "
                "Use “Migrate configuration” to make it editable."
            ).format(path=legacy)
        )

    def migrate_now(self) -> None:
        if not self._read_only:
            return

        source = self.config_path
        target = canonical_config_path()
        try:
            count = migrate_config(source, target)
        except Exception as exc:
            QMessageBox.critical(
                self,
                self.tr("Migration"),
                self.tr(
                    "Could not migrate the configuration:\n{error}"
                ).format(error=exc),
            )
            return

        self.config_path = target
        self.config_target = ConfigTarget(
            target, explicit=False, canonical=True
        )
        self.store = ConfigStore(target)
        self._read_only = False
        self.append_log(
            self.tr(
                "Configuration migrated ({count} connections): "
                "{source} → {target}"
            ).format(count=count, source=source, target=target)
        )
        self.reload_config()

    # ------------------------------------------------------ importar/exportar

    def import_config(self) -> None:
        if self._read_only:
            QMessageBox.warning(
                self,
                APP_NAME,
                self.tr(
                    "The active configuration is read-only. "
                    "Migrate it first to import."
                ),
            )
            return
        if not self._config_ok:
            QMessageBox.warning(
                self,
                APP_NAME,
                self.tr(
                    "The current configuration is invalid. "
                    "Fix it before importing."
                ),
            )
            return

        filename, _filter = QFileDialog.getOpenFileName(
            self,
            self.tr("Import configuration"),
            str(Path.home()),
            self.tr("JSON (*.json);;All files (*)"),
        )
        if not filename:
            return

        source = Path(filename)
        try:
            raw = load_raw(source, missing_ok=False)
            parse_servers(raw)
        except Exception as exc:
            QMessageBox.critical(
                self, self.tr("Import configuration"), str(exc)
            )
            return

        box = QMessageBox(self)
        box.setWindowTitle(self.tr("Import configuration"))
        box.setIcon(QMessageBox.Question)
        box.setText(
            self.tr(
                "Found {count} connection(s) in {source}."
            ).format(count=len(raw), source=source)
        )
        box.setInformativeText(self.tr("What do you want to do?"))
        replace_button = box.addButton(
            self.tr("Replace all"), QMessageBox.DestructiveRole
        )
        merge_button = box.addButton(
            self.tr("Merge by name"), QMessageBox.AcceptRole
        )
        box.addButton(self.tr("Cancel"), QMessageBox.RejectRole)
        box.setDefaultButton(merge_button)
        box.exec()

        clicked = box.clickedButton()
        if clicked is replace_button:
            new_raw = raw
            action = self.tr("replaced")
        elif clicked is merge_button:
            new_raw, added, skipped = merge_connections(
                self.store.raw, raw
            )
            action = self.tr(
                "merged (+{added}, skipped {skipped})"
            ).format(added=added, skipped=skipped)
        else:
            return

        try:
            self.store.replace(new_raw)
        except Exception as exc:
            QMessageBox.critical(
                self, self.tr("Import configuration"), str(exc)
            )
            return

        if not self._save_store():
            return

        self.append_log(
            self.tr(
                "Configuration imported from {source}: {action}."
            ).format(source=source, action=action)
        )
        self.reload_config()

    def export_config(self) -> None:
        filename, _filter = QFileDialog.getSaveFileName(
            self,
            self.tr("Export configuration"),
            str(Path.home() / "pasaporte-hosts.json"),
            self.tr("JSON (*.json);;All files (*)"),
        )
        if not filename:
            return

        destination = Path(filename)
        if not destination.suffix:
            destination = destination.with_suffix(".json")

        try:
            save_raw(destination, self.store.raw)
        except Exception as exc:
            QMessageBox.critical(
                self, self.tr("Export configuration"), str(exc)
            )
            return

        self.append_log(
            self.tr("Configuration exported to {path}.").format(
                path=destination
            )
        )

    # ---------------------------------------------------------------- CRUD

    def _can_edit(self) -> bool:
        if self._read_only:
            QMessageBox.warning(
                self,
                APP_NAME,
                self.tr(
                    "The active configuration is read-only. "
                    "Press “Migrate configuration” to move it to "
                    "~/.config/pasaporte/hosts.json."
                ),
            )
            return False
        if not self._config_ok:
            QMessageBox.warning(
                self,
                APP_NAME,
                self.tr(
                    "The configuration could not be loaded. Fix the JSON "
                    "or restore the backup and press Reload."
                ),
            )
            return False
        if self._state not in _EDITABLE_STATES:
            QMessageBox.information(
                self,
                APP_NAME,
                self.tr(
                    "Disconnect the VPN before modifying the configuration."
                ),
            )
            return False
        return True

    def _save_store(self) -> bool:
        try:
            self.store.save()
        except ConfigConflictError:
            answer = QMessageBox.question(
                self,
                self.tr("Configuration changed"),
                self.tr(
                    "{path} changed outside {app}.\n\n"
                    "Overwrite it with the current changes?"
                ).format(path=self.config_path, app=APP_NAME),
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No,
            )
            if answer != QMessageBox.Yes:
                try:
                    self.store.reload()
                except Exception:
                    pass
                self.reload_config()
                return False
            try:
                self.store.save(force=True)
            except Exception as exc:
                QMessageBox.critical(
                    self,
                    self.tr("Configuration"),
                    self.tr("Could not save:\n{error}").format(
                        error=exc
                    ),
                )
                try:
                    self.store.reload()
                except Exception:
                    pass
                self.reload_config()
                return False
        except Exception as exc:
            QMessageBox.critical(
                self,
                self.tr("Configuration"),
                self.tr("Could not save:\n{error}").format(
                    error=exc
                ),
            )
            try:
                self.store.reload()
            except Exception:
                pass
            self.reload_config()
            return False

        return True

    def add_server(self) -> None:
        if not self._can_edit():
            return

        dialog = ConnectionDialog(
            existing=self.store.servers, parent=self
        )
        if (
            dialog.exec() != QDialog.Accepted
            or dialog.result_server is None
        ):
            return

        server = dialog.result_server
        try:
            self.store.add(server)
        except Exception as exc:
            QMessageBox.critical(self, self.tr("Configuration"), str(exc))
            self.reload_config()
            return

        if not self._save_store():
            return

        self.append_log(
            self.tr("Connection added: {name}").format(
                name=server.display_name
            )
        )
        self.reload_config(select_name=server.name)

    def edit_server(self) -> None:
        if not self._can_edit():
            return

        index = self.current_index()
        if not 0 <= index < len(self.store.servers):
            QMessageBox.information(
                self,
                APP_NAME,
                self.tr("Select a connection to edit."),
            )
            return

        current = self.store.servers[index]
        dialog = ConnectionDialog(
            server=current,
            existing=self.store.servers,
            index=index,
            parent=self,
        )
        if (
            dialog.exec() != QDialog.Accepted
            or dialog.result_server is None
        ):
            return

        server = dialog.result_server
        try:
            self.store.update(index, server)
        except Exception as exc:
            QMessageBox.critical(self, self.tr("Configuration"), str(exc))
            self.reload_config()
            return

        if not self._save_store():
            return

        self.append_log(
            self.tr("Connection edited: {name}").format(
                name=server.display_name
            )
        )
        self.reload_config(select_index=index)

    def delete_server(self) -> None:
        if not self._can_edit():
            return

        index = self.current_index()
        if not 0 <= index < len(self.store.servers):
            QMessageBox.information(
                self,
                APP_NAME,
                self.tr("Select a connection to delete."),
            )
            return

        server = self.store.servers[index]
        answer = QMessageBox.question(
            self,
            self.tr("Delete connection"),
            self.tr(
                "Delete “{name}”?\n\n"
                "A backup will be saved to {backup}."
            ).format(
                name=server.display_name,
                backup=self.config_path.name + ".bak",
            ),
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )
        if answer != QMessageBox.Yes:
            return

        try:
            self.store.delete(index)
        except Exception as exc:
            QMessageBox.critical(self, self.tr("Configuration"), str(exc))
            self.reload_config()
            return

        if not self._save_store():
            return

        self.append_log(
            self.tr("Connection deleted: {name}").format(
                name=server.display_name
            )
        )
        remaining = len(self.store.servers)
        self.reload_config(
            select_index=min(index, remaining - 1) if remaining else None
        )

    # ------------------------------------------------------------- conexión

    def connect_selected(self) -> None:
        if self._worker is not None and self._worker.isRunning():
            return

        server = self.current_server()
        if server is None:
            QMessageBox.information(
                self,
                APP_NAME,
                self.tr("Select a connection from the list."),
            )
            return

        if self.runner.is_running():
            QMessageBox.information(
                self,
                APP_NAME,
                self.tr(
                    "There is already an active connection. "
                    "Disconnect it first."
                ),
            )
            return

        self.append_log("")
        self.append_log(f"→ {server.display_name} ({server.protocol})")

        if server.requires_saml:
            self._start_saml(server)
            return

        dialog = PasswordDialog(server, self)
        if dialog.exec() != QDialog.Accepted:
            self.append_log(self.tr("Cancelled."))
            return

        self._start_openconnect(server, password=dialog.password)

    def connect_by_name(self, name: str) -> None:
        for index, server in enumerate(self.servers):
            if server.name == name or server.display_name == name:
                self.list.setCurrentRow(index)
                self.connect_selected()
                return
        self.append_log(
            self.tr("Connection not found: {name}").format(name=name)
        )

    def _start_saml(self, server: VPNServer) -> None:
        if self._devtools_port <= 0:
            QMessageBox.critical(
                self,
                "SAML",
                self.tr(
                    "DevTools is not available, so ACS headers cannot be "
                    "captured. Start the app with pasaporte or "
                    "python -m pasaporte."
                ),
            )
            return

        self.status_label.setText(self.tr("Getting SAML configuration…"))
        self._update_buttons("connecting")

        self._worker = PreloginWorker(server, self)
        self._pending_server = server
        self._worker.done.connect(self._on_prelogin_done)
        self._worker.failed.connect(self._on_prelogin_error)
        self._worker.finished.connect(self._on_worker_finished)
        self._worker.start()

    def _on_prelogin_done(self, request) -> None:
        server = self._pending_server
        self._pending_server = None
        if server is None:
            return

        dialog = SamlLoginDialog(
            server, request, self._devtools_port, self
        )
        accepted = dialog.exec() == QDialog.Accepted
        result: SamlResult | None = dialog.result_data
        dialog.deleteLater()

        if not accepted or result is None:
            self.append_log(self.tr("SAML cancelled."))
            self.status_label.setText(self.tr("Disconnected"))
            self._update_buttons("idle")
            return

        self.append_log(
            self.tr(
                "SAML OK: user={user}, field={field}, host={host}"
            ).format(
                user=result.username,
                field=result.cookie_field,
                host=result.server,
            )
        )
        self._start_openconnect(server, saml_result=result)

    def _on_prelogin_error(self, message: str) -> None:
        self._pending_server = None
        self.status_label.setText(self.tr("Disconnected"))
        self._update_buttons("idle")
        self.append_log(
            self.tr("SAML error: {message}").format(message=message)
        )
        QMessageBox.critical(self, "GlobalProtect / SAML", message)

    def _on_worker_finished(self) -> None:
        worker = self._worker
        self._worker = None
        if worker is not None:
            worker.deleteLater()

    def _start_openconnect(
        self,
        server: VPNServer,
        *,
        password: str | None = None,
        saml_result: SamlResult | None = None,
    ) -> None:
        try:
            prefix = privilege_prefix(server)
            args, secret = build_connection(
                server,
                password=password,
                saml_result=saml_result,
            )
        except Exception as exc:
            QMessageBox.critical(self, APP_NAME, str(exc))
            self.append_log(
                self.tr("Error: {error}").format(error=exc)
            )
            self._update_buttons("idle")
            return

        self.status_label.setText(self.tr("Connecting…"))
        self.runner.start(prefix, args, secret)

    # --------------------------------------------------------------- estado

    def on_state_changed(self, state: str) -> None:
        self._state = state
        self._update_status_text()

        if state == "connected":
            self._elapsed.start()
            self._tick.start()
        elif state == "error":
            self._tick.stop()
            self.elapsed_label.setText("")
        elif state == "idle":
            self._tick.stop()
            self.elapsed_label.setText("")

        self._update_buttons(state)

    def _update_status_text(self) -> None:
        if self._state == "connecting":
            self.status_label.setText(self.tr("Connecting…"))
        elif self._state == "connected":
            self.status_label.setText(self.tr("Connected"))
        elif self._state == "disconnecting":
            self.status_label.setText(self.tr("Disconnecting…"))
        elif self._state == "error":
            self.status_label.setText(self.tr("Error"))
        else:
            self.status_label.setText(self.tr("Disconnected"))

    def _update_buttons(self, state: str) -> None:
        has_selection = self.list.currentItem() is not None
        editable = (
            self._config_ok
            and not self._read_only
            and state in _EDITABLE_STATES
        )

        self.connect_button.setEnabled(
            has_selection and state in _EDITABLE_STATES
        )
        self.disconnect_button.setEnabled(
            self.runner.is_running() and state != "disconnecting"
        )

        self.add_button.setEnabled(editable)
        self.empty_add_button.setEnabled(editable)
        self.edit_button.setEnabled(editable and has_selection)
        self.delete_button.setEnabled(editable and has_selection)

        self.new_action.setEnabled(editable)
        self.edit_action.setEnabled(editable and has_selection)
        self.delete_action.setEnabled(editable and has_selection)

        self.import_action.setEnabled(editable)
        self.export_action.setEnabled(self._config_ok)
        self.migrate_action.setEnabled(
            self._read_only
            and self._config_ok
            and state in _EDITABLE_STATES
        )
        self.migrate_button.setVisible(self._read_only)
        self.migrate_button.setEnabled(
            self._read_only
            and self._config_ok
            and state in _EDITABLE_STATES
        )

        self.readonly_banner.setVisible(self._read_only)
        if self._read_only:
            self.readonly_label.setText(
                self.tr(
                    "<b>Read-only configuration.</b> Using "
                    "<code>{path}</code>. Migrate to "
                    "<code>~/.config/pasaporte/hosts.json</code> to add, "
                    "edit or delete connections."
                ).format(path=html.escape(str(self.config_path)))
            )
            read_only_tip = self.tr(
                "Read-only configuration. Press “Migrate now” to move it "
                "to ~/.config/pasaporte/hosts.json."
            )
            self.add_button.setToolTip(read_only_tip)
            self.edit_button.setToolTip(read_only_tip)
            self.delete_button.setToolTip(read_only_tip)
        else:
            self.add_button.setToolTip("")
            self.edit_button.setToolTip("")
            self.delete_button.setToolTip("")
        self.readonly_migrate_button.setEnabled(
            self._read_only
            and self._config_ok
            and state in _EDITABLE_STATES
        )

    def update_elapsed(self) -> None:
        if self._state != "connected" or not self._elapsed.isValid():
            return
        total = self._elapsed.elapsed() // 1000
        hours, remainder = divmod(total, 3600)
        minutes, seconds = divmod(remainder, 60)
        self.elapsed_label.setText(
            f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        )

    def on_finished(self, exit_code: int) -> None:
        self._tick.stop()
        self.elapsed_label.setText("")
        if exit_code != 0 and self._state == "error":
            self.append_log(
                self.tr(
                    "openconnect exited with code {code}. Check the log."
                ).format(code=exit_code)
            )
        if self._quit_after_stop:
            self._quit_after_stop = False
            self.close()

    # ---------------------------------------------------------------- log

    def append_log(self, text: str) -> None:
        clean = _ANSI_RE.sub("", text)
        self.log_view.appendPlainText(clean.rstrip("\n"))
        scrollbar = self.log_view.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())

    def clear_log(self) -> None:
        self.log_view.clear()

    # --------------------------------------------------------------- varios

    def show_about(self) -> None:
        QMessageBox.about(
            self,
            self.tr("About {app}").format(app=APP_NAME),
            self.tr(
                "<h3>{app}</h3>"
                "<p>Graphical interface for <b>openconnect</b>.</p>"
                "<p>Supports Fortinet, GlobalProtect with embedded SAML "
                "and any other openconnect protocol.</p>"
                "<p>The password and SAML cookie are passed over stdin; "
                "never on the command line.</p>"
            ).format(app=APP_NAME),
        )

    def _restore_geometry(self) -> None:
        geometry = self.settings.value("geometry")
        if geometry:
            self.restoreGeometry(geometry)

    def showEvent(self, event) -> None:
        super().showEvent(event)
        if not getattr(self, "_geometry_checked", False):
            self._geometry_checked = True
            self._ensure_on_screen()

    def _ensure_on_screen(self) -> None:
        screen = self.screen() or QApplication.primaryScreen()
        if screen is None:
            return

        available = screen.availableGeometry()
        if self.width() > available.width():
            self.resize(available.width(), self.height())
        if self.height() > available.height():
            self.resize(self.width(), available.height())

        frame = self.frameGeometry()
        max_x = available.left() + max(
            available.width() - frame.width(), 0
        )
        max_y = available.top() + max(
            available.height() - frame.height(), 0
        )
        x = min(max(frame.x(), available.left()), max_x)
        y = min(max(frame.y(), available.top()), max_y)
        if x != frame.x() or y != frame.y():
            self.move(x, y)

    def _save_geometry(self) -> None:
        self.settings.setValue("geometry", self.saveGeometry())

    def closeEvent(self, event) -> None:
        if self._worker is not None and self._worker.isRunning():
            QMessageBox.information(
                self,
                APP_NAME,
                self.tr("Wait for the SAML request to finish before quitting."),
            )
            event.ignore()
            return

        if self.runner.is_running():
            answer = QMessageBox.question(
                self,
                self.tr("Quit"),
                self.tr("A VPN is connected. Disconnect and quit?"),
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No,
            )
            if answer != QMessageBox.Yes:
                event.ignore()
                return
            # Cerramos solo cuando openconnect haya terminado de verdad.
            # Si no se puede cerrar, la ventana sigue abierta y la VPN
            # no queda activa sin que la app lo sepa.
            self._quit_after_stop = True
            self.runner.stop()
            event.ignore()
            return

        self._save_geometry()
        if self.tray is not None:
            self.tray.hide()
        event.accept()
