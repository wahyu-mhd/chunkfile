from typing import Any


def derive_aes_key(secret: str) -> bytes:
    ...


def encrypt_chunk(plaintext: bytes, secret: str) -> tuple[bytes, str]:
    ...


def decrypt_chunk(ciphertext: bytes, nonce: str, secret: str) -> bytes:
    ...


def hash_password(password: str) -> str:
    ...


def verify_password(password: str, stored_hash: str) -> bool:
    ...


def create_session_token(
    user_id: int,
    username: str,
    secret: str,
    ttl_seconds: int,
) -> str:
    ...


def decode_session_token(token: str, secret: str) -> dict[str, Any] | None:
    ...
