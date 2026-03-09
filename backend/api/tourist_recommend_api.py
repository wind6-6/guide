# 旅游推荐接口
from flask import Blueprint, request, jsonify
from database.models import Scenic, Building
from database.db_utils import DBUtils
from database.db_init import init_database
from algorithm.sort_algorithm import SortAlgorithm
from algorithm.search_algorithm import SearchAlgorithm

tourist_recommend_bp = Blueprint('tourist_recommend', __name__)

def get_session():
    _, SessionLocal = init_database()
    return SessionLocal()

@tourist_recommend_bp.route('/list', methods=['GET'])
def get_recommend_list():
    """获取推荐列表（只排前10）"""
    session = get_session()
    try:
        # 获取所有景区
        scenics = session.query(Scenic).all()
        
        # 按热度和评分排序（只排前10）
        sorted_scenics = SortAlgorithm.top_n_sort(scenics, lambda x: x.hotness * 0.3 + x.rating * 0.7, n=10)
        
        # 构建响应数据
        data = []
        for scenic in sorted_scenics:
            data.append({
                'id': scenic.id,
                'name': scenic.name,
                'description': scenic.description,
                'hotness': scenic.hotness,
                'rating': scenic.rating,
                'category': scenic.category,
                'ticket_price': scenic.ticket_price,
                'open_time': scenic.open_time,
                'address': scenic.address,
                'lat': scenic.lat,
                'lng': scenic.lng
            })
        
        return jsonify({'status': 200, 'data': data})
    finally:
        session.close()

@tourist_recommend_bp.route('/sort', methods=['POST'])
def sort_recommend():
    """排序推荐"""
    data = request.json
    sort_by = data.get('sort_by', 'rating')  # 按评分排序
    category = data.get('category')
    
    session = get_session()
    try:
        query = session.query(Scenic)
        
        # 按类别筛选
        if category:
            query = query.filter_by(category=category)
        
        scenics = query.all()
        
        # 排序
        def key_func(item):
            if sort_by == 'hotness':
                return item.hotness
            elif sort_by == 'rating':
                return item.rating
            else:
                return item.id
        
        sorted_scenics = sorted(scenics, key=key_func, reverse=True)
        
        # 构建响应数据
        data = []
        for scenic in sorted_scenics:
            data.append({
                'id': scenic.id,
                'name': scenic.name,
                'hotness': scenic.hotness,
                'rating': scenic.rating
            })
        
        return jsonify({'status': 200, 'data': data})
    finally:
        session.close()
