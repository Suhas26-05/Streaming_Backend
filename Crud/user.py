from sqlalchemy.orm import Session
from datetime import datetime
from models import Profile, User, UserSession

def get_user_by_user_id(db: Session, user_id: str):
    return db.query(User).filter(User.userId == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def get_user_profiles(db: Session, user_id: str):
    return db.query(Profile).filter(Profile.userId == user_id).all()


def find_profile(db: Session, user_id: str, profile_name: str):
    return ( 
            db.query(Profile).filter(Profile.userId == user_id,Profile.profile_name == profile_name,).first()
            )

def create_profile(db: Session, profile: Profile):
    db.add(profile)
    db.commit()
    db.refresh(profile)
    return profile


def get_profile(db: Session, user_id: str, profile_id: int):
    return (
        db.query(Profile).filter(Profile.id == profile_id, Profile.userId == user_id).first()
    )


def update_profile(db: Session, profile: Profile, profile_name=None, profile_pic=None):
    if profile_name is not None:
        profile.profile_name = profile_name
    if profile_pic is not None:
        profile.profile_pic = profile_pic

    db.commit()
    db.refresh(profile)
    return profile


def delete_profile(db: Session, profile: Profile):
    db.delete(profile)
    db.commit()


def create_user_session(db: Session, user_id: str, profile_id: int):
    session = UserSession(
        userId=user_id,
        profile_id=profile_id,
        login_time=datetime.now(),
        is_active=1,
    )
    db.add(session)
    db.commit()
    db.refresh(session)
    return session


def logout_user_session(db: Session, session_id: int):
    session = db.query(UserSession).filter(UserSession.id == session_id, UserSession.is_active == 1).first()
    if session is None:
        return None
    session.logout_time = datetime.now()
    session.is_active = 0
    db.commit()
    db.refresh(session)
    return session