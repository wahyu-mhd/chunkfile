import uuid

from app.core.object_keys import build_chunk_object_key


def test_build_chunk_object_key():
    user_id = uuid.UUID("11111111-1111-1111-1111-111111111111")
    file_id = uuid.UUID("22222222-2222-2222-2222-222222222222")

    key = build_chunk_object_key(
        user_id=user_id,
        file_id=file_id,
        chunk_index=7,
    )

    assert key == (
        "users/11111111-1111-1111-1111-111111111111/"
        "files/22222222-2222-2222-2222-222222222222/"
        "chunks/00000007.bin"
    )