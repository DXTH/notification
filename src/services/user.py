from typing import Optional
from sqlalchemy.orm import Session
from ..models import User
from ..schemas import UserCreate, UserUpdate
from .base import BaseService
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserService(BaseService[User, UserCreate, UserUpdate]):
    """Service for handling user operations."""

    def create(self, user_in: UserCreate) -> User:
        """Create a new user."""
        hashed_password = pwd_context.hash(user_in.password)
        db_user = User(email=user_in.email, hashed_password=hashed_password)
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def get(self, id: int) -> Optional[User]:
        """Get a user by ID."""
        return self.db.query(User).filter(User.id == id).first()

    def get_by_email(self, email: str) -> Optional[User]:
        """Get a user by email."""
        return self.db.query(User).filter(User.email == email).first()

    def get_all(self, skip: int = 0, limit: int = 100) -> list[User]:
        """Get all users with pagination."""
        return self.db.query(User).offset(skip).limit(limit).all()

    def update(self, id: int, user_in: UserUpdate) -> Optional[User]:
        """Update a user."""
        db_user = self.get(id)
        if not db_user:
            return None

        update_data = user_in.model_dump(exclude_unset=True)
        if "password" in update_data:
            update_data["hashed_password"] = pwd_context.hash(
                update_data.pop("password")
            )

        for field, value in update_data.items():
            setattr(db_user, field, value)

        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def delete(self, id: int) -> bool:
        """Delete a user."""
        db_user = self.get(id)
        if not db_user:
            return False

        self.db.delete(db_user)
        self.db.commit()
        return True

    def authenticate(self, email: str, password: str) -> Optional[User]:
        """Authenticate a user."""
        user = self.get_by_email(email)
        if not user:
            return None
        if not pwd_context.verify(password, user.hashed_password):
            return None
        return user
