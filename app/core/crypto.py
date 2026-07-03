import base64
import os
from dataclasses import dataclass

from cryptography.hazmat.primitives.ciphers.aead import AESGCM

from app.config import settings


@dataclass
class EncryptedChunk:
    nonce: bytes
    ciphertext: bytes


def load_master_key() -> bytes:
    key = base64.b64decode(settings.master_encryption_key_base64)

    if len(key) != 32:
        raise ValueError("MASTER_ENCRYPTION_KEY_BASE64 must decode to 32 bytes")

    return key


def encrypt_chunk(plaintext: bytes, key: bytes) -> EncryptedChunk:
    nonce = os.urandom(12)
    aesgcm = AESGCM(key)

    ciphertext = aesgcm.encrypt(
        nonce=nonce,
        data=plaintext,
        associated_data=None,
    )

    return EncryptedChunk(
        nonce=nonce,
        ciphertext=ciphertext,
    )


def decrypt_chunk(ciphertext: bytes, nonce: bytes, key: bytes) -> bytes:
    aesgcm = AESGCM(key)

    plaintext = aesgcm.decrypt(
        nonce=nonce,
        data=ciphertext,
        associated_data=None,
    )

    return plaintext