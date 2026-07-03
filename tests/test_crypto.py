import pytest

from app.core.crypto import decrypt_chunk, encrypt_chunk, load_master_key


def test_encrypt_then_decrypt_chunk():
    key = load_master_key()
    plaintext = b"this is secret data"

    encrypted = encrypt_chunk(plaintext, key)
    decrypted = decrypt_chunk(encrypted.ciphertext, encrypted.nonce, key)

    assert decrypted == plaintext
    assert encrypted.ciphertext != plaintext
    assert len(encrypted.nonce) == 12


def test_decrypt_fails_if_ciphertext_modified():
    key = load_master_key()
    plaintext = b"important data"

    encrypted = encrypt_chunk(plaintext, key)

    modified_ciphertext = encrypted.ciphertext[:-1] + b"0"

    with pytest.raises(Exception):
        decrypt_chunk(modified_ciphertext, encrypted.nonce, key)