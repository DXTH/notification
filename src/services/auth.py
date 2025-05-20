from datetime import datetime, timedelta
from typing import Optional
from jose import jwt
from ..config import get_settings
from .user import UserService

settings = get_settings()


class AuthService:
    """Service for handling authentication operations."""

    def __init__(self, user_service: UserService):
        self.user_service = user_service

    def create_access_token(self, data: dict) -> str:
        """Create a new JWT access token."""
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

    def authenticate_user(self, email: str, password: str) -> Optional[str]:
        """Authenticate a user and return an access token."""
        user = self.user_service.authenticate(email, password)
        if not user:
            return None
        return self.create_access_token(data={"sub": user.email})
