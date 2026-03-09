# 设施模型
from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from database.db_init import Base

class Facility(Base):
    __tablename__ = 'facilities'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, index=True)
    scenic_id = Column(Integer, ForeignKey('scenics.id'))
    type = Column(String(50))  # 超市/卫生间/餐厅等
    location = Column(String(255))
    description = Column(Text)
    open_time = Column(String(100))
    
    # 关系
    scenic = relationship('Scenic', backref='facilities')
    
    def __repr__(self):
        return f"<Facility(id={self.id}, name='{self.name}', type='{self.type}')>"
