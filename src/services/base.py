from abc import ABC, abstractmethod
from typing import Generic, TypeVar, List, Optional
from sqlalchemy.orm import Session
from pydantic import BaseModel

T = TypeVar("T")
CreateSchema = TypeVar("CreateSchema", bound=BaseModel)
UpdateSchema = TypeVar("UpdateSchema", bound=BaseModel)


class BaseService(Generic[T, CreateSchema, UpdateSchema], ABC):
    """Abstract base class for all services."""

    def __init__(self, db: Session):
        self.db = db

    @abstractmethod
    def create(self, obj_in: CreateSchema) -> T:
        """Create a new object."""
        pass

    @abstractmethod
    def get(self, id: int) -> Optional[T]:
        """Get an object by ID."""
        pass

    @abstractmethod
    def get_all(self, skip: int = 0, limit: int = 100) -> List[T]:
        """Get all objects with pagination."""
        pass

    @abstractmethod
    def update(self, id: int, obj_in: UpdateSchema) -> Optional[T]:
        """Update an object."""
        pass

    @abstractmethod
    def delete(self, id: int) -> bool:
        """Delete an object."""
        pass
