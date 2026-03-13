# 路线规划接口
from flask import Blueprint, request, jsonify
from database.models import Road, Scenic
from database.db_init import init_database
from algorithm.shortest_path import ShortestPath
import heapq

route_plan_bp = Blueprint('route_plan', __name__)

def get_session():
    _, SessionLocal = init_database()
    return SessionLocal()

def calculate_distance(lat1, lon1, lat2, lon2):
    """计算两点之间的实际距离（米）"""
    from math import radians, cos, sin, asin, sqrt
    R = 6371  # 地球半径（公里）
    dLat = radians(lat2 - lat1)
    dLon = radians(lon2 - lon1)
    a = sin(dLat/2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dLon/2)**2
    c = 2 * asin(sqrt(a))
    return c * R * 1000  # 转换为米

@route_plan_bp.route('/plan', methods=['POST'])
def plan_route():
    """路线规划（最短路径）- 使用真实道路网络"""
    data = request.json
    start = data.get('start')
    end = data.get('end')
    strategy = data.get('strategy', 'distance')
    transport_type = data.get('transport_type', '步行')
    
    if not start or not end:
        return jsonify({'status': 400, 'msg': '起点和终点不能为空'})
    
    session = get_session()
    try:
        # 1. 获取前20个景区（只使用这20个节点进行路径规划）
        scenics = session.query(Scenic).limit(20).all()
        scenic_dict = {s.name: s for s in scenics}
        scenic_names = set(scenic_dict.keys())
        
        # 检查起点和终点
        if start not in scenic_names:
            return jsonify({'status': 400, 'msg': f'起点 "{start}" 不在地图中'})
        if end not in scenic_names:
            return jsonify({'status': 400, 'msg': f'终点 "{end}" 不在地图中'})
        
        # 2. 获取这些景区之间的道路
        roads = session.query(Road).filter(
            Road.start_node.in_(scenic_names),
            Road.end_node.in_(scenic_names)
        ).all()
        
        # 3. 构建图 - 只使用数据库中的道路
        graph = {name: {} for name in scenic_names}
        
        for road in roads:
            if road.start_node in scenic_names and road.end_node in scenic_names:
                # 添加双向边
                graph[road.start_node][road.end_node] = {
                    'distance': road.distance,
                    'crowd_level': road.crowd_level,
                    'transport_type': getattr(road, 'transport_type', '步行')
                }
                graph[road.end_node][road.start_node] = {
                    'distance': road.distance,
                    'crowd_level': road.crowd_level,
                    'transport_type': getattr(road, 'transport_type', '步行')
                }
        
        # 4. 确保连通性 - 为没有连接的节点添加最近邻连接
        for name in scenic_names:
            if not graph[name]:  # 如果没有出边
                scenic = scenic_dict[name]
                # 找到最近的3个邻居
                neighbors = []
                for other_name, other in scenic_dict.items():
                    if other_name != name:
                        dist = calculate_distance(
                            scenic.lat or 39.9, scenic.lng or 116.4,
                            other.lat or 39.9, other.lng or 116.4
                        )
                        neighbors.append((other_name, dist))
                
                neighbors.sort(key=lambda x: x[1])
                for neighbor_name, dist in neighbors[:3]:
                    if dist < 15000:  # 15公里内
                        graph[name][neighbor_name] = {
                            'distance': int(dist),
                            'crowd_level': 2,
                            'transport_type': '步行'
                        }
                        graph[neighbor_name][name] = {
                            'distance': int(dist),
                            'crowd_level': 2,
                            'transport_type': '步行'
                        }
        
        # 5. 使用Dijkstra算法
        path, total_cost = dijkstra(graph, start, end, strategy, transport_type)
        
        if not path or len(path) < 2:
            return jsonify({'status': 404, 'msg': '无法找到可行路径'})
        
        # 6. 计算实际距离和时间
        actual_distance = 0
        for i in range(len(path) - 1):
            if path[i+1] in graph[path[i]]:
                actual_distance += graph[path[i]][path[i+1]]['distance']
        
        speed_map = {'步行': 5, '自行车': 15, '电瓶车': 25, '汽车': 40}
        speed = speed_map.get(transport_type, 5)
        estimated_time = (actual_distance / 1000) / speed * 60
        
        return jsonify({
            'status': 200,
            'msg': '路线规划成功',
            'data': {
                'path': path,
                'distance': actual_distance,
                'estimated_time': round(estimated_time, 1),
                'strategy': strategy,
                'transport_type': transport_type
            }
        })
        
    except Exception as e:
        import traceback
        print(f"路线规划出错: {str(e)}")
        print(traceback.format_exc())
        return jsonify({'status': 500, 'msg': f'路线规划失败: {str(e)}'})
    finally:
        session.close()

def dijkstra(graph, start, end, strategy='distance', transport_type='步行'):
    """Dijkstra最短路径算法"""
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    previous = {}
    
    # 优先队列: (距离, 节点)
    pq = [(0, start)]
    visited = set()
    
    speed_map = {'步行': 5, '自行车': 15, '电瓶车': 25, '汽车': 40}
    speed = speed_map.get(transport_type, 5)
    
    while pq:
        current_dist, current = heapq.heappop(pq)
        
        if current in visited:
            continue
        visited.add(current)
        
        if current == end:
            break
        
        for neighbor, edge in graph[current].items():
            if neighbor in visited:
                continue
            
            # 计算边权重
            if strategy == 'distance':
                weight = edge['distance']
            else:  # time
                crowd = edge.get('crowd_level', 1)
                factor = 1 + (crowd - 1) * 0.2
                weight = (edge['distance'] / 1000 / speed * 60) * factor
            
            new_dist = current_dist + weight
            
            if new_dist < distances[neighbor]:
                distances[neighbor] = new_dist
                previous[neighbor] = current
                heapq.heappush(pq, (new_dist, neighbor))
    
    # 重建路径
    if distances[end] == float('inf'):
        return [], 0
    
    path = []
    current = end
    while current:
        path.append(current)
        current = previous.get(current)
    path.reverse()
    
    return path, distances[end]

@route_plan_bp.route('/roads', methods=['GET'])
def get_roads():
    """获取道路数据 - 只返回前20个景区之间的道路"""
    session = get_session()
    try:
        # 获取前20个景区
        scenics = session.query(Scenic).limit(20).all()
        scenic_names = {s.name for s in scenics}
        
        # 只获取这些景区之间的道路
        roads = session.query(Road).filter(
            Road.start_node.in_(scenic_names),
            Road.end_node.in_(scenic_names)
        ).all()
        
        return jsonify({
            'status': 200,
            'data': [{
                'start': road.start_node,
                'end': road.end_node,
                'distance': road.distance,
                'crowd_level': road.crowd_level,
                'transport_type': getattr(road, 'transport_type', '步行')
            } for road in roads]
        })
    finally:
        session.close()


@route_plan_bp.route('/nodes', methods=['GET'])
def get_nodes():
    """获取路径规划使用的所有节点（前20个景区）"""
    session = get_session()
    try:
        # 获取前20个景区 - 与路径规划使用的一致
        scenics = session.query(Scenic).limit(20).all()
        
        return jsonify({
            'status': 200,
            'data': [{
                'id': scenic.id,
                'name': scenic.name,
                'lat': scenic.lat,
                'lng': scenic.lng,
                'address': scenic.address,
                'category': scenic.category,
                'hotness': scenic.hotness,
                'rating': scenic.rating
            } for scenic in scenics]
        })
    finally:
        session.close()

@route_plan_bp.route('/transport-options', methods=['POST'])
def get_transport_options():
    """获取多种交通工具的路径选项"""
    data = request.json
    start = data.get('start')
    end = data.get('end')
    strategy = data.get('strategy', 'distance')
    
    if not start or not end:
        return jsonify({'status': 400, 'msg': '起点和终点不能为空'})
    
    session = get_session()
    try:
        # 获取所有道路
        roads = session.query(Road).all()
        
        # 构建图（添加双向边）
        graph = {}
        for road in roads:
            # 确保节点名称不为空
            if not road.start_node or not road.end_node:
                continue
                
            # 添加正向边
            if road.start_node not in graph:
                graph[road.start_node] = {}
            graph[road.start_node][road.end_node] = {
                'distance': road.distance,
                'crowd_level': road.crowd_level,
                'transport_type': road.transport_type if hasattr(road, 'transport_type') else '步行'
            }
            # 添加反向边（假设道路是双向的）
            if road.end_node not in graph:
                graph[road.end_node] = {}
            graph[road.end_node][road.start_node] = {
                'distance': road.distance,
                'crowd_level': road.crowd_level,
                'transport_type': road.transport_type if hasattr(road, 'transport_type') else '步行'
            }
        
        # 打印图的节点数量，用于调试
        print(f"图中节点数量: {len(graph)}")
        print(f"图中节点: {list(graph.keys())[:10]}")  # 打印前10个节点
        
        # 获取多种交通工具的路径选项
        results = ShortestPath.get_path_with_transport_options(graph, start, end, strategy)
        
        return jsonify({
            'status': 200,
            'data': results
        })
    finally:
        session.close()

@route_plan_bp.route('/navigate', methods=['POST'])
def navigate():
    """多点导航"""
    data = request.json
    points = data.get('points', [])
    
    if len(points) < 2:
        return jsonify({'status': 400, 'msg': '至少需要两个点'})
    
    session = get_session()
    try:
        # 获取所有道路
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
        
        return jsonify({
            'status': 200,
            'data': {
                'path': path,
                'total_distance': total_distance
            }
        })
    finally:
        session.close()
