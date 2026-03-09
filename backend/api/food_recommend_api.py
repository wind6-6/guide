# 美食推荐接口
from flask import Blueprint, request, jsonify
from database.models import Food
from database.db_utils import DBUtils
from database.db_init import init_database
from algorithm.sort_algorithm import SortAlgorithm
from algorithm.search_algorithm import SearchAlgorithm

food_recommend_bp = Blueprint('food_recommend', __name__)

def get_session():
    _, SessionLocal = init_database()
    return SessionLocal()

@food_recommend_bp.route('/list', methods=['GET'])
def get_food_list():
    """获取美食列表"""
    cuisine = request.args.get('cuisine')
    
    session = get_session()
    try:
        query = session.query(Food)
        
        # 按菜系筛选
        if cuisine:
            query = query.filter_by(cuisine=cuisine)
        
        foods = query.all()
        
        # 按热度和评分排序
        sorted_foods = SortAlgorithm.weighted_sort(foods)
        
        # 构建响应数据
        data = []
        for food in sorted_foods:
            data.append({
                'id': food.id,
                'name': food.name,
                'description': food.description,
                'hotness': food.hotness,
                'rating': food.rating,
                'cuisine': food.cuisine,
                'price': food.price
            })
        
        return jsonify({'status': 200, 'data': data})
    finally:
        session.close()

@food_recommend_bp.route('/recommend', methods=['GET'])
def recommend_food():
    """美食推荐"""
    scenic_id = request.args.get('scenic_id')
    
    session = get_session()
    try:
        query = session.query(Food)
        
        # 按景区筛选
        if scenic_id:
            query = query.filter_by(scenic_id=scenic_id)
        
        foods = query.all()
        
        # 取前10个推荐
        top_foods = SortAlgorithm.top_n_sort(foods, lambda x: x.rating * 0.7 + x.hotness * 0.3)
        
        # 构建响应数据
        data = []
        for food in top_foods:
            data.append({
                'id': food.id,
                'name': food.name,
                'rating': food.rating,
                'cuisine': food.cuisine
            })
        
        return jsonify({'status': 200, 'data': data})
    finally:
        session.close()
