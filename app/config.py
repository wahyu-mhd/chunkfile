from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings:
    app_name = "ChunkVault"
    app_env = "development"
    database_url = "sqlite:///./data/chunkvault.db"
    b2_endpoint_url: str
    b2_region: str
    b2_bucket: str
    b2_key_id: str
    b2_application_key: str

    master_encryption_key_base64: str
    jwt_secret_key: str

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )
    chunk_size = 4* 1024 * 1024
    max_upload_bytes = 250 * 1024 * 1024

    def ensure_dirs(self) -> None:
        ...


def get_settings() -> Settings:
    return Settings()
