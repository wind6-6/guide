# 旅游推荐业务逻辑
from database.models import Scenic, Building
from database.db_init import init_database
from algorithm.sort_algorithm import SortAlgorithm
from algorithm.search_algorithm import SearchAlgorithm

class TouristRecommendService:
    def __init__(self):
        _, self.SessionLocal = init_database()
    
    def get_recommend_list(self, category=None):
        """获取推荐列表"""
        session = self.SessionLocal()
        try:
            query = session.query(Scenic)
            if category:
                query = query.filter_by(category=category)
            scenics = query.all()
            
            # 排序
            sorted_scenics = SortAlgorithm.weighted_sort(scenics)
            return sorted_scenics
        finally:
            session.close()
    
    def search_scenic(self, keyword):
        """搜索景区"""
        session = self.SessionLocal()
        try:
            scenics = session.query(Scenic).all()
            results = SearchAlgorithm.fuzzy_search(scenics, 'name', keyword)
            return results
        finally:
            session.close()
