#!/usr/bin/env bash
set -euo pipefail

PREFIX="${1:-/opt/animus-prime-node}"
SERVICE="${2:-prime-node}"
DATA="/var/lib/animus-prime-node"

if [[ "${3:-}" == "uninstall" ]]; then
  systemctl disable --now "$SERVICE" 2>/dev/null || true
  rm -f "/etc/systemd/system/${SERVICE}.service"
  systemctl daemon-reload
  echo "Removed ${SERVICE}; ${DATA} was preserved for explicit identity-retention/removal decision."
  exit 0
fi

install -d -m 0750 "$PREFIX" "$DATA" /etc/animus-prime
install -m 0644 "$(dirname "$0")/prime-node.service" "/etc/systemd/system/${SERVICE}.service"
sed -i "s#^WorkingDirectory=.*#WorkingDirectory=${PREFIX}#; s#^ExecStart=.*#ExecStart=${PREFIX}/.venv/bin/python -m apps.node.main#; s#^ReadWritePaths=.*#ReadWritePaths=${DATA}#" "/etc/systemd/system/${SERVICE}.service"
systemctl daemon-reload
systemctl enable "$SERVICE"
echo "Installed ${SERVICE} with automatic startup. Configure /etc/animus-prime/node.env with TLS/mTLS and allowed roots before starting."
echo "Identity state is outside the repository at ${DATA}; rerunning this installer preserves it."
