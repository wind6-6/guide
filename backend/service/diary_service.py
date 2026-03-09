# 日记业务逻辑
from database.models import Diary
from database.db_init import init_database
from algorithm.sort_algorithm import SortAlgorithm
from algorithm.text_search import TextSearch
from algorithm.lossless_compression import LosslessCompression

class DiaryService:
    def __init__(self):
        _, self.SessionLocal = init_database()
    
    def get_user_diaries(self, user_id):
        """获取用户日记"""
        session = self.SessionLocal()
        try:
            diaries = session.query(Diary).filter_by(user_id=user_id).all()
            diaries.sort(key=lambda x: x.create_time, reverse=True)
            return diaries
        finally:
            session.close()
    
    def create_diary(self, user_id, title, content, scenic_id=None):
        """创建日记"""
        session = self.SessionLocal()
        try:
            # 压缩内容
            compressed_content = LosslessCompression.compress(content)
            
            diary = Diary(
                user_id=user_id,
                title=title,
                content=content,
                scenic_id=scenic_id
            )
            session.add(diary)
            session.commit()
            session.refresh(diary)
            return diary
        finally:
            session.close()
    
    def search_diary(self, user_id, keyword):
        """搜索日记"""
        session = self.SessionLocal()
        try:
            diaries = session.query(Diary).filter_by(user_id=user_id).all()
            
            # 文本搜索
            results = []
            for diary in diaries:
                if keyword.lower() in diary.title.lower() or keyword.lower() in diary.content.lower():
                    results.append(diary)
            
            return results
        finally:
            session.close()
