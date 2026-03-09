# 用户业务逻辑
from database.models import User
from database.db_init import init_database
import hashlib

class UserService:
    def __init__(self):
        _, self.SessionLocal = init_database()
    
    def hash_password(self, password):
        """密码加密"""
        return hashlib.md5(password.encode()).hexdigest()
    
    def get_user_by_username(self, username):
        """根据用户名获取用户"""
        session = self.SessionLocal()
        try:
            return session.query(User).filter_by(username=username).first()
        finally:
            session.close()
    
    def get_user_by_id(self, user_id):
        """根据ID获取用户"""
        session = self.SessionLocal()
        try:
            return session.query(User).filter_by(id=user_id).first()
        finally:
            session.close()
    
    def create_user(self, username, password, name, phone=None, email=None):
        """创建用户"""
        session = self.SessionLocal()
        try:
            # 检查用户名是否已存在
            existing_user = session.query(User).filter_by(username=username).first()
            if existing_user:
                return None
            
            # 创建新用户
            user = User(
                username=username,
                password=self.hash_password(password),
                name=name,
                phone=phone,
                email=email
            )
            session.add(user)
            session.commit()
            session.refresh(user)
            return user
        finally:
            session.close()
    
    def verify_password(self, user, password):
        """验证密码"""
        return user.password == self.hash_password(password)
