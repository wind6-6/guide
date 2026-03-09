# 路线规划接口
from flask import Blueprint, request, jsonify
from database.models import Road
from database.db_init import init_database
from algorithm.shortest_path import ShortestPath
from algorithm.multi_point_path import MultiPointPath

route_plan_bp = Blueprint('route_plan', __name__)

def get_session():
    _, SessionLocal = init_database()
    return SessionLocal()

@route_plan_bp.route('/plan', methods=['POST'])
def plan_route():
    """路线规划（最短路径）"""
    data = request.json
    start = data.get('start')
    end = data.get('end')
    strategy = data.get('strategy', 'distance')  # distance 或 time
    
    if not start or not end:
        return jsonify({'status': 400, 'msg': '起点和终点不能为空'})
    
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
                'distance': road.distance,
                'crowd_level': road.crowd_level
            }
        
        # 计算最短路径
        path, distance = ShortestPath.dijkstra(graph, start, end, strategy)
        
        return jsonify({
            'status': 200,
            'data': {
                'path': path,
                'distance': distance,
                'strategy': strategy
            }
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
