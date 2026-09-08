from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from auth import hash_password, verify_password
from database import get_db
from models import Admin, Profile, User
from schema import ProfileCreate, ProfileUpdate, ProfileSelect, UserCreate, UserLogin, UserLogout
import Crud.all as all_crud
import Crud.user as user_crud
import Crud.admin as admin_crud

router = APIRouter()

@router.post("/signup")
def signup(user: UserCreate, db: Session = Depends(get_db)):
    # userId, email and username must be unique across BOTH tables.
    if all_crud.get_user_by_user_id(db, user.userId):
        raise HTTPException(status_code=400, detail="User ID already exists")

    if all_crud.get_user_by_email(db, user.email):
        raise HTTPException(status_code=400, detail="Email already exists")

    new_user = User(
        userId=user.userId,
        username=user.username,
        email=user.email,
        password=hash_password(user.password),
    )

    try:
        return all_crud.create_user(db, new_user)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="User already exists")

@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    # Look across BOTH tables (users + admin), same as signup's uniqueness check.
    if user.userId is not None:
        db_user = all_crud.get_user_by_user_id(db, user.userId)
    else:
        db_user = all_crud.get_user_by_email(db, user.email)

    if db_user is None or not verify_password(user.password, db_user.password):
        raise HTTPException(
            status_code=401,
            detail="Invalid userId/email or password",
        )

    # Admin accounts have no profiles -> log them straight into an admin session.
    if isinstance(db_user, Admin):
        session = admin_crud.create_admin_session(db, db_user.userId)   # <-- CALL SITE (line 53)
        return {
            "message": "Admin login successful.",
            "userId": db_user.userId,
            "username": db_user.username,
            "email": db_user.email,
            "session_id": session.id,
        }

    # Regular users still pick a profile afterwards to create a UserSession.
    profiles = user_crud.get_user_profiles(db, db_user.userId)

    return {
        "message": "Login successful. Select a profile to create a session.",
        "userId": db_user.userId,
        "username": db_user.username,
        "email": db_user.email,
        "profiles": [
            {
                "id": profile.id,
                "profile_name": profile.profile_name,
                "profile_pic": profile.profile_pic,
            }
            for profile in profiles
        ],
    }