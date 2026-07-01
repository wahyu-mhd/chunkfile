from pathlib import Path


class Settings:
    app_title = "ChunkVault"
    database_url = "sqlite:///./data/chunkvault.db"
    staging_dir = Path("./data/staging")
    restore_dir = Path("./data/temp_restore")
    chunk_size = 1024 * 1024
    max_upload_bytes = 1024 * 1024 * 1024

    def ensure_dirs(self) -> None:
        ...


def get_settings() -> Settings:
    return Settings()
