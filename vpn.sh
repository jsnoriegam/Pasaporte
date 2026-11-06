#!/usr/bin/env bash
# Selector de VPN con openconnect.
# Lee una lista de conexiones desde un JSON, deja elegir una y solo pide el password.
#
# Uso:  vpn.sh            (usa ~/.config/pasaporte/hosts.json)
#       VPN_CONFIG=/ruta/otro.json vpn.sh
#
# Formato del JSON:
# [
#   {
#     "name": "Cliente X",
#     "host": "vpn.example.com:10443",
#     "username": "usuario",
#     "servercert": "pin-sha256:XXXXXXXX",   <- opcional
#     "protocol": "fortinet"                 <- opcional (por defecto: fortinet)
#   }
# ]

set -euo pipefail

CONFIG="${VPN_CONFIG:-${XDG_CONFIG_HOME:-$HOME/.config}/pasaporte/hosts.json}"

for cmd in jq openconnect sudo; do
  command -v "$cmd" >/dev/null 2>&1 || { echo "Error: falta '$cmd' en el PATH." >&2; exit 1; }
done

[[ -f "$CONFIG" ]] || { echo "Error: no existe $CONFIG. Abre Pasaporte para crear o migrar la configuración." >&2; exit 1; }
jq -e 'type == "array"' "$CONFIG" >/dev/null 2>&1 \
  || { echo "Error: $CONFIG debe ser un arreglo JSON." >&2; exit 1; }
jq -e 'length > 0' "$CONFIG" >/dev/null 2>&1 \
  || { echo "Error: no hay conexiones en $CONFIG. Añade alguna con Pasaporte." >&2; exit 1; }

# Etiquetas para el menú: "nombre (usuario@host:puerto)"
mapfile -t LABELS < <(jq -r '.[] | "\(.name // .host) (\(.username)@\(.host))"' "$CONFIG")

echo "Elige la VPN (Ctrl+C para cancelar):"
PS3="> "
select _ in "${LABELS[@]}"; do
  if [[ -n "${REPLY:-}" && "$REPLY" =~ ^[0-9]+$ && "$REPLY" -ge 1 && "$REPLY" -le ${#LABELS[@]} ]]; then
    IDX=$((REPLY - 1))
    break
  fi
  echo "Opción inválida."
done

HOST=$(jq -r ".[$IDX].host" "$CONFIG")
USERNAME=$(jq -r ".[$IDX].username" "$CONFIG")
SERVERCERT=$(jq -r ".[$IDX].servercert // empty" "$CONFIG")
PROTOCOL=$(jq -r ".[$IDX].protocol // \"fortinet\"" "$CONFIG")

ARGS=(--protocol="$PROTOCOL" --user="$USERNAME")
[[ -n "$SERVERCERT" ]] && ARGS+=(--servercert="$SERVERCERT")

# Pide primero la clave de sudo para que no se mezcle con el prompt del password de la VPN
sudo -v

echo "Conectando a $HOST como $USERNAME..."

if [[ -n "$SERVERCERT" ]]; then
  # Con servercert no hay prompts intermedios: el password se pide aquí y va por stdin
  read -rsp "Password VPN: " PASSWORD
  echo
  printf '%s\n' "$PASSWORD" | sudo openconnect "${ARGS[@]}" --passwd-on-stdin "$HOST"
else
  # Sin servercert, openconnect puede preguntar si aceptas el certificado,
  # así que se deja que él mismo pida todo de forma interactiva.
  echo "(Sin servercert: openconnect mostrará el certificado y pedirá confirmación y password.)"
  sudo openconnect "${ARGS[@]}" "$HOST"
fi
