from uuid import UUID


def build_chunk_object_key(
    user_id: UUID,
    file_id: UUID,
    chunk_index: int,
) -> str:
    return (
        f"users/{user_id}/files/{file_id}/chunks/"
        f"{chunk_index:08d}.bin"
    )