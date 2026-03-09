# 数据库工具类
from sqlalchemy.orm import Session

class DBUtils:
    @staticmethod
    def get_by_id(session: Session, model, id):
        """根据ID查询对象"""
        return session.query(model).filter(model.id == id).first()
    
    @staticmethod
    def get_all(session: Session, model, limit=None, offset=None):
        """获取所有对象"""
        query = session.query(model)
        if limit:
            query = query.limit(limit)
        if offset:
            query = query.offset(offset)
        return query.all()
    
    @staticmethod
    def create(session: Session, model, **kwargs):
        """创建对象"""
        instance = model(**kwargs)
        session.add(instance)
        session.commit()
        session.refresh(instance)
        return instance
    
    @staticmethod
    def update(session: Session, instance, **kwargs):
        """更新对象"""
        for key, value in kwargs.items():
            setattr(instance, key, value)
        session.commit()
        session.refresh(instance)
        return instance
    
    @staticmethod
    def delete(session: Session, instance):
        """删除对象"""
        session.delete(instance)
        session.commit()
    
    @staticmethod
    def filter_by(session: Session, model, **kwargs):
        """根据条件过滤"""
        return session.query(model).filter_by(**kwargs).all()
    
    @staticmethod
    def search(session: Session, model, field, keyword):
        """模糊搜索"""
        from sqlalchemy import or_
        return session.query(model).filter(
            getattr(model, field).ilike(f"%{keyword}%")
        ).all()
