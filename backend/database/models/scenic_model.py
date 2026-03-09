# 景区模型
from sqlalchemy import Column, Integer, String, Float, Text, DateTime
from sqlalchemy.sql import func
from database.db_init import Base

class Scenic(Base):
    __tablename__ = 'scenics'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, index=True)
    description = Column(Text)
    address = Column(String(255))
    hotness = Column(Float, default=0.0)
    rating = Column(Float, default=0.0)
    category = Column(String(50))
    open_time = Column(String(100))
    ticket_price = Column(String(50))
    create_time = Column(DateTime(timezone=True), server_default=func.now())
    update_time = Column(DateTime(timezone=True), onupdate=func.now())
    
    def __repr__(self):
        return f"<Scenic(id={self.id}, name='{self.name}', rating={self.rating})>"
