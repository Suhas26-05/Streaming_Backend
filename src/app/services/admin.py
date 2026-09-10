from datetime import datetime
from sqlalchemy.orm import Session
from app.models import AdminSession, User, UserRole

def get_admin_by_user_id(db: Session, user_id: str): 
    return db.query(User).filter(User.userId == user_id, User.role == UserRole.ADMIN).first()

def get_admin_by_email(db: Session, email: str): 
    return db.query(User).filter(User.email == email, User.role == UserRole.ADMIN).first()

def create_admin_session(db: Session, admin_id: str):
    session = AdminSession(adminId=admin_id, login_time=datetime.now(), is_active=1)
    
    db.add(session)
    db.commit() 
    db.refresh(session) 
    
    return session

def logout_admin_session(db: Session, session_id: int):
    session = db.query(AdminSession).filter(AdminSession.id == session_id, AdminSession.is_active == 1).first()
    if session is None: 
        return None
    
    session.logout_time = datetime.now()
    session.is_active = 0; db.commit()
    db.refresh(session)
    
    return session
