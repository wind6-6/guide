# 美食模型
from sqlalchemy import Column, Integer, String, Text, Float, ForeignKey
from sqlalchemy.orm import relationship
from database.db_init import Base

class Food(Base):
    __tablename__ = 'foods'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, index=True)
    description = Column(Text)
    hotness = Column(Float, default=0.0)
    rating = Column(Float, default=0.0)
    cuisine = Column(String(50))  # 菜系
    price = Column(String(50))
    address = Column(String(255))
    scenic_id = Column(Integer, ForeignKey('scenics.id'))
    
    # 关系
    scenic = relationship('Scenic', backref='foods')
    
    def __repr__(self):
        return f"<Food(id={self.id}, name='{self.name}', rating={self.rating})>"
