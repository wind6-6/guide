# 道路模型
from sqlalchemy import Column, Integer, String, Float
from database.db_init import Base

class Road(Base):
    __tablename__ = 'roads'
    
    id = Column(Integer, primary_key=True, index=True)
    start_node = Column(String(50), nullable=False, index=True)
    end_node = Column(String(50), nullable=False, index=True)
    distance = Column(Float, nullable=False)  # 距离（米）
    crowd_level = Column(Integer, default=1)  # 拥挤度（1-5）
    transport_type = Column(String(50))  # 步行/骑行/驾车
    
    def __repr__(self):
        return f"<Road(id={self.id}, start='{self.start_node}', end='{self.end_node}', distance={self.distance})>"
