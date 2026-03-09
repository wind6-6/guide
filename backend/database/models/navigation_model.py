# 导航模型
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from database.db_init import Base

class Navigation(Base):
    __tablename__ = 'navigation'
    
    id = Column(Integer, primary_key=True, index=True)
    building_id = Column(Integer, ForeignKey('buildings.id'))
    node_id = Column(String(50), nullable=False, index=True)
    floor = Column(Integer)  # 楼层
    x_coordinate = Column(Float)  # x坐标
    y_coordinate = Column(Float)  # y坐标
    type = Column(String(50))  # 电梯/楼梯/房间等
    
    # 关系
    building = relationship('Building', backref='navigation_nodes')
    
    def __repr__(self):
        return f"<Navigation(id={self.id}, node_id='{self.node_id}', floor={self.floor})>"
