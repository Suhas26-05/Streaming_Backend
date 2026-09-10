from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from app.core.dependencies import get_db
from app.services import user as user_crud
from app.models import Profile
from app.schemas.auth import UserLogout
from app.schemas.user import ProfileCreate, ProfileSelect, ProfileUpdate

router = APIRouter()
@router.post("/users/{user_id}/profiles/select")
def select_profile(user_id: str, profile: ProfileSelect, db: Session = Depends(get_db)):
    
    if user_crud.get_user_by_user_id(db, user_id) is None: 
        raise HTTPException(status_code=404, detail="User not found")
    
    selected = user_crud.get_profile(db, user_id, profile.profile_id)
    
    if selected is None: 
        raise HTTPException(status_code=404, detail="Profile not found for this user")
    
    session = user_crud.create_user_session(db, user_id, selected.id)
    return {
        "message": "Profile selected and session created",
        "session_id": session.id, "userId": session.userId,
        "profile_id": session.profile_id
        }
    
@router.post("/logout")
def logout(logout_data: UserLogout, db: Session = Depends(get_db)):
    session = user_crud.logout_user_session(db, logout_data.session_id)
    
    if session is None: 
        raise HTTPException(status_code=404, detail="Active session not found")
    return {
        "message": "Logout successful", 
        "session_id": session.id,
        "logout_time": session.logout_time
        }
    
@router.post("/users/{user_id}/profiles")
def create_profile(user_id: str, profile: ProfileCreate, db: Session = Depends(get_db)):
    
    if user_crud.get_user_by_user_id(db, user_id) is None: 
        raise HTTPException(status_code=404, detail="User not found")
    
    if user_crud.find_profile(db, user_id, profile.profile_name): 
        raise HTTPException(status_code=400, detail="Profile name already exists")
    
    try:
        return user_crud.create_profile(db, Profile(userId=user_id, profile_name=profile.profile_name, profile_pic=profile.profile_pic))
    
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Profile name already exists")
    
@router.get("/users/{user_id}/profiles")
def get_profiles(user_id: str, db: Session = Depends(get_db)):
    
    if user_crud.get_user_by_user_id(db, user_id) is None: 
        raise HTTPException(status_code=404, detail="User not found")
    
    return user_crud.get_user_profiles(db, user_id)

@router.put("/users/{user_id}/profiles/{profile_id}")
def update_profile(user_id: str, profile_id: int, profile: ProfileUpdate, db: Session = Depends(get_db)):
    
    if user_crud.get_user_by_user_id(db, user_id) is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    existing = user_crud.get_profile(db, user_id, profile_id)
    
    if existing is None: 
        raise HTTPException(status_code=404, detail="Profile not found")
    
    if profile.profile_name is not None:
        
        duplicate = user_crud.find_profile(db, user_id, profile.profile_name)
        
        if duplicate is not None and duplicate.id != profile_id: 
            raise HTTPException(status_code=400, detail="Profile name already exists")
        
    try: 
        return user_crud.update_profile(db, existing, profile.profile_name, profile.profile_pic)
    
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Profile name already exists")
    
@router.delete("/users/{user_id}/profiles/{profile_id}")
def delete_profile(user_id: str, profile_id: int, db: Session = Depends(get_db)):
    if user_crud.get_user_by_user_id(db, user_id) is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    profile = user_crud.get_profile(db, user_id, profile_id)
    
    if profile is None: 
        raise HTTPException(status_code=404, detail="Profile not found")
    
    user_crud.delete_profile(db, profile)
    return {
        "message": "Profile deleted successfully", 
        "profile_id": profile_id
        }
