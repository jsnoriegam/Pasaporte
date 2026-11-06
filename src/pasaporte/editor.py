"""Diálogo para crear y editar conexiones VPN."""

from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPlainTextEdit,
    QPushButton,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)

from .config import (
    VPNServer,
    find_duplicate,
    validate_server,
)

PROTOCOL_LABELS = [
    ("Fortinet", "fortinet"),
    ("GlobalProtect", "gp"),
    ("AnyConnect", "anyconnect"),
    ("Pulse / Ivanti", "pulse"),
    ("Juniper NC", "nc"),
    ("F5 Big-IP", "f5"),
    ("Array Networks", "array"),
]

CLIENTOS_TO_OS = {
    "windows": "win",
    "linux": "linux-64",
    "mac": "mac-intel",
    "macos": "mac-intel",
    "osx": "mac-intel",
}


class ConnectionDialog(QDialog):
    """Editor de una conexión. Devuelve el resultado en ``result_server``."""

    def __init__(
        self,
        server: VPNServer | None = None,
        existing: list[VPNServer] | None = None,
        index: int | None = None,
        parent=None,
    ) -> None:
        super().__init__(parent)

        self.existing = existing or []
        self.index = index
        self.result_server: VPNServer | None = None

        self.setWindowTitle(
            self.tr("Edit connection") if server is not None else self.tr("New connection")
        )
        self.setModal(True)
        self.resize(680, 640)
        self.setMinimumWidth(560)

        layout = QVBoxLayout(self)

        self.tabs = QTabWidget(self)
        layout.addWidget(self.tabs, 1)

        self._build_general_tab()
        self._build_gp_tab()
        self._build_advanced_tab()

        note = QLabel(
            self.tr("Passwords and cookies are not saved in the JSON."),
            self,
        )
        note.setStyleSheet("color: palette(mid);")
        note.setWordWrap(True)
        layout.addWidget(note)

        buttons = QDialogButtonBox(
            QDialogButtonBox.Save | QDialogButtonBox.Cancel, self
        )
        buttons.button(QDialogButtonBox.Save).setText(self.tr("Save"))
        buttons.button(QDialogButtonBox.Cancel).setText(self.tr("Cancel"))
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

        if server is not None:
            self._load_server(server)
        else:
            self._load_server(
                VPNServer(name="", host="", username="")
            )

        self.protocol_combo.currentIndexChanged.connect(
            self._update_saml_state
        )
        self.saml_check.toggled.connect(self._update_saml_state)
        self.clientos_combo.currentTextChanged.connect(
            self._on_clientos_changed
        )
        self.sync_os_check.toggled.connect(self._on_sync_toggled)
        self._update_saml_state()

    # ------------------------------------------------------------------ UI

    def _build_general_tab(self) -> None:
        tab = QWidget(self)
        form = QFormLayout(tab)
        form.setFieldGrowthPolicy(
            QFormLayout.FieldGrowthPolicy.AllNonFixedFieldsGrow
        )

        self.name_edit = QLineEdit(tab)
        self.name_edit.setPlaceholderText("Work VPN")
        form.addRow(self.tr("Name"), self.name_edit)

        self.host_edit = QLineEdit(tab)
        self.host_edit.setPlaceholderText(self.tr("vpn.example.com:443"))
        form.addRow(self.tr("Host"), self.host_edit)

        self.username_edit = QLineEdit(tab)
        self.username_edit.setPlaceholderText(self.tr("user@example.com"))
        form.addRow(self.tr("Username"), self.username_edit)

        self.username_hint = QLabel(
            self.tr(
                "Optional with SAML: the ACS username will be used. "
                "Fill it only as a fallback."
            ),
            tab,
        )
        self.username_hint.setWordWrap(True)
        self.username_hint.setStyleSheet("color: palette(mid);")
        form.addRow("", self.username_hint)

        self.protocol_combo = QComboBox(tab)
        for label, value in PROTOCOL_LABELS:
            self.protocol_combo.addItem(label, value)
        form.addRow(self.tr("Protocol"), self.protocol_combo)

        self.servercert_edit = QLineEdit(tab)
        self.servercert_edit.setPlaceholderText("pin-sha256:...")
        form.addRow("servercert", self.servercert_edit)

        self.description_edit = QLineEdit(tab)
        self.description_edit.setPlaceholderText(
            self.tr("Optional text for the list")
        )
        form.addRow(self.tr("Description"), self.description_edit)

        self.tabs.addTab(tab, self.tr("General"))

    def _build_gp_tab(self) -> None:
        tab = QWidget(self)
        form = QFormLayout(tab)
        form.setFieldGrowthPolicy(
            QFormLayout.FieldGrowthPolicy.AllNonFixedFieldsGrow
        )

        self.saml_check = QCheckBox(self.tr("Use SAML (SSO)"), tab)
        form.addRow("", self.saml_check)

        self.gateway_check = QCheckBox(
            self.tr("Authenticate against the gateway (instead of the portal)"), tab
        )
        form.addRow("", self.gateway_check)

        self.os_combo = QComboBox(tab)
        self.os_combo.setEditable(True)
        self.os_combo.addItems(["", "win", "linux-64", "mac-intel"])
        form.addRow("--os", self.os_combo)

        self.clientos_combo = QComboBox(tab)
        self.clientos_combo.setEditable(True)
        self.clientos_combo.addItems(["", "Windows", "Linux", "Mac"])
        form.addRow("clientos", self.clientos_combo)

        sync_row = QHBoxLayout()
        self.sync_os_check = QCheckBox(
            "Sincronizar --os con clientos", tab
        )
        sync_row.addWidget(self.sync_os_check)

        self.os_help_button = QPushButton(
            self.tr("What's the difference?"), tab
        )
        self.os_help_button.setFlat(True)
        self.os_help_button.setStyleSheet(
            "color: palette(link); text-decoration: underline;"
        )
        self.os_help_button.setCursor(Qt.PointingHandCursor)
        self.os_help_button.clicked.connect(self._show_os_help)
        sync_row.addWidget(self.os_help_button)
        sync_row.addStretch(1)
        form.addRow("", sync_row)

        self.os_hint = QLabel(
            self.tr(
                "clientos is sent to the portal during SAML prelogin; "
                "--os is passed to openconnect for the tunnel. They are "
                "not interchangeable."
            ),
            tab,
        )
        self.os_hint.setWordWrap(True)
        self.os_hint.setStyleSheet("color: palette(mid);")
        form.addRow("", self.os_hint)

        self.usergroup_edit = QLineEdit(tab)
        self.usergroup_edit.setPlaceholderText(
            self.tr("gateway or gateway:prelogin-cookie (empty = automatic)")
        )
        form.addRow("usergroup", self.usergroup_edit)

        self.useragent_edit = QLineEdit(tab)
        self.useragent_edit.setPlaceholderText("PAN GlobalProtect")
        form.addRow("User-Agent", self.useragent_edit)

        self.browser_useragent_edit = QLineEdit(tab)
        self.browser_useragent_edit.setPlaceholderText(
            self.tr("WebView User-Agent (optional)")
        )
        form.addRow("User-Agent WebView", self.browser_useragent_edit)

        self.ignore_redirects_check = QCheckBox(
            self.tr("Ignore ACS redirects"), tab
        )
        form.addRow("", self.ignore_redirects_check)

        self.tabs.addTab(tab, "GlobalProtect / SAML")
        self.gp_tab = tab

    def _build_advanced_tab(self) -> None:
        tab = QWidget(self)
        form = QFormLayout(tab)
        form.setFieldGrowthPolicy(
            QFormLayout.FieldGrowthPolicy.AllNonFixedFieldsGrow
        )

        self.privilege_combo = QComboBox(tab)
        self.privilege_combo.addItem(self.tr("Automatic"), None)
        self.privilege_combo.addItem("pkexec (Polkit)", "pkexec")
        self.privilege_combo.addItem(self.tr("sudo (passwordless)"), "sudo")
        form.addRow(self.tr("Privilege escalation"), self.privilege_combo)

        self.no_verify_check = QCheckBox(
            self.tr("Ignore TLS errors during login (insecure)"), tab
        )
        form.addRow("", self.no_verify_check)

        no_verify_hint = QLabel(
            self.tr(
                "Only affects prelogin and the WebView. openconnect will "
                "still validate the tunnel certificate."
            ),
            tab,
        )
        no_verify_hint.setWordWrap(True)
        no_verify_hint.setStyleSheet("color: palette(mid);")
        form.addRow("", no_verify_hint)

        self.allow_insecure_crypto_check = QCheckBox(
            self.tr("Allow legacy ciphers (--allow-insecure-crypto)"), tab
        )
        form.addRow("", self.allow_insecure_crypto_check)

        self.extra_args_edit = QPlainTextEdit(tab)
        self.extra_args_edit.setPlaceholderText(
            self.tr("--csd-wrapper=/path/hip.sh\n--no-dtls")
        )
        self.extra_args_edit.setFixedHeight(110)
        form.addRow(self.tr("Extra arguments"), self.extra_args_edit)

        hint = QLabel(
            self.tr("One argument per line. Do not put passwords here."),
            tab,
        )
        hint.setWordWrap(True)
        hint.setStyleSheet("color: palette(mid);")
        form.addRow("", hint)

        self.tabs.addTab(tab, self.tr("Advanced"))

    # ------------------------------------------------------------- estado

    def _set_protocol(self, protocol: str) -> None:
        for index in range(self.protocol_combo.count()):
            if self.protocol_combo.itemData(index) == protocol:
                self.protocol_combo.setCurrentIndex(index)
                return

    def _load_server(self, server: VPNServer) -> None:
        self.name_edit.setText(server.name)
        self.host_edit.setText(server.host)
        self.username_edit.setText(server.username)
        self._set_protocol(server.protocol)
        self.servercert_edit.setText(server.servercert or "")
        self.description_edit.setText(server.description or "")

        self.saml_check.setChecked(server.saml)
        self.gateway_check.setChecked(server.gateway)
        self.os_combo.setCurrentText(server.os or "")
        self.clientos_combo.setCurrentText(server.clientos or "")

        clientos_value = (server.clientos or "").strip()
        os_value = (server.os or "").strip()
        expected_os = CLIENTOS_TO_OS.get(clientos_value.lower())
        self.sync_os_check.setChecked(
            (not clientos_value and not os_value)
            or (
                expected_os is not None
                and expected_os == os_value
            )
        )
        self.usergroup_edit.setText(server.usergroup or "")
        self.useragent_edit.setText(server.useragent or "")
        self.browser_useragent_edit.setText(
            server.browser_useragent or ""
        )
        self.ignore_redirects_check.setChecked(server.ignore_redirects)

        self.no_verify_check.setChecked(server.no_verify)
        self.allow_insecure_crypto_check.setChecked(
            server.allow_insecure_crypto
        )
        self.extra_args_edit.setPlainText(
            "\n".join(server.extra_args)
        )

        for index in range(self.privilege_combo.count()):
            if self.privilege_combo.itemData(index) == server.privilege:
                self.privilege_combo.setCurrentIndex(index)
                break

    def _is_gp(self) -> bool:
        return self.protocol_combo.currentData() == "gp"

    def _is_saml(self) -> bool:
        return self._is_gp() and self.saml_check.isChecked()

    def _update_saml_state(self) -> None:
        is_gp = self._is_gp()
        is_saml = self._is_saml()

        self.gp_tab.setEnabled(is_gp)
        self.saml_check.setEnabled(is_gp)
        if not is_gp:
            self.saml_check.setChecked(False)

        self.gateway_check.setEnabled(is_saml)
        self.clientos_combo.setEnabled(is_saml)
        self.usergroup_edit.setEnabled(is_gp)
        self.ignore_redirects_check.setEnabled(is_saml)
        self.username_hint.setVisible(is_saml)
        self.sync_os_check.setEnabled(is_saml)
        self.os_hint.setVisible(is_gp)
        self.os_help_button.setEnabled(is_gp)

        if is_saml:
            self.os_hint.setText(
                self.tr(
                    "clientos is sent to the portal during SAML prelogin; "
                    "--os is passed to openconnect for the tunnel. They "
                    "are not interchangeable."
                )
            )
        else:
            self.os_hint.setText(
                self.tr(
                    "SAML disabled: clientos is not used. --os is passed "
                    "to openconnect for the tunnel."
                )
            )

        # Valores por defecto útiles al activar SAML.
        if is_saml:
            if not self.os_combo.currentText().strip():
                self.os_combo.setCurrentText("win")
            if not self.clientos_combo.currentText().strip():
                self.clientos_combo.setCurrentText("Windows")
            if self.sync_os_check.isChecked():
                self._sync_os_from_clientos()

        self.os_combo.setEnabled(
            is_gp
            and not (
                is_saml and self.sync_os_check.isChecked()
            )
        )

    def _sync_os_from_clientos(self) -> None:
        clientos = self.clientos_combo.currentText().strip().lower()
        mapped = CLIENTOS_TO_OS.get(clientos)
        if mapped:
            self.os_combo.setCurrentText(mapped)

    def _on_clientos_changed(self, _text: str) -> None:
        if self.sync_os_check.isChecked() and self._is_saml():
            self._sync_os_from_clientos()

    def _on_sync_toggled(self, checked: bool) -> None:
        if checked and self._is_saml():
            self._sync_os_from_clientos()
        self.os_combo.setEnabled(
            self._is_gp()
            and not (self._is_saml() and checked)
        )

    def _show_os_help(self) -> None:
        QMessageBox.information(
            self,
            self.tr("Help: --os and clientos"),
            self.tr(
                "<h3>--os vs clientos</h3>"
                "<p><b>clientos</b> is sent to the portal in "
                "<code>prelogin.esp</code> so it can decide which SAML "
                "flow to offer. Typical values: <code>Windows</code>, "
                "<code>Linux</code>, <code>Mac</code>.</p>"
                "<p><b>--os</b> is passed to openconnect when connecting "
                "the tunnel and affects the DAP/HIP policy. Values: "
                "<code>win</code>, <code>linux-64</code>, "
                "<code>mac-intel</code>, <code>linux</code>, "
                "<code>android</code>, <code>apple-ios</code>.</p>"
                "<p>They are not the same and are not used in the same "
                "phase. Some portals only offer SAML with "
                "<code>clientos=Windows</code> even if the tunnel uses "
                "<code>--os=linux-64</code>.</p>"
                "<p><b>Equivalences:</b> Windows → win, Linux → "
                "linux-64, Mac → mac-intel.</p>"
            ),
        )

    # ------------------------------------------------------------ guardar

    def _build_server(self) -> VPNServer | None:
        is_gp = self._is_gp()
        is_saml = self._is_saml()

        host = self.host_edit.text().strip()
        username = self.username_edit.text().strip()
        name = self.name_edit.text().strip() or host

        extra_args = [
            line.strip()
            for line in self.extra_args_edit.toPlainText().splitlines()
            if line.strip()
        ]

        clientos_value = (
            (self.clientos_combo.currentText().strip() or None)
            if is_saml
            else None
        )
        os_value = (
            (self.os_combo.currentText().strip() or None)
            if is_gp
            else None
        )
        if (
            is_saml
            and clientos_value
            and self.sync_os_check.isChecked()
        ):
            mapped = CLIENTOS_TO_OS.get(clientos_value.lower())
            if mapped:
                os_value = mapped

        server = VPNServer(
            name=name,
            host=host,
            username=username,
            protocol=self.protocol_combo.currentData() or "fortinet",
            servercert=self.servercert_edit.text().strip() or None,
            saml=is_saml,
            gateway=is_saml and self.gateway_check.isChecked(),
            usergroup=(
                self.usergroup_edit.text().strip()
                if is_gp
                else None
            ) or None,
            os=os_value,
            clientos=clientos_value,
            useragent=(
                (self.useragent_edit.text().strip() or None)
                if is_gp
                else None
            ),
            browser_useragent=(
                (self.browser_useragent_edit.text().strip() or None)
                if is_gp
                else None
            ),
            ignore_redirects=(
                is_saml and self.ignore_redirects_check.isChecked()
            ),
            no_verify=self.no_verify_check.isChecked(),
            allow_insecure_crypto=(
                self.allow_insecure_crypto_check.isChecked()
            ),
            privilege=self.privilege_combo.currentData(),
            extra_args=extra_args,
            description=self.description_edit.text().strip() or None,
        )

        errors = validate_server(server)
        if errors:
            QMessageBox.warning(
                self,
                self.tr("Check the connection"),
                "\n".join(f"• {error}" for error in errors),
            )
            return None

        duplicate = find_duplicate(server, self.existing, self.index)
        if duplicate is not None:
            other = self.existing[duplicate]
            answer = QMessageBox.question(
                self,
                self.tr("Duplicate connection"),
                self.tr(
                    "A connection with the same host, user and protocol "
                    "already exists:\n\n{name}\n\nSave anyway?"
                ).format(name=other.display_name),
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No,
            )
            if answer != QMessageBox.Yes:
                return None

        return server

    def accept(self) -> None:
        server = self._build_server()
        if server is None:
            return
        self.result_server = server
        super().accept()
