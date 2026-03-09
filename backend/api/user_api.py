# 用户接口
from flask import Blueprint, request, jsonify
from database.models import User
from database.db_utils import DBUtils
from database.db_init import init_database
import jwt
import hashlib
from config.server_config import ServerConfig

user_bp = Blueprint('user', __name__)

# 初始化数据库
def get_session():
    _, SessionLocal = init_database()
    return SessionLocal()

# 密码加密
def hash_password(password):
    return hashlib.md5(password.encode()).hexdigest()

# 生成token
def generate_token(user_id):
    payload = {'user_id': user_id}
    return jwt.encode(payload, ServerConfig.SECRET_KEY, algorithm='HS256')

# 验证token
def verify_token(token):
    try:
        payload = jwt.decode(token, ServerConfig.SECRET_KEY, algorithms=['HS256'])
        return payload.get('user_id')
    except:
        return None

@user_bp.route('/login', methods=['POST'])
def login():
    """用户登录"""
    data = request.json
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({'status': 400, 'msg': '用户名和密码不能为空'})
    
    session = get_session()
    try:
        user = session.query(User).filter_by(username=username).first()
        if not user:
            return jsonify({'status': 400, 'msg': '用户名不存在'})
        
        # 验证密码
        if user.password != hash_password(password):
            return jsonify({'status': 400, 'msg': '密码错误'})
        
        # 生成token
        token = generate_token(user.id)
        
        return jsonify({
            'status': 200,
            'msg': '登录成功',
            'data': {
                'token': token,
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'name': user.name,
                    'phone': user.phone
                }
            }
        })
    finally:
        session.close()

@user_bp.route('/register', methods=['POST'])
def register():
    """用户注册"""
    data = request.json
    username = data.get('username')
    password = data.get('password')
    name = data.get('name')
    phone = data.get('phone')
    
    if not username or not password or not name:
        return jsonify({'status': 400, 'msg': '用户名、密码和姓名不能为空'})
    
    session = get_session()
    try:
        # 检查用户名是否已存在
        existing_user = session.query(User).filter_by(username=username).first()
        if existing_user:
            return jsonify({'status': 400, 'msg': '用户名已存在'})
        
        # 创建新用户
        user = User(
            username=username,
            password=hash_password(password),
            name=name,
            phone=phone
        )
        session.add(user)
        session.commit()
        
        return jsonify({'status': 200, 'msg': '注册成功'})
    finally:
        session.close()

@user_bp.route('/info', methods=['GET'])
def get_user_info():
    """获取用户信息"""
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({'status': 401, 'msg': '未授权'})
    
    # 提取token
    token = token.replace('Bearer ', '')
    user_id = verify_token(token)
    if not user_id:
        return jsonify({'status': 401, 'msg': 'token无效'})
    
    session = get_session()
    try:
        user = session.query(User).filter_by(id=user_id).first()
        if not user:
            return jsonify({'status': 404, 'msg': '用户不存在'})
        
        return jsonify({
            'status': 200,
            'data': {
                'id': user.id,
                'username': user.username,
                'name': user.name,
                'phone': user.phone,
                'email': user.email
            }
        })
    finally:
        session.close()
