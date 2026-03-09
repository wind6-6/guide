# 建筑物模型
from sqlalchemy import Column, Integer, String, Text, Float, ForeignKey
from sqlalchemy.orm import relationship
from database.db_init import Base

class Building(Base):
    __tablename__ = 'buildings'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, index=True)
    scenic_id = Column(Integer, ForeignKey('scenics.id'))
    description = Column(Text)
    type = Column(String(50))  # 景点/教学楼/办公楼
    height = Column(Float)
    floor_count = Column(Integer)
    
    # 关系
    scenic = relationship('Scenic', backref='buildings')
    
    def __repr__(self):
        return f"<Building(id={self.id}, name='{self.name}', type='{self.type}')>"
