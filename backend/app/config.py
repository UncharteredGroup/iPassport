"""Runtime configuration loaded from environment / backend/.env."""

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    mock_mode: bool = True
    evidence_dir: str = ".evidence"
    package_signing_key: str = "change-me-in-production"
    data_retention_hours: int = 24
    cors_origins: str = "http://localhost:5173"

    meta_api_key: str = ""
    meta_api_base: str = "https://api.meta.com/v1"
    meta_agent_model: str = "muse-spark"
    meta_vision_model: str = "sam-3.1"
    meta_image_model: str = "muse-image"


@lru_cache
def get_settings() -> Settings:
    return Settings()
