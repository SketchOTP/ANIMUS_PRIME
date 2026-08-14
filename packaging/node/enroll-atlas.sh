#!/usr/bin/env bash
set -euo pipefail

CORE_URL="${PRIME_CORE_URL:-http://127.0.0.1:18000}"
NODE_URL="${PRIME_NODE_URL:-https://127.0.0.1:18001}"
NODE_ID="${PRIME_NODE_ID:-node-041-atlas-native}"
PASSWORD_FILE="${PRIME_OPERATOR_PASSWORD_FILE:-/home/sketch/.config/animus-prime/operator.password}"
NODE_CSR_FILE="${PRIME_NODE_CSR_FILE:-/home/sketch/.local/share/animus-prime-node/trust/node.csr}"
NODE_CA_FILE="${PRIME_NODE_CA_FILE:-/home/sketch/.local/share/animus-prime-node/trust/ca.crt}"
CORE_CERT_FILE="${PRIME_NODE_CORE_CERT_FILE:-/home/sketch/.local/share/animus-prime-core/trust/core-client.crt}"
CORE_KEY_FILE="${PRIME_NODE_CORE_KEY_FILE:-/home/sketch/.local/share/animus-prime-core/trust/core-client.key}"

for required in "$PASSWORD_FILE" "$NODE_CSR_FILE" "$NODE_CA_FILE" "$CORE_CERT_FILE" "$CORE_KEY_FILE"; do
  [[ -f "$required" ]] || { echo "required secure enrollment reference is missing" >&2; exit 1; }
done

tmp_dir="$(mktemp -d)"
chmod 0700 "$tmp_dir"
trap 'rm -rf "$tmp_dir"' EXIT
cookie_file="$tmp_dir/cookies"
login_file="$tmp_dir/login.json"
bootstrap_file="$tmp_dir/bootstrap.json"
node_file="$tmp_dir/node.json"
proof_file="$tmp_dir/proof.json"

password="$(<"$PASSWORD_FILE")"
curl -fsS -o "$login_file" -c "$cookie_file" -H "Origin: http://127.0.0.1:8000" -H 'Content-Type: application/json' \
  --data "$(jq -cn --arg password "$password" '{password:$password}')" "$CORE_URL/v1/auth/login"
csrf="$(jq -er '.csrf_token' "$login_file")"

curl -fsS -o "$bootstrap_file" -b "$cookie_file" -c "$cookie_file" -H "Origin: http://127.0.0.1:8000" -H "X-PRIME-CSRF: $csrf" -H 'Content-Type: application/json' \
  --data "$(jq -cn --arg node_id "$NODE_ID" '{node_id:$node_id,endpoint:"https://127.0.0.1:18001",requested_metadata:{platform:"atlas",allowed_roots:["/home/sketch/Projects"],capabilities:["repository.inspect","files.read","files.list","git.read","health","heartbeat"],protocol_version:"node-control-v1"}}')" "$CORE_URL/v1/nodes/enrollment"
challenge_id="$(jq -er '.challenge_id' "$bootstrap_file")"
credential="$(jq -er '.bootstrap_credential' "$bootstrap_file")"

curl -fsS -o "$node_file" --cacert "$NODE_CA_FILE" --cert "$CORE_CERT_FILE" --key "$CORE_KEY_FILE" -H 'Content-Type: application/json' \
  --data "$(jq -cn --arg credential "$credential" --arg node_id "$NODE_ID" --rawfile csr "$NODE_CSR_FILE" '{credential:$credential,node_id:$node_id,csr_pem:$csr}')" "$NODE_URL/v1/enroll"

curl -fsS -o "$proof_file" -b "$cookie_file" -H "Origin: http://127.0.0.1:8000" -H "X-PRIME-CSRF: $csrf" -H 'Content-Type: application/json' \
  --data "$(jq -cn --arg node_id "$NODE_ID" --rawfile csr "$NODE_CSR_FILE" '{node_id:$node_id,csr_pem:$csr,metadata:{source:"atlas-enrollment-script",node_proof:"mTLS response received"}}')" "$CORE_URL/v1/nodes/enrollment/$challenge_id/proof"

echo "Atlas Node enrollment proof submitted for operator approval: $challenge_id"
