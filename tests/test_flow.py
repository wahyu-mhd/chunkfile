from app.core.chunker import iter_file_chunks, rebuild_file_from_chunks
from app.core.crypto import decrypt_chunk, encrypt_chunk, load_master_key
from app.core.hasher import sha256_bytes, sha256_file


def test_full_chunk_encrypt_decrypt_rebuild_flow(tmp_path):
    key = load_master_key()

    original_path = tmp_path / "original.txt"
    rebuilt_path = tmp_path / "rebuilt.txt"

    original_content = (
        b"This is a ChunkVault test file. "
        b"It will be split, encrypted, decrypted, and rebuilt."
    )

    original_path.write_bytes(original_content)

    encrypted_records = []

    for chunk_index, plaintext_chunk in iter_file_chunks(
        original_path,
        chunk_size_bytes=16,
    ):
        encrypted = encrypt_chunk(plaintext_chunk, key)
        encrypted_hash = sha256_bytes(encrypted.ciphertext)

        encrypted_records.append(
            {
                "chunk_index": chunk_index,
                "nonce": encrypted.nonce,
                "ciphertext": encrypted.ciphertext,
                "sha256_encrypted": encrypted_hash,
            }
        )

    rebuilt_chunks = []

    for record in sorted(encrypted_records, key=lambda item: item["chunk_index"]):
        current_hash = sha256_bytes(record["ciphertext"])

        assert current_hash == record["sha256_encrypted"]

        plaintext = decrypt_chunk(
            ciphertext=record["ciphertext"],
            nonce=record["nonce"],
            key=key,
        )

        rebuilt_chunks.append(plaintext)

    rebuild_file_from_chunks(rebuilt_chunks, rebuilt_path)

    assert sha256_file(original_path) == sha256_file(rebuilt_path)
    assert rebuilt_path.read_bytes() == original_content