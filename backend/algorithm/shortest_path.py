# 最短路径算法
import heapq
from config.algorithm_config import AlgorithmConfig

class ShortestPath:
    # 交通工具速度配置（km/h）
    TRANSPORT_SPEED = {
        '步行': 5.0,
        '自行车': 15.0,
        '电瓶车': 25.0,
        '汽车': 40.0
    }
    
    @staticmethod
    def dijkstra(graph, start, end, strategy='distance', transport_type='步行'):
        """
        Dijkstra 最短路径算法
        
        Args:
            graph: 图结构
            start: 起点
            end: 终点
            strategy: 策略 ('distance'-最短距离, 'time'-最短时间)
            transport_type: 交通工具 ('步行', '自行车', '电瓶车', '汽车')
        
        Returns:
            path: 路径列表
            distance: 总距离或时间
        """
        # 初始化距离字典
        distances = {node: float('inf') for node in graph}
        distances[start] = 0
        
        # 优先队列
        priority_queue = [(0, start)]
        
        # 前驱节点
        previous = {}
        
        # 获取交通工具速度
        speed = ShortestPath.TRANSPORT_SPEED.get(transport_type, 5.0)
        
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
                # 检查交通工具是否允许
                allowed_transport = edge.get('transport_type', '步行')
                # 步行可以走所有道路，其他交通工具只能走对应类型的道路
                if transport_type != '步行' and allowed_transport != transport_type:
                    continue  # 非步行交通工具只能走对应类型的道路
                
                # 计算权重
                if strategy == 'distance':
                    edge_weight = edge['distance']
                elif strategy == 'time':
                    # 考虑拥挤度和速度
                    crowd_level = edge.get('crowd_level', 1)
                    crowd_factor = 1 + (crowd_level - 1) * AlgorithmConfig.CROWD_PENALTY
                    edge_weight = (edge['distance'] / 1000) / speed * 60 * crowd_factor
                else:
                    edge_weight = edge.get(strategy, edge['distance'])
                
                distance = current_distance + edge_weight
                
                # 如果找到更短的路径
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    previous[neighbor] = current_node
                    heapq.heappush(priority_queue, (distance, neighbor))
        
        # 重建路径
        path = []
        current = end
        
        # 检查起点和终点是否在图中
        if start not in graph:
            print(f"起点 '{start}' 不在图中")
            return ["起点不在地图中"], 0
        if end not in graph:
            print(f"终点 '{end}' 不在图中")
            return ["终点不在地图中"], 0
        
        # 打印起点和终点的邻居
        print(f"起点 '{start}' 的邻居: {list(graph.get(start, {}).keys())}")
        print(f"终点 '{end}' 的邻居: {list(graph.get(end, {}).keys())}")
        
        # 检查是否找到路径
        if distances[end] == float('inf'):
            print(f"无法找到从 '{start}' 到 '{end}' 的路径")
            print(f"终点 '{end}' 的距离: {distances[end]}")
            return ["无可用路径"], 0
        
        while current:
            path.append(current)
            current = previous.get(current)
        path.reverse()
        
        return path, distances[end]
    
    @staticmethod
    def get_path_with_transport_options(graph, start, end, strategy='distance'):
        """
        获取多种交通工具的路径选项
        
        Returns:
            dict: 各交通工具的路径信息
        """
        results = {}
        for transport_type in ShortestPath.TRANSPORT_SPEED.keys():
            try:
                path, distance = ShortestPath.dijkstra(graph, start, end, strategy, transport_type)
                if path and len(path) > 1:
                    results[transport_type] = {
                        'path': path,
                        'distance': distance if strategy == 'distance' else round(distance, 2),
                        'time': round((distance / 1000) / ShortestPath.TRANSPORT_SPEED[transport_type] * 60, 2) if strategy == 'distance' else round(distance, 2)
                    }
            except:
                continue
        return results
