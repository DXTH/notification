from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from . import models
from .config import get_settings
from .database import get_db
from .schemas import (
    Reminder,
    ReminderCreate,
    ReminderUpdate,
    Token,
    User,
    UserCreate,
)
from .services.auth import AuthService
from .services.reminder import ReminderService
from .services.user import UserService

settings = get_settings()

# Create database tables
models.Base.metadata.create_all(bind=models.engine)

app = FastAPI(title="Reminder API", version="1.0.0")

# Security
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> models.User:
    """Get the current authenticated user."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user_service = UserService(db)
    user = user_service.get_by_email(email)
    if user is None:
        raise credentials_exception
    return user


# User endpoints
@app.post("/users/", response_model=User)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """Create a new user."""
    user_service = UserService(db)
    return user_service.create(user)


@app.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    """Login and get access token."""
    user_service = UserService(db)
    auth_service = AuthService(user_service)

    token = auth_service.authenticate_user(form_data.username, form_data.password)
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return {"access_token": token, "token_type": "bearer"}


# Reminder endpoints
@app.post("/reminders/", response_model=Reminder)
def create_reminder(
    reminder: ReminderCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    """Create a new reminder."""
    reminder_service = ReminderService(db, current_user)
    return reminder_service.create(reminder)


@app.get("/reminders/", response_model=list[Reminder])
def read_reminders(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    """Get all reminders for the current user."""
    reminder_service = ReminderService(db, current_user)
    return reminder_service.get_all(skip, limit)


@app.get("/reminders/{reminder_id}", response_model=Reminder)
def read_reminder(
    reminder_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    """Get a specific reminder."""
    reminder_service = ReminderService(db, current_user)
    reminder = reminder_service.get(reminder_id)
    if not reminder:
        raise HTTPException(status_code=404, detail="Reminder not found")
    return reminder


@app.put("/reminders/{reminder_id}", response_model=Reminder)
def update_reminder(
    reminder_id: int,
    reminder: ReminderUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    """Update a reminder."""
    reminder_service = ReminderService(db, current_user)
    updated_reminder = reminder_service.update(reminder_id, reminder)
    if not updated_reminder:
        raise HTTPException(status_code=404, detail="Reminder not found")
    return updated_reminder


@app.delete("/reminders/{reminder_id}")
def delete_reminder(
    reminder_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    """Delete a reminder."""
    reminder_service = ReminderService(db, current_user)
    if not reminder_service.delete(reminder_id):
        raise HTTPException(status_code=404, detail="Reminder not found")
    return {"message": "Reminder deleted successfully"}
