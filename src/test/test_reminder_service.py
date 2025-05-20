import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.models import Base, User
from src.schemas import ReminderCreate
from src.services.reminder import ReminderService


@pytest.fixture(scope="module")
def test_db():
    engine = create_engine("sqlite:///:memory:")  # Use in-memory SQLite for testing
    Base.metadata.create_all(engine)
    connection = engine.connect()
    transaction = connection.begin()
    yield sessionmaker(bind=engine)()
    transaction.rollback()
    connection.close()


def test_create_reminder(test_db):
    user = User(email="test@example.com", hashed_password="hashed_password")
    test_db.add(user)
    test_db.commit()

    reminder_service = ReminderService(test_db, user)
    reminder_data = ReminderCreate(
        title="Test Reminder",
        description="Test Description",
        due_date="2023-12-31T12:00:00",
        reminder_type="ONE_TIME",
    )
    reminder = reminder_service.create(reminder_data)
    assert reminder.title == "Test Reminder"
    assert reminder.description == "Test Description"
