# 日记接口
from flask import Blueprint, request, jsonify
from database.models import Diary, User
from database.db_utils import DBUtils
from database.db_init import init_database
from algorithm.sort_algorithm import SortAlgorithm
from algorithm.text_search import TextSearch
from algorithm.lossless_compression import LosslessCompression
from api.user_api import verify_token

diary_bp = Blueprint('diary', __name__)

def get_session():
    _, SessionLocal = init_database()
    return SessionLocal()

@diary_bp.route('/list', methods=['GET'])
def get_diary_list():
    """获取日记列表"""
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({'status': 401, 'msg': '未授权'})
    
    token = token.replace('Bearer ', '')
    user_id = verify_token(token)
    if not user_id:
        return jsonify({'status': 401, 'msg': 'token无效'})
    
    session = get_session()
    try:
        # 获取用户的日记
        diaries = session.query(Diary).filter_by(user_id=user_id).all()
        
        # 按创建时间排序
        diaries.sort(key=lambda x: x.create_time, reverse=True)
        
        # 构建响应数据
        data = []
        for diary in diaries:
            data.append({
                'id': diary.id,
                'title': diary.title,
                'content': diary.content[:100] + '...' if len(diary.content) > 100 else diary.content,
                'hotness': diary.hotness,
                'rating': diary.rating,
                'create_time': diary.create_time.strftime('%Y-%m-%d %H:%M:%S')
            })
        
        return jsonify({'status': 200, 'data': data})
    finally:
        session.close()

@diary_bp.route('/create', methods=['POST'])
def create_diary():
    """创建日记"""
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({'status': 401, 'msg': '未授权'})
    
    token = token.replace('Bearer ', '')
    user_id = verify_token(token)
    if not user_id:
        return jsonify({'status': 401, 'msg': 'token无效'})
    
    data = request.json
    title = data.get('title')
    content = data.get('content')
    scenic_id = data.get('scenic_id')
    
    if not title or not content:
        return jsonify({'status': 400, 'msg': '标题和内容不能为空'})
    
    session = get_session()
    try:
        # 压缩内容
        compressed_content = LosslessCompression.compress(content)
        
        # 创建日记
        diary = Diary(
            user_id=user_id,
            title=title,
            content=content,  # 存储原始内容
            scenic_id=scenic_id
        )
        session.add(diary)
        session.commit()
        
        return jsonify({'status': 200, 'msg': '日记创建成功', 'data': {'id': diary.id}})
    finally:
        session.close()
