import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.database import get_db
from src.models import Base, User
from src.schemas import UserCreate
from src.services.user import UserService


@pytest.fixture(scope="module")
def test_db():
    engine = create_engine("sqlite:///:memory:")  # Use in-memory SQLite for testing
    Base.metadata.create_all(engine)
    connection = engine.connect()
    transaction = connection.begin()
    yield sessionmaker(bind=engine)()
    transaction.rollback()
    connection.close()


def test_create_user(test_db):
    user_service = UserService(test_db)
    user_data = UserCreate(email="test@example.com", password="password")
    user = user_service.create(user_data)
    assert user.email == "test@example.com"
    assert user.hashed_password is not None
