# 地图工具
import math

class MapUtils:
    @staticmethod
    def calculate_distance(lat1, lon1, lat2, lon2):
        """计算地理距离（Haversine公式）"""
        R = 6371  # 地球半径（公里）
        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lon2 - lon1)
        a = math.sin(dlat/2) * math.sin(dlat/2) + \
            math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * \
            math.sin(dlon/2) * math.sin(dlon/2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        distance = R * c * 1000  # 转换为米
        return distance
    
    @staticmethod
    def parse_road_map(roads):
        """解析道路图"""
        graph = {}
        for road in roads:
            if road.start_node not in graph:
                graph[road.start_node] = {}
            graph[road.start_node][road.end_node] = {
                'distance': road.distance,
                'crowd_level': road.crowd_level
            }
        return graph
