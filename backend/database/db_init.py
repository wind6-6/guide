# 数据库初始化脚本
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from config.db_config import DBConfig
import random

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

# 生成景区数据（≥200个）
def generate_scenics():
    scenic_names = [
        "颐和园", "故宫", "长城", "天坛", "圆明园", "北海公园", "景山公园", "中山公园",
        "奥林匹克公园", "鸟巢", "水立方", "国家大剧院", "首都博物馆", "中国美术馆",
        "北京动物园", "北京植物园", "香山公园", "八大处公园", "潭柘寺", "戒台寺",
        "雍和宫", "白云观", "孔庙", "国子监", "恭王府", "什刹海", "南锣鼓巷",
        "前门大街", "王府井", "西单", "三里屯", "国贸", "中关村", "望京", "亚运村",
        "五道口", "知春路", "西直门", "东直门", "朝阳门", "建国门", "复兴门",
        "阜成门", "宣武门", "和平门", "正阳门", "崇文门", "安定门", "德胜门",
        "北京大学", "清华大学", "中国人民大学", "北京师范大学", "北京航空航天大学",
        "北京理工大学", "中国农业大学", "中央民族大学", "北京交通大学", "北京邮电大学",
        "北京化工大学", "北京科技大学", "北京林业大学", "北京中医药大学", "北京外国语大学",
        "北京语言大学", "中国传媒大学", "中央财经大学", "对外经济贸易大学", "中国政法大学",
        "华北电力大学", "中国矿业大学", "中国石油大学", "中国地质大学", "北京工业大学",
        "北京建筑大学", "北京印刷学院", "北京电子科技学院", "北京信息科技大学", "北京联合大学",
        "北京城市学院", "首都师范大学", "首都医科大学", "北京第二外国语学院", "北京物资学院",
        "首都经济贸易大学", "中国音乐学院", "中央美术学院", "中央戏剧学院", "中国戏曲学院",
        "北京电影学院", "北京舞蹈学院", "北京体育大学", "北京农学院", "北京石油化工学院",
        "北京工商大学", "北京服装学院", "北京机械工业学院", "北京吉利学院", "北京培黎职业学院",
        "北京科技职业学院", "北京汇佳职业学院", "北京北大方正软件职业技术学院", "北京经贸职业学院",
        "北京经济技术职业学院", "北京戏曲艺术职业学院", "北京艺术传媒职业学院", "北京网络职业学院",
        "天津大学", "南开大学", "天津师范大学", "天津工业大学", "天津理工大学", "天津科技大学",
        "天津财经大学", "天津外国语大学", "天津商业大学", "天津职业技术师范大学", "天津城建大学",
        "天津农学院", "天津音乐学院", "天津美术学院", "天津体育学院", "天津中德应用技术大学",
        "河北工业大学", "燕山大学", "河北大学", "河北师范大学", "河北农业大学", "河北医科大学",
        "河北科技大学", "河北经贸大学", "河北工程大学", "石家庄铁道大学", "华北理工大学",
        "河北地质大学", "河北建筑工程学院", "河北水利电力学院", "河北金融学院", "北华航天工业学院",
        "廊坊师范学院", "唐山师范学院", "沧州师范学院", "衡水学院", "邢台学院", "邯郸学院",
        "保定学院", "张家口学院", "承德医学院", "河北北方学院", "河北中医学院", "河北体育学院",
        "石家庄学院", "唐山学院", "华北科技学院", "防灾科技学院", "中央司法警官学院",
        "中国人民警察大学", "河北环境工程学院", "河北工业职业技术大学", "河北科技工程职业技术大学",
        "河北石油职业技术大学", "山西大学", "太原理工大学", "中北大学", "山西农业大学", "山西医科大学",
        "山西师范大学", "山西财经大学", "太原科技大学", "山西中医药大学", "长治医学院",
        "太原师范学院", "忻州师范学院", "运城学院", "晋中学院", "长治学院", "吕梁学院",
        "太原工业学院", "山西传媒学院", "山西工程技术学院", "山西能源学院", "山西警察学院",
        "山西应用科技学院", "山西工商学院", "内蒙古大学", "内蒙古科技大学", "内蒙古工业大学",
        "内蒙古农业大学", "内蒙古医科大学", "内蒙古师范大学", "内蒙古民族大学", "赤峰学院",
        "集宁师范学院", "呼伦贝尔学院", "呼和浩特民族学院", "包头师范学院", "河套学院",
        "鄂尔多斯应用技术学院", "辽宁大学", "大连理工大学", "东北大学", "大连海事大学",
        "中国医科大学", "东北财经大学", "辽宁师范大学", "沈阳师范大学", "渤海大学",
        "鞍山师范学院", "沈阳大学", "大连大学", "辽宁科技学院", "沈阳工程学院", "辽东学院",
        "辽宁对外经贸学院", "大连民族大学", "沈阳工学院", "大连科技学院", "沈阳城市建设学院",
        "大连艺术学院", "辽宁何氏医学院", "沈阳城市学院", "大连财经学院", "沈阳科技学院",
        "吉林大学", "东北师范大学", "延边大学", "长春理工大学", "东北电力大学", "长春工业大学",
        "吉林建筑大学", "吉林化工学院", "吉林农业大学", "长春中医药大学", "北华大学",
        "通化师范学院", "吉林师范大学", "吉林工程技术师范学院", "长春师范大学", "白城师范学院",
        "吉林财经大学", "吉林体育学院", "吉林艺术学院", "吉林工商学院", "长春工程学院",
        "吉林农业科技学院", "吉林警察学院", "长春大学", "吉林外国语大学", "长春光华学院",
        "长春工业大学人文信息学院", "长春理工大学光电信息学院", "长春财经学院", "吉林建筑科技学院",
        "长春建筑学院", "长春科技学院", "吉林动画学院", "长春大学旅游学院", "东北师范大学人文学院"
    ]
    
    categories = ["历史文化", "自然风光", "主题公园", "现代建筑", "宗教文化", "教育科研", "商业休闲", "体育健身"]
    
    scenics = []
    for i in range(min(200, len(scenic_names))):
        scenics.append({
            "name": scenic_names[i],
            "description": f"{scenic_names[i]}是一个著名的旅游景点，拥有悠久的历史和丰富的文化内涵。",
            "hotness": round(random.uniform(5.0, 10.0), 1),
            "rating": round(random.uniform(3.5, 5.0), 1),
            "category": random.choice(categories),
            "address": f"北京市区{i+1}号",
            "open_time": "08:00-18:00",
            "ticket_price": f"{random.randint(20, 200)}元"
        })
    return scenics

# 生成建筑物数据（每个景区≥20个）
def generate_buildings(scenic_count):
    building_types = ["景点", "教学楼", "图书馆", "实验室", "体育馆", "食堂", "宿舍", "办公楼", "博物馆", "纪念馆"]
    buildings = []
    
    for scenic_id in range(1, scenic_count + 1):
        # 每个景区生成20-30个建筑物
        for i in range(20):
            buildings.append({
                "name": f"建筑{scenic_id}-{i+1}",
                "scenic_id": scenic_id,
                "description": f"这是{scenic_id}号景区的第{i+1}个建筑物",
                "type": random.choice(building_types),
                "floor": random.randint(1, 10),
                "area": random.randint(100, 10000)
            })
    return buildings

# 生成设施数据（≥50个，≥10种类型）
def generate_facilities(scenic_count):
    facility_types = ["卫生间", "商店", "饭店", "图书馆", "食堂", "超市", "咖啡馆", "医务室", "停车场", "休息区", "ATM", "快递点", "打印店", "理发店", "洗衣房"]
    facilities = []
    
    for scenic_id in range(1, scenic_count + 1):
        # 每个景区生成3-5个设施
        for i in range(random.randint(3, 5)):
            for facility_type in facility_types:
                facilities.append({
                    "name": f"{scenic_id}号{facility_type}{i+1}",
                    "scenic_id": scenic_id,
                    "type": facility_type,
                    "location": f"{scenic_id}号景区{facility_type}区域{i+1}",
                    "description": f"提供{facility_type}服务"
                })
    return facilities

# 生成道路数据（≥200条）
def generate_roads(scenic_count):
    roads = []
    transport_types = ["步行", "自行车", "电瓶车", "汽车"]
    
    for scenic_id in range(1, scenic_count + 1):
        # 每个景区生成至少10条道路
        for i in range(10):
            roads.append({
                "scenic_id": scenic_id,
                "start_node": f"S{scenic_id}-Node{i}",
                "end_node": f"S{scenic_id}-Node{i+1}",
                "distance": random.randint(50, 500),
                "crowd_level": random.randint(1, 5),
                "transport_type": random.choice(transport_types)
            })
    
    # 确保至少有200条道路
    while len(roads) < 200:
        scenic_id = random.randint(1, scenic_count)
        i = len(roads)
        roads.append({
            "scenic_id": scenic_id,
            "start_node": f"S{scenic_id}-Node{i}",
            "end_node": f"S{scenic_id}-Node{i+1}",
            "distance": random.randint(50, 500),
            "crowd_level": random.randint(1, 5),
            "transport_type": random.choice(transport_types)
        })
    
    return roads

# 生成用户数据（≥10人）
def generate_users():
    users = []
    for i in range(15):  # 生成15个用户，超过最低要求
        users.append({
            "username": f"user{i+1}" if i > 0 else "admin",
            "password": __import__('hashlib').md5("123456".encode()).hexdigest(),
            "name": f"用户{i+1}" if i > 0 else "管理员",
            "phone": f"1380013800{i}",
            "email": f"user{i+1}@example.com" if i > 0 else "admin@example.com"
        })
    return users

# 生成美食数据
def generate_foods(scenic_count):
    cuisines = ["川菜", "粤菜", "鲁菜", "淮扬菜", "湘菜", "浙菜", "闽菜", "徽菜", "京菜", "东北菜"]
    foods = []
    
    for scenic_id in range(1, scenic_count + 1):
        for i in range(5):  # 每个景区5个美食
            foods.append({
                "name": f"美食{scenic_id}-{i+1}",
                "scenic_id": scenic_id,
                "description": f"{scenic_id}号景区的特色美食",
                "hotness": round(random.uniform(5.0, 10.0), 1),
                "rating": round(random.uniform(3.5, 5.0), 1),
                "cuisine": random.choice(cuisines),
                "price": random.randint(20, 200)
            })
    return foods

# 生成日记数据
def generate_diaries(user_count, scenic_count):
    diaries = []
    
    for user_id in range(1, user_count + 1):
        for i in range(3):  # 每个用户3篇日记
            diaries.append({
                "user_id": user_id,
                "title": f"用户{user_id}的游记{i+1}",
                "content": f"这是用户{user_id}的第{i+1}篇旅游日记，记录了一次难忘的旅行经历。",
                "scenic_id": random.randint(1, scenic_count),
                "hotness": random.randint(10, 1000),
                "rating": round(random.uniform(3.0, 5.0), 1)
            })
    return diaries

# 插入初始数据
def insert_initial_data():
    from database.models import User, Scenic, Building, Facility, Road, Diary, Food, Navigation
    
    engine, SessionLocal = init_database()
    session = SessionLocal()
    
    try:
        # 插入用户数据（≥10人）
        users = generate_users()
        for user_data in users:
            user = User(**user_data)
            session.add(user)
        session.commit()
        print(f"插入{len(users)}个用户")
        
        # 插入景区数据（≥200个）
        scenics = generate_scenics()
        for scenic_data in scenics:
            scenic = Scenic(**scenic_data)
            session.add(scenic)
        session.commit()
        print(f"插入{len(scenics)}个景区")
        
        scenic_count = len(scenics)
        
        # 插入建筑物数据（每个景区≥20个）
        buildings = generate_buildings(scenic_count)
        for building_data in buildings:
            building = Building(**building_data)
            session.add(building)
        session.commit()
        print(f"插入{len(buildings)}个建筑物")
        
        # 插入设施数据（≥50个，≥10种类型）
        facilities = generate_facilities(scenic_count)
        for facility_data in facilities:
            facility = Facility(**facility_data)
            session.add(facility)
        session.commit()
        print(f"插入{len(facilities)}个设施")
        
        # 插入道路数据（≥200条）
        roads = generate_roads(scenic_count)
        for road_data in roads:
            road = Road(**road_data)
            session.add(road)
        session.commit()
        print(f"插入{len(roads)}条道路")
        
        # 插入美食数据
        foods = generate_foods(scenic_count)
        for food_data in foods:
            food = Food(**food_data)
            session.add(food)
        session.commit()
        print(f"插入{len(foods)}个美食")
        
        # 插入日记数据
        diaries = generate_diaries(len(users), scenic_count)
        for diary_data in diaries:
            diary = Diary(**diary_data)
            session.add(diary)
        session.commit()
        print(f"插入{len(diaries)}篇日记")
        
        print("初始数据插入完成")
        
    except Exception as e:
        print(f"数据插入失败: {e}")
        session.rollback()
        raise
    finally:
        session.close()
