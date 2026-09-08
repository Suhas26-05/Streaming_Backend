from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from auth import hash_password
from database import get_db
from models import Admin
from schema import UserCreate, UserLogout
import Crud.admin as admin_crud
import Crud.all as all_crud

router = APIRouter(prefix="/admin")


@router.post("/signup")
def admin_signup(user: UserCreate, db: Session = Depends(get_db)):
    # Admin userId, email and username must also be unique across BOTH tables.
    if all_crud.get_user_by_user_id(db, user.userId):
        raise HTTPException(status_code=400, detail="User ID already exists")

    if all_crud.get_user_by_email(db, user.email):
        raise HTTPException(status_code=400, detail="Email already exists")

    new_admin = Admin(
        userId=user.userId,
        username=user.username,
        email=user.email,
        password=hash_password(user.password),
    )

    try:
        return all_crud.create_user(db, new_admin)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Admin already exists")


@router.post("/logout")
def admin_logout(logout_data: UserLogout, db: Session = Depends(get_db)):
    session = admin_crud.logout_admin_session(db, logout_data.session_id)   # <-- CALL SITE

    if session is None:
        raise HTTPException(status_code=404, detail="Active admin session not found")

    return {"message": "Admin logout successful", "session_id": session.id, "logout_time": session.logout_time}