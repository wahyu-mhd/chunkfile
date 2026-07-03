from app.core.hasher import sha256_bytes, sha256_file


def test_sha256_bytes_same_input_same_hash():
    data = b"hello world"

    hash_one = sha256_bytes(data)
    hash_two = sha256_bytes(data)

    assert hash_one == hash_two
    assert len(hash_one) == 64


def test_sha256_file(tmp_path):
    file_path = tmp_path / "sample.txt"
    file_path.write_bytes(b"ChunkVault test file")

    file_hash = sha256_file(file_path)

    assert len(file_hash) == 64