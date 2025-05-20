# Reminder API

A FastAPI-based backend for an iPhone reminder application. This API provides endpoints for managing reminders and user authentication.

## Features

- User authentication with JWT tokens
- CRUD operations for reminders
- Support for different types of reminders (one-time, daily, weekly, monthly)
- PostgreSQL database integration
- FastAPI with automatic API documentation

## Prerequisites

- Python 3.13.3
- Poetry (Python package manager)
- PostgreSQL database

## Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd reminder-api
```

2. Install dependencies using Poetry:
```bash
poetry install
```

3. Create a PostgreSQL database named `reminder_db`

4. Create a `.env` file in the root directory with the following content:
```
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/reminder_db
SECRET_KEY=your-secret-key-here
```

5. Start the application:
```bash
poetry run start
```

The API will be available at `http://localhost:8000`

## API Documentation

Once the server is running, you can access:
- Interactive API documentation (Swagger UI): `http://localhost:8000/docs`
- Alternative API documentation (ReDoc): `http://localhost:8000/redoc`

## API Endpoints

### Authentication
- `POST /users/` - Create a new user
- `POST /token` - Login and get access token

### Reminders
- `POST /reminders/` - Create a new reminder
- `GET /reminders/` - List all reminders
- `GET /reminders/{reminder_id}` - Get a specific reminder
- `PUT /reminders/{reminder_id}` - Update a reminder
- `DELETE /reminders/{reminder_id}` - Delete a reminder

## Security

- All endpoints except user creation and login require authentication
- Passwords are hashed using bcrypt
- JWT tokens are used for authentication
- Each user can only access their own reminders

## Development

To run the development server with auto-reload:
```bash
poetry run start
``` 