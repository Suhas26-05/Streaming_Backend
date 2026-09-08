from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = "users"

    userId = Column(String(50), primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(255), nullable=False)

    profiles = relationship("Profile",back_populates="user",cascade="all, delete-orphan")
    
class Admin(Base):

    __tablename__ = "admin"

    userId = Column(String(50),primary_key=True,index=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    
class UserSession(Base):

    __tablename__ = "user_sessions"

    id = Column(Integer, primary_key=True, index=True)
    userId = Column(String(50), ForeignKey("users.userId"), nullable=False, index=True)
    profile_id = Column(Integer, ForeignKey("user_profiles.id"), nullable=False, index=True)
    login_time = Column(DateTime, nullable=False)
    logout_time = Column(DateTime, nullable=True)
    is_active = Column(Integer, nullable=False, default=1)
    
class AdminSession(Base):
    __tablename__ = "admin_sessions"

    id = Column(Integer, primary_key=True)
    adminId = Column(String(50), ForeignKey("admin.userId"), nullable=False)
    login_time = Column(DateTime, nullable=False)
    logout_time = Column(DateTime, nullable=True)
    is_active = Column(Integer, nullable=False, default=1)

class Profile(Base):
    __tablename__ = "user_profiles"
    
    id = Column(Integer, primary_key=True, index=True)
    userId = Column(String(50),ForeignKey("users.userId"),nullable=False,index=True)
    profile_name = Column(String(50), nullable=False)
    profile_pic = Column(String(100), nullable=True)

    user = relationship("User",back_populates="profiles")
    __table_args__ = (UniqueConstraint("userId","profile_name",name="uq_user_profile_name"),)
    # above line is to define a composite unique constraint in SQLAlchemy.