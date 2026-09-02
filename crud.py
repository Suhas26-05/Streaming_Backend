from sqlalchemy.orm import Session
from models import User, UserSession
from datetime import datetime


def get_user_by_user_id(db: Session, user_id: str):
    return db.query(User).filter(User.userId == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def create_user(db: Session, user: User):
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def create_session(db: Session, user_id: str):
    session = UserSession(userId=user_id, login_time=datetime.now(),is_active=1)
    db.add(session)
    db.commit()
    db.refresh(session)

    return session


def logout_session(db: Session, session_id: int):
    session = (db.query(UserSession).filter(UserSession.id == session_id,UserSession.is_active == 1).first())

    if session is None:
        return None

    session.logout_time = datetime.now()
    session.is_active = 0

    db.commit()
    db.refresh(session)

    return session