# 旅游推荐接口
from flask import Blueprint, request, jsonify
from database.models.scenic_model import Scenic
from database.models.building_model import Building
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
    """获取推荐列表（返回所有200个景区）"""
    session = get_session()
    try:
        # 获取所有景区
        scenics = session.query(Scenic).all()
        
        # 按热度和评分排序（返回所有200个景区）
        sorted_scenics = SortAlgorithm.top_n_sort(scenics, lambda x: x.hotness * 0.3 + x.rating * 0.7, n=200)
        
        # 构建响应数据
        response_data = []
        for scenic in sorted_scenics:
            response_data.append({
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
        
        return jsonify({'status': 200, 'data': response_data})
    finally:
        session.close()

@tourist_recommend_bp.route('/top10', methods=['GET'])
def get_top10():
    """获取前10个推荐景点或学校"""
    session = get_session()
    try:
        # 获取所有景区
        scenics = session.query(Scenic).all()
        
        # 使用top_n_sort算法获取前10个，无需完全排序
        top10_scenics = SortAlgorithm.top_n_sort(scenics, lambda x: x.hotness * 0.3 + x.rating * 0.7, n=10)
        
        # 构建响应数据
        response_data = []
        for scenic in top10_scenics:
            response_data.append({
                'id': scenic.id,
                'name': scenic.name,
                'hotness': scenic.hotness,
                'rating': scenic.rating,
                'category': scenic.category
            })
        
        return jsonify({'status': 200, 'data': response_data})
    finally:
        session.close()

@tourist_recommend_bp.route('/sort', methods=['POST'])
def sort_recommend():
    """排序推荐"""
    request_data = request.json
    sort_by = request_data.get('sort_by', 'rating')  # 按评分排序
    category = request_data.get('category')
    
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
        response_data = []
        for scenic in sorted_scenics:
            response_data.append({
                'id': scenic.id,
                'name': scenic.name,
                'hotness': scenic.hotness,
                'rating': scenic.rating
            })
        
        return jsonify({'status': 200, 'data': response_data})
    finally:
        session.close()

@tourist_recommend_bp.route('/search', methods=['POST'])
def search_recommend():
    """搜索推荐"""
    request_data = request.json
    if not request_data:
        return jsonify({'status': 400, 'message': '请求数据为空'})
    
    keyword = request_data.get('keyword', '')
    category = request_data.get('category', '')
    sort_by = request_data.get('sort_by', 'rating')
    
    print(f"DEBUG: keyword={keyword}, category={category}, sort_by={sort_by}")
    
    session = get_session()
    try:
        query = session.query(Scenic)
        
        # 按类别筛选
        if category:
            query = query.filter_by(category=category)
        
        scenics = query.all()
        print(f"DEBUG: total scenics: {len(scenics)}")
        
        # 搜索
        search_results = []
        if keyword:
            # 按名称搜索
            name_results = SearchAlgorithm.fuzzy_search(scenics, 'name', keyword)
            # 按描述搜索
            desc_results = SearchAlgorithm.fuzzy_search(scenics, 'description', keyword)
            # 按地址搜索
            addr_results = SearchAlgorithm.fuzzy_search(scenics, 'address', keyword)
            
            print(f"DEBUG: name_results count: {len(name_results)}")
            print(f"DEBUG: desc_results count: {len(desc_results)}")
            print(f"DEBUG: addr_results count: {len(addr_results)}")
            
            # 合并结果，去重
            seen_ids = set()
            for result in name_results + desc_results + addr_results:
                if result.id not in seen_ids:
                    search_results.append(result)
                    seen_ids.add(result.id)
            
            print(f"DEBUG: search_results count: {len(search_results)}")
        else:
            search_results = scenics
        
        # 排序
        def key_func(item):
            if sort_by == 'hotness':
                return item.hotness
            elif sort_by == 'rating':
                return item.rating
            else:
                return item.id
        
        sorted_results = sorted(search_results, key=key_func, reverse=True)
        
        # 构建响应数据
        response_data = []
        for scenic in sorted_results:
            response_data.append({
                'id': scenic.id,
                'name': scenic.name,
                'description': scenic.description,
                'hotness': scenic.hotness,
                'rating': scenic.rating,
                'category': scenic.category,
                'address': scenic.address
            })
        
        print(f"DEBUG: response_data count: {len(response_data)}")
        return jsonify({'status': 200, 'data': response_data})
    finally:
        session.close()

@tourist_recommend_bp.route('/personalized', methods=['POST'])
def personalized_recommend():
    """个性化推荐"""
    request_data = request.json
    interests = request_data.get('interests', [])  # 用户兴趣标签
    
    session = get_session()
    try:
        # 获取所有景区
        scenics = session.query(Scenic).all()
        
        # 个性化推荐算法
        def personal_key_func(item):
            # 基础分数
            base_score = item.hotness * 0.3 + item.rating * 0.7
            
            # 兴趣匹配分数
            interest_score = 0
            if interests:
                # 检查景区类别是否与用户兴趣匹配
                if item.category and any(interest.lower() in item.category.lower() for interest in interests):
                    interest_score += 2.0
                # 检查景区名称是否与用户兴趣匹配
                if any(interest.lower() in item.name.lower() for interest in interests):
                    interest_score += 1.5
                # 检查景区描述是否与用户兴趣匹配
                if item.description:
                    if any(interest.lower() in item.description.lower() for interest in interests):
                        interest_score += 1.0
            
            return base_score + interest_score
        
        # 使用top_n_sort获取前20个推荐
        personalized_scenics = SortAlgorithm.top_n_sort(scenics, personal_key_func, n=20)
        
        # 构建响应数据
        response_data = []
        for scenic in personalized_scenics:
            response_data.append({
                'id': scenic.id,
                'name': scenic.name,
                'description': scenic.description,
                'hotness': scenic.hotness,
                'rating': scenic.rating,
                'category': scenic.category,
                'address': scenic.address
            })
        
        return jsonify({'status': 200, 'data': response_data})
    finally:
        session.close()
