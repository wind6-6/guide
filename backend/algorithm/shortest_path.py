# 最短路径算法
import heapq
from config.algorithm_config import AlgorithmConfig

class ShortestPath:
    @staticmethod
    def dijkstra(graph, start, end, weight='distance'):
        """Dijkstra 最短路径算法"""
        # 初始化距离字典
        distances = {node: float('inf') for node in graph}
        distances[start] = 0
        
        # 优先队列
        priority_queue = [(0, start)]
        
        # 前驱节点
        previous = {}
        
        while priority_queue:
            current_distance, current_node = heapq.heappop(priority_queue)
            
            # 如果到达终点
            if current_node == end:
                break
            
            # 如果当前距离大于已知距离，跳过
            if current_distance > distances[current_node]:
                continue
            
            # 遍历邻居节点
            for neighbor, edge in graph[current_node].items():
                # 计算权重
                if weight == 'distance':
                    edge_weight = edge['distance']
                elif weight == 'time':
                    # 考虑拥挤度和速度
                    speed = AlgorithmConfig.IDEAL_SPEED
                    crowd_factor = 1 + (edge.get('crowd_level', 1) - 1) * AlgorithmConfig.CROWD_PENALTY
                    edge_weight = (edge['distance'] / 1000) / speed * 60 * crowd_factor
                else:
                    edge_weight = edge.get(weight, edge['distance'])
                
                distance = current_distance + edge_weight
                
                # 如果找到更短的路径
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    previous[neighbor] = current_node
                    heapq.heappush(priority_queue, (distance, neighbor))
        
        # 重建路径
        path = []
        current = end
        while current:
            path.append(current)
            current = previous.get(current)
        path.reverse()
        
        return path, distances[end]
