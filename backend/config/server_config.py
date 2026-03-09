# 服务器配置
class ServerConfig:
    # 服务器运行端口
    PORT = 8080
    
    # 调试模式
    DEBUG = True
    
    # 跨域配置
    CORS_ORIGINS = ['http://localhost:8081', 'http://127.0.0.1:8081', 'http://localhost:8083', 'http://127.0.0.1:8083', 'http://localhost:8084', 'http://127.0.0.1:8084']  # 前端运行地址
    CORS_SUPPORTS_CREDENTIALS = True
    
    # 项目根路径
    BASE_DIR = '/api'
    
    # 密钥配置
    SECRET_KEY = 'tourism_system_secret_key_2026'
