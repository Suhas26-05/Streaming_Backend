from sqlalchemy import Column, Integer, String, DateTime, ForeignKey 
from database import Base


class User(Base):

    __tablename__ = "users"

    userId = Column(String(50),primary_key=True,index=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    
class UserSession(Base):

    __tablename__ = "user_sessions"

    id = Column(Integer, primary_key=True, index=True)
    userId = Column(String(50), ForeignKey("users.userId"), nullable=False, index=True)
    login_time = Column(DateTime, nullable=False)
    logout_time = Column(DateTime, nullable=True)
    is_active = Column(Integer, nullable=False, default=1)