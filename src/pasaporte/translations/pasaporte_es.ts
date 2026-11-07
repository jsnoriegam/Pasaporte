<?xml version='1.0' encoding='utf-8'?>
<TS version="2.1" language="es_ES">
    <context>
        <name>CdpClient</name>
        <message>
            <location filename="../cdp.py" line="92" />
            <source>DevTools unavailable: {error}</source>
            <translation>DevTools no disponible: {error}</translation>
        </message>
        <message>
            <location filename="../cdp.py" line="101" />
            <source>no WebEngine page yet</source>
            <translation>aún no hay una página WebEngine</translation>
        </message>
        <message>
            <location filename="../cdp.py" line="161" />
            <source>error processing CDP: {error}</source>
            <translation>error procesando CDP: {error}</translation>
        </message>
        <message>
            <location filename="../cdp.py" line="173" />
            <source>lost connection to DevTools</source>
            <translation>se perdió la conexión con DevTools</translation>
        </message>
    </context>
    <context>
        <name>Config</name>
        <message>
            <location filename="../config.py" line="57" />
            <source>'extra_args' must be a list of strings.</source>
            <translation>'extra_args' debe ser una lista de cadenas.</translation>
        </message>
        <message>
            <location filename="../config.py" line="107" />
            <source>Host is required.</source>
            <translation>El host es obligatorio.</translation>
        </message>
        <message>
            <location filename="../config.py" line="111" />
            <source>Host must not include http:// or https://.</source>
            <translation>El host no debe incluir http:// ni https://.</translation>
        </message>
        <message>
            <location filename="../config.py" line="115" />
            <source>Host must not include a path; use host:port.</source>
            <translation>El host no debe incluir una ruta; usa host:puerto.</translation>
        </message>
        <message>
            <location filename="../config.py" line="119" />
            <source>Host must not contain spaces.</source>
            <translation>El host no debe contener espacios.</translation>
        </message>
        <message>
            <location filename="../config.py" line="134" />
            <source>Unknown protocol: {protocol!r}.</source>
            <translation>Protocolo desconocido: {protocol!r}.</translation>
        </message>
        <message>
            <location filename="../config.py" line="141" />
            <source>'saml' is only supported with protocol 'gp'.</source>
            <translation>'saml' solo está soportado con protocol 'gp'.</translation>
        </message>
        <message>
            <location filename="../config.py" line="149" />
            <source>Username is required (except for GlobalProtect with SAML).</source>
            <translation>El usuario es obligatorio (salvo en GlobalProtect con SAML).</translation>
        </message>
        <message>
            <location filename="../config.py" line="159" />
            <source>servercert must start with pin-sha256:, sha256: or sha1:.</source>
            <translation>servercert debe empezar por pin-sha256:, sha256: o sha1:.</translation>
        </message>
        <message>
            <location filename="../config.py" line="167" />
            <source>privilege must be 'pkexec', 'sudo' or empty.</source>
            <translation>privilege debe ser 'pkexec', 'sudo' o vacío.</translation>
        </message>
        <message>
            <location filename="../config.py" line="177" />
            <source>extra_args must be a list of strings.</source>
            <translation>extra_args debe ser una lista de cadenas.</translation>
        </message>
        <message>
            <location filename="../config.py" line="265" />
            <source>Entry #{number} ({name}): {error}</source>
            <translation>entrada #{number} ({name}): {error}</translation>
        </message>
        <message>
            <location filename="../config.py" line="280" />
            <source>The JSON must be an array of connections.</source>
            <translation>el JSON debe ser un arreglo de conexiones</translation>
        </message>
        <message>
            <location filename="../config.py" line="290" />
            <source>Entry #{number} is not a JSON object.</source>
            <translation>la entrada #{number} no es un objeto JSON</translation>
        </message>
        <message>
            <location filename="../config.py" line="364" />
            <source>Configuration file does not exist: {path}</source>
            <translation>no existe el archivo de configuración: {path}</translation>
        </message>
        <message>
            <location filename="../config.py" line="378" />
            <source>Invalid JSON in {path}: {error}</source>
            <translation>JSON inválido en {path}: {error}</translation>
        </message>
        <message>
            <location filename="../config.py" line="385" />
            <source>{path} must contain a JSON array.</source>
            <translation>{path} debe contener un arreglo JSON</translation>
        </message>
        <message>
            <location filename="../config.py" line="485" />
            <source>{path} changed outside Pasaporte.</source>
            <translation>{path} cambió fuera de Pasaporte.</translation>
        </message>
        <message>
            <location filename="../config.py" line="500" />
            <location filename="../config.py" line="518" />
            <source>Index out of range: {index}</source>
            <translation>índice fuera de rango: {index}</translation>
        </message>
    </context>
    <context>
        <name>ConnectionDialog</name>
        <message>
            <location filename="../editor.py" line="65" />
            <source>Edit connection</source>
            <translation>Editar conexión</translation>
        </message>
        <message>
            <location filename="../editor.py" line="65" />
            <source>New connection</source>
            <translation>Nueva conexión</translation>
        </message>
        <message>
            <location filename="../editor.py" line="81" />
            <source>Passwords and cookies are not saved in the JSON.</source>
            <translation>Las contraseñas y cookies no se guardan en el JSON.</translation>
        </message>
        <message>
            <location filename="../editor.py" line="91" />
            <source>Save</source>
            <translation>Guardar</translation>
        </message>
        <message>
            <location filename="../editor.py" line="92" />
            <source>Cancel</source>
            <translation>Cancelar</translation>
        </message>
        <message>
            <location filename="../editor.py" line="125" />
            <source>Name</source>
            <translation>Nombre</translation>
        </message>
        <message>
            <location filename="../editor.py" line="128" />
            <source>vpn.example.com:443</source>
            <translation>vpn.cliente.com:443</translation>
        </message>
        <message>
            <location filename="../editor.py" line="129" />
            <source>Host</source>
            <translation>Host</translation>
        </message>
        <message>
            <location filename="../editor.py" line="132" />
            <source>user@example.com</source>
            <translation>usuario@cliente.com</translation>
        </message>
        <message>
            <location filename="../editor.py" line="133" />
            <source>Username</source>
            <translation>Usuario</translation>
        </message>
        <message>
            <location filename="../editor.py" line="137" />
            <source>Optional with SAML: the ACS username will be used. Fill it only as a fallback.</source>
            <translation>Opcional con SAML: se usará el usuario que devuelva el ACS. Rellénalo solo como respaldo.</translation>
        </message>
        <message>
            <location filename="../editor.py" line="149" />
            <source>Protocol</source>
            <translation>Protocolo</translation>
        </message>
        <message>
            <location filename="../editor.py" line="157" />
            <source>Optional text for the list</source>
            <translation>Texto opcional para la lista</translation>
        </message>
        <message>
            <location filename="../editor.py" line="159" />
            <source>Description</source>
            <translation>Descripción</translation>
        </message>
        <message>
            <location filename="../editor.py" line="161" />
            <source>General</source>
            <translation>General</translation>
        </message>
        <message>
            <location filename="../editor.py" line="170" />
            <source>Use SAML (SSO)</source>
            <translation>Usar SAML (SSO)</translation>
        </message>
        <message>
            <location filename="../editor.py" line="174" />
            <source>Authenticate against the gateway (instead of the portal)</source>
            <translation>Autenticar contra el gateway (en vez del portal)</translation>
        </message>
        <message>
            <location filename="../editor.py" line="195" />
            <source>What's the difference?</source>
            <translation>¿Qué diferencia hay?</translation>
        </message>
        <message>
            <location filename="../editor.py" line="209" />
            <location filename="../editor.py" line="372" />
            <source>clientos is sent to the portal during SAML prelogin; --os is passed to openconnect for the tunnel. They are not interchangeable.</source>
            <translation>clientos se envía al portal en el prelogin SAML; --os se envía a openconnect para el túnel. No son intercambiables.</translation>
        </message>
        <message>
            <location filename="../editor.py" line="221" />
            <source>gateway or gateway:prelogin-cookie (empty = automatic)</source>
            <translation>gateway o gateway:prelogin-cookie (vacío = automático)</translation>
        </message>
        <message>
            <location filename="../editor.py" line="231" />
            <source>WebView User-Agent (optional)</source>
            <translation>User-Agent del WebView (opcional)</translation>
        </message>
        <message>
            <location filename="../editor.py" line="236" />
            <source>Ignore ACS redirects</source>
            <translation>Ignorar redirecciones del ACS</translation>
        </message>
        <message>
            <location filename="../editor.py" line="251" />
            <source>Automatic</source>
            <translation>Automático</translation>
        </message>
        <message>
            <location filename="../editor.py" line="253" />
            <source>sudo (passwordless)</source>
            <translation>sudo (sin contraseña)</translation>
        </message>
        <message>
            <location filename="../editor.py" line="254" />
            <source>Privilege escalation</source>
            <translation>Elevación</translation>
        </message>
        <message>
            <location filename="../editor.py" line="257" />
            <source>Ignore TLS errors during login (insecure)</source>
            <translation>Ignorar errores TLS en el login (inseguro)</translation>
        </message>
        <message>
            <location filename="../editor.py" line="263" />
            <source>Only affects prelogin and the WebView. openconnect will still validate the tunnel certificate.</source>
            <translation>Solo afecta a prelogin y al WebView. openconnect seguirá validando el certificado del túnel.</translation>
        </message>
        <message>
            <location filename="../editor.py" line="273" />
            <source>Allow legacy ciphers (--allow-insecure-crypto)</source>
            <translation>Permitir cifrados antiguos (--allow-insecure-crypto)</translation>
        </message>
        <message>
            <location filename="../editor.py" line="279" />
            <source>--csd-wrapper=/path/hip.sh
--no-dtls</source>
            <translation>--csd-wrapper=/ruta/hip.sh
--no-dtls</translation>
        </message>
        <message>
            <location filename="../editor.py" line="282" />
            <source>Extra arguments</source>
            <translation>Argumentos extra</translation>
        </message>
        <message>
            <location filename="../editor.py" line="285" />
            <source>One argument per line. Do not put passwords here.</source>
            <translation>Un argumento por línea. No pongas contraseñas aquí.</translation>
        </message>
        <message>
            <location filename="../editor.py" line="292" />
            <source>Advanced</source>
            <translation>Avanzado</translation>
        </message>
        <message>
            <location filename="../editor.py" line="380" />
            <source>SAML disabled: clientos is not used. --os is passed to openconnect for the tunnel.</source>
            <translation>SAML desactivado: clientos no se usa. --os se envía a openconnect para el túnel.</translation>
        </message>
        <message>
            <location filename="../editor.py" line="422" />
            <source>Help: --os and clientos</source>
            <translation>Ayuda: --os y clientos</translation>
        </message>
        <message>
            <location filename="../editor.py" line="424" />
            <source>&lt;h3&gt;--os vs clientos&lt;/h3&gt;&lt;p&gt;&lt;b&gt;clientos&lt;/b&gt; is sent to the portal in &lt;code&gt;prelogin.esp&lt;/code&gt; so it can decide which SAML flow to offer. Typical values: &lt;code&gt;Windows&lt;/code&gt;, &lt;code&gt;Linux&lt;/code&gt;, &lt;code&gt;Mac&lt;/code&gt;.&lt;/p&gt;&lt;p&gt;&lt;b&gt;--os&lt;/b&gt; is passed to openconnect when connecting the tunnel and affects the DAP/HIP policy. Values: &lt;code&gt;win&lt;/code&gt;, &lt;code&gt;linux-64&lt;/code&gt;, &lt;code&gt;mac-intel&lt;/code&gt;, &lt;code&gt;linux&lt;/code&gt;, &lt;code&gt;android&lt;/code&gt;, &lt;code&gt;apple-ios&lt;/code&gt;.&lt;/p&gt;&lt;p&gt;They are not the same and are not used in the same phase. Some portals only offer SAML with &lt;code&gt;clientos=Windows&lt;/code&gt; even if the tunnel uses &lt;code&gt;--os=linux-64&lt;/code&gt;.&lt;/p&gt;&lt;p&gt;&lt;b&gt;Equivalences:&lt;/b&gt; Windows → win, Linux → linux-64, Mac → mac-intel.&lt;/p&gt;</source>
            <translation>&lt;h3&gt;--os vs clientos&lt;/h3&gt;&lt;p&gt;&lt;b&gt;clientos&lt;/b&gt; se envía al portal en &lt;code&gt;prelogin.esp&lt;/code&gt; para que decida qué flujo SAML ofrecer. Valores habituales: &lt;code&gt;Windows&lt;/code&gt;, &lt;code&gt;Linux&lt;/code&gt;, &lt;code&gt;Mac&lt;/code&gt;.&lt;/p&gt;&lt;p&gt;&lt;b&gt;--os&lt;/b&gt; se pasa a openconnect al conectar el túnel y afecta a la política DAP/HIP. Valores: &lt;code&gt;win&lt;/code&gt;, &lt;code&gt;linux-64&lt;/code&gt;, &lt;code&gt;mac-intel&lt;/code&gt;, &lt;code&gt;linux&lt;/code&gt;, &lt;code&gt;android&lt;/code&gt;, &lt;code&gt;apple-ios&lt;/code&gt;.&lt;/p&gt;&lt;p&gt;No son lo mismo ni se usan en la misma fase. En algunos portales el SAML solo aparece con &lt;code&gt;clientos=Windows&lt;/code&gt; aunque el túnel use &lt;code&gt;--os=linux-64&lt;/code&gt;.&lt;/p&gt;&lt;p&gt;&lt;b&gt;Equivalencias:&lt;/b&gt; Windows → win, Linux → linux-64, Mac → mac-intel.&lt;/p&gt;</translation>
        </message>
        <message>
            <location filename="../editor.py" line="519" />
            <source>Check the connection</source>
            <translation>Revisa la conexión</translation>
        </message>
        <message>
            <location filename="../editor.py" line="529" />
            <source>Duplicate connection</source>
            <translation>Conexión duplicada</translation>
        </message>
        <message>
            <location filename="../editor.py" line="531" />
            <source>A connection with the same host, user and protocol already exists:

{name}

Save anyway?</source>
            <translation>Ya existe una conexión con el mismo host, usuario y protocolo:

{name}

¿Guardar igualmente?</translation>
        </message>
    </context>
    <context>
        <name>GlobalProtect</name>
        <message>
            <location filename="../gp.py" line="138" />
            <source>{endpoint} returned HTTP {code}</source>
            <translation>{endpoint} respondió HTTP {code}</translation>
        </message>
        <message>
            <location filename="../gp.py" line="144" />
            <source>Could not contact {endpoint}: {error}</source>
            <translation>No se pudo contactar {endpoint}: {error}</translation>
        </message>
        <message>
            <location filename="../gp.py" line="153" />
            <source>Invalid response from {endpoint}: {error}</source>
            <translation>Respuesta inválida de {endpoint}: {error}</translation>
        </message>
        <message>
            <location filename="../gp.py" line="161" />
            <source>{host} does not appear to be a GlobalProtect {interface} (response &lt;{tag}&gt;)</source>
            <translation>{host} no parece ser un {interface} GlobalProtect (respuesta &lt;{tag}&gt;)</translation>
        </message>
        <message>
            <location filename="../gp.py" line="177" />
            <source>GlobalProtect returned an error: {detail}</source>
            <translation>GlobalProtect respondió con error: {detail}</translation>
        </message>
        <message>
            <location filename="../gp.py" line="189" />
            <source>{host} does not advertise SAML on the {interface} interface. Try 'gateway': {gateway} or disable 'saml'.</source>
            <translation>{host} no anuncia SAML en la interfaz {interface}. Prueba con 'gateway': {gateway} o desactiva 'saml'.</translation>
        </message>
        <message>
            <location filename="../gp.py" line="204" />
            <source>Could not decode the SAML request: {error}</source>
            <translation>No se pudo decodificar la petición SAML: {error}</translation>
        </message>
        <message>
            <location filename="../gp.py" line="212" />
            <source>Unknown SAML method: {method}</source>
            <translation>Método SAML desconocido: {method}</translation>
        </message>
    </context>
    <context>
        <name>MainWindow</name>
        <message>
            <location filename="../ui.py" line="277" />
            <location filename="../ui.py" line="713" />
            <source>Reload</source>
            <translation>Recargar</translation>
        </message>
        <message>
            <location filename="../ui.py" line="278" />
            <location filename="../ui.py" line="715" />
            <source>Re-read the connections JSON</source>
            <translation>Volver a leer el JSON de conexiones</translation>
        </message>
        <message>
            <location filename="../ui.py" line="298" />
            <location filename="../ui.py" line="717" />
            <source>Migrate now</source>
            <translation>Migrar ahora</translation>
        </message>
        <message>
            <location filename="../ui.py" line="307" />
            <location filename="../ui.py" line="718" />
            <source>Connections</source>
            <translation>Conexiones</translation>
        </message>
        <message>
            <location filename="../ui.py" line="311" />
            <location filename="../ui.py" line="719" />
            <source>Add</source>
            <translation>Añadir</translation>
        </message>
        <message>
            <location filename="../ui.py" line="315" />
            <location filename="../ui.py" line="720" />
            <source>Edit</source>
            <translation>Editar</translation>
        </message>
        <message>
            <location filename="../ui.py" line="319" />
            <location filename="../ui.py" line="721" />
            <location filename="../ui.py" line="796" />
            <source>Delete</source>
            <translation>Eliminar</translation>
        </message>
        <message>
            <location filename="../ui.py" line="323" />
            <location filename="../ui.py" line="722" />
            <source>Migrate configuration</source>
            <translation>Migrar configuración</translation>
        </message>
        <message>
            <location filename="../ui.py" line="326" />
            <location filename="../ui.py" line="725" />
            <source>Copy the legacy configuration to ~/.config/pasaporte/hosts.json and switch to editable mode</source>
            <translation>Copiar la configuración legacy a ~/.config/pasaporte/hosts.json y pasar a modo editable</translation>
        </message>
        <message>
            <location filename="../ui.py" line="364" />
            <location filename="../ui.py" line="729" />
            <source>No connections yet</source>
            <translation>No hay conexiones todavía</translation>
        </message>
        <message>
            <location filename="../ui.py" line="374" />
            <location filename="../ui.py" line="731" />
            <source>Press “Add” to create the first connection.</source>
            <translation>Pulsa «Añadir» para crear la primera conexión.</translation>
        </message>
        <message>
            <location filename="../ui.py" line="385" />
            <location filename="../ui.py" line="733" />
            <source>Add connection</source>
            <translation>Añadir conexión</translation>
        </message>
        <message>
            <location filename="../ui.py" line="404" />
            <location filename="../ui.py" line="734" />
            <source>Log</source>
            <translation>Registro</translation>
        </message>
        <message>
            <location filename="../ui.py" line="408" />
            <location filename="../ui.py" line="735" />
            <source>Clear</source>
            <translation>Limpiar</translation>
        </message>
        <message>
            <location filename="../ui.py" line="421" />
            <location filename="../ui.py" line="737" />
            <source>openconnect output will appear here.</source>
            <translation>Aquí verás la salida de openconnect.</translation>
        </message>
        <message>
            <location filename="../ui.py" line="433" />
            <location filename="../ui.py" line="601" />
            <location filename="../ui.py" line="739" />
            <location filename="../ui.py" line="766" />
            <location filename="../ui.py" line="787" />
            <source>Connect</source>
            <translation>Conectar</translation>
        </message>
        <message>
            <location filename="../ui.py" line="438" />
            <location filename="../ui.py" line="604" />
            <location filename="../ui.py" line="740" />
            <location filename="../ui.py" line="767" />
            <source>Disconnect</source>
            <translation>Desconectar</translation>
        </message>
        <message>
            <location filename="../ui.py" line="445" />
            <location filename="../ui.py" line="741" />
            <source>Open configuration</source>
            <translation>Abrir configuración</translation>
        </message>
        <message>
            <location filename="../ui.py" line="455" />
            <location filename="../ui.py" line="1513" />
            <location filename="../ui.py" line="1530" />
            <location filename="../ui.py" line="1596" />
            <source>Disconnected</source>
            <translation>Sin conexión</translation>
        </message>
        <message>
            <location filename="../ui.py" line="473" />
            <location filename="../ui.py" line="743" />
            <source>File</source>
            <translation>Archivo</translation>
        </message>
        <message>
            <location filename="../ui.py" line="476" />
            <location filename="../ui.py" line="745" />
            <source>New connection</source>
            <translation>Nueva conexión</translation>
        </message>
        <message>
            <location filename="../ui.py" line="482" />
            <location filename="../ui.py" line="746" />
            <source>Edit connection</source>
            <translation>Editar conexión</translation>
        </message>
        <message>
            <location filename="../ui.py" line="488" />
            <location filename="../ui.py" line="747" />
            <location filename="../ui.py" line="1391" />
            <source>Delete connection</source>
            <translation>Eliminar conexión</translation>
        </message>
        <message>
            <location filename="../ui.py" line="497" />
            <location filename="../ui.py" line="748" />
            <source>Import configuration…</source>
            <translation>Importar configuración…</translation>
        </message>
        <message>
            <location filename="../ui.py" line="503" />
            <location filename="../ui.py" line="749" />
            <source>Export configuration…</source>
            <translation>Exportar configuración…</translation>
        </message>
        <message>
            <location filename="../ui.py" line="509" />
            <location filename="../ui.py" line="750" />
            <source>Open configuration folder</source>
            <translation>Abrir carpeta de configuración</translation>
        </message>
        <message>
            <location filename="../ui.py" line="517" />
            <location filename="../ui.py" line="751" />
            <source>Migrate configuration…</source>
            <translation>Migrar configuración…</translation>
        </message>
        <message>
            <location filename="../ui.py" line="526" />
            <location filename="../ui.py" line="752" />
            <source>Reload configuration</source>
            <translation>Recargar configuración</translation>
        </message>
        <message>
            <location filename="../ui.py" line="532" />
            <location filename="../ui.py" line="753" />
            <source>Open configuration…</source>
            <translation>Abrir configuración…</translation>
        </message>
        <message>
            <location filename="../ui.py" line="536" />
            <location filename="../ui.py" line="758" />
            <source>Language</source>
            <translation>Idioma</translation>
        </message>
        <message>
            <location filename="../ui.py" line="542" />
            <location filename="../ui.py" line="761" />
            <source>Automatic (system)</source>
            <translation>Automático (sistema)</translation>
        </message>
        <message>
            <location filename="../ui.py" line="561" />
            <location filename="../ui.py" line="755" />
            <source>Minimize to tray</source>
            <translation>Minimizar a la bandeja</translation>
        </message>
        <message>
            <location filename="../ui.py" line="569" />
            <location filename="../ui.py" line="608" />
            <location filename="../ui.py" line="754" />
            <location filename="../ui.py" line="768" />
            <location filename="../ui.py" line="1820" />
            <source>Quit</source>
            <translation>Salir</translation>
        </message>
        <message>
            <location filename="../ui.py" line="574" />
            <location filename="../ui.py" line="744" />
            <source>Help</source>
            <translation>Ayuda</translation>
        </message>
        <message>
            <location filename="../ui.py" line="575" />
            <source>Check for updates…</source>
            <translation>Buscar actualizaciones…</translation>
        </message>
        <message>
            <location filename="../ui.py" line="579" />
            <location filename="../ui.py" line="757" />
            <source>About…</source>
            <translation>Acerca de…</translation>
        </message>
        <message>
            <location filename="../ui.py" line="598" />
            <location filename="../ui.py" line="765" />
            <source>Show</source>
            <translation>Mostrar</translation>
        </message>
        <message>
            <location filename="../ui.py" line="633" />
            <source>Keep Pasaporte in the tray when its window is closed or minimized</source>
            <translation>Mantener Pasaporte en la bandeja cuando se cierre o minimice su ventana</translation>
        </message>
        <message>
            <location filename="../ui.py" line="637" />
            <source>No system tray is available on this desktop</source>
            <translation>Este escritorio no ofrece bandeja del sistema</translation>
        </message>
        <message>
            <location filename="../ui.py" line="660" />
            <source>Pasaporte keeps running in the tray. Use its icon to show the window or quit.</source>
            <translation>Pasaporte sigue en la bandeja. Usa su icono para mostrar la ventana o salir.</translation>
        </message>
        <message>
            <location filename="../ui.py" line="793" />
            <source>Edit…</source>
            <translation>Editar…</translation>
        </message>
        <message>
            <location filename="../ui.py" line="801" />
            <source>Add connection…</source>
            <translation>Añadir conexión…</translation>
        </message>
        <message>
            <location filename="../ui.py" line="827" />
            <location filename="../ui.py" line="1272" />
            <location filename="../ui.py" line="1286" />
            <location filename="../ui.py" line="1317" />
            <location filename="../ui.py" line="1361" />
            <location filename="../ui.py" line="1408" />
            <source>Configuration</source>
            <translation>Configuración</translation>
        </message>
        <message>
            <location filename="../ui.py" line="829" />
            <source>Configuration error: {error}</source>
            <translation>Error de configuración: {error}</translation>
        </message>
        <message>
            <location filename="../ui.py" line="875" />
            <source>Configuration loaded: {count} connection(s) from {path}</source>
            <translation>Configuración cargada: {count} conexión(es) desde {path}</translation>
        </message>
        <message>
            <location filename="../ui.py" line="940" />
            <source> (read-only)</source>
            <translation> (solo lectura)</translation>
        </message>
        <message>
            <location filename="../ui.py" line="954" />
            <location filename="../ui.py" line="969" />
            <source>Could not open the folder:
{error}</source>
            <translation>No se pudo abrir la carpeta:
{error}</translation>
        </message>
        <message>
            <location filename="../ui.py" line="994" />
            <location filename="../ui.py" line="1068" />
            <source>Migration</source>
            <translation>Migración</translation>
        </message>
        <message>
            <location filename="../ui.py" line="996" />
            <location filename="../ui.py" line="1070" />
            <source>Could not migrate the configuration:
{error}</source>
            <translation>No se pudo migrar la configuración:
{error}</translation>
        </message>
        <message>
            <location filename="../ui.py" line="1003" />
            <location filename="../ui.py" line="1083" />
            <source>Configuration migrated ({count} connections): {source} → {target}</source>
            <translation>Configuración migrada ({count} conexiones): {source} → {target}</translation>
        </message>
        <message>
            <location filename="../ui.py" line="1018" />
            <source>An existing configuration was found.</source>
            <translation>Se encontró una configuración existente.</translation>
        </message>
        <message>
            <location filename="../ui.py" line="1021" />
            <source>{source}

Do you want to copy it to the new location?

{target}

If you choose “Continue without migrating”, it will be used in read-only mode and you will see a notice to migrate it whenever you want.</source>
            <translation>{source}

¿Quieres copiarla ahora a la nueva ubicación?

{target}

Si eliges «Seguir sin migrar», se usará en modo solo lectura y verás un aviso para migrarla cuando quieras.</translation>
        </message>
        <message>
            <location filename="../ui.py" line="1030" />
            <source>Import</source>
            <translation>Importar</translation>
        </message>
        <message>
            <location filename="../ui.py" line="1033" />
            <source>Continue without migrating (read-only)</source>
            <translation>Seguir sin migrar (solo lectura)</translation>
        </message>
        <message>
            <location filename="../ui.py" line="1052" />
            <source>Using legacy configuration in read-only mode: {path}. Use “Migrate configuration” to make it editable.</source>
            <translation>Usando configuración legacy en modo solo lectura: {path}. Usa «Migrar configuración» para poder editarla.</translation>
        </message>
        <message>
            <location filename="../ui.py" line="1097" />
            <source>The active configuration is read-only. Migrate it first to import.</source>
            <translation>La configuración activa es de solo lectura. Migra primero para poder importar.</translation>
        </message>
        <message>
            <location filename="../ui.py" line="1107" />
            <source>The current configuration is invalid. Fix it before importing.</source>
            <translation>La configuración actual no es válida. Corrígela antes de importar.</translation>
        </message>
        <message>
            <location filename="../ui.py" line="1115" />
            <location filename="../ui.py" line="1128" />
            <location filename="../ui.py" line="1133" />
            <location filename="../ui.py" line="1169" />
            <source>Import configuration</source>
            <translation>Importar configuración</translation>
        </message>
        <message>
            <location filename="../ui.py" line="1117" />
            <location filename="../ui.py" line="1188" />
            <source>JSON (*.json);;All files (*)</source>
            <translation>JSON (*.json);;Todos los archivos (*)</translation>
        </message>
        <message>
            <location filename="../ui.py" line="1137" />
            <source>Found {count} connection(s) in {source}.</source>
            <translation>Se encontraron {count} conexiones en {source}.</translation>
        </message>
        <message>
            <location filename="../ui.py" line="1140" />
            <source>What do you want to do?</source>
            <translation>¿Qué quieres hacer?</translation>
        </message>
        <message>
            <location filename="../ui.py" line="1142" />
            <source>Replace all</source>
            <translation>Reemplazar todo</translation>
        </message>
        <message>
            <location filename="../ui.py" line="1145" />
            <source>Merge by name</source>
            <translation>Fusionar por nombre</translation>
        </message>
        <message>
            <location filename="../ui.py" line="1147" />
            <source>Cancel</source>
            <translation>Cancelar</translation>
        </message>
        <message>
            <location filename="../ui.py" line="1154" />
            <source>replaced</source>
            <translation>reemplazada</translation>
        </message>
        <message>
            <location filename="../ui.py" line="1160" />
            <source>merged (+{added}, skipped {skipped})</source>
            <translation>fusionada (+{added}, omitidas {skipped})</translation>
        </message>
        <message>
            <location filename="../ui.py" line="1178" />
            <source>Configuration imported from {source}: {action}.</source>
            <translation>Configuración importada desde {source}: {action}.</translation>
        </message>
        <message>
            <location filename="../ui.py" line="1186" />
            <location filename="../ui.py" line="1201" />
            <source>Export configuration</source>
            <translation>Exportar configuración</translation>
        </message>
        <message>
            <location filename="../ui.py" line="1206" />
            <source>Configuration exported to {path}.</source>
            <translation>Configuración exportada a {path}.</translation>
        </message>
        <message>
            <location filename="../ui.py" line="1219" />
            <source>The active configuration is read-only. Press “Migrate configuration” to move it to ~/.config/pasaporte/hosts.json.</source>
            <translation>La configuración activa es de solo lectura. Pulsa «Migrar configuración» para moverla a ~/.config/pasaporte/hosts.json.</translation>
        </message>
        <message>
            <location filename="../ui.py" line="1230" />
            <source>The configuration could not be loaded. Fix the JSON or restore the backup and press Reload.</source>
            <translation>La configuración no se pudo cargar. Corrige el JSON o restaura el backup y pulsa Recargar.</translation>
        </message>
        <message>
            <location filename="../ui.py" line="1240" />
            <source>Disconnect the VPN before modifying the configuration.</source>
            <translation>Desconecta la VPN antes de modificar la configuración.</translation>
        </message>
        <message>
            <location filename="../ui.py" line="1252" />
            <source>Configuration changed</source>
            <translation>Configuración modificada</translation>
        </message>
        <message>
            <location filename="../ui.py" line="1254" />
            <source>{path} changed outside {app}.

Overwrite it with the current changes?</source>
            <translation>{path} cambió fuera de {app}.

¿Sobrescribirlo con los cambios actuales?</translation>
        </message>
        <message>
            <location filename="../ui.py" line="1273" />
            <location filename="../ui.py" line="1287" />
            <source>Could not save:
{error}</source>
            <translation>No se pudo guardar:
{error}</translation>
        </message>
        <message>
            <location filename="../ui.py" line="1325" />
            <source>Connection added: {name}</source>
            <translation>Añadida conexión: {name}</translation>
        </message>
        <message>
            <location filename="../ui.py" line="1340" />
            <source>Select a connection to edit.</source>
            <translation>Selecciona una conexión para editarla.</translation>
        </message>
        <message>
            <location filename="../ui.py" line="1369" />
            <source>Connection edited: {name}</source>
            <translation>Editada conexión: {name}</translation>
        </message>
        <message>
            <location filename="../ui.py" line="1384" />
            <source>Select a connection to delete.</source>
            <translation>Selecciona una conexión para eliminarla.</translation>
        </message>
        <message>
            <location filename="../ui.py" line="1393" />
            <source>Delete “{name}”?

A backup will be saved to {backup}.</source>
            <translation>¿Eliminar «{name}»?

Se guardará un backup en {backup}.</translation>
        </message>
        <message>
            <location filename="../ui.py" line="1416" />
            <source>Connection deleted: {name}</source>
            <translation>Eliminada conexión: {name}</translation>
        </message>
        <message>
            <location filename="../ui.py" line="1436" />
            <source>Select a connection from the list.</source>
            <translation>Selecciona una conexión de la lista.</translation>
        </message>
        <message>
            <location filename="../ui.py" line="1445" />
            <source>There is already an active connection. Disconnect it first.</source>
            <translation>Ya hay una conexión activa. Desconéctala primero.</translation>
        </message>
        <message>
            <location filename="../ui.py" line="1460" />
            <source>Cancelled.</source>
            <translation>Cancelado.</translation>
        </message>
        <message>
            <location filename="../ui.py" line="1472" />
            <source>Connection not found: {name}</source>
            <translation>No se encontró la conexión: {name}</translation>
        </message>
        <message>
            <location filename="../ui.py" line="1481" />
            <source>DevTools is not available, so ACS headers cannot be captured. Start the app with pasaporte or python -m pasaporte.</source>
            <translation>DevTools no está disponible, así que no se pueden capturar las cabeceras del ACS. Inicia la app con pasaporte o con python -m pasaporte.</translation>
        </message>
        <message>
            <location filename="../ui.py" line="1488" />
            <source>Getting SAML configuration…</source>
            <translation>Obteniendo configuración SAML…</translation>
        </message>
        <message>
            <location filename="../ui.py" line="1512" />
            <source>SAML cancelled.</source>
            <translation>SAML cancelado.</translation>
        </message>
        <message>
            <location filename="../ui.py" line="1519" />
            <source>SAML OK: user={user}, field={field}, host={host}</source>
            <translation>SAML OK: usuario={user}, campo={field}, host={host}</translation>
        </message>
        <message>
            <location filename="../ui.py" line="1533" />
            <source>SAML error: {message}</source>
            <translation>Error SAML: {message}</translation>
        </message>
        <message>
            <location filename="../ui.py" line="1560" />
            <source>Error: {error}</source>
            <translation>Error: {error}</translation>
        </message>
        <message>
            <location filename="../ui.py" line="1565" />
            <location filename="../ui.py" line="1588" />
            <source>Connecting…</source>
            <translation>Conectando…</translation>
        </message>
        <message>
            <location filename="../ui.py" line="1590" />
            <source>Connected</source>
            <translation>Conectado</translation>
        </message>
        <message>
            <location filename="../ui.py" line="1592" />
            <source>Disconnecting…</source>
            <translation>Desconectando…</translation>
        </message>
        <message>
            <location filename="../ui.py" line="1594" />
            <source>Error</source>
            <translation>Error</translation>
        </message>
        <message>
            <location filename="../ui.py" line="1640" />
            <source>&lt;b&gt;Read-only configuration.&lt;/b&gt; Using &lt;code&gt;{path}&lt;/code&gt;. Migrate to &lt;code&gt;~/.config/pasaporte/hosts.json&lt;/code&gt; to add, edit or delete connections.</source>
            <translation>&lt;b&gt;Configuración de solo lectura.&lt;/b&gt; Se está usando &lt;code&gt;{path}&lt;/code&gt;. Migra a &lt;code&gt;~/.config/pasaporte/hosts.json&lt;/code&gt; para poder añadir, editar o eliminar conexiones.</translation>
        </message>
        <message>
            <location filename="../ui.py" line="1647" />
            <source>Read-only configuration. Press “Migrate now” to move it to ~/.config/pasaporte/hosts.json.</source>
            <translation>Configuración de solo lectura. Pulsa «Migrar ahora» para moverla a ~/.config/pasaporte/hosts.json.</translation>
        </message>
        <message>
            <location filename="../ui.py" line="1679" />
            <source>openconnect exited with code {code}. Check the log.</source>
            <translation>openconnect terminó con código {code}. Revisa el registro.</translation>
        </message>
        <message>
            <location filename="../ui.py" line="1708" />
            <source>Checking for updates…</source>
            <translation>Buscando actualizaciones…</translation>
        </message>
        <message>
            <location filename="../ui.py" line="1717" />
            <source>Could not check for updates:
{error}</source>
            <translation>No se pudo buscar actualizaciones:
{error}</translation>
        </message>
        <message>
            <location filename="../ui.py" line="1727" />
            <source>You are using the latest version ({version}).</source>
            <translation>Estás usando la versión más reciente ({version}).</translation>
        </message>
        <message>
            <location filename="../ui.py" line="1737" />
            <source>Version {new} is available. You have {current}.</source>
            <translation>Está disponible la versión {new}. Tienes la {current}.</translation>
        </message>
        <message>
            <location filename="../ui.py" line="1741" />
            <source>Open download page</source>
            <translation>Abrir página de descarga</translation>
        </message>
        <message>
            <location filename="../ui.py" line="1743" />
            <source>Later</source>
            <translation>Más tarde</translation>
        </message>
        <message>
            <location filename="../ui.py" line="1751" />
            <source>About {app}</source>
            <translation>Acerca de {app}</translation>
        </message>
        <message>
            <location filename="../ui.py" line="1753" />
            <source>&lt;h3&gt;{app}&lt;/h3&gt;&lt;p&gt;Graphical interface for &lt;b&gt;openconnect&lt;/b&gt;.&lt;/p&gt;&lt;p&gt;Supports Fortinet, GlobalProtect with embedded SAML and any other openconnect protocol.&lt;/p&gt;&lt;p&gt;The password and SAML cookie are passed over stdin; never on the command line.&lt;/p&gt;</source>
            <translation>&lt;h3&gt;{app}&lt;/h3&gt;&lt;p&gt;Interfaz gráfica para &lt;b&gt;openconnect&lt;/b&gt;.&lt;/p&gt;&lt;p&gt;Soporta Fortinet, GlobalProtect con SAML embebido y cualquier otro protocolo de openconnect.&lt;/p&gt;&lt;p&gt;La contraseña y la cookie SAML se pasan por stdin; nunca por la línea de comandos.&lt;/p&gt;</translation>
        </message>
        <message>
            <location filename="../ui.py" line="1812" />
            <source>Wait for the SAML request to finish before quitting.</source>
            <translation>Espera a que termine la consulta SAML antes de salir.</translation>
        </message>
        <message>
            <location filename="../ui.py" line="1821" />
            <source>A VPN is connected. Disconnect and quit?</source>
            <translation>Hay una VPN conectada. ¿Desconectar y salir?</translation>
        </message>
    </context>
    <context>
        <name>OpenConnect</name>
        <message>
            <source>'openconnect' was not found in PATH. Install it first.</source>
            <translation type="vanished">no se encontró 'openconnect' en el PATH. Instálalo primero.</translation>
        </message>
        <message>
            <location filename="../openconnect.py" line="37" />
            <source>OPENCONNECT_BIN points to '{path}', but it is not an executable file.</source>
            <translation>OPENCONNECT_BIN apunta a '{path}', pero no es un archivo ejecutable.</translation>
        </message>
        <message>
            <location filename="../openconnect.py" line="49" />
            <source>'openconnect' was not found. Install it or set OPENCONNECT_BIN to its path.</source>
            <translation>no se encontró 'openconnect'. Instálalo o define OPENCONNECT_BIN con su ruta.</translation>
        </message>
        <message>
            <location filename="../openconnect.py" line="78" />
            <source>'pkexec' was not found. Install polkit or use VPN_GUI_PRIVILEGE=sudo.</source>
            <translation>no se encontró 'pkexec'. Instala polkit o usa VPN_GUI_PRIVILEGE=sudo.</translation>
        </message>
        <message>
            <location filename="../openconnect.py" line="89" />
            <source>'sudo' was not found.</source>
            <translation>no se encontró 'sudo'.</translation>
        </message>
        <message>
            <location filename="../openconnect.py" line="96" />
            <source>Unknown privilege mode: {mode!r} (use 'pkexec' or 'sudo')</source>
            <translation>modo de privilegios desconocido: {mode!r} (usa 'pkexec' o 'sudo')</translation>
        </message>
        <message>
            <location filename="../openconnect.py" line="115" />
            <source>No username for openconnect. The ACS did not return 'saml-username' and the connection has no fallback 'username'. Add one in the configuration.</source>
            <translation>No hay usuario para openconnect. El ACS no devolvió 'saml-username' y la conexión no tiene un 'username' de respaldo. Añádelo en la configuración.</translation>
        </message>
    </context>
    <context>
        <name>OpenConnectRunner</name>
        <message>
            <location filename="../runner.py" line="75" />
            <source>An openconnect process is already running.</source>
            <translation>Ya hay un proceso openconnect en ejecución.</translation>
        </message>
        <message>
            <location filename="../runner.py" line="96" />
            <source>Closing the openconnect session…</source>
            <translation>Cerrando la sesión de openconnect…</translation>
        </message>
        <message>
            <location filename="../runner.py" line="140" />
            <source>The openconnect process was not found; the session cannot be closed from here.</source>
            <translation>No se encontró el proceso openconnect; no se puede cerrar la sesión desde aquí.</translation>
        </message>
        <message>
            <location filename="../runner.py" line="153" />
            <source>Could not run kill -{signal} (did you cancel authorization?)</source>
            <translation>No se pudo ejecutar kill -{signal} (¿cancelaste la autorización?)</translation>
        </message>
        <message>
            <location filename="../runner.py" line="166" />
            <source>Signal {signal} sent to openconnect.</source>
            <translation>Señal {signal} enviada a openconnect.</translation>
        </message>
        <message>
            <location filename="../runner.py" line="173" />
            <source>Could not send {signal} to openconnect (code {code}). Did you cancel authorization?</source>
            <translation>No se pudo enviar {signal} a openconnect (código {code}). ¿Cancelaste la autorización?</translation>
        </message>
        <message>
            <location filename="../runner.py" line="184" />
            <source>openconnect did not exit in time; sending KILL.</source>
            <translation>openconnect no terminó a tiempo; enviando KILL.</translation>
        </message>
        <message>
            <location filename="../runner.py" line="194" />
            <source>Could not close openconnect; the VPN is still active as root. Press “Disconnect” again or close it with: pkexec pkill -x openconnect</source>
            <translation>No se pudo cerrar openconnect; la VPN sigue activa como root. Pulsa «Desconectar» de nuevo o ciérrala con: pkexec pkill -x openconnect</translation>
        </message>
        <message>
            <location filename="../runner.py" line="206" />
            <source>openconnect started; waiting for authentication…</source>
            <translation>openconnect iniciado; esperando autenticación…</translation>
        </message>
        <message>
            <location filename="../runner.py" line="233" />
            <source>Hint: the portal rejected the SAML cookie (512). Check that “gateway” matches the interface where you started SAML, or reconnect: the cookie expires quickly.</source>
            <translation>Sugerencia: el portal rechazó la cookie SAML (512). Comprueba que «gateway» coincide con la interfaz donde iniciaste el SAML, o vuelve a conectar: la cookie caduca pronto.</translation>
        </message>
        <message>
            <location filename="../runner.py" line="256" />
            <source>openconnect could not run. If using pkexec, cancel or authorize the Polkit dialog; if using sudo, configure passwordless sudoers.</source>
            <translation>openconnect no pudo ejecutarse. Si usas pkexec, cancela o autoriza el diálogo de Polkit; si usas sudo, configura sudoers sin contraseña.</translation>
        </message>
        <message>
            <location filename="../runner.py" line="272" />
            <source>Could not start the process. Is openconnect installed?</source>
            <translation>No se pudo iniciar el proceso. ¿Está instalado openconnect?</translation>
        </message>
        <message>
            <location filename="../runner.py" line="277" />
            <source>openconnect terminated abnormally.</source>
            <translation>openconnect terminó de forma anormal.</translation>
        </message>
    </context>
    <context>
        <name>PasswordDialog</name>
        <message>
            <location filename="../ui.py" line="104" />
            <source>Password · {name}</source>
            <translation>Contraseña · {name}</translation>
        </message>
        <message>
            <location filename="../ui.py" line="128" />
            <source>VPN password</source>
            <translation>Contraseña de la VPN</translation>
        </message>
        <message>
            <location filename="../ui.py" line="131" />
            <source>Show password</source>
            <translation>Mostrar contraseña</translation>
        </message>
    </context>
    <context>
        <name>SamlLoginDialog</name>
        <message>
            <location filename="../saml_dialog.py" line="93" />
            <source>SAML · {name}</source>
            <translation>SAML · {name}</translation>
        </message>
        <message>
            <location filename="../saml_dialog.py" line="112" />
            <source>&lt;b&gt;{name}&lt;/b&gt;&lt;br&gt;Complete the SSO login. When finished, the VPN will connect automatically.</source>
            <translation>&lt;b&gt;{name}&lt;/b&gt;&lt;br&gt;Completa el inicio de sesión SSO. Al terminar, la VPN se conectará automáticamente.</translation>
        </message>
        <message>
            <location filename="../saml_dialog.py" line="130" />
            <source>Preparing browser…</source>
            <translation>Preparando el navegador…</translation>
        </message>
        <message>
            <location filename="../saml_dialog.py" line="146" />
            <source>Cancel</source>
            <translation>Cancelar</translation>
        </message>
        <message>
            <location filename="../saml_dialog.py" line="151" />
            <source>Loading…</source>
            <translation>Cargando…</translation>
        </message>
        <message>
            <location filename="../saml_dialog.py" line="162" />
            <source>DevTools: {message}</source>
            <translation>DevTools: {message}</translation>
        </message>
        <message>
            <location filename="../saml_dialog.py" line="200" />
            <source>Loading… {value}%</source>
            <translation>Cargando… {value}%</translation>
        </message>
        <message>
            <location filename="../saml_dialog.py" line="207" />
            <source>Could not load: {url}</source>
            <translation>No se pudo cargar: {url}</translation>
        </message>
        <message>
            <location filename="../saml_dialog.py" line="214" />
            <source>Loaded: {url}</source>
            <translation>Cargado: {url}</translation>
        </message>
        <message>
            <location filename="../saml_dialog.py" line="234" />
            <source>Certificate rejected: {error}</source>
            <translation>Certificado rechazado: {error}</translation>
        </message>
        <message>
            <location filename="../saml_dialog.py" line="254" />
            <source>Waiting for SSO login…</source>
            <translation>Esperando el inicio de sesión SSO…</translation>
        </message>
        <message>
            <location filename="../saml_dialog.py" line="378" />
            <source>The SAML provider rejected authentication.</source>
            <translation>El proveedor SAML rechazó la autenticación.</translation>
        </message>
        <message>
            <location filename="../saml_dialog.py" line="392" />
            <source>The ACS did not return 'saml-username'. Cancel and add a fallback username in the configuration.</source>
            <translation>El ACS no devolvió 'saml-username'. Cancela y añade un usuario de respaldo en la configuración.</translation>
        </message>
        <message>
            <location filename="../saml_dialog.py" line="419" />
            <source>SAML complete. Connecting…</source>
            <translation>SAML completado. Conectando…</translation>
        </message>
        <message>
            <location filename="../saml_dialog.py" line="429" />
            <source>SAML login took too long. Try again.</source>
            <translation>El inicio de sesión SAML tardó demasiado. Inténtalo de nuevo.</translation>
        </message>
    </context>
</TS>