from enum import Enum
from sqlalchemy import Boolean, Column, DateTime, Enum as SqlEnum, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import relationship
from app.models.base import Base

class UserRole(str, Enum):
    USER = "user"
    ADMIN = "admin"

class User(Base):
    __tablename__ = "users"
    userId = Column(String(50), primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(SqlEnum(UserRole), unique=False, default=UserRole.USER)
    profile_flag = Column(Boolean, unique=False, nullable=False)
    updated_time = Column(DateTime, unique=False, nullable=False)
    profiles = relationship("Profile", back_populates="user", cascade="all, delete-orphan")

class UserSession(Base):
    __tablename__ = "user_sessions"
    id = Column(Integer, primary_key=True)
    userId = Column(String(50), ForeignKey("users.userId"), nullable=False, index=True)
    profile_id = Column(Integer, ForeignKey("user_profiles.id"), nullable=True, index=True)
    login_time = Column(DateTime(timezone=True), nullable=False)
    logout_time = Column(DateTime(timezone=True), nullable=True)
    is_active = Column(Boolean, nullable=False, default=True)

class Profile(Base):
    __tablename__ = "user_profiles"
    id = Column(Integer, primary_key=True, index=True)
    userId = Column(String(50), ForeignKey("users.userId"), nullable=False, index=True)
    profile_name = Column(String(50), nullable=False)
    profile_pic = Column(String(100), nullable=True)
    user = relationship("User", back_populates="profiles")
    __table_args__ = (UniqueConstraint("userId", "profile_name", name="uq_user_profile_name"),)
