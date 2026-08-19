from __future__ import annotations

import base64
import hashlib
import ipaddress
import json
import os
import secrets
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

from cryptography import x509
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ed25519
from cryptography.x509.oid import ExtendedKeyUsageOID, NameOID


UTC = timezone.utc


@dataclass(frozen=True)
class NodeTrustSettings:
    ca_certificate: Path
    ca_private_key: Path
    bootstrap_signing_private_key: Path
    bootstrap_signing_public_key: Path
    core_client_certificate: Path
    core_client_private_key: Path
    credential_directory: Path

    @classmethod
    def from_environment(cls) -> "NodeTrustSettings":
        root = Path(os.getenv("PRIME_NODE_TRUST_ROOT", "/var/lib/animus-prime-core/trust"))
        return cls(
            ca_certificate=Path(os.getenv("PRIME_NODE_CA_FILE", str(root / "ca.crt"))),
            ca_private_key=Path(os.getenv("PRIME_NODE_CA_KEY_FILE", str(root / "ca.key"))),
            bootstrap_signing_private_key=Path(os.getenv("PRIME_NODE_BOOTSTRAP_SIGNING_KEY_FILE", str(root / "bootstrap-signing-key.pem"))),
            bootstrap_signing_public_key=Path(os.getenv("PRIME_NODE_BOOTSTRAP_SIGNING_PUBLIC_KEY_FILE", str(root / "bootstrap-signing-public.pem"))),
            core_client_certificate=Path(os.getenv("PRIME_NODE_CORE_CERT_FILE", str(root / "core-client.crt"))),
            core_client_private_key=Path(os.getenv("PRIME_NODE_CORE_KEY_FILE", str(root / "core-client.key"))),
            credential_directory=Path(os.getenv("PRIME_NODE_CREDENTIAL_DIRECTORY", str(root))),
        )


def _b64(value: bytes) -> str:
    return base64.urlsafe_b64encode(value).rstrip(b"=").decode("ascii")


def _unb64(value: str) -> bytes:
    return base64.urlsafe_b64decode(value + "=" * (-len(value) % 4))


def _canonical(payload: dict[str, Any]) -> bytes:
    return json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")


def digest(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def ensure_signing_key(settings: NodeTrustSettings) -> None:
    settings.bootstrap_signing_private_key.parent.mkdir(parents=True, exist_ok=True)
    if settings.bootstrap_signing_private_key.exists() and settings.bootstrap_signing_public_key.exists():
        return
    private = ed25519.Ed25519PrivateKey.generate()
    settings.bootstrap_signing_private_key.write_bytes(
        private.private_bytes(serialization.Encoding.PEM, serialization.PrivateFormat.PKCS8, serialization.NoEncryption())
    )
    os.chmod(settings.bootstrap_signing_private_key, 0o600)
    settings.bootstrap_signing_public_key.write_bytes(
        private.public_key().public_bytes(serialization.Encoding.PEM, serialization.PublicFormat.SubjectPublicKeyInfo)
    )
    os.chmod(settings.bootstrap_signing_public_key, 0o644)


def issue_bootstrap(settings: NodeTrustSettings, node_id: str, ttl_seconds: int = 300) -> tuple[str, dict[str, Any]]:
    ensure_signing_key(settings)
    now = datetime.now(UTC)
    payload = {
        "version": 1,
        "challenge_id": f"enroll_{secrets.token_hex(16)}",
        "node_id": node_id,
        "issued_at": now.isoformat(),
        "expires_at": (now + timedelta(seconds=ttl_seconds)).isoformat(),
        "nonce": secrets.token_hex(32),
    }
    private = serialization.load_pem_private_key(settings.bootstrap_signing_private_key.read_bytes(), password=None)
    if not isinstance(private, ed25519.Ed25519PrivateKey):
        raise ValueError("bootstrap signing key is not Ed25519")
    body = _b64(_canonical(payload))
    token = f"{body}.{_b64(private.sign(body.encode('ascii')))}"
    return token, payload


def verify_bootstrap(token: str, public_key_file: Path) -> dict[str, Any]:
    try:
        body, signature = token.split(".", 1)
        public = serialization.load_pem_public_key(public_key_file.read_bytes())
        if not isinstance(public, ed25519.Ed25519PublicKey):
            raise ValueError("bootstrap verification key is not Ed25519")
        public.verify(_unb64(signature), body.encode("ascii"))
        payload = json.loads(_unb64(body).decode("utf-8"))
    except (ValueError, TypeError, KeyError, json.JSONDecodeError) as exc:
        raise PermissionError("invalid node bootstrap proof") from exc
    expires_at = datetime.fromisoformat(payload["expires_at"])
    if expires_at <= datetime.now(UTC):
        raise PermissionError("node bootstrap proof expired")
    return payload


def csr_fingerprint(csr_pem: str) -> str:
    csr = x509.load_pem_x509_csr(csr_pem.encode("utf-8"))
    return hashlib.sha256(csr.public_bytes(serialization.Encoding.DER)).hexdigest()


def sign_node_certificate(
    settings: NodeTrustSettings,
    csr_pem: str,
    node_id: str,
    days: int = 30,
    control_endpoint: str | None = None,
) -> tuple[str, dict[str, Any]]:
    csr = x509.load_pem_x509_csr(csr_pem.encode("utf-8"))
    if not csr.is_signature_valid:
        raise ValueError("Node CSR signature is invalid")
    ca_cert = x509.load_pem_x509_certificate(settings.ca_certificate.read_bytes())
    ca_key = serialization.load_pem_private_key(settings.ca_private_key.read_bytes(), password=None)
    subject = x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, node_id)])
    now = datetime.now(UTC)
    subject_alt_names: list[x509.GeneralName] = [
        x509.UniformResourceIdentifier(f"spiffe://animus-prime/node/{node_id}"),
        x509.DNSName(node_id),
        x509.IPAddress(ipaddress.ip_address("127.0.0.1")),
    ]
    if control_endpoint:
        parsed = urlparse(control_endpoint)
        if parsed.scheme != "https" or not parsed.hostname or parsed.username or parsed.password:
            raise ValueError("Node control endpoint must be an authenticated HTTPS host")
        host = parsed.hostname
        try:
            endpoint_name: x509.GeneralName = x509.IPAddress(ipaddress.ip_address(host))
        except ValueError:
            if "*" in host or len(host) > 253:
                raise ValueError("Node control endpoint hostname is invalid")
            endpoint_name = x509.DNSName(host)
        if endpoint_name not in subject_alt_names:
            subject_alt_names.append(endpoint_name)
    certificate = (
        x509.CertificateBuilder()
        .subject_name(subject)
        .issuer_name(ca_cert.subject)
        .public_key(csr.public_key())
        .serial_number(x509.random_serial_number())
        .not_valid_before(now - timedelta(minutes=1))
        .not_valid_after(now + timedelta(days=days))
        .add_extension(x509.BasicConstraints(ca=False, path_length=None), critical=True)
        .add_extension(x509.SubjectKeyIdentifier.from_public_key(csr.public_key()), critical=False)
        .add_extension(x509.AuthorityKeyIdentifier.from_issuer_public_key(ca_key.public_key()), critical=False)
        .add_extension(x509.SubjectAlternativeName(subject_alt_names), critical=False)
        .add_extension(x509.ExtendedKeyUsage([ExtendedKeyUsageOID.SERVER_AUTH, ExtendedKeyUsageOID.CLIENT_AUTH]), critical=False)
        .sign(ca_key, hashes.SHA256())
    )
    pem = certificate.public_bytes(serialization.Encoding.PEM).decode("ascii")
    return pem, {
        "fingerprint": certificate.fingerprint(hashes.SHA256()).hex(),
        "serial": str(certificate.serial_number),
        "issued_at": now.isoformat(),
        "expires_at": certificate.not_valid_after_utc.isoformat(),
        "control_endpoint_host": urlparse(control_endpoint).hostname if control_endpoint else "127.0.0.1",
    }
