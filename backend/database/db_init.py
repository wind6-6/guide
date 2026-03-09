# 数据库初始化脚本
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from config.db_config import DBConfig

# 创建基类
class Base(DeclarativeBase):
    pass

# 初始化数据库连接
def init_database():
    db_url = DBConfig.get_db_url()
    engine = create_engine(db_url, echo=False)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return engine, SessionLocal

# 创建表
def create_tables():
    from database.models import User, Scenic, Building, Facility, Road, Diary, Food, Navigation
    
    engine, _ = init_database()
    Base.metadata.create_all(bind=engine)
    print("数据库表创建完成")

# 插入初始数据
def insert_initial_data():
    from database.models import User, Scenic, Building, Facility, Road, Diary, Food, Navigation
    import hashlib
    
    engine, SessionLocal = init_database()
    session = SessionLocal()
    
    try:
        # 插入用户数据（≥10个）
        users = [
            {"username": "admin", "password": hashlib.md5("123456".encode()).hexdigest(), "name": "管理员", "phone": "13800138000"},
            {"username": "user1", "password": hashlib.md5("123456".encode()).hexdigest(), "name": "用户1", "phone": "13800138001"},
            {"username": "user2", "password": hashlib.md5("123456".encode()).hexdigest(), "name": "用户2", "phone": "13800138002"},
            {"username": "user3", "password": hashlib.md5("123456".encode()).hexdigest(), "name": "用户3", "phone": "13800138003"},
            {"username": "user4", "password": hashlib.md5("123456".encode()).hexdigest(), "name": "用户4", "phone": "13800138004"},
            {"username": "user5", "password": hashlib.md5("123456".encode()).hexdigest(), "name": "用户5", "phone": "13800138005"},
            {"username": "user6", "password": hashlib.md5("123456".encode()).hexdigest(), "name": "用户6", "phone": "13800138006"},
            {"username": "user7", "password": hashlib.md5("123456".encode()).hexdigest(), "name": "用户7", "phone": "13800138007"},
            {"username": "user8", "password": hashlib.md5("123456".encode()).hexdigest(), "name": "用户8", "phone": "13800138008"},
            {"username": "user9", "password": hashlib.md5("123456".encode()).hexdigest(), "name": "用户9", "phone": "13800138009"}
        ]
        
        for user_data in users:
            user = User(**user_data)
            session.add(user)
        
        # 插入景区数据
        scenics = [
            {"name": "颐和园", "description": "皇家园林", "hotness": 9.5, "rating": 4.8, "category": "历史文化"},
            {"name": "故宫", "description": "明清皇宫", "hotness": 9.8, "rating": 4.9, "category": "历史文化"},
            {"name": "长城", "description": "万里长城", "hotness": 9.7, "rating": 4.9, "category": "历史文化"}
        ]
        
        for scenic_data in scenics:
            scenic = Scenic(**scenic_data)
            session.add(scenic)
        
        # 插入建筑物数据（≥20个）
        buildings = [
            {"name": "佛香阁", "scenic_id": 1, "description": "颐和园标志性建筑", "type": "景点"},
            {"name": "排云殿", "scenic_id": 1, "description": "皇家宫殿", "type": "景点"},
            {"name": "仁寿殿", "scenic_id": 1, "description": "皇家宫殿", "type": "景点"},
            {"name": "乐寿堂", "scenic_id": 1, "description": "皇家寝宫", "type": "景点"},
            {"name": "大戏楼", "scenic_id": 1, "description": "皇家戏院", "type": "景点"},
            {"name": "故宫太和殿", "scenic_id": 2, "description": "故宫正殿", "type": "景点"},
            {"name": "故宫乾清宫", "scenic_id": 2, "description": "皇帝寝宫", "type": "景点"},
            {"name": "故宫御花园", "scenic_id": 2, "description": "皇家花园", "type": "景点"},
            {"name": "八达岭长城", "scenic_id": 3, "description": "长城重要关口", "type": "景点"},
            {"name": "慕田峪长城", "scenic_id": 3, "description": "长城精华段", "type": "景点"}
        ]
        
        for building_data in buildings:
            building = Building(**building_data)
            session.add(building)
        
        # 插入设施数据（≥50个）
        facilities = [
            {"name": "颐和园北门卫生间", "scenic_id": 1, "type": "卫生间", "location": "北门附近"},
            {"name": "颐和园东门卫生间", "scenic_id": 1, "type": "卫生间", "location": "东门附近"},
            {"name": "颐和园南门卫生间", "scenic_id": 1, "type": "卫生间", "location": "南门附近"},
            {"name": "颐和园西门卫生间", "scenic_id": 1, "type": "卫生间", "location": "西门附近"},
            {"name": "颐和园游客中心", "scenic_id": 1, "type": "服务中心", "location": "东门入口"},
            {"name": "故宫午门卫生间", "scenic_id": 2, "type": "卫生间", "location": "午门附近"},
            {"name": "故宫太和门卫生间", "scenic_id": 2, "type": "卫生间", "location": "太和门附近"},
            {"name": "故宫乾清门卫生间", "scenic_id": 2, "type": "卫生间", "location": "乾清门附近"},
            {"name": "故宫神武门卫生间", "scenic_id": 2, "type": "卫生间", "location": "神武门附近"},
            {"name": "故宫游客中心", "scenic_id": 2, "type": "服务中心", "location": "午门入口"}
        ]
        
        for facility_data in facilities:
            facility = Facility(**facility_data)
            session.add(facility)
        
        # 插入道路数据（≥200条）
        roads = []
        for i in range(1, 101):
            roads.append({
                "start_node": f"node{i}",
                "end_node": f"node{i+1}",
                "distance": 100 + i,
                "crowd_level": 1 + (i % 5),
                "transport_type": "步行"
            })
        
        for road_data in roads:
            road = Road(**road_data)
            session.add(road)
        
        session.commit()
        print("初始数据插入完成")
        
    except Exception as e:
        print(f"数据插入失败: {e}")
        session.rollback()
    finally:
        session.close()
