from datetime import datetime, timedelta, timezone
from ipaddress import ip_address
from pathlib import Path

import pytest
from cryptography import x509
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.x509.oid import NameOID

from src.prime_core.node_trust import NodeTrustSettings, sign_node_certificate


def trust_fixture(tmp_path: Path) -> tuple[NodeTrustSettings, str]:
    ca_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    name = x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, "PRIME test CA")])
    now = datetime.now(timezone.utc)
    ca_cert = (
        x509.CertificateBuilder()
        .subject_name(name)
        .issuer_name(name)
        .public_key(ca_key.public_key())
        .serial_number(x509.random_serial_number())
        .not_valid_before(now - timedelta(minutes=1))
        .not_valid_after(now + timedelta(days=30))
        .add_extension(x509.BasicConstraints(ca=True, path_length=None), critical=True)
        .sign(ca_key, hashes.SHA256())
    )
    settings = NodeTrustSettings(
        tmp_path / "ca.crt",
        tmp_path / "ca.key",
        tmp_path / "bootstrap.key",
        tmp_path / "bootstrap.pub",
        tmp_path / "core.crt",
        tmp_path / "core.key",
        tmp_path / "credentials",
    )
    settings.ca_certificate.write_bytes(ca_cert.public_bytes(serialization.Encoding.PEM))
    settings.ca_private_key.write_bytes(
        ca_key.private_bytes(
            serialization.Encoding.PEM,
            serialization.PrivateFormat.PKCS8,
            serialization.NoEncryption(),
        )
    )
    node_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    csr = (
        x509.CertificateSigningRequestBuilder()
        .subject_name(x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, "node-windows")]))
        .sign(node_key, hashes.SHA256())
    )
    return settings, csr.public_bytes(serialization.Encoding.PEM).decode("ascii")


def test_final_node_certificate_covers_approved_lan_endpoint(tmp_path: Path) -> None:
    settings, csr_pem = trust_fixture(tmp_path)
    pem, metadata = sign_node_certificate(
        settings,
        csr_pem,
        "node-windows",
        control_endpoint="https://192.168.254.5:18001",
    )
    cert = x509.load_pem_x509_certificate(pem.encode("ascii"))
    sans = cert.extensions.get_extension_for_class(x509.SubjectAlternativeName).value
    assert ip_address("192.168.254.5") in sans.get_values_for_type(x509.IPAddress)
    assert ip_address("127.0.0.1") in sans.get_values_for_type(x509.IPAddress)
    assert "node-windows" in sans.get_values_for_type(x509.DNSName)
    assert metadata["control_endpoint_host"] == "192.168.254.5"


@pytest.mark.parametrize(
    "endpoint",
    ["http://192.168.254.5:18001", "https://user@example.test:18001", "https://*.example.test:18001"],
)
def test_final_node_certificate_refuses_unsafe_endpoint_identity(tmp_path: Path, endpoint: str) -> None:
    settings, csr_pem = trust_fixture(tmp_path)
    with pytest.raises(ValueError):
        sign_node_certificate(settings, csr_pem, "node-windows", control_endpoint=endpoint)
