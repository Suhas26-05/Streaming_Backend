from sqlalchemy.orm import Session
from app.models import User

def get_user_by_user_id(db: Session, user_id: str):
    return db.query(User).filter(User.userId == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def create_user(db: Session, user: User):
    db.add(user); db.commit(); db.refresh(user); return user
