from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from app.models.base import Base

class AdminSession(Base):
    __tablename__ = "admin_sessions"
    id = Column(Integer, primary_key=True)
    adminId = Column(String(50), ForeignKey("users.userId"), nullable=False)
    login_time = Column(DateTime, nullable=False)
    logout_time = Column(DateTime, nullable=True)
    is_active = Column(Integer, nullable=False, default=1)
