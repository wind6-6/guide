# 用户模型
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from database.db_init import Base

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    password = Column(String(255), nullable=False)
    name = Column(String(50), nullable=False)
    phone = Column(String(20))
    email = Column(String(100))
    avatar = Column(String(255))
    create_time = Column(DateTime(timezone=True), server_default=func.now())
    update_time = Column(DateTime(timezone=True), onupdate=func.now())
    
    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}', name='{self.name}')>"
