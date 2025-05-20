import os
from src.config import get_settings


def test_settings():
    settings = get_settings()
    assert (
        settings.DATABASE_URL
        == "postgresql://postgres:postgres@localhost:5432/reminder_db"
    )
    assert settings.SECRET_KEY == "your-secret-key-here"
    assert settings.ALGORITHM == "HS256"
    assert settings.ACCESS_TOKEN_EXPIRE_MINUTES == 30
