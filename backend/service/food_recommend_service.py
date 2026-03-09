# 美食推荐业务逻辑
from database.models import Food
from database.db_init import init_database
from algorithm.sort_algorithm import SortAlgorithm
from algorithm.search_algorithm import SearchAlgorithm

class FoodRecommendService:
    def __init__(self):
        _, self.SessionLocal = init_database()
    
    def get_food_list(self, cuisine=None):
        """获取美食列表"""
        session = self.SessionLocal()
        try:
            query = session.query(Food)
            if cuisine:
                query = query.filter_by(cuisine=cuisine)
            foods = query.all()
            
            # 排序
            sorted_foods = SortAlgorithm.weighted_sort(foods)
            return sorted_foods
        finally:
            session.close()
    
    def recommend_food(self, scenic_id=None, limit=10):
        """推荐美食"""
        session = self.SessionLocal()
        try:
            query = session.query(Food)
            if scenic_id:
                query = query.filter_by(scenic_id=scenic_id)
            foods = query.all()
            
            # 取前N个推荐
            top_foods = SortAlgorithm.top_n_sort(foods, lambda x: x.rating * 0.7 + x.hotness * 0.3, n=limit)
            return top_foods
        finally:
            session.close()
