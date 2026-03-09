# 路线规划业务逻辑
from database.models import Road
from database.db_init import init_database
from algorithm.shortest_path import ShortestPath
from algorithm.multi_point_path import MultiPointPath

class RoutePlanService:
    def __init__(self):
        _, self.SessionLocal = init_database()
    
    def plan_route(self, start, end, strategy='distance'):
        """规划路线"""
        session = self.SessionLocal()
        try:
            roads = session.query(Road).all()
            
            # 构建图
            graph = {}
            for road in roads:
                if road.start_node not in graph:
                    graph[road.start_node] = {}
                graph[road.start_node][road.end_node] = {
                    'distance': road.distance,
                    'crowd_level': road.crowd_level
                }
            
            # 计算最短路径
            path, distance = ShortestPath.dijkstra(graph, start, end, strategy)
            return path, distance
        finally:
            session.close()
    
    def multi_point_navigation(self, points):
        """多点导航"""
        session = self.SessionLocal()
        try:
            roads = session.query(Road).all()
            
            # 构建图
            graph = {}
            for road in roads:
                if road.start_node not in graph:
                    graph[road.start_node] = {}
                graph[road.start_node][road.end_node] = {
                    'distance': road.distance
                }
            
            # 计算多点路径
            path, total_distance = MultiPointPath.tsp_path(graph, points)
            return path, total_distance
        finally:
            session.close()
