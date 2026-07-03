from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "ChunkVault"
    app_env: str = "development"

    database_url: str = "postgresql+psycopg://chunkvault_user:chunkvault_password@localhost:5432/chunkvault"

    chunk_size_mb: int = 4
    max_upload_mb: int = 250

    b2_endpoint_url: str = "replace_later"
    b2_region: str = "replace_later"
    b2_bucket: str = "replace_later"
    b2_key_id: str = "replace_later"
    b2_application_key: str = "replace_later"

    master_encryption_key_base64: str
    jwt_secret_key: str = "change_this_secret"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )


settings = Settings()