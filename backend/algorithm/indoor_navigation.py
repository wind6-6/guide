# 室内导航算法
from .shortest_path import ShortestPath
from config.algorithm_config import AlgorithmConfig

class IndoorNavigation:
    @staticmethod
    def create_indoor_graph(nodes):
        """创建室内导航图"""
        graph = {}
        
        for node in nodes:
            node_id = node.node_id
            graph[node_id] = {}
            
            # 连接同一楼层的相邻节点
            for other_node in nodes:
                if other_node != node and other_node.floor == node.floor:
                    # 计算欧几里得距离
                    distance = ((other_node.x_coordinate - node.x_coordinate) ** 2 +
                               (other_node.y_coordinate - node.y_coordinate) ** 2) ** 0.5
                    
                    # 如果距离小于阈值，视为可通行
                    if distance <= AlgorithmConfig.INDOOR_NODE_RADIUS * 2:
                        graph[node_id][other_node.node_id] = {
                            'distance': distance,
                            'type': 'corridor'
                        }
        
        return graph
    
    @staticmethod
    def navigate(graph, start_node, end_node):
        """室内导航"""
        return ShortestPath.dijkstra(graph, start_node, end_node)
