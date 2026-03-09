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
    """创建日记（支持无损压缩）"""
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
    images = data.get('images', [])  # 图片列表
    videos = data.get('videos', [])  # 视频列表
    
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
            compressed_content=compressed_content,  # 存储压缩内容
            scenic_id=scenic_id,
            images=','.join(images) if images else '',
            videos=','.join(videos) if videos else ''
        )
        session.add(diary)
        session.commit()
        
        return jsonify({'status': 200, 'msg': '日记创建成功', 'data': {'id': diary.id}})
    finally:
        session.close()

@diary_bp.route('/search', methods=['GET'])
def search_diaries():
    """搜索日记（按目的地/名称/内容检索）"""
    keyword = request.args.get('keyword', '')
    scenic_id = request.args.get('scenic_id')
    
    session = get_session()
    try:
        query = session.query(Diary)
        
        # 按景区筛选
        if scenic_id:
            query = query.filter_by(scenic_id=scenic_id)
        
        diaries = query.all()
        
        # 文本搜索
        if keyword:
            results = []
            for diary in diaries:
                # 搜索标题和内容
                title_match = keyword.lower() in diary.title.lower()
                content_match = keyword.lower() in diary.content.lower()
                
                if title_match or content_match:
                    # 计算匹配度
                    match_score = 0
                    if title_match:
                        match_score += 2
                    if content_match:
                        match_score += 1
                    results.append((match_score, diary))
            
            # 按匹配度排序
            results.sort(key=lambda x: x[0], reverse=True)
            diaries = [item for _, item in results]
        
        # 构建响应数据
        data = []
        for diary in diaries:
            data.append({
                'id': diary.id,
                'title': diary.title,
                'content': diary.content[:200] + '...' if len(diary.content) > 200 else diary.content,
                'hotness': diary.hotness,
                'rating': diary.rating,
                'create_time': diary.create_time.strftime('%Y-%m-%d %H:%M:%S')
            })
        
        return jsonify({'status': 200, 'data': data})
    finally:
        session.close()

@diary_bp.route('/generate-animation', methods=['POST'])
def generate_animation():
    """AIGC生成旅游动画（照片+文字）"""
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({'status': 401, 'msg': '未授权'})
    
    token = token.replace('Bearer ', '')
    user_id = verify_token(token)
    if not user_id:
        return jsonify({'status': 401, 'msg': 'token无效'})
    
    data = request.json
    diary_id = data.get('diary_id')
    
    if not diary_id:
        return jsonify({'status': 400, 'msg': '日记ID不能为空'})
    
    session = get_session()
    try:
        diary = session.query(Diary).filter_by(id=diary_id, user_id=user_id).first()
        if not diary:
            return jsonify({'status': 404, 'msg': '日记不存在'})
        
        # 模拟AIGC生成动画
        # 实际应用中这里应该调用AIGC服务
        animation_url = f"/animations/diary_{diary_id}.mp4"
        
        return jsonify({
            'status': 200,
            'msg': '动画生成成功',
            'data': {
                'animation_url': animation_url,
                'title': diary.title,
                'preview': f"基于{diary.title}生成的旅游动画"
            }
        })
    finally:
        session.close()
