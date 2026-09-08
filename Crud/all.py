from datetime import datetime

from sqlalchemy.orm import Session

from models import Admin, User, UserSession


def get_user_by_user_id(db: Session, user_id: str):
    return (
        db.query(User).filter(User.userId == user_id).first()
        or db.query(Admin).filter(Admin.userId == user_id).first()
    )


def get_user_by_email(db: Session, email: str):
    return (
        db.query(User).filter(User.email == email).first()
        or db.query(Admin).filter(Admin.email == email).first()
    )

def create_user(db: Session, user: User | Admin):
    db.add(user)
    db.commit()
    db.refresh(user)
    return user