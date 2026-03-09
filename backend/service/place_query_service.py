# 场所查询业务逻辑
from database.models import Facility
from database.db_init import init_database
from algorithm.search_algorithm import SearchAlgorithm

class PlaceQueryService:
    def __init__(self):
        _, self.SessionLocal = init_database()
    
    def search_place(self, keyword, facility_type=None):
        """搜索场所"""
        session = self.SessionLocal()
        try:
            facilities = session.query(Facility).all()
            
            # 模糊搜索
            if keyword:
                facilities = SearchAlgorithm.fuzzy_search(facilities, 'name', keyword)
            
            # 按类型筛选
            if facility_type:
                facilities = [f for f in facilities if f.type == facility_type]
            
            return facilities
        finally:
            session.close()
    
    def get_nearby_facilities(self, latitude, longitude, radius=1000):
        """获取附近设施"""
        session = self.SessionLocal()
        try:
            facilities = session.query(Facility).all()
            
            # 简单的距离过滤
            nearby_facilities = []
            for facility in facilities:
                # 模拟距离计算
                distance = 500
                if distance <= radius:
                    facility.distance = distance
                    nearby_facilities.append(facility)
            
            # 按距离排序
            nearby_facilities.sort(key=lambda x: x.distance)
            return nearby_facilities
        finally:
            session.close()
