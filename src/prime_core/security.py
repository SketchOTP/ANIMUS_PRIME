from __future__ import annotations

import base64
import hashlib
import hmac
import secrets


def new_token() -> str:
    return secrets.token_urlsafe(32)


def token_digest(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def password_hash(password: str, salt: bytes | None = None) -> str:
    salt = salt or secrets.token_bytes(16)
    derived = hashlib.scrypt(
        password.encode("utf-8"), salt=salt, n=2**14, r=8, p=1, dklen=32
    )
    return "scrypt$16384$8$1$" + base64.urlsafe_b64encode(salt + derived).decode()


def password_verify(password: str, encoded: str) -> bool:
    try:
        prefix, encoded_value = encoded.rsplit("$", 1)
        if prefix != "scrypt$16384$8$1":
            return False
        raw = base64.urlsafe_b64decode(encoded_value.encode())
        salt, expected = raw[:16], raw[16:]
        actual = hashlib.scrypt(
            password.encode("utf-8"), salt=salt, n=2**14, r=8, p=1, dklen=32
        )
        return hmac.compare_digest(actual, expected)
    except (ValueError, TypeError):
        return False


def constant_time_equal(left: str, right: str) -> bool:
    return hmac.compare_digest(left.encode(), right.encode())

