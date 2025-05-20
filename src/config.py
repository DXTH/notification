"""Configuration settings for the application.

This module provides configuration settings using Pydantic settings management.
It includes database connection, security settings, and token expiration.
"""

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings configuration.

    Attributes:
        DATABASE_URL: PostgreSQL database connection string
        SECRET_KEY: Secret key for JWT token encryption
        ALGORITHM: Algorithm used for JWT token encryption
        ACCESS_TOKEN_EXPIRE_MINUTES: Token expiration time in minutes
    """

    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    model_config = SettingsConfigDict(env_file=".env")


@lru_cache
def get_settings() -> Settings:
    """Get cached application settings.

    Returns:
        Settings: Application settings instance
    """
    return Settings()
