import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.models import Base
from src.schemas import UserCreate
from src.services.auth import AuthService
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


def test_authenticate_user(test_db):
    """Test user authentication and token generation."""
    user_service = UserService(test_db)
    user_data = UserCreate(email="test@example.com", password="password")
    user = user_service.create(user_data)

    auth_service = AuthService(user_service)
    token = auth_service.authenticate_user("test@example.com", "password")
    assert token is not None

    # Test with incorrect password
    invalid_token = auth_service.authenticate_user("test@example.com", "wrong_password")
    assert invalid_token is None

    # Test with non-existent user
    non_existent_token = auth_service.authenticate_user(
        "nonexistent@example.com", "password",
    )
    assert non_existent_token is None
