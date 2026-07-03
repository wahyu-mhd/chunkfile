from pathlib import Path
from typing import Iterator



def iter_file_chunks(file_path: str | Path, chunk_size_bytes: int ) -> Iterator[bytes]:
    path = Path(file_path)

    with path.open("rb") as file:
        chunk_index = 0

        while True:
            chunk = file.read(chunk_size_bytes)

            if not chunk:
                break

            yield chunk_index, chunk
            chunk_index += 1


def rebuild_file_from_chunks(
    chunks: list[bytes],
    output_path: str | Path,
) -> None:
    path = Path(output_path)

    with path.open("wb") as output_file:
        for chunk in chunks:
            output_file.write(chunk)
