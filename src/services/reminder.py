from typing import Optional, List
from sqlalchemy.orm import Session
from ..models import Reminder, User
from ..schemas import ReminderCreate, ReminderUpdate
from .base import BaseService


class ReminderService(BaseService[Reminder, ReminderCreate, ReminderUpdate]):
    """Service for handling reminder operations."""

    def __init__(self, db: Session, user: User):
        super().__init__(db)
        self.user = user

    def create(self, reminder_in: ReminderCreate) -> Reminder:
        """Create a new reminder."""
        db_reminder = Reminder(**reminder_in.model_dump(), user_id=self.user.id)
        self.db.add(db_reminder)
        self.db.commit()
        self.db.refresh(db_reminder)
        return db_reminder

    def get(self, id: int) -> Optional[Reminder]:
        """Get a reminder by ID."""
        return (
            self.db.query(Reminder)
            .filter(Reminder.id == id, Reminder.user_id == self.user.id)
            .first()
        )

    def get_all(self, skip: int = 0, limit: int = 100) -> List[Reminder]:
        """Get all reminders for the current user with pagination."""
        return (
            self.db.query(Reminder)
            .filter(Reminder.user_id == self.user.id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def update(self, id: int, reminder_in: ReminderUpdate) -> Optional[Reminder]:
        """Update a reminder."""
        db_reminder = self.get(id)
        if not db_reminder:
            return None

        update_data = reminder_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_reminder, field, value)

        self.db.commit()
        self.db.refresh(db_reminder)
        return db_reminder

    def delete(self, id: int) -> bool:
        """Delete a reminder."""
        db_reminder = self.get(id)
        if not db_reminder:
            return False

        self.db.delete(db_reminder)
        self.db.commit()
        return True

    def get_upcoming(self, limit: int = 10) -> List[Reminder]:
        """Get upcoming reminders for the current user."""
        return (
            self.db.query(Reminder)
            .filter(Reminder.user_id == self.user.id, Reminder.is_completed == False)
            .order_by(Reminder.due_date.asc())
            .limit(limit)
            .all()
        )
