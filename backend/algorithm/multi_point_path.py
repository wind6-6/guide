# 多点最短路径算法
from .shortest_path import ShortestPath

class MultiPointPath:
    @staticmethod
    def tsp_path(graph, points):
        """旅行商问题（TSP）的近似解法"""
        if not points:
            return [], 0
        
        # 起点
        path = [points[0]]
        remaining = points[1:]
        total_distance = 0
        
        # 贪心算法：每次选择最近的点
        while remaining:
            current = path[-1]
            nearest = None
            min_distance = float('inf')
            
            for point in remaining:
                _, distance = ShortestPath.dijkstra(graph, current, point)
                if distance < min_distance:
                    min_distance = distance
                    nearest = point
            
            if nearest:
                path_segment, _ = ShortestPath.dijkstra(graph, current, nearest)
                path.extend(path_segment[1:])  # 避免重复添加当前点
                total_distance += min_distance
                remaining.remove(nearest)
        
        # 返回起点
        if path[-1] != points[0]:
            path_segment, distance = ShortestPath.dijkstra(graph, path[-1], points[0])
            path.extend(path_segment[1:])
            total_distance += distance
        
        return path, total_distance
