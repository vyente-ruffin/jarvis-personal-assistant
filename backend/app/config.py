"""Configuration management for JARVIS."""

from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # API Keys
    gemini_api_key: str = ""

    # Memory API (Mem0)
    mem0_api_url: str = "http://localhost:8765"
    mem0_api_key: str = ""

    # User Configuration
    user_id: str = "default_user"

    # Server Configuration
    host: str = "0.0.0.0"
    port: int = 8000
    debug: bool = False

    # Azure Monitoring
    applicationinsights_connection_string: str = ""

    # Audio Configuration
    input_device_name: str = ""
    output_device_name: str = ""

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
