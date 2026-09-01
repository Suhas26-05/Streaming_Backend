# P Streaming Backend

FastAPI service for P Streaming authentication. It validates signup and login requests, stores users through SQLAlchemy, and returns the authenticated user's basic profile details.

## Features

- User signup with unique user ID and email checks.
- Secure password hashing before user records are stored.
- Login with either a user ID or email address.
- Password verification for existing users.
- Pydantic request validation for authentication payloads.
- SQLAlchemy database access and a managed database connection lifecycle.
- Local CORS support for the Vite frontend.

## Technology

- Python
- FastAPI
- SQLAlchemy
- Pydantic
- Passlib and bcrypt
- pyodbc for SQL Server connectivity

## Prerequisites

- Python 3.10 or later
- A SQL Server instance and the connection configuration required by `database.py`
- The SQL Server ODBC driver required by pyodbc

## Run locally

Install the Python dependencies, configure the database connection expected by `database.py`, then start the API from this repository:

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

The service runs at `http://127.0.0.1:8000` by default. Local CORS support is configured for Vite frontend origins on `localhost` and `127.0.0.1`.

## API reference

| Method | Path | Request body | Result |
| --- | --- | --- | --- |
| `GET` | `/` | None | Confirms the service is running. |
| `POST` | `/signup` | `userId`, `username`, `email`, `password` | Creates a user and returns basic profile details. |
| `POST` | `/login` | Exactly one of `userId` or `email`, plus `password` | Verifies credentials and returns basic profile details. |

### Example signup request

```json
{
  "userId": "jane_01",
  "username": "Jane Doe",
  "email": "jane@example.com",
  "password": "secure-password"
}
```

### Example login request

```json
{
  "email": "jane@example.com",
  "password": "secure-password"
}
```

## This repository's structure

```text
Backend/
|- main.py                    # FastAPI app, CORS middleware, and auth routes
|- database.py                # SQLAlchemy engine, session, and base model setup
|- models.py                  # User database model
|- schema.py                  # Pydantic request validation schemas
|- crud.py                    # User lookup and creation database operations
|- auth.py                    # Password hashing and password verification
`- requirements.txt           # Python runtime dependencies
```

## Frontend reference structure

The following is a documentation-only reference to the companion frontend repository. The frontend code is maintained, versioned, and pushed in its own `Frontend` repository; do not add or edit frontend source files in this backend repository.

```text
Frontend/
|- index.html                 # Vite HTML entry point and font loading
|- package.json               # React, Axios, and Vite dependencies/scripts
|- package-lock.json          # Locked npm dependency versions
|- vite.config.js             # Vite development configuration
`- src/
   |- main.jsx                # React application mount point
   |- App.jsx                 # Login, signup, validation, and session UI
   |- api.js                  # Axios client and auth API requests
   `- styles.css              # Responsive visual design and layout rules
```

## API endpoints

- `GET /` confirms that the FastAPI service is running.
- `POST /signup` accepts `userId`, `username`, `email`, and `password`.
- `POST /login` accepts exactly one identifier, `userId` or `email`, with `password`.

## Development notes

- The database schema is created through `Base.metadata.create_all(bind=engine)` when the application module loads.
- Passwords are hashed and never returned in API responses.
- The current API returns user profile details after successful authentication; it does not yet issue access or refresh tokens.
- This project intentionally contains only backend source code and backend dependencies.
