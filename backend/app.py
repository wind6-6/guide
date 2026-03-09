# 后端入口文件
from flask import Flask
from flask_cors import CORS
from config.server_config import ServerConfig
from config.db_config import DBConfig
from api import api_bp
from database.db_init import init_database, create_tables, insert_initial_data
from utils.log_utils import LogUtils

# 初始化日志
logger = LogUtils.setup_logger()

# 创建Flask应用
app = Flask(__name__)

# 配置应用
app.config['SECRET_KEY'] = ServerConfig.SECRET_KEY
app.config['DEBUG'] = ServerConfig.DEBUG

# 配置数据库
app.config['SQLALCHEMY_DATABASE_URI'] = DBConfig.get_db_url()
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 配置跨域
CORS(app, origins=ServerConfig.CORS_ORIGINS, supports_credentials=ServerConfig.CORS_SUPPORTS_CREDENTIALS)

# 注册API蓝图
app.register_blueprint(api_bp)

# 健康检查
@app.route('/health')
def health_check():
    return {'status': 'ok'}

if __name__ == '__main__':
    # 初始化数据库
    try:
        create_tables()
        insert_initial_data()
        logger.info("数据库初始化完成")
    except Exception as e:
        logger.error(f"数据库初始化失败: {e}")
    
    # 启动服务
    logger.info(f"启动服务，端口: {ServerConfig.PORT}")
    app.run(host='0.0.0.0', port=ServerConfig.PORT, debug=ServerConfig.DEBUG)
