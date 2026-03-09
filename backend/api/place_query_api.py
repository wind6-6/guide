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
    """附近设施"""
    latitude = float(request.args.get('latitude', 0))
    longitude = float(request.args.get('longitude', 0))
    radius = float(request.args.get('radius', 1000))  # 默认1000米
    
    session = get_session()
    try:
        # 获取所有设施
        facilities = session.query(Facility).all()
        
        # 简单的距离过滤（实际应用中应使用地理距离计算）
        nearby_facilities = []
        for facility in facilities:
            # 这里使用模拟距离
            distance = 500  # 模拟距离
            if distance <= radius:
                facility.distance = distance
                nearby_facilities.append(facility)
        
        # 按距离排序
        nearby_facilities.sort(key=lambda x: x.distance)
        
        # 构建响应数据
        data = []
        for facility in nearby_facilities:
            data.append({
                'id': facility.id,
                'name': facility.name,
                'type': facility.type,
                'distance': facility.distance
            })
        
        return jsonify({'status': 200, 'data': data})
    finally:
        session.close()
