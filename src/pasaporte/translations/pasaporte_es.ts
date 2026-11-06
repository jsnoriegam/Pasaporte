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
            <location filename="../ui.py" line="258" />
            <location filename="../ui.py" line="613" />
            <source>Reload</source>
            <translation>Recargar</translation>
        </message>
        <message>
            <location filename="../ui.py" line="259" />
            <location filename="../ui.py" line="615" />
            <source>Re-read the connections JSON</source>
            <translation>Volver a leer el JSON de conexiones</translation>
        </message>
        <message>
            <location filename="../ui.py" line="279" />
            <location filename="../ui.py" line="617" />
            <source>Migrate now</source>
            <translation>Migrar ahora</translation>
        </message>
        <message>
            <location filename="../ui.py" line="288" />
            <location filename="../ui.py" line="618" />
            <source>Connections</source>
            <translation>Conexiones</translation>
        </message>
        <message>
            <location filename="../ui.py" line="292" />
            <location filename="../ui.py" line="619" />
            <source>Add</source>
            <translation>Añadir</translation>
        </message>
        <message>
            <location filename="../ui.py" line="296" />
            <location filename="../ui.py" line="620" />
            <source>Edit</source>
            <translation>Editar</translation>
        </message>
        <message>
            <location filename="../ui.py" line="300" />
            <location filename="../ui.py" line="621" />
            <location filename="../ui.py" line="694" />
            <source>Delete</source>
            <translation>Eliminar</translation>
        </message>
        <message>
            <location filename="../ui.py" line="304" />
            <location filename="../ui.py" line="622" />
            <source>Migrate configuration</source>
            <translation>Migrar configuración</translation>
        </message>
        <message>
            <location filename="../ui.py" line="307" />
            <location filename="../ui.py" line="625" />
            <source>Copy the legacy configuration to ~/.config/pasaporte/hosts.json and switch to editable mode</source>
            <translation>Copiar la configuración legacy a ~/.config/pasaporte/hosts.json y pasar a modo editable</translation>
        </message>
        <message>
            <location filename="../ui.py" line="345" />
            <location filename="../ui.py" line="629" />
            <source>No connections yet</source>
            <translation>No hay conexiones todavía</translation>
        </message>
        <message>
            <location filename="../ui.py" line="355" />
            <location filename="../ui.py" line="631" />
            <source>Press “Add” to create the first connection.</source>
            <translation>Pulsa «Añadir» para crear la primera conexión.</translation>
        </message>
        <message>
            <location filename="../ui.py" line="366" />
            <location filename="../ui.py" line="633" />
            <source>Add connection</source>
            <translation>Añadir conexión</translation>
        </message>
        <message>
            <location filename="../ui.py" line="385" />
            <location filename="../ui.py" line="634" />
            <source>Log</source>
            <translation>Registro</translation>
        </message>
        <message>
            <location filename="../ui.py" line="389" />
            <location filename="../ui.py" line="635" />
            <source>Clear</source>
            <translation>Limpiar</translation>
        </message>
        <message>
            <location filename="../ui.py" line="402" />
            <location filename="../ui.py" line="637" />
            <source>openconnect output will appear here.</source>
            <translation>Aquí verás la salida de openconnect.</translation>
        </message>
        <message>
            <location filename="../ui.py" line="414" />
            <location filename="../ui.py" line="569" />
            <location filename="../ui.py" line="639" />
            <location filename="../ui.py" line="664" />
            <location filename="../ui.py" line="685" />
            <source>Connect</source>
            <translation>Conectar</translation>
        </message>
        <message>
            <location filename="../ui.py" line="419" />
            <location filename="../ui.py" line="572" />
            <location filename="../ui.py" line="640" />
            <location filename="../ui.py" line="665" />
            <source>Disconnect</source>
            <translation>Desconectar</translation>
        </message>
        <message>
            <location filename="../ui.py" line="426" />
            <location filename="../ui.py" line="641" />
            <source>Open configuration</source>
            <translation>Abrir configuración</translation>
        </message>
        <message>
            <location filename="../ui.py" line="436" />
            <location filename="../ui.py" line="1411" />
            <location filename="../ui.py" line="1428" />
            <location filename="../ui.py" line="1494" />
            <source>Disconnected</source>
            <translation>Sin conexión</translation>
        </message>
        <message>
            <location filename="../ui.py" line="453" />
            <location filename="../ui.py" line="643" />
            <source>File</source>
            <translation>Archivo</translation>
        </message>
        <message>
            <location filename="../ui.py" line="456" />
            <location filename="../ui.py" line="645" />
            <source>New connection</source>
            <translation>Nueva conexión</translation>
        </message>
        <message>
            <location filename="../ui.py" line="462" />
            <location filename="../ui.py" line="646" />
            <source>Edit connection</source>
            <translation>Editar conexión</translation>
        </message>
        <message>
            <location filename="../ui.py" line="468" />
            <location filename="../ui.py" line="647" />
            <location filename="../ui.py" line="1289" />
            <source>Delete connection</source>
            <translation>Eliminar conexión</translation>
        </message>
        <message>
            <location filename="../ui.py" line="477" />
            <location filename="../ui.py" line="648" />
            <source>Import configuration…</source>
            <translation>Importar configuración…</translation>
        </message>
        <message>
            <location filename="../ui.py" line="483" />
            <location filename="../ui.py" line="649" />
            <source>Export configuration…</source>
            <translation>Exportar configuración…</translation>
        </message>
        <message>
            <location filename="../ui.py" line="489" />
            <location filename="../ui.py" line="650" />
            <source>Open configuration folder</source>
            <translation>Abrir carpeta de configuración</translation>
        </message>
        <message>
            <location filename="../ui.py" line="497" />
            <location filename="../ui.py" line="651" />
            <source>Migrate configuration…</source>
            <translation>Migrar configuración…</translation>
        </message>
        <message>
            <location filename="../ui.py" line="506" />
            <location filename="../ui.py" line="652" />
            <source>Reload configuration</source>
            <translation>Recargar configuración</translation>
        </message>
        <message>
            <location filename="../ui.py" line="512" />
            <location filename="../ui.py" line="653" />
            <source>Open configuration…</source>
            <translation>Abrir configuración…</translation>
        </message>
        <message>
            <location filename="../ui.py" line="516" />
            <location filename="../ui.py" line="656" />
            <source>Language</source>
            <translation>Idioma</translation>
        </message>
        <message>
            <location filename="../ui.py" line="522" />
            <location filename="../ui.py" line="659" />
            <source>Automatic (system)</source>
            <translation>Automático (sistema)</translation>
        </message>
        <message>
            <location filename="../ui.py" line="541" />
            <location filename="../ui.py" line="576" />
            <location filename="../ui.py" line="654" />
            <location filename="../ui.py" line="666" />
            <location filename="../ui.py" line="1661" />
            <source>Quit</source>
            <translation>Salir</translation>
        </message>
        <message>
            <location filename="../ui.py" line="546" />
            <location filename="../ui.py" line="644" />
            <source>Help</source>
            <translation>Ayuda</translation>
        </message>
        <message>
            <location filename="../ui.py" line="547" />
            <location filename="../ui.py" line="655" />
            <source>About…</source>
            <translation>Acerca de…</translation>
        </message>
        <message>
            <location filename="../ui.py" line="566" />
            <location filename="../ui.py" line="663" />
            <source>Show</source>
            <translation>Mostrar</translation>
        </message>
        <message>
            <location filename="../ui.py" line="691" />
            <source>Edit…</source>
            <translation>Editar…</translation>
        </message>
        <message>
            <location filename="../ui.py" line="699" />
            <source>Add connection…</source>
            <translation>Añadir conexión…</translation>
        </message>
        <message>
            <location filename="../ui.py" line="725" />
            <location filename="../ui.py" line="1170" />
            <location filename="../ui.py" line="1184" />
            <location filename="../ui.py" line="1215" />
            <location filename="../ui.py" line="1259" />
            <location filename="../ui.py" line="1306" />
            <source>Configuration</source>
            <translation>Configuración</translation>
        </message>
        <message>
            <location filename="../ui.py" line="727" />
            <source>Configuration error: {error}</source>
            <translation>Error de configuración: {error}</translation>
        </message>
        <message>
            <location filename="../ui.py" line="773" />
            <source>Configuration loaded: {count} connection(s) from {path}</source>
            <translation>Configuración cargada: {count} conexión(es) desde {path}</translation>
        </message>
        <message>
            <location filename="../ui.py" line="838" />
            <source> (read-only)</source>
            <translation> (solo lectura)</translation>
        </message>
        <message>
            <location filename="../ui.py" line="852" />
            <location filename="../ui.py" line="867" />
            <source>Could not open the folder:
{error}</source>
            <translation>No se pudo abrir la carpeta:
{error}</translation>
        </message>
        <message>
            <location filename="../ui.py" line="892" />
            <location filename="../ui.py" line="966" />
            <source>Migration</source>
            <translation>Migración</translation>
        </message>
        <message>
            <location filename="../ui.py" line="894" />
            <location filename="../ui.py" line="968" />
            <source>Could not migrate the configuration:
{error}</source>
            <translation>No se pudo migrar la configuración:
{error}</translation>
        </message>
        <message>
            <location filename="../ui.py" line="901" />
            <location filename="../ui.py" line="981" />
            <source>Configuration migrated ({count} connections): {source} → {target}</source>
            <translation>Configuración migrada ({count} conexiones): {source} → {target}</translation>
        </message>
        <message>
            <location filename="../ui.py" line="916" />
            <source>An existing configuration was found.</source>
            <translation>Se encontró una configuración existente.</translation>
        </message>
        <message>
            <location filename="../ui.py" line="919" />
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
            <location filename="../ui.py" line="928" />
            <source>Import</source>
            <translation>Importar</translation>
        </message>
        <message>
            <location filename="../ui.py" line="931" />
            <source>Continue without migrating (read-only)</source>
            <translation>Seguir sin migrar (solo lectura)</translation>
        </message>
        <message>
            <location filename="../ui.py" line="950" />
            <source>Using legacy configuration in read-only mode: {path}. Use “Migrate configuration” to make it editable.</source>
            <translation>Usando configuración legacy en modo solo lectura: {path}. Usa «Migrar configuración» para poder editarla.</translation>
        </message>
        <message>
            <location filename="../ui.py" line="995" />
            <source>The active configuration is read-only. Migrate it first to import.</source>
            <translation>La configuración activa es de solo lectura. Migra primero para poder importar.</translation>
        </message>
        <message>
            <location filename="../ui.py" line="1005" />
            <source>The current configuration is invalid. Fix it before importing.</source>
            <translation>La configuración actual no es válida. Corrígela antes de importar.</translation>
        </message>
        <message>
            <location filename="../ui.py" line="1013" />
            <location filename="../ui.py" line="1026" />
            <location filename="../ui.py" line="1031" />
            <location filename="../ui.py" line="1067" />
            <source>Import configuration</source>
            <translation>Importar configuración</translation>
        </message>
        <message>
            <location filename="../ui.py" line="1015" />
            <location filename="../ui.py" line="1086" />
            <source>JSON (*.json);;All files (*)</source>
            <translation>JSON (*.json);;Todos los archivos (*)</translation>
        </message>
        <message>
            <location filename="../ui.py" line="1035" />
            <source>Found {count} connection(s) in {source}.</source>
            <translation>Se encontraron {count} conexiones en {source}.</translation>
        </message>
        <message>
            <location filename="../ui.py" line="1038" />
            <source>What do you want to do?</source>
            <translation>¿Qué quieres hacer?</translation>
        </message>
        <message>
            <location filename="../ui.py" line="1040" />
            <source>Replace all</source>
            <translation>Reemplazar todo</translation>
        </message>
        <message>
            <location filename="../ui.py" line="1043" />
            <source>Merge by name</source>
            <translation>Fusionar por nombre</translation>
        </message>
        <message>
            <location filename="../ui.py" line="1045" />
            <source>Cancel</source>
            <translation>Cancelar</translation>
        </message>
        <message>
            <location filename="../ui.py" line="1052" />
            <source>replaced</source>
            <translation>reemplazada</translation>
        </message>
        <message>
            <location filename="../ui.py" line="1058" />
            <source>merged (+{added}, skipped {skipped})</source>
            <translation>fusionada (+{added}, omitidas {skipped})</translation>
        </message>
        <message>
            <location filename="../ui.py" line="1076" />
            <source>Configuration imported from {source}: {action}.</source>
            <translation>Configuración importada desde {source}: {action}.</translation>
        </message>
        <message>
            <location filename="../ui.py" line="1084" />
            <location filename="../ui.py" line="1099" />
            <source>Export configuration</source>
            <translation>Exportar configuración</translation>
        </message>
        <message>
            <location filename="../ui.py" line="1104" />
            <source>Configuration exported to {path}.</source>
            <translation>Configuración exportada a {path}.</translation>
        </message>
        <message>
            <location filename="../ui.py" line="1117" />
            <source>The active configuration is read-only. Press “Migrate configuration” to move it to ~/.config/pasaporte/hosts.json.</source>
            <translation>La configuración activa es de solo lectura. Pulsa «Migrar configuración» para moverla a ~/.config/pasaporte/hosts.json.</translation>
        </message>
        <message>
            <location filename="../ui.py" line="1128" />
            <source>The configuration could not be loaded. Fix the JSON or restore the backup and press Reload.</source>
            <translation>La configuración no se pudo cargar. Corrige el JSON o restaura el backup y pulsa Recargar.</translation>
        </message>
        <message>
            <location filename="../ui.py" line="1138" />
            <source>Disconnect the VPN before modifying the configuration.</source>
            <translation>Desconecta la VPN antes de modificar la configuración.</translation>
        </message>
        <message>
            <location filename="../ui.py" line="1150" />
            <source>Configuration changed</source>
            <translation>Configuración modificada</translation>
        </message>
        <message>
            <location filename="../ui.py" line="1152" />
            <source>{path} changed outside {app}.

Overwrite it with the current changes?</source>
            <translation>{path} cambió fuera de {app}.

¿Sobrescribirlo con los cambios actuales?</translation>
        </message>
        <message>
            <location filename="../ui.py" line="1171" />
            <location filename="../ui.py" line="1185" />
            <source>Could not save:
{error}</source>
            <translation>No se pudo guardar:
{error}</translation>
        </message>
        <message>
            <location filename="../ui.py" line="1223" />
            <source>Connection added: {name}</source>
            <translation>Añadida conexión: {name}</translation>
        </message>
        <message>
            <location filename="../ui.py" line="1238" />
            <source>Select a connection to edit.</source>
            <translation>Selecciona una conexión para editarla.</translation>
        </message>
        <message>
            <location filename="../ui.py" line="1267" />
            <source>Connection edited: {name}</source>
            <translation>Editada conexión: {name}</translation>
        </message>
        <message>
            <location filename="../ui.py" line="1282" />
            <source>Select a connection to delete.</source>
            <translation>Selecciona una conexión para eliminarla.</translation>
        </message>
        <message>
            <location filename="../ui.py" line="1291" />
            <source>Delete “{name}”?

A backup will be saved to {backup}.</source>
            <translation>¿Eliminar «{name}»?

Se guardará un backup en {backup}.</translation>
        </message>
        <message>
            <location filename="../ui.py" line="1314" />
            <source>Connection deleted: {name}</source>
            <translation>Eliminada conexión: {name}</translation>
        </message>
        <message>
            <location filename="../ui.py" line="1334" />
            <source>Select a connection from the list.</source>
            <translation>Selecciona una conexión de la lista.</translation>
        </message>
        <message>
            <location filename="../ui.py" line="1343" />
            <source>There is already an active connection. Disconnect it first.</source>
            <translation>Ya hay una conexión activa. Desconéctala primero.</translation>
        </message>
        <message>
            <location filename="../ui.py" line="1358" />
            <source>Cancelled.</source>
            <translation>Cancelado.</translation>
        </message>
        <message>
            <location filename="../ui.py" line="1370" />
            <source>Connection not found: {name}</source>
            <translation>No se encontró la conexión: {name}</translation>
        </message>
        <message>
            <location filename="../ui.py" line="1379" />
            <source>DevTools is not available, so ACS headers cannot be captured. Start the app with pasaporte or python -m pasaporte.</source>
            <translation>DevTools no está disponible, así que no se pueden capturar las cabeceras del ACS. Inicia la app con pasaporte o con python -m pasaporte.</translation>
        </message>
        <message>
            <location filename="../ui.py" line="1386" />
            <source>Getting SAML configuration…</source>
            <translation>Obteniendo configuración SAML…</translation>
        </message>
        <message>
            <location filename="../ui.py" line="1410" />
            <source>SAML cancelled.</source>
            <translation>SAML cancelado.</translation>
        </message>
        <message>
            <location filename="../ui.py" line="1417" />
            <source>SAML OK: user={user}, field={field}, host={host}</source>
            <translation>SAML OK: usuario={user}, campo={field}, host={host}</translation>
        </message>
        <message>
            <location filename="../ui.py" line="1431" />
            <source>SAML error: {message}</source>
            <translation>Error SAML: {message}</translation>
        </message>
        <message>
            <location filename="../ui.py" line="1458" />
            <source>Error: {error}</source>
            <translation>Error: {error}</translation>
        </message>
        <message>
            <location filename="../ui.py" line="1463" />
            <location filename="../ui.py" line="1486" />
            <source>Connecting…</source>
            <translation>Conectando…</translation>
        </message>
        <message>
            <location filename="../ui.py" line="1488" />
            <source>Connected</source>
            <translation>Conectado</translation>
        </message>
        <message>
            <location filename="../ui.py" line="1490" />
            <source>Disconnecting…</source>
            <translation>Desconectando…</translation>
        </message>
        <message>
            <location filename="../ui.py" line="1492" />
            <source>Error</source>
            <translation>Error</translation>
        </message>
        <message>
            <location filename="../ui.py" line="1538" />
            <source>&lt;b&gt;Read-only configuration.&lt;/b&gt; Using &lt;code&gt;{path}&lt;/code&gt;. Migrate to &lt;code&gt;~/.config/pasaporte/hosts.json&lt;/code&gt; to add, edit or delete connections.</source>
            <translation>&lt;b&gt;Configuración de solo lectura.&lt;/b&gt; Se está usando &lt;code&gt;{path}&lt;/code&gt;. Migra a &lt;code&gt;~/.config/pasaporte/hosts.json&lt;/code&gt; para poder añadir, editar o eliminar conexiones.</translation>
        </message>
        <message>
            <location filename="../ui.py" line="1545" />
            <source>Read-only configuration. Press “Migrate now” to move it to ~/.config/pasaporte/hosts.json.</source>
            <translation>Configuración de solo lectura. Pulsa «Migrar ahora» para moverla a ~/.config/pasaporte/hosts.json.</translation>
        </message>
        <message>
            <location filename="../ui.py" line="1577" />
            <source>openconnect exited with code {code}. Check the log.</source>
            <translation>openconnect terminó con código {code}. Revisa el registro.</translation>
        </message>
        <message>
            <location filename="../ui.py" line="1600" />
            <source>About {app}</source>
            <translation>Acerca de {app}</translation>
        </message>
        <message>
            <location filename="../ui.py" line="1602" />
            <source>&lt;h3&gt;{app}&lt;/h3&gt;&lt;p&gt;Graphical interface for &lt;b&gt;openconnect&lt;/b&gt;.&lt;/p&gt;&lt;p&gt;Supports Fortinet, GlobalProtect with embedded SAML and any other openconnect protocol.&lt;/p&gt;&lt;p&gt;The password and SAML cookie are passed over stdin; never on the command line.&lt;/p&gt;</source>
            <translation>&lt;h3&gt;{app}&lt;/h3&gt;&lt;p&gt;Interfaz gráfica para &lt;b&gt;openconnect&lt;/b&gt;.&lt;/p&gt;&lt;p&gt;Soporta Fortinet, GlobalProtect con SAML embebido y cualquier otro protocolo de openconnect.&lt;/p&gt;&lt;p&gt;La contraseña y la cookie SAML se pasan por stdin; nunca por la línea de comandos.&lt;/p&gt;</translation>
        </message>
        <message>
            <location filename="../ui.py" line="1653" />
            <source>Wait for the SAML request to finish before quitting.</source>
            <translation>Espera a que termine la consulta SAML antes de salir.</translation>
        </message>
        <message>
            <location filename="../ui.py" line="1662" />
            <source>A VPN is connected. Disconnect and quit?</source>
            <translation>Hay una VPN conectada. ¿Desconectar y salir?</translation>
        </message>
    </context>
    <context>
        <name>OpenConnect</name>
        <message>
            <source>'openconnect' was not found in PATH. Install it first.</source>
            <translation>no se encontró 'openconnect' en el PATH. Instálalo primero.</translation>
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
            <location filename="../ui.py" line="103" />
            <source>Password · {name}</source>
            <translation>Contraseña · {name}</translation>
        </message>
        <message>
            <location filename="../ui.py" line="127" />
            <source>VPN password</source>
            <translation>Contraseña de la VPN</translation>
        </message>
        <message>
            <location filename="../ui.py" line="130" />
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