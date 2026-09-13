from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from app.core.dependencies import get_db
from app.core.security import hash_password, verify_password
from app.services import admin as admin_crud
from app.services import common as all_crud
from app.services import user as user_crud
from app.models import User, UserRole
from app.schemas.auth import UserLogin
from app.schemas.user import UserCreate

router = APIRouter()
@router.post("/signup")
def signup(user: UserCreate, db: Session = Depends(get_db)):
    
    if all_crud.get_user_by_user_id(db, user.userId): 
        raise HTTPException(status_code=400, detail="User ID already exists")
    
    if all_crud.get_user_by_email(db, user.email): 
        raise HTTPException(status_code=400, detail="Email already exists")
    
    new_user = User(
        userId=user.userId, 
        name=user.name, 
        email=user.email, 
        password_hash=hash_password(user.password),
        role=UserRole.USER,
        profile_flag=True,
        updated_time=datetime.now(),
        )
    
    try: 
        all_crud.create_user(db, new_user)
        return {
            "message": "User account is created"
        }
    
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="User already exists")

@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    
    if user.userId is not None:
        db_user = all_crud.get_user_by_user_id(db, user.userId) 
    else:
        db_user = all_crud.get_user_by_email(db, user.email)
    
    if db_user is None or not verify_password(user.password, db_user.password_hash):
        raise HTTPException(
            status_code=401,
            detail="Invalid userId/email or password",
        )

    if db_user.role == UserRole.ADMIN:
        session = admin_crud.create_admin_session(db, db_user.userId)
        
        return {
            "message": "Admin login successful.", 
            "userId": db_user.userId, 
            "name": db_user.name, 
            "email": db_user.email,
            "session_token": session.session_token
            }
        
    profiles = user_crud.get_user_profiles(db, db_user.userId)
    
    return {
        "message": "Login successful. Select a profile to create a session.", 
        "userId": db_user.userId, 
        "name": db_user.name, 
        "email": db_user.email, 
        "profiles": [
            {"id": p.id, 
             "profile_name": p.profile_name, 
             "profile_pic": p.profile_pic
             }
            for p in profiles
            ]
        }
