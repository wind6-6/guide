# 数据库配置
class DBConfig:
    # 数据库类型：mysql 或 sqlite
    DB_TYPE = 'sqlite'  # 可切换为 'mysql'
    
    # MySQL 配置
    MYSQL_HOST = 'localhost'
    MYSQL_PORT = 3306
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = '123456'  # 本地数据库密码
    MYSQL_DATABASE = 'tourism_system'
    
    # SQLite 配置
    SQLITE_PATH = 'tourism.db'
    
    # 数据库 URL 构建
    @classmethod
    def get_db_url(cls):
        if cls.DB_TYPE == 'mysql':
            return f"mysql+pymysql://{cls.MYSQL_USER}:{cls.MYSQL_PASSWORD}@{cls.MYSQL_HOST}:{cls.MYSQL_PORT}/{cls.MYSQL_DATABASE}?charset=utf8mb4"
        else:
            return f"sqlite:///{cls.SQLITE_PATH}"
