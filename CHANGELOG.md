# Changelog

Todos los cambios notables de Pasaporte se documentan en este archivo.

El formato sigue [Keep a Changelog](https://keepachangelog.com/es-ES/1.1.0/)
y el proyecto usa [SemVer](https://semver.org/lang/es/).

## [Sin publicar]

### Añadido

- Licencia GPL-3.0-or-later (`LICENSE`).
- Plantillas de issues para errores y propuestas de función.
- Badges de CI, release y licencia en los READMEs.
- Ayuda → *Buscar actualizaciones…*: consulta manual a GitHub. No hay
  comprobaciones automáticas en segundo plano.
- Archivo → *Minimizar a la bandeja*: cerrar o minimizar la ventana la deja en
  la bandeja sin desconectar la VPN. Salir se hace con *Salir* o desde el menú
  de la bandeja.

## [0.1.0-beta.1] - 2026-11-06

Primera beta pública.

### Añadido

- Interfaz gráfica en PySide6 para `openconnect`, con soporte de Fortinet y
  GlobalProtect.
- Login SAML para GlobalProtect dentro de la aplicación, con WebView embebido
  y lectura de las cabeceras del ACS mediante DevTools.
- Gestión de conexiones (añadir, editar, eliminar, recargar) con escritura
  atómica, copias de seguridad `.bak` y permisos `0600`.
- Configuración canónica en `~/.config/pasaporte/hosts.json`, con migración
  desde la configuración anterior e importación/exportación.
- Interfaz en inglés (idioma fuente) y español, con cambio de idioma en
  caliente.
- Ruta de `openconnect` configurable con `OPENCONNECT_BIN`.
- Opciones de línea de comandos `--config`, `--connect NAME` y `--version`.
- Empaquetado como AppImage, construido en Ubuntu 22.04 con Podman o Docker.
- CI en GitHub Actions: tests en cada push, AppImage como artifact y release
  automático al empujar un tag `v*`.

[Sin publicar]: https://github.com/jsnoriegam/Pasaporte/compare/v0.1.0-beta.1...HEAD
[0.1.0-beta.1]: https://github.com/jsnoriegam/Pasaporte/releases/tag/v0.1.0-beta.1
