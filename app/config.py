from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "ChunkVault"
    app_env: str = "development"

    database_url: str = "postgresql+psycopg://chunkvault_user:chunkvault_password@localhost:5432/chunkvault"

    chunk_size_mb: int = 4
    max_upload_mb: int = 250
    max_chunks_per_file: int = 200
    uploads_per_minute: int = 5
    failed_login_limit: int = 5
    failed_login_window_seconds: int = 300

    b2_endpoint_url: str 
    b2_region: str 
    b2_bucket: str 
    b2_key_id: str 
    b2_application_key: str 

    master_encryption_key_base64: str
    jwt_secret_key: str = "change_this_secret"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )


settings = Settings()