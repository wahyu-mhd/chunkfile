from app.core.chunker import iter_file_chunks, rebuild_file_from_chunks
from app.core.hasher import sha256_file


def test_iter_file_chunks_splits_file(tmp_path):
    file_path = tmp_path / "sample.bin"
    file_path.write_bytes(b"abcdefghij")

    chunks = list(iter_file_chunks(file_path, chunk_size_bytes=4))

    assert len(chunks) == 3
    assert chunks[0] == (0, b"abcd")
    assert chunks[1] == (1, b"efgh")
    assert chunks[2] == (2, b"ij")


def test_rebuild_file_from_chunks(tmp_path):
    original_path = tmp_path / "original.bin"
    rebuilt_path = tmp_path / "rebuilt.bin"

    original_path.write_bytes(b"hello this is a test file")

    chunks = [
        chunk_data
        for _, chunk_data in iter_file_chunks(original_path, chunk_size_bytes=5)
    ]

    rebuild_file_from_chunks(chunks, rebuilt_path)

    assert sha256_file(original_path) == sha256_file(rebuilt_path)