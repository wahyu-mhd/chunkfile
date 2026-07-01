from app.config import Settings, get_settings


class StorageConfigError(RuntimeError):
    pass


class B2Storage:
    def __init__(self, settings: Settings | None = None):
        self.settings = settings or get_settings()

    def upload_bytes(self, object_key: str, data: bytes) -> None:
        ...

    def download_bytes(self, object_key: str) -> bytes:
        ...

    def delete_object(self, object_key: str) -> None:
        ...
