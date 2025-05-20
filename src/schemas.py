from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import datetime
from typing import Optional
from .models import ReminderType


class UserBase(BaseModel):
    """Base user schema."""

    email: EmailStr


class UserCreate(UserBase):
    """Schema for creating a new user."""

    password: str


class UserUpdate(UserBase):
    """Schema for updating a user."""

    password: Optional[str] = None


class User(UserBase):
    """Schema for user response."""

    id: int
    is_active: bool

    model_config = ConfigDict(from_attributes=True)


class ReminderBase(BaseModel):
    """Base reminder schema."""

    title: str
    description: Optional[str] = None
    due_date: datetime
    reminder_type: ReminderType


class ReminderCreate(ReminderBase):
    """Schema for creating a new reminder."""

    pass


class ReminderUpdate(ReminderBase):
    """Schema for updating a reminder."""

    title: Optional[str] = None
    due_date: Optional[datetime] = None
    reminder_type: Optional[ReminderType] = None


class Reminder(ReminderBase):
    """Schema for reminder response."""

    id: int
    is_completed: bool
    created_at: datetime
    user_id: int

    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    """Schema for authentication token."""

    access_token: str
    token_type: str


class TokenData(BaseModel):
    """Schema for token data."""

    email: Optional[str] = None
