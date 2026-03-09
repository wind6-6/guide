# 室内导航算法
from .shortest_path import ShortestPath
from config.algorithm_config import AlgorithmConfig

class IndoorNavigation:
    # 楼层高度（米）
    FLOOR_HEIGHT = 3.0
    
    @staticmethod
    def create_indoor_graph(buildings, facilities):
        """
        创建室内导航图
        
        Args:
            buildings: 建筑物列表
            facilities: 设施列表（包含电梯、楼梯等）
        
        Returns:
            graph: 室内导航图
        """
        graph = {}
        
        # 为每个建筑物创建节点
        for building in buildings:
            building_id = building.id
            floors = building.floors if hasattr(building, 'floors') else 5
            
            for floor in range(1, floors + 1):
                # 创建楼层节点
                node_id = f"B{building_id}-F{floor}"
                graph[node_id] = {}
                
                # 连接同一建筑物的相邻楼层（楼梯）
                if floor > 1:
                    prev_node = f"B{building_id}-F{floor-1}"
                    graph[node_id][prev_node] = {
                        'distance': IndoorNavigation.FLOOR_HEIGHT,
                        'type': 'stairs',
                        'time': 30  # 爬楼时间（秒）
                    }
                    graph[prev_node][node_id] = {
                        'distance': IndoorNavigation.FLOOR_HEIGHT,
                        'type': 'stairs',
                        'time': 30
                    }
                
                # 连接电梯节点
                if floor == 1:  # 在一楼创建电梯节点
                    elevator_id = f"B{building_id}-Elevator"
                    graph[elevator_id] = {}
                    for f in range(1, floors + 1):
                        target_node = f"B{building_id}-F{f}"
                        graph[elevator_id][target_node] = {
                            'distance': IndoorNavigation.FLOOR_HEIGHT * abs(f - 1),
                            'type': 'elevator',
                            'time': 10 * abs(f - 1)  # 电梯时间（秒）
                        }
                        graph[target_node][elevator_id] = {
                            'distance': IndoorNavigation.FLOOR_HEIGHT * abs(f - 1),
                            'type': 'elevator',
                            'time': 10 * abs(f - 1)
                        }
        
        # 添加设施节点
        for facility in facilities:
            if hasattr(facility, 'building_id') and facility.building_id:
                building_id = facility.building_id
                floor = facility.floor if hasattr(facility, 'floor') else 1
                facility_node = f"F{facility.id}"
                floor_node = f"B{building_id}-F{floor}"
                
                graph[facility_node] = {}
                graph[facility_node][floor_node] = {
                    'distance': 10,  # 设施到楼层中心的距离
                    'type': 'facility'
                }
                graph[floor_node][facility_node] = {
                    'distance': 10,
                    'type': 'facility'
                }
        
        return graph
    
    @staticmethod
    def navigate(graph, start_node, end_node, use_elevator=True):
        """
        室内导航
        
        Args:
            graph: 室内导航图
            start_node: 起点节点
            end_node: 终点节点
            use_elevator: 是否优先使用电梯
        
        Returns:
            path: 路径列表
            distance: 总距离
            instructions: 导航指令
        """
        if not use_elevator:
            # 如果不使用电梯，移除电梯节点
            filtered_graph = {}
            for node, edges in graph.items():
                if 'Elevator' not in node:
                    filtered_graph[node] = {}
                    for neighbor, edge in edges.items():
                        if 'Elevator' not in neighbor:
                            filtered_graph[node][neighbor] = edge
            graph = filtered_graph
        
        path, distance = ShortestPath.dijkstra(graph, start_node, end_node, weight='time')
        
        # 生成导航指令
        instructions = IndoorNavigation.generate_instructions(path, graph)
        
        return path, distance, instructions
    
    @staticmethod
    def generate_instructions(path, graph):
        """生成导航指令"""
        if not path or len(path) < 2:
            return []
        
        instructions = []
        for i in range(len(path) - 1):
            current = path[i]
            next_node = path[i + 1]
            
            edge = graph.get(current, {}).get(next_node, {})
            edge_type = edge.get('type', 'corridor')
            
            if edge_type == 'stairs':
                if 'F' in current and 'F' in next_node:
                    current_floor = int(current.split('F')[1])
                    next_floor = int(next_node.split('F')[1])
                    if next_floor > current_floor:
                        instructions.append(f"从{current_floor}楼上楼梯到{next_floor}楼")
                    else:
                        instructions.append(f"从{current_floor}楼下楼梯到{next_floor}楼")
            elif edge_type == 'elevator':
                if 'Elevator' in next_node:
                    instructions.append("乘坐电梯")
                elif 'Elevator' in current:
                    floor = next_node.split('F')[1] if 'F' in next_node else '目标'
                    instructions.append(f"电梯到达{floor}楼，出电梯")
            elif edge_type == 'facility':
                instructions.append(f"到达{next_node}")
            else:
                instructions.append(f"从{current}前往{next_node}")
        
        return instructions
