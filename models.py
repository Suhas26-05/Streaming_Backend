from sqlalchemy import Column, Integer, String
from database import Base


class User(Base):

    __tablename__ = "users"

    userId = Column(String(50),primary_key=True,index=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    
