# API模块初始化
from flask import Blueprint
from .user_api import user_bp
from .tourist_recommend_api import tourist_recommend_bp
from .route_plan_api import route_plan_bp
from .place_query_api import place_query_bp
from .diary_api import diary_bp
from .food_recommend_api import food_recommend_bp

# 创建蓝图
api_bp = Blueprint('api', __name__, url_prefix='/api')

# 注册子蓝图
api_bp.register_blueprint(user_bp, url_prefix='/user')
api_bp.register_blueprint(tourist_recommend_bp, url_prefix='/recommend')
api_bp.register_blueprint(route_plan_bp, url_prefix='/route')
api_bp.register_blueprint(place_query_bp, url_prefix='/place')
api_bp.register_blueprint(diary_bp, url_prefix='/diary')
api_bp.register_blueprint(food_recommend_bp, url_prefix='/food')

__all__ = ['api_bp']
