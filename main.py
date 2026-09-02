from contextlib import asynccontextmanager

from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from sqlalchemy.orm import Session

from database import engine, get_db, Base
from schema import UserCreate, UserLogin, UserLogout
from models import User
from auth import hash_password, verify_password
import crud


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("FastAPI application is starting...")

    try:
        # Test database connection
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1")).scalar()

            if result == 1:
                print("Successfully connected to SQL Server!")

    except Exception as e:
        print(f"Database connection failed: {e}")
        raise

    yield

    # =========================
    # SHUTDOWN
    # =========================

    print("FastAPI application is shutting down...")
    engine.dispose()
    print("Database connection pool closed.")

Base.metadata.create_all(bind=engine)
app = FastAPI(lifespan=lifespan)

# Allow the local Vite frontend to complete JSON preflight and auth requests.
app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=r"https?://(localhost|127\.0\.0\.1)(:\d+)?$",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =========================
# HOME
# =========================

@app.get("/")
def home():
    return { "message": "FastAPI is running"}


# =========================
# SIGNUP
# =========================

@app.post("/signup")
def signup(user: UserCreate, db: Session = Depends(get_db)):

    # Check userId
    existing_user = crud.get_user_by_user_id(db, user.userId)

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="User already exists"
        )

    # Check email
    existing_email = crud.get_user_by_email(db, user.email)

    if existing_email:
        raise HTTPException(
            status_code=400,
            detail="Email already exists"
        )

    # Hash password
    hashed_password = hash_password(user.password)

    # Create user object
    new_user = User(
        userId=user.userId,
        username=user.username,
        email=user.email,
        password=hashed_password
    )

    # Save user
    crud.create_user(db, new_user)

    return {
        "message": "User created successfully",
        "userId": new_user.userId,
        "username": new_user.username,
        "email": new_user.email
    }


# =========================
# LOGIN
# =========================
@app.post("/login")
def login(user: UserLogin,db: Session = Depends(get_db)):

    # Find user by userId
    if user.userId is not None:
        db_user = crud.get_user_by_user_id(db,user.userId)

    # Find user by email
    else:
        db_user = crud.get_user_by_email(db,user.email)

    # Check user
    if db_user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid userId/email or password"
        )

    # Verify password
    password_valid = verify_password(user.password,db_user.password)

    if not password_valid:
        raise HTTPException(
            status_code=401,
            detail="Invalid userId/email or password"
        )
    
    session = crud.create_session(db,db_user.userId)

    return {
        "message": "Login successful",
        "session_id": session.id,
        "userId": db_user.userId,
        "username": db_user.username,
        "email": db_user.email
    }

# =========================
# LOGOUT
# =========================
@app.post("/logout")
def logout(logout_data: UserLogout,db: Session = Depends(get_db)):

    session = crud.logout_session(db,logout_data.session_id)

    if session is None:
        raise HTTPException(
            status_code=404,
            detail="Active session not found"
        )

    return {
        "message": "Logout successful",
        "session_id": session.id,
        "logout_time": session.logout_time
    }