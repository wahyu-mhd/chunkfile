class UploadLimitError(ValueError):
    pass


def validate_upload_size(size_bytes: int, max_upload_bytes: int) -> None:
    ...
