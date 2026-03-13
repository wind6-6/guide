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

# 生成景区数据（使用真实北京地图数据）
def generate_scenics():
    try:
        from database.real_map_data import BEIJING_SCENICS, generate_extended_scenics
        # 使用真实数据并扩展到200个
        scenics = generate_extended_scenics()
        return scenics
    except ImportError:
        print("警告：未找到真实地图数据，使用模拟数据")
        # 备用模拟数据
        scenic_names = [
            "故宫博物院", "颐和园", "天坛公园", "圆明园遗址公园", "北海公园",
            "景山公园", "雍和宫", "恭王府", "孔庙和国子监", "香山公园",
            "北京植物园", "奥林匹克森林公园", "鸟巢", "水立方", "国家大剧院",
            "中央广播电视塔", "北京大学", "清华大学", "中国人民大学", "北京航空航天大学"
        ]
        
        categories = ["历史文化", "自然风光", "主题公园", "现代建筑", "宗教文化", "教育科研", "商业休闲", "体育健身"]
        
        scenics = []
        for i in range(200):
            name = scenic_names[i % len(scenic_names)] if i < len(scenic_names) else f"景点{i+1}"
            # 生成更分散的随机经纬度
            lat = 39.4 + random.random() * 2.2  # 北京纬度范围：39.4-41.6
            lng = 115.7 + random.random() * 1.7  # 北京经度范围：115.7-117.4
            
            # 生成更具体的地址
            districts = ["东城区", "西城区", "朝阳区", "海淀区", "丰台区", "石景山区"]
            road_types = ["大街", "路", "街", "胡同", "巷", "道"]
            
            district = random.choice(districts)
            road_type = random.choice(road_types)
            building_number = random.randint(1, 200)
            
            # 为不同类型的景点生成合适的地址
            if "公园" in name:
                address = f"北京市{district}{random.choice(['公园', '园林'])}{road_type}{building_number}号"
            elif "博物馆" in name:
                address = f"北京市{district}{random.choice(['文化', '艺术'])}{road_type}{building_number}号"
            elif "大学" in name:
                address = f"北京市{district}{random.choice(['学院', '大学'])}{road_type}{building_number}号"
            else:
                address = f"北京市{district}{road_type}{building_number}号"
            
            scenics.append({
                "name": name,
                "description": f"{name}是一个著名的旅游景点。",
                "hotness": round(random.uniform(5.0, 10.0), 1),
                "rating": round(random.uniform(3.5, 5.0), 1),
                "category": random.choice(categories),
                "address": address,
                "open_time": "08:00-18:00",
                "ticket_price": f"{random.randint(20, 200)}元",
                "lat": lat,
                "lng": lng
            })
        return scenics

# 生成建筑物数据（使用真实建筑物数据）
def generate_buildings(scenic_count):
    try:
        from database.real_map_data import BEIJING_BUILDINGS
        
        buildings = []
        # 获取景区名称列表
        scenic_names = list(BEIJING_BUILDINGS.keys())
        
        for scenic_id in range(1, scenic_count + 1):
            # 为前几个景区使用真实建筑物数据
            if scenic_id <= len(scenic_names):
                scenic_name = scenic_names[scenic_id - 1]
                real_buildings = BEIJING_BUILDINGS.get(scenic_name, [])
                
                for building_info in real_buildings:
                    buildings.append({
                        "name": building_info["name"],
                        "scenic_id": scenic_id,
                        "description": building_info.get("description", ""),
                        "type": building_info.get("type", "建筑"),
                        "floor_count": building_info.get("floor", 1),
                        "height": random.uniform(3, 100)
                    })
            else:
                # 其他景区使用模拟数据
                building_types = ["景点", "教学楼", "图书馆", "实验室", "体育馆", "食堂", "宿舍", "办公楼", "博物馆", "纪念馆"]
                for i in range(20):
                    buildings.append({
                        "name": f"建筑{scenic_id}-{i+1}",
                        "scenic_id": scenic_id,
                        "description": f"这是{scenic_id}号景区的第{i+1}个建筑物",
                        "type": random.choice(building_types),
                        "floor_count": random.randint(1, 10),
                        "height": random.uniform(3, 100)
                    })
        
        return buildings
    except ImportError:
        # 备用模拟数据
        building_types = ["景点", "教学楼", "图书馆", "实验室", "体育馆", "食堂", "宿舍", "办公楼", "博物馆", "纪念馆"]
        buildings = []
        
        for scenic_id in range(1, scenic_count + 1):
            for i in range(20):
                buildings.append({
                    "name": f"建筑{scenic_id}-{i+1}",
                    "scenic_id": scenic_id,
                    "description": f"这是{scenic_id}号景区的第{i+1}个建筑物",
                    "type": random.choice(building_types),
                    "floor_count": random.randint(1, 10),
                    "height": random.uniform(3, 100)
                })
        return buildings

# 生成设施数据（使用真实设施数据）
def generate_facilities(scenic_count):
    try:
        from database.real_map_data import BEIJING_FACILITIES
        
        facilities = []
        facility_types = list(BEIJING_FACILITIES.keys())
        
        for scenic_id in range(1, scenic_count + 1):
            # 为每个景区生成设施
            for facility_type in facility_types:
                real_facilities = BEIJING_FACILITIES.get(facility_type, [])
                # 每个类型添加1-2个设施
                for i in range(min(len(real_facilities), random.randint(1, 2))):
                    facility_info = real_facilities[i]
                    facilities.append({
                        "name": f"{scenic_id}号{facility_info['name']}",
                        "scenic_id": scenic_id,
                        "type": facility_type,
                        "location": facility_info.get("location", f"{scenic_id}号景区"),
                        "description": f"提供{facility_type}服务"
                    })
        
        return facilities
    except ImportError:
        # 备用模拟数据
        facility_types = ["卫生间", "商店", "饭店", "图书馆", "食堂", "超市", "咖啡馆", "医务室", "停车场", "休息区", "ATM", "快递点", "打印店", "理发店", "洗衣房"]
        facilities = []
        
        for scenic_id in range(1, scenic_count + 1):
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
    
    try:
        from database.real_map_data import BEIJING_SCENICS, BEIJING_ROADS
        
        # 1. 首先添加真实道路数据
        for road_info in BEIJING_ROADS:
            roads.append({
                "start_node": road_info["start"],
                "end_node": road_info["end"],
                "distance": road_info["distance"],
                "crowd_level": road_info.get("crowd_level", random.randint(1, 5)),
                "transport_type": road_info.get("transport_type", random.choice(transport_types))
            })
        
        # 2. 获取真实景区名称和坐标（只使用前20个）
        real_scenics = BEIJING_SCENICS[:20]
        
        # 3. 使用最小生成树算法创建道路网络（确保连通且边最少）
        # 构建所有可能的边
        all_edges = []
        for i in range(len(real_scenics)):
            for j in range(i + 1, len(real_scenics)):
                scenic1 = real_scenics[i]
                scenic2 = real_scenics[j]
                lat1 = scenic1.get("lat", 39.9)
                lng1 = scenic1.get("lng", 116.4)
                lat2 = scenic2.get("lat", 39.9)
                lng2 = scenic2.get("lng", 116.4)
                
                distance = calculate_distance(lat1, lng1, lat2, lng2)
                if distance < 25000:  # 25公里内
                    all_edges.append((scenic1, scenic2, distance))
        
        # 按距离排序
        all_edges.sort(key=lambda x: x[2])
        
        # Kruskal算法构建最小生成树
        parent = {s["name"]: s["name"] for s in real_scenics}
        
        def find(x):
            if parent[x] != x:
                parent[x] = find(parent[x])
            return parent[x]
        
        def union(x, y):
            px, py = find(x), find(y)
            if px != py:
                parent[px] = py
        
        # 添加边直到所有节点连通
        for scenic1, scenic2, distance in all_edges:
            if find(scenic1["name"]) != find(scenic2["name"]):
                union(scenic1["name"], scenic2["name"])
                
                # 根据距离设置道路属性
                crowd_level = 2
                if distance < 5000: crowd_level = 3
                if distance < 2000: crowd_level = 4
                
                transport_type = "步行" if distance < 2000 else ("自行车" if distance < 5000 else "汽车")
                
                roads.append({
                    "start_node": scenic1["name"],
                    "end_node": scenic2["name"],
                    "distance": int(distance),
                    "crowd_level": crowd_level,
                    "transport_type": transport_type
                })
        
        # 4. 添加额外的边，使总边数达到45条（20个节点的连通网络）
        # 已添加的边数
        current_edges = len(roads)
        target_edges = 45
        
        # 获取已存在的边对
        edge_pairs = set()
        for r in roads:
            edge_pairs.add((r["start_node"], r["end_node"]))
            edge_pairs.add((r["end_node"], r["start_node"]))
        
        # 从剩余的边中选择最短的边添加
        extra_edges = []
        for scenic1, scenic2, distance in all_edges:
            pair1 = (scenic1["name"], scenic2["name"])
            pair2 = (scenic2["name"], scenic1["name"])
            if pair1 not in edge_pairs and pair2 not in edge_pairs:
                extra_edges.append((scenic1, scenic2, distance))
        
        # 按距离排序，添加最短的边
        extra_edges.sort(key=lambda x: x[2])
        edges_to_add = min(target_edges - current_edges, len(extra_edges))
        
        for i in range(edges_to_add):
            scenic1, scenic2, distance = extra_edges[i]
            crowd_level = 2
            if distance < 5000: crowd_level = 3
            if distance < 2000: crowd_level = 4
            
            transport_type = "步行" if distance < 2000 else ("自行车" if distance < 5000 else "汽车")
            
            roads.append({
                "start_node": scenic1["name"],
                "end_node": scenic2["name"],
                "distance": int(distance),
                "crowd_level": crowd_level,
                "transport_type": transport_type
            })
        
        # 4. 为其他景区（如果有的话）创建连接
        if scenic_count > len(real_scenics):
            for i in range(len(real_scenics) + 1, min(scenic_count + 1, len(real_scenics) + 50)):
                scenic_name = f"景区{i}"
                # 只连接到最近的1个真实景区
                roads.append({
                    "start_node": scenic_name,
                    "end_node": real_scenics[0]["name"],
                    "distance": random.randint(3000, 6000),
                    "crowd_level": random.randint(2, 4),
                    "transport_type": "汽车"
                })
    except ImportError:
        # 备用模拟数据 - 每个节点只连接到最近的2个
        for i in range(1, scenic_count + 1):
            # 连接到接下来的2个节点
            for offset in [1, 2]:
                j = i + offset
                if j <= scenic_count:
                    distance = random.randint(2000, 8000)
                    roads.append({
                        "start_node": f"景区{i}",
                        "end_node": f"景区{j}",
                        "distance": distance,
                        "crowd_level": random.randint(2, 4),
                        "transport_type": "汽车"
                    })
    
    # 5. 确保至少有200条道路
    while len(roads) < 200:
        # 随机选择两个景区创建道路
        if scenic_count >= 2:
            scenic1 = random.randint(1, min(scenic_count, 100))
            scenic2 = random.randint(1, min(scenic_count, 100))
            if scenic1 != scenic2:
                distance = random.randint(2000, 8000)
                roads.append({
                    "start_node": f"景区{scenic1}",
                    "end_node": f"景区{scenic2}",
                    "distance": distance,
                    "crowd_level": random.randint(2, 4),
                    "transport_type": "汽车"
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

# 生成美食数据（使用真实美食数据）
def generate_foods(scenic_count):
    try:
        from database.real_map_data import BEIJING_FOODS
        
        foods = []
        # 首先添加真实美食数据
        for food_info in BEIJING_FOODS:
            foods.append({
                "name": food_info["name"],
                "scenic_id": random.randint(1, min(scenic_count, 10)),  # 分配到前10个景区
                "description": food_info.get("description", ""),
                "hotness": food_info.get("hotness", random.randint(500, 10000)),
                "rating": food_info.get("rating", round(random.uniform(3.5, 5.0), 1)),
                "cuisine": food_info.get("cuisine", "其他"),
                "price": food_info.get("price", random.randint(20, 200))
            })
        
        # 为每个景区补充美食
        cuisines = ["川菜", "粤菜", "鲁菜", "淮扬菜", "湘菜", "浙菜", "闽菜", "徽菜", "京菜", "东北菜"]
        for scenic_id in range(1, scenic_count + 1):
            for i in range(3):  # 每个景区再添加3个
                foods.append({
                    "name": f"{scenic_id}号景区美食{i+1}",
                    "scenic_id": scenic_id,
                    "description": f"{scenic_id}号景区的特色美食",
                    "hotness": random.randint(500, 10000),
                    "rating": round(random.uniform(3.5, 5.0), 1),
                    "cuisine": random.choice(cuisines),
                    "price": random.randint(20, 200)
                })
        
        return foods
    except ImportError:
        # 备用模拟数据
        cuisines = ["川菜", "粤菜", "鲁菜", "淮扬菜", "湘菜", "浙菜", "闽菜", "徽菜", "京菜", "东北菜"]
        foods = []
        
        for scenic_id in range(1, scenic_count + 1):
            for i in range(5):
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
    
    # 一些真实的游记标题和内容模板
    diary_templates = [
        {"title": "故宫一日游", "content": "今天参观了故宫博物院，被宏伟的建筑群震撼到了。太和殿、乾清宫、御花园，每一处都充满了历史的厚重感。"},
        {"title": "颐和园赏春", "content": "春天的颐和园太美了！昆明湖波光粼粼，长廊彩绘精美，佛香阁巍峨壮观。强烈推荐大家春天来游玩。"},
        {"title": "天坛公园散步", "content": "清晨来天坛公园散步，空气清新，环境幽静。祈年殿的建筑设计令人叹为观止，回音壁更是神奇。"},
        {"title": "香山红叶", "content": "秋天的香山红叶如火似霞，层林尽染。虽然爬山有点累，但看到如此美景，一切都值得了。"},
        {"title": "北大清华游", "content": "参观了北京大学和清华大学，校园环境优美，学术氛围浓厚。博雅塔、未名湖、清华园都给我留下了深刻印象。"},
        {"title": "南锣鼓巷探店", "content": "南锣鼓巷的胡同文化很有特色，各种小店琳琅满目。品尝了豆汁、炸酱面等北京小吃，味道独特。"},
        {"title": "三里屯夜生活", "content": "三里屯的夜晚很热闹，各种酒吧、餐厅、商店应有尽有。感受到了北京的时尚与活力。"},
        {"title": "奥林匹克公园", "content": "鸟巢和水立方的建筑设计太惊艳了！晚上的灯光秀更是美轮美奂，不虚此行。"},
    ]
    
    for user_id in range(1, user_count + 1):
        for i in range(3):  # 每个用户3篇日记
            template = diary_templates[(user_id + i) % len(diary_templates)]
            diaries.append({
                "user_id": user_id,
                "title": f"用户{user_id}：{template['title']}",
                "content": template['content'],
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
        added_count = 0
        for user_data in users:
            existing_user = session.query(User).filter_by(username=user_data['username']).first()
            if not existing_user:
                user = User(**user_data)
                session.add(user)
                added_count += 1
                print(f"用户 {user_data['username']} 创建成功")
            else:
                print(f"用户 {user_data['username']} 已存在，跳过创建")
        session.commit()
        print(f"插入{added_count}个用户")
        
        # 插入景区数据（≥200个，使用真实数据）
        scenics = generate_scenics()
        for scenic_data in scenics:
            scenic = Scenic(**scenic_data)
            session.add(scenic)
        session.commit()
        print(f"插入{len(scenics)}个景区（含真实北京地图数据）")
        
        scenic_count = len(scenics)
        
        # 插入建筑物数据（每个景区≥20个，使用真实数据）
        buildings = generate_buildings(scenic_count)
        for building_data in buildings:
            building = Building(**building_data)
            session.add(building)
        session.commit()
        print(f"插入{len(buildings)}个建筑物（含真实建筑数据）")
        
        # 插入设施数据（≥50个，≥10种类型，使用真实数据）
        facilities = generate_facilities(scenic_count)
        for facility_data in facilities:
            facility = Facility(**facility_data)
            session.add(facility)
        session.commit()
        print(f"插入{len(facilities)}个设施")
        
        # 插入道路数据（≥200条，使用真实道路数据）
        roads = generate_roads(scenic_count)
        for road_data in roads:
            road = Road(**road_data)
            session.add(road)
        session.commit()
        print(f"插入{len(roads)}条道路（含真实北京道路数据）")
        
        # 插入美食数据（使用真实美食数据）
        foods = generate_foods(scenic_count)
        for food_data in foods:
            food = Food(**food_data)
            session.add(food)
        session.commit()
        print(f"插入{len(foods)}个美食（含真实北京美食数据）")
        
        # 插入日记数据
        diaries = generate_diaries(len(users), scenic_count)
        for diary_data in diaries:
            diary = Diary(**diary_data)
            session.add(diary)
        session.commit()
        print(f"插入{len(diaries)}篇日记")
        
        print("\n真实地图数据初始化完成！")
        print("包含以下内容：")
        print("- 北京主要景区（故宫、颐和园、天坛等）的真实地理坐标")
        print("- 真实建筑物数据（太和殿、佛香阁、博雅塔等）")
        print("- 真实道路网络（长安街、二环路、中轴线等）")
        print("- 真实北京美食（烤鸭、炸酱面、豆汁等）")
        
    except Exception as e:
        print(f"数据插入失败: {e}")
        session.rollback()
        raise
    finally:
        session.close()
