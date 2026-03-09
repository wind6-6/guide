# 场所查询接口
from flask import Blueprint, request, jsonify
from database.models import Facility, Building
from database.db_utils import DBUtils
from database.db_init import init_database
from algorithm.search_algorithm import SearchAlgorithm
from algorithm.sort_algorithm import SortAlgorithm

place_query_bp = Blueprint('place_query', __name__)

def get_session():
    _, SessionLocal = init_database()
    return SessionLocal()

@place_query_bp.route('/search', methods=['GET'])
def search_place():
    """场所搜索"""
    keyword = request.args.get('keyword', '')
    facility_type = request.args.get('type')
    
    session = get_session()
    try:
        # 搜索设施
        facilities = session.query(Facility).all()
        
        # 模糊搜索
        if keyword:
            facilities = SearchAlgorithm.fuzzy_search(facilities, 'name', keyword)
        
        # 按类型筛选
        if facility_type:
            facilities = [f for f in facilities if f.type == facility_type]
        
        # 构建响应数据
        data = []
        for facility in facilities:
            data.append({
                'id': facility.id,
                'name': facility.name,
                'type': facility.type,
                'location': facility.location,
                'description': facility.description
            })
        
        return jsonify({'status': 200, 'data': data})
    finally:
        session.close()

@place_query_bp.route('/nearby', methods=['GET'])
def get_nearby_facilities():
    """附近设施（使用路径距离）"""
    location = request.args.get('location', '')  # 当前位置节点
    radius = float(request.args.get('radius', 1000))  # 默认1000米
    facility_type = request.args.get('type')  # 设施类型过滤
    
    if not location:
        return jsonify({'status': 400, 'msg': '当前位置不能为空'})
    
    session = get_session()
    try:
        # 获取所有道路构建图
        roads = session.query(Road).all()
        graph = {}
        for road in roads:
            if road.start_node not in graph:
                graph[road.start_node] = {}
            graph[road.start_node][road.end_node] = {
                'distance': road.distance,
                'crowd_level': road.crowd_level
            }
        
        # 获取设施
        query = session.query(Facility)
        if facility_type:
            query = query.filter_by(type=facility_type)
        facilities = query.all()
        
        # 使用路径距离计算
        nearby_facilities = []
        for facility in facilities:
            if hasattr(facility, 'location') and facility.location:
                try:
                    # 使用最短路径算法计算路径距离
                    _, distance = ShortestPath.dijkstra(graph, location, facility.location, 'distance')
                    if distance <= radius:
                        facility.distance = distance
                        nearby_facilities.append(facility)
                except:
                    # 如果无法计算路径距离，跳过该设施
                    continue
        
        # 按距离排序（只取前10）
        nearby_facilities.sort(key=lambda x: x.distance)
        nearby_facilities = nearby_facilities[:10]  # 只排前10
        
        # 构建响应数据
        data = []
        for facility in nearby_facilities:
            data.append({
                'id': facility.id,
                'name': facility.name,
                'type': facility.type,
                'distance': facility.distance,
                'location': facility.location
            })
        
        return jsonify({'status': 200, 'data': data})
    finally:
        session.close()
