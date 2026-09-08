# P Streaming Backend

FastAPI backend for user/admin authentication and user profiles.

## Structure

```text
Backend/
|- main.py
|- database.py
|- models.py
|- schema.py
|- auth.py
|- Crud/
|  |- all.py       # Operations shared by users and admins
|  |- user.py      # User-only operations, including profiles
|  `- admin.py     # Admin-only operations
`- endpoints/
   |- user.py      # User endpoints
   `- admin.py      # Admin endpoints
```

## Rules

- A new user is checked against both `users` and `admin` before creation.
- A new admin is checked against both `users` and `admin` before creation.
- `userId`, `username`, and `email` are treated as globally unique across the two account tables.
- User endpoints are kept in `endpoints/user.py`.
- Admin endpoints are kept in `endpoints/admin.py`.
- Shared CRUD operations are kept in `Crud/all.py`.
- User-specific CRUD operations are kept in `Crud/user.py`.
- Admin-specific CRUD operations are kept in `Crud/admin.py`.
- A user can create multiple profiles.
- The same user cannot create two profiles with the same `profile_name`.
- Profile names may be reused by different users.
- Admins do not have profiles in this implementation.

## Endpoints

| Method | Path | Purpose |
| --- | --- | --- |
| GET | `/` | Health check |
| POST | `/signup` | Create a user |
| POST | `/login` | User login |
| POST | `/logout` | User logout |
| POST | `/admin/signup` | Create an admin |
| POST | `/users/{user_id}/profiles` | Create a profile for a user |
| GET | `/users/{user_id}/profiles` | Get all profiles for a user |
