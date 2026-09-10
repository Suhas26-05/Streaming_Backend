from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from app.core.dependencies import get_db
from app.core.security import hash_password
from app.services import admin as admin_crud
from app.services import common as all_crud
from app.models import User, UserRole
from app.schemas.auth import UserLogout
from app.schemas.user import UserCreate

router = APIRouter(prefix="/admin")

@router.post("/signup")
def admin_signup(user: UserCreate, db: Session = Depends(get_db)):
    
    if all_crud.get_user_by_user_id(db, user.userId): 
        raise HTTPException(status_code=400, detail="User ID already exists")
    
    if all_crud.get_user_by_email(db, user.email): 
        raise HTTPException(status_code=400, detail="Email already exists")
    
    try: 
        return all_crud.create_user(db, User(userId=user.userId, name=user.username, email=user.email, password_hash=hash_password(user.password), role=UserRole.ADMIN, profile_flag=False, updated_time=datetime.now()))
    except IntegrityError:
        db.rollback(); raise HTTPException(status_code=400, detail="Admin already exists")

@router.post("/logout")
def admin_logout(logout_data: UserLogout, db: Session = Depends(get_db)):
    
    session = admin_crud.logout_admin_session(db, logout_data.session_id)
    
    if session is None: 
        raise HTTPException(status_code=404, detail="Active admin session not found")
    
    return {
        "message": "Admin logout successful", 
        "session_id": session.id, 
        "logout_time": session.logout_time
        }
