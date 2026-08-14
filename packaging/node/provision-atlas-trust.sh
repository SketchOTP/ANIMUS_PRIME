#!/usr/bin/env bash
set -euo pipefail

CORE_TRUST_ROOT="${PRIME_CORE_TRUST_ROOT:-/home/sketch/.local/share/animus-prime-core/trust}"
NODE_TRUST_ROOT="${PRIME_NODE_TRUST_ROOT:-/home/sketch/.local/share/animus-prime-node/trust}"
NODE_ID="${PRIME_NODE_ID:-node-041-atlas-native}"

install -d -m 0700 "$CORE_TRUST_ROOT" "$NODE_TRUST_ROOT"

ca_reissued=0
if [[ ! -f "$CORE_TRUST_ROOT/ca.key" || ! -f "$CORE_TRUST_ROOT/ca.crt" ]] || ! openssl x509 -in "$CORE_TRUST_ROOT/ca.crt" -text -noout 2>/dev/null | grep -q "X509v3 Key Usage"; then
  openssl req -x509 -newkey rsa:3072 -nodes -days 3650 \
    -keyout "$CORE_TRUST_ROOT/ca.key" -out "$CORE_TRUST_ROOT/ca.crt" \
    -subj "/CN=ANIMUS PRIME Atlas Local CA" \
    -addext "basicConstraints=critical,CA:TRUE,pathlen:1" \
    -addext "keyUsage=critical,keyCertSign,cRLSign" \
    -addext "subjectKeyIdentifier=hash" \
    -addext "authorityKeyIdentifier=keyid:always,issuer" >/dev/null 2>&1
  ca_reissued=1
  chmod 0600 "$CORE_TRUST_ROOT/ca.key"
  chmod 0644 "$CORE_TRUST_ROOT/ca.crt"
fi

if [[ "$ca_reissued" == "1" ]]; then
  rm -f "$CORE_TRUST_ROOT/core-client.crt" "$NODE_TRUST_ROOT/node.crt"
fi

if [[ ! -f "$CORE_TRUST_ROOT/core-client.key" ]]; then
  openssl genrsa -out "$CORE_TRUST_ROOT/core-client.key" 3072 >/dev/null 2>&1
  chmod 0600 "$CORE_TRUST_ROOT/core-client.key"
fi
if [[ ! -f "$CORE_TRUST_ROOT/core-client.crt" ]]; then
  tmp_dir="$(mktemp -d)"
  trap 'rm -rf "$tmp_dir"' EXIT
  openssl req -new -key "$CORE_TRUST_ROOT/core-client.key" -out "$tmp_dir/core.csr" -subj "/CN=prime-core" >/dev/null 2>&1
  cat >"$tmp_dir/core.ext" <<EOF
basicConstraints=critical,CA:FALSE
keyUsage=critical,digitalSignature,keyEncipherment
extendedKeyUsage=clientAuth
subjectAltName=DNS:prime-core
subjectKeyIdentifier=hash
authorityKeyIdentifier=keyid,issuer
EOF
  openssl x509 -req -in "$tmp_dir/core.csr" -CA "$CORE_TRUST_ROOT/ca.crt" -CAkey "$CORE_TRUST_ROOT/ca.key" -CAcreateserial -days 365 -out "$CORE_TRUST_ROOT/core-client.crt" -extfile "$tmp_dir/core.ext" >/dev/null 2>&1
  chmod 0600 "$CORE_TRUST_ROOT/core-client.key"
  chmod 0644 "$CORE_TRUST_ROOT/core-client.crt"
fi

if [[ ! -f "$NODE_TRUST_ROOT/node.key" ]]; then
  openssl genrsa -out "$NODE_TRUST_ROOT/node.key" 3072 >/dev/null 2>&1
  chmod 0600 "$NODE_TRUST_ROOT/node.key"
fi
if [[ ! -f "$NODE_TRUST_ROOT/node.crt" ]]; then
  tmp_dir="$(mktemp -d)"
  trap 'rm -rf "$tmp_dir"' EXIT
  openssl req -new -key "$NODE_TRUST_ROOT/node.key" -out "$tmp_dir/node.csr" -subj "/CN=$NODE_ID" >/dev/null 2>&1
  cat >"$tmp_dir/node.ext" <<EOF
basicConstraints=critical,CA:FALSE
keyUsage=critical,digitalSignature,keyEncipherment
extendedKeyUsage=serverAuth,clientAuth
subjectAltName=DNS:$NODE_ID,IP:127.0.0.1
subjectKeyIdentifier=hash
authorityKeyIdentifier=keyid,issuer
EOF
  openssl x509 -req -in "$tmp_dir/node.csr" -CA "$CORE_TRUST_ROOT/ca.crt" -CAkey "$CORE_TRUST_ROOT/ca.key" -CAcreateserial -days 7 -out "$NODE_TRUST_ROOT/node.crt" -extfile "$tmp_dir/node.ext" >/dev/null 2>&1
  cp "$tmp_dir/node.csr" "$NODE_TRUST_ROOT/node.csr"
  chmod 0600 "$NODE_TRUST_ROOT/node.csr"
  chmod 0644 "$NODE_TRUST_ROOT/node.crt"
fi

if [[ ! -f "$CORE_TRUST_ROOT/bootstrap-signing-key.pem" || ! -f "$CORE_TRUST_ROOT/bootstrap-signing-public.pem" ]]; then
  openssl genpkey -algorithm ED25519 -out "$CORE_TRUST_ROOT/bootstrap-signing-key.pem" >/dev/null 2>&1
  openssl pkey -in "$CORE_TRUST_ROOT/bootstrap-signing-key.pem" -pubout -out "$CORE_TRUST_ROOT/bootstrap-signing-public.pem" >/dev/null 2>&1
  chmod 0600 "$CORE_TRUST_ROOT/bootstrap-signing-key.pem"
  chmod 0644 "$CORE_TRUST_ROOT/bootstrap-signing-public.pem"
fi

cp "$CORE_TRUST_ROOT/ca.crt" "$NODE_TRUST_ROOT/ca.crt"
cp "$CORE_TRUST_ROOT/bootstrap-signing-public.pem" "$NODE_TRUST_ROOT/bootstrap-signing-public.pem"
chmod 0644 "$NODE_TRUST_ROOT/ca.crt" "$NODE_TRUST_ROOT/bootstrap-signing-public.pem"
rm -f "$CORE_TRUST_ROOT"/*.srl "$NODE_TRUST_ROOT"/*.srl
echo "Atlas PRIME trust material provisioned for canonical Node $NODE_ID; secret values were not displayed."
