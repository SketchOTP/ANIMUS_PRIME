#!/usr/bin/env bash
set -euo pipefail

umask 077
STATE_DIR="${PRIME_STATE_DIR:-/home/sketch/.config/animus-prime}"
LOCAL_FILE="$STATE_DIR/local-recovery.secret"
RECOVERY_FILE="$STATE_DIR/recovery.credential"
RESPONSE_FILE="$STATE_DIR/local-recovery.response.json"

mkdir -p "$STATE_DIR"
chmod 700 "$STATE_DIR"

if [[ ! -s "$LOCAL_FILE" ]]; then
  openssl rand -hex 48 >"$LOCAL_FILE"
  chmod 600 "$LOCAL_FILE"
  curl --fail --silent --show-error --request POST \
    --header "X-PRIME-Local-Recovery: $(<"$LOCAL_FILE")" \
    http://127.0.0.1:18000/v1/auth/local-recovery/provision >/dev/null
fi

if [[ -z "${PRIME_OPERATOR_PASSWORD:-}" ]]; then
  read -r -s -p "New PRIME operator password (12+ characters): " PRIME_OPERATOR_PASSWORD
  printf '\n'
fi
if (( ${#PRIME_OPERATOR_PASSWORD} < 12 )); then
  echo "Password must contain at least 12 characters." >&2
  exit 1
fi

command -v jq >/dev/null || { echo "jq is required for secret-safe JSON handling." >&2; exit 1; }
jq -n --arg password "$PRIME_OPERATOR_PASSWORD" '{new_password:$password}' |
  curl --fail --silent --show-error --request POST \
    --header "Content-Type: application/json" \
    --header "X-PRIME-Local-Recovery: $(<"$LOCAL_FILE")" \
    --data-binary @- "http://127.0.0.1:18000/v1/auth/local-recovery" >"$RESPONSE_FILE"
chmod 600 "$RESPONSE_FILE"

jq -e '.recovery_credential and .local_recovery_credential' "$RESPONSE_FILE" >/dev/null
jq -r '.recovery_credential' "$RESPONSE_FILE" >"$RECOVERY_FILE"
jq -r '.local_recovery_credential' "$RESPONSE_FILE" >"$LOCAL_FILE"
chmod 600 "$RECOVERY_FILE" "$LOCAL_FILE"
rm -f "$RESPONSE_FILE"
unset PRIME_OPERATOR_PASSWORD
echo "PRIME operator recovery completed. Replacement credentials are stored in the platform-secured local reference."
