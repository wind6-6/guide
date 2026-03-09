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
    lat = Column(Float)  # 纬度
    lng = Column(Float)  # 经度
    hotness = Column(Float, default=0.0)
    rating = Column(Float, default=0.0)
    category = Column(String(50))
    open_time = Column(String(100))
    ticket_price = Column(String(50))
    create_time = Column(DateTime(timezone=True), server_default=func.now())
    update_time = Column(DateTime(timezone=True), onupdate=func.now())
    
    def __repr__(self):
        return f"<Scenic(id={self.id}, name='{self.name}', lat={self.lat}, lng={self.lng})>"
    
    def to_dict(self):
        """转换为字典格式，包含经纬度信息"""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'address': self.address,
            'lat': self.lat,
            'lng': self.lng,
            'hotness': self.hotness,
            'rating': self.rating,
            'category': self.category,
            'open_time': self.open_time,
            'ticket_price': self.ticket_price,
            'create_time': self.create_time.isoformat() if self.create_time else None,
            'update_time': self.update_time.isoformat() if self.update_time else None
        }
