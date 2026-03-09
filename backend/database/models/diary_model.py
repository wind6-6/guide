# 日记模型
from sqlalchemy import Column, Integer, String, Text, Float, ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database.db_init import Base

class Diary(Base):
    __tablename__ = 'diaries'
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    title = Column(String(200), nullable=False, index=True)
    content = Column(Text, nullable=False)
    hotness = Column(Float, default=0.0)
    rating = Column(Float, default=0.0)
    scenic_id = Column(Integer, ForeignKey('scenics.id'))
    images = Column(Text)  # 图片路径，用逗号分隔
    create_time = Column(DateTime(timezone=True), server_default=func.now())
    update_time = Column(DateTime(timezone=True), onupdate=func.now())
    
    # 关系
    user = relationship('User', backref='diaries')
    scenic = relationship('Scenic', backref='diaries')
    
    def __repr__(self):
        return f"<Diary(id={self.id}, title='{self.title}', user_id={self.user_id})>"
