# 真实地图数据 - 北京地区
# 包含真实的地理坐标、景点、建筑物和道路信息

# 北京主要景区/地标 - 带真实地理坐标（经纬度）
BEIJING_SCENICS = [
    # 历史文化类
    {"name": "故宫博物院", "lat": 39.916345, "lng": 116.397155, "category": "历史文化", 
     "address": "北京市东城区景山前街4号", "ticket_price": "60元", "open_time": "08:30-17:00",
     "description": "中国明清两代的皇家宫殿，旧称紫禁城，是世界上现存规模最大、保存最为完整的木质结构古建筑之一。",
     "hotness": 9.8, "rating": 4.9},
    
    {"name": "颐和园", "lat": 39.999982, "lng": 116.275461, "category": "历史文化",
     "address": "北京市海淀区新建宫门路19号", "ticket_price": "30元", "open_time": "06:00-20:00",
     "description": "中国清朝时期皇家园林，保存最完整的一座皇家行宫御苑，被誉为'皇家园林博物馆'。",
     "hotness": 9.5, "rating": 4.8},
    
    {"name": "天坛公园", "lat": 39.883455, "lng": 116.412866, "category": "历史文化",
     "address": "北京市东城区天坛东里甲1号", "ticket_price": "15元", "open_time": "06:00-22:00",
     "description": "明清两代皇帝祭天的场所，是中国现存最大的古代祭祀性建筑群。",
     "hotness": 9.2, "rating": 4.7},
    
    {"name": "圆明园遗址公园", "lat": 40.008449, "lng": 116.301364, "category": "历史文化",
     "address": "北京市海淀区清华西路28号", "ticket_price": "10元", "open_time": "07:00-19:00",
     "description": "清代大型皇家园林，有'万园之园'之称，1860年遭英法联军焚毁。",
     "hotness": 8.9, "rating": 4.6},
    
    {"name": "北海公园", "lat": 39.928276, "lng": 116.395531, "category": "历史文化",
     "address": "北京市西城区文津街1号", "ticket_price": "10元", "open_time": "06:00-21:00",
     "description": "中国现存最古老、最完整、最具综合性和代表性的皇家园林之一。",
     "hotness": 8.7, "rating": 4.6},
    
    {"name": "景山公园", "lat": 39.924418, "lng": 116.397087, "category": "历史文化",
     "address": "北京市西城区景山西街44号", "ticket_price": "2元", "open_time": "06:00-21:00",
     "description": "位于故宫北面，原为元、明、清三代的皇家御苑，可俯瞰故宫全景。",
     "hotness": 8.5, "rating": 4.5},
    
    {"name": "雍和宫", "lat": 39.947200, "lng": 116.417755, "category": "宗教文化",
     "address": "北京市东城区雍和宫大街12号", "ticket_price": "25元", "open_time": "09:00-16:30",
     "description": "北京市内最大的藏传佛教寺院，原为清雍正帝即位前的府邸。",
     "hotness": 8.6, "rating": 4.6},
    
    {"name": "恭王府", "lat": 39.937049, "lng": 116.386351, "category": "历史文化",
     "address": "北京市西城区前海西街17号", "ticket_price": "40元", "open_time": "08:30-17:00",
     "description": "清代规模最大的一座王府，曾先后作为和珅、永璘的宅邸。",
     "hotness": 8.8, "rating": 4.7},
    
    {"name": "孔庙和国子监", "lat": 39.948018, "lng": 116.414444, "category": "历史文化",
     "address": "北京市东城区国子监街15号", "ticket_price": "30元", "open_time": "08:30-17:00",
     "description": "中国元、明、清三朝祭祀孔子的场所，也是当时最高学府和教育管理机构。",
     "hotness": 8.0, "rating": 4.4},
    
    # 自然风光类
    {"name": "香山公园", "lat": 39.991087, "lng": 116.188883, "category": "自然风光",
     "address": "北京市海淀区买卖街40号", "ticket_price": "10元", "open_time": "06:00-18:00",
     "description": "是一座具有山林特色的皇家园林，香山红叶最为著名。",
     "hotness": 9.0, "rating": 4.6},
    
    {"name": "北京植物园", "lat": 40.001886, "lng": 116.213005, "category": "自然风光",
     "address": "北京市海淀区香山卧佛寺路", "ticket_price": "5元", "open_time": "06:00-21:00",
     "description": "集植物科学研究、植物知识普及、游览观赏休憩于一体的综合性植物园。",
     "hotness": 8.3, "rating": 4.5},
    
    {"name": "奥林匹克森林公园", "lat": 40.014978, "lng": 116.391632, "category": "自然风光",
     "address": "北京市朝阳区科荟路33号", "ticket_price": "免费", "open_time": "06:00-21:00",
     "description": "北京奥运会配套工程，是亚洲最大的城市绿化景观。",
     "hotness": 8.7, "rating": 4.6},
    
    # 现代建筑类
    {"name": "国家体育场(鸟巢)", "lat": 39.992936, "lng": 116.396531, "category": "现代建筑",
     "address": "北京市朝阳区国家体育场南路1号", "ticket_price": "50元", "open_time": "09:00-18:00",
     "description": "2008年北京奥运会的主体育场，因其形态如同孕育生命的'巢'而得名。",
     "hotness": 9.1, "rating": 4.5},
    
    {"name": "国家游泳中心(水立方)", "lat": 39.991264, "lng": 116.384892, "category": "现代建筑",
     "address": "北京市朝阳区天辰东路11号", "ticket_price": "30元", "open_time": "09:00-18:00",
     "description": "2008年北京奥运会游泳比赛场馆，外观如蓝色水晶般晶莹剔透。",
     "hotness": 8.8, "rating": 4.5},
    
    {"name": "国家大剧院", "lat": 39.904153, "lng": 116.383776, "category": "现代建筑",
     "address": "北京市西城区西长安街2号", "ticket_price": "30元", "open_time": "09:00-17:00",
     "description": "中国最高表演艺术中心，外形为半椭球形，被誉为'水上明珠'。",
     "hotness": 8.9, "rating": 4.7},
    
    {"name": "中央广播电视塔", "lat": 39.918668, "lng": 116.304092, "category": "现代建筑",
     "address": "北京市海淀区西三环中路11号", "ticket_price": "80元", "open_time": "08:30-22:00",
     "description": "北京标志性建筑之一，高405米，可俯瞰整个北京城。",
     "hotness": 8.4, "rating": 4.4},
    
    # 教育科研类
    {"name": "北京大学", "lat": 39.987045, "lng": 116.305435, "category": "教育科研",
     "address": "北京市海淀区颐和园路5号", "ticket_price": "免费", "open_time": "08:00-17:00",
     "description": "中国近代第一所国立综合性大学，'五四运动'的发源地。",
     "hotness": 9.3, "rating": 4.8},
    
    {"name": "清华大学", "lat": 40.000106, "lng": 116.326686, "category": "教育科研",
     "address": "北京市海淀区清华园1号", "ticket_price": "免费", "open_time": "08:00-17:00",
     "description": "中国著名高等学府，以工科见长，被誉为'红色工程师的摇篮'。",
     "hotness": 9.4, "rating": 4.8},
    
    {"name": "中国人民大学", "lat": 39.969789, "lng": 116.321548, "category": "教育科研",
     "address": "北京市海淀区中关村大街59号", "ticket_price": "免费", "open_time": "08:00-17:00",
     "description": "中国共产党创办的第一所新型正规大学，以人文社会科学为主。",
     "hotness": 8.5, "rating": 4.5},
    
    {"name": "北京航空航天大学", "lat": 39.982850, "lng": 116.346561, "category": "教育科研",
     "address": "北京市海淀区学院路37号", "ticket_price": "免费", "open_time": "08:00-17:00",
     "description": "新中国第一所航空航天高等学府，'双一流'建设高校。",
     "hotness": 8.6, "rating": 4.6},
    
    # 商业休闲类
    {"name": "王府井大街", "lat": 39.911056, "lng": 116.410876, "category": "商业休闲",
     "address": "北京市东城区王府井大街", "ticket_price": "免费", "open_time": "全天",
     "description": "北京最著名的商业街，有'中华第一商业街'之称。",
     "hotness": 9.2, "rating": 4.5},
    
    {"name": "三里屯太古里", "lat": 39.935344, "lng": 116.454866, "category": "商业休闲",
     "address": "北京市朝阳区三里屯路19号", "ticket_price": "免费", "open_time": "10:00-22:00",
     "description": "北京时尚潮流地标，集购物、餐饮、娱乐于一体的开放式商业区。",
     "hotness": 9.0, "rating": 4.6},
    
    {"name": "南锣鼓巷", "lat": 39.937243, "lng": 116.403076, "category": "商业休闲",
     "address": "北京市东城区南锣鼓巷", "ticket_price": "免费", "open_time": "全天",
     "description": "北京最古老的街区之一，保留了元代'鱼骨状'胡同肌理。",
     "hotness": 9.1, "rating": 4.4},
    
    {"name": "什刹海", "lat": 39.942123, "lng": 116.388456, "category": "商业休闲",
     "address": "北京市西城区什刹海", "ticket_price": "免费", "open_time": "全天",
     "description": "北京城内面积最大、风貌保存最完整的一片历史街区。",
     "hotness": 8.9, "rating": 4.5},
    
    {"name": "前门大街", "lat": 39.900456, "lng": 116.398234, "category": "商业休闲",
     "address": "北京市东城区前门大街", "ticket_price": "免费", "open_time": "全天",
     "description": "北京中轴线上的重要商业街，历史悠久，老字号云集。",
     "hotness": 8.7, "rating": 4.4},
    
    # 博物馆类
    {"name": "中国国家博物馆", "lat": 39.905489, "lng": 116.401253, "category": "历史文化",
     "address": "北京市东城区东长安街16号", "ticket_price": "免费", "open_time": "09:00-17:00",
     "description": "世界上建筑面积最大的博物馆，馆藏珍贵文物140余万件。",
     "hotness": 9.3, "rating": 4.8},
    
    {"name": "首都博物馆", "lat": 39.906789, "lng": 116.342156, "category": "历史文化",
     "address": "北京市西城区复兴门外大街16号", "ticket_price": "免费", "open_time": "09:00-17:00",
     "description": "北京地区大型综合性博物馆，馆藏文物25万余件。",
     "hotness": 8.6, "rating": 4.6},
    
    {"name": "中国美术馆", "lat": 39.924567, "lng": 116.412345, "category": "历史文化",
     "address": "北京市东城区五四大街1号", "ticket_price": "免费", "open_time": "09:00-17:00",
     "description": "中国唯一的国家造型艺术博物馆，收藏近现代美术作品10万余件。",
     "hotness": 8.4, "rating": 4.5},
    
    # 动物园类
    {"name": "北京动物园", "lat": 39.941234, "lng": 116.338765, "category": "主题公园",
     "address": "北京市西城区西直门外大街137号", "ticket_price": "15元", "open_time": "07:30-18:00",
     "description": "中国开放最早、饲养展出动物种类最多的动物园。",
     "hotness": 9.0, "rating": 4.6},
    
    {"name": "北京海洋馆", "lat": 39.942345, "lng": 116.336543, "category": "主题公园",
     "address": "北京市海淀区高粱桥斜街乙18号", "ticket_price": "170元", "open_time": "09:00-17:30",
     "description": "亚洲第一、世界内陆最大、设施最先进的海洋馆。",
     "hotness": 8.7, "rating": 4.5},
]

# 主要道路网络（基于真实北京道路）
BEIJING_ROADS = [
    # 长安街沿线
    {"name": "长安街", "start": "建国门", "end": "复兴门", "distance": 3800, "type": "主干道", "crowd_level": 5},
    {"name": "东长安街", "start": "东单", "end": "建国门", "distance": 1200, "type": "主干道", "crowd_level": 4},
    {"name": "西长安街", "start": "西单", "end": "复兴门", "distance": 1500, "type": "主干道", "crowd_level": 4},
    
    # 二环路
    {"name": "二环路北段", "start": "东直门", "end": "西直门", "distance": 8000, "type": "快速路", "crowd_level": 5},
    {"name": "二环路东段", "start": "东直门", "end": "建国门", "distance": 3500, "type": "快速路", "crowd_level": 5},
    {"name": "二环路西段", "start": "西直门", "end": "复兴门", "distance": 3800, "type": "快速路", "crowd_level": 4},
    {"name": "二环路南段", "start": "建国门", "end": "复兴门", "distance": 7500, "type": "快速路", "crowd_level": 4},
    
    # 三环路
    {"name": "三环路北段", "start": "三元桥", "end": "苏州桥", "distance": 12000, "type": "快速路", "crowd_level": 4},
    {"name": "三环路东段", "start": "三元桥", "end": "国贸", "distance": 5000, "type": "快速路", "crowd_level": 5},
    {"name": "三环路西段", "start": "苏州桥", "end": "公主坟", "distance": 5500, "type": "快速路", "crowd_level": 4},
    
    # 中轴线
    {"name": "永定门内大街", "start": "永定门", "end": "天桥", "distance": 800, "type": "主干道", "crowd_level": 3},
    {"name": "前门大街", "start": "天桥", "end": "前门", "distance": 600, "type": "步行街", "crowd_level": 4},
    {"name": "南长街", "start": "前门", "end": "天安门", "distance": 900, "type": "主干道", "crowd_level": 5},
    {"name": "北长街", "start": "天安门", "end": "景山", "distance": 700, "type": "主干道", "crowd_level": 4},
    {"name": "地安门内大街", "start": "景山", "end": "地安门", "distance": 500, "type": "主干道", "crowd_level": 3},
    {"name": "鼓楼大街", "start": "地安门", "end": "鼓楼", "distance": 600, "type": "主干道", "crowd_level": 3},
    {"name": "钟楼湾胡同", "start": "鼓楼", "end": "钟楼", "distance": 200, "type": "胡同", "crowd_level": 2},
    
    # 东西向主干道
    {"name": "平安大街", "start": "东四十条", "end": "官园", "distance": 7000, "type": "主干道", "crowd_level": 4},
    {"name": "朝阜大街", "start": "朝阳门", "end": "阜成门", "distance": 6500, "type": "主干道", "crowd_level": 4},
    {"name": "两广路", "start": "广渠门", "end": "广安门", "distance": 8000, "type": "主干道", "crowd_level": 3},
    
    # 南北向主干道
    {"name": "崇雍大街", "start": "崇文门", "end": "雍和宫", "distance": 4500, "type": "主干道", "crowd_level": 4},
    {"name": "王府井大街", "start": "长安街", "end": "美术馆", "distance": 1200, "type": "步行街", "crowd_level": 5},
    {"name": "中关村大街", "start": "北三环", "end": "北四环", "distance": 3000, "type": "主干道", "crowd_level": 5},
    
    # 景区内部道路
    {"name": "故宫东城墙路", "start": "东华门", "end": "神武门", "distance": 900, "type": "景区道路", "crowd_level": 4},
    {"name": "故宫西城墙路", "start": "西华门", "end": "神武门", "distance": 900, "type": "景区道路", "crowd_level": 3},
    {"name": "颐和园东堤", "start": "东宫门", "end": "十七孔桥", "distance": 1500, "type": "景区道路", "crowd_level": 3},
    {"name": "颐和园西堤", "start": "石舫", "end": "镜桥", "distance": 2000, "type": "景区道路", "crowd_level": 2},
    {"name": "香山南路", "start": "香山公园东门", "end": "香炉峰", "distance": 2500, "type": "景区道路", "crowd_level": 3},
]

# 建筑物数据（基于真实建筑）
BEIJING_BUILDINGS = {
    "故宫博物院": [
        {"name": "太和殿", "type": "宫殿", "floor": 1, "description": "故宫最大的殿宇，俗称'金銮殿'，是举行重大典礼的地方。"},
        {"name": "中和殿", "type": "宫殿", "floor": 1, "description": "皇帝去太和殿大典之前休息的地方。"},
        {"name": "保和殿", "type": "宫殿", "floor": 1, "description": "清代每年除夕皇帝赐宴外藩王公的场所。"},
        {"name": "乾清宫", "type": "宫殿", "floor": 1, "description": "皇帝的寝宫，处理日常政务的地方。"},
        {"name": "坤宁宫", "type": "宫殿", "floor": 1, "description": "皇后的寝宫，也是皇帝大婚的洞房。"},
        {"name": "御花园", "type": "园林", "floor": 0, "description": "故宫内的皇家园林，古柏参天，奇石罗布。"},
        {"name": "珍宝馆", "type": "展览馆", "floor": 1, "description": "展示清代宫廷制作及收藏的珍贵文物。"},
        {"name": "钟表馆", "type": "展览馆", "floor": 1, "description": "展示中外各式钟表，以清宫造办处制造为主。"},
        {"name": "文华殿", "type": "宫殿", "floor": 1, "description": "明代皇太子摄事之所，清代为举行经筵的地方。"},
        {"name": "武英殿", "type": "宫殿", "floor": 1, "description": "清代内务府修书处，现为书画馆。"},
    ],
    "颐和园": [
        {"name": "佛香阁", "type": "楼阁", "floor": 4, "description": "颐和园最高建筑，高41米，八面三层四重檐。"},
        {"name": "长廊", "type": "廊道", "floor": 1, "description": "全长728米，是中国园林中最长的游廊。"},
        {"name": "昆明湖", "type": "湖泊", "floor": 0, "description": "颐和园的主要水面，约占全园面积的四分之三。"},
        {"name": "万寿山", "type": "山岳", "floor": 0, "description": "颐和园的主体山景，高58.59米。"},
        {"name": "十七孔桥", "type": "桥梁", "floor": 0, "description": "连接东堤和南湖岛的石桥，长150米。"},
        {"name": "石舫", "type": "建筑", "floor": 2, "description": "又名清晏舫，是颐和园中著名的水上建筑。"},
        {"name": "苏州街", "type": "商业街", "floor": 1, "description": "仿江南水乡而建的商业街，供帝后游览购物。"},
        {"name": "谐趣园", "type": "园林", "floor": 0, "description": "颐和园内著名的园中之园，仿无锡寄畅园而建。"},
        {"name": "德和园", "type": "戏楼", "floor": 3, "description": "清代三大戏楼之一，专供慈禧太后看戏。"},
        {"name": "乐寿堂", "type": "宫殿", "floor": 1, "description": "慈禧太后的寝宫，也是颐和园居住生活区中的主建筑。"},
    ],
    "天坛公园": [
        {"name": "祈年殿", "type": "祭祀建筑", "floor": 3, "description": "天坛的主体建筑，是明清两代皇帝孟春祈谷之所。"},
        {"name": "圜丘坛", "type": "祭祀建筑", "floor": 1, "description": "皇帝冬至日祭天的地方，俗称祭天台。"},
        {"name": "皇穹宇", "type": "祭祀建筑", "floor": 1, "description": "存放皇天上帝牌位的地方，著名的回音壁就在此。"},
        {"name": "回音壁", "type": "建筑", "floor": 0, "description": "皇穹宇的圆形围墙，因声波反射产生回音效果而闻名。"},
        {"name": "三音石", "type": "景观", "floor": 0, "description": "位于皇穹宇台阶下，站在上面击掌可听到多次回声。"},
        {"name": "丹陛桥", "type": "桥梁", "floor": 0, "description": "连接祈年殿和圜丘坛的甬道，长360米。"},
        {"name": "斋宫", "type": "宫殿", "floor": 1, "description": "皇帝祭天前斋戒的地方。"},
        {"name": "神乐署", "type": "官署", "floor": 1, "description": "明清两代演习祭祀礼乐的场所。"},
    ],
    "北京大学": [
        {"name": "博雅塔", "type": "塔", "floor": 0, "description": "北大标志性建筑之一，位于未名湖东南小丘上。"},
        {"name": "未名湖", "type": "湖泊", "floor": 0, "description": "北大校园内最大的人工湖，湖光塔影是北大著名景观。"},
        {"name": "图书馆", "type": "图书馆", "floor": 5, "description": "亚洲最大的高校图书馆之一，藏书800余万册。"},
        {"name": "百周年纪念讲堂", "type": "礼堂", "floor": 3, "description": "北大百年校庆时建成，是学校重要的文化活动场所。"},
        {"name": "理科教学楼", "type": "教学楼", "floor": 5, "description": "北大主要的理科教学场所。"},
        {"name": "文史楼", "type": "教学楼", "floor": 4, "description": "人文科学学部的主要教学楼。"},
        {"name": "光华管理学院", "type": "教学楼", "floor": 5, "description": "亚洲领先的商学院之一。"},
        {"name": "西门", "type": "校门", "floor": 0, "description": "北大最著名的校门，匾额上书'北京大学'四字。"},
    ],
    "清华大学": [
        {"name": "清华园", "type": "园林", "floor": 0, "description": "清华大学的发源地，清代皇家园林遗址。"},
        {"name": "大礼堂", "type": "礼堂", "floor": 2, "description": "清华标志性建筑，采用希腊式与罗马式建筑风格。"},
        {"name": "图书馆", "type": "图书馆", "floor": 4, "description": "清华图书馆新馆，藏书量居全国高校前列。"},
        {"name": "二校门", "type": "校门", "floor": 0, "description": "清华最著名的校门，始建于1909年。"},
        {"name": "荷塘月色", "type": "景观", "floor": 0, "description": "朱自清《荷塘月色》的创作地，清华著名景点。"},
        {"name": "主楼", "type": "教学楼", "floor": 12, "description": "清华最高的建筑，是学校行政中心。"},
        {"name": "新清华学堂", "type": "礼堂", "floor": 3, "description": "清华百年校庆时建成，是高水平演出场所。"},
        {"name": "科学馆", "type": "教学楼", "floor": 4, "description": "清华早期四大建筑之一，现为物理系所在地。"},
    ],
}

# 服务设施数据
BEIJING_FACILITIES = {
    "卫生间": [
        {"name": "公共卫生间A", "location": "景区入口附近"},
        {"name": "公共卫生间B", "location": "景区中心区域"},
        {"name": "公共卫生间C", "location": "景区出口附近"},
    ],
    "商店": [
        {"name": "纪念品商店", "location": "景区主路旁边"},
        {"name": "便利店", "location": "景区入口处"},
    ],
    "饭店": [
        {"name": "景区餐厅", "location": "景区中心广场"},
        {"name": "快餐店", "location": "景区东门附近"},
        {"name": "咖啡厅", "location": "景区西门附近"},
    ],
    "医务室": [
        {"name": "景区医务室", "location": "景区管理中心旁边"},
    ],
    "停车场": [
        {"name": "P1停车场", "location": "景区南门"},
        {"name": "P2停车场", "location": "景区北门"},
    ],
    "休息区": [
        {"name": "中心休息区", "location": "景区中心广场"},
        {"name": "湖边休息区", "location": "湖边凉亭"},
    ],
}

# 美食数据（北京特色美食）
BEIJING_FOODS = [
    {"name": "北京烤鸭", "cuisine": "京菜", "price": 258, "hotness": 9850, "rating": 4.8,
     "description": "北京最著名的菜肴，以全聚德、便宜坊最为著名，皮脆肉嫩，肥而不腻。"},
    
    {"name": "炸酱面", "cuisine": "京菜", "price": 28, "hotness": 7650, "rating": 4.5,
     "description": "老北京传统面食，黄酱炸制的肉酱拌面，配以黄瓜丝、豆芽等菜码。"},
    
    {"name": "豆汁焦圈", "cuisine": "京菜", "price": 8, "hotness": 4230, "rating": 4.0,
     "description": "老北京特色早餐，豆汁酸甜，焦圈酥脆，是北京独有的味道。"},
    
    {"name": "卤煮火烧", "cuisine": "京菜", "price": 35, "hotness": 5680, "rating": 4.3,
     "description": "北京传统小吃，猪肠、猪肺等内脏配以火烧，汤汁浓郁。"},
    
    {"name": "驴打滚", "cuisine": "京菜", "price": 15, "hotness": 6230, "rating": 4.4,
     "description": "北京传统糕点，黄豆面裹着红豆馅，口感软糯香甜。"},
    
    {"name": "艾窝窝", "cuisine": "京菜", "price": 12, "hotness": 4890, "rating": 4.2,
     "description": "北京传统清真小吃，糯米制成的球形糕点，内馅多样。"},
    
    {"name": "糖葫芦", "cuisine": "京菜", "price": 10, "hotness": 7120, "rating": 4.5,
     "description": "北京传统小吃，山楂串蘸冰糖制成，酸甜可口。"},
    
    {"name": "涮羊肉", "cuisine": "京菜", "price": 128, "hotness": 8230, "rating": 4.7,
     "description": "北京冬季传统美食，薄切羊肉在铜锅中涮煮，配以麻酱调料。"},
    
    {"name": "宫保鸡丁", "cuisine": "川菜", "price": 48, "hotness": 8920, "rating": 4.6,
     "description": "经典川菜，酸甜微辣，鸡肉嫩滑，花生酥脆。"},
    
    {"name": "麻婆豆腐", "cuisine": "川菜", "price": 38, "hotness": 8560, "rating": 4.5,
     "description": "四川传统名菜，麻辣鲜香，豆腐嫩滑，肉末酥香。"},
    
    {"name": "水煮鱼", "cuisine": "川菜", "price": 88, "hotness": 7890, "rating": 4.6,
     "description": "川菜代表，鱼肉鲜嫩，麻辣过瘾，油而不腻。"},
    
    {"name": "回锅肉", "cuisine": "川菜", "price": 58, "hotness": 7340, "rating": 4.5,
     "description": "川菜之首，肥而不腻，色泽红亮，口味独特。"},
    
    {"name": "白切鸡", "cuisine": "粤菜", "price": 68, "hotness": 6540, "rating": 4.4,
     "description": "粤菜代表，皮黄肉白，肥嫩鲜美，原汁原味。"},
    
    {"name": "烧鹅", "cuisine": "粤菜", "price": 98, "hotness": 7120, "rating": 4.5,
     "description": "粤菜经典，皮脆肉嫩，色泽金红，香味浓郁。"},
    
    {"name": "虾饺", "cuisine": "粤菜", "price": 32, "hotness": 6780, "rating": 4.6,
     "description": "粤式点心代表，皮薄馅大，鲜美可口。"},
    
    {"name": "糖醋里脊", "cuisine": "鲁菜", "price": 52, "hotness": 7450, "rating": 4.5,
     "description": "鲁菜经典，酸甜可口，外酥里嫩，色泽红亮。"},
    
    {"name": "九转大肠", "cuisine": "鲁菜", "price": 78, "hotness": 5230, "rating": 4.3,
     "description": "鲁菜名菜，酸甜苦辣咸五味俱全，色泽红润。"},
    
    {"name": "狮子头", "cuisine": "淮扬菜", "price": 68, "hotness": 6120, "rating": 4.4,
     "description": "淮扬菜代表，肉质鲜嫩，肥而不腻，汤汁浓郁。"},
    
    {"name": "剁椒鱼头", "cuisine": "湘菜", "price": 88, "hotness": 6890, "rating": 4.5,
     "description": "湘菜代表，鲜辣可口，鱼肉细嫩，剁椒香味浓郁。"},
    
    {"name": "东坡肉", "cuisine": "浙菜", "price": 88, "hotness": 7230, "rating": 4.6,
     "description": "浙菜代表，色泽红亮，味醇汁浓，酥烂而形不碎。"},
]

def get_scenic_coordinates(scenic_name):
    """获取景区坐标"""
    for scenic in BEIJING_SCENICS:
        if scenic["name"] == scenic_name:
            return scenic["lat"], scenic["lng"]
    return None, None

def calculate_real_distance(lat1, lng1, lat2, lng2):
    """计算两点间的真实距离（米）"""
    import math
    R = 6371000  # 地球半径（米）
    
    lat1_rad = math.radians(lat1)
    lat2_rad = math.radians(lat2)
    delta_lat = math.radians(lat2 - lat1)
    delta_lng = math.radians(lng2 - lng1)
    
    a = math.sin(delta_lat/2) * math.sin(delta_lat/2) + \
        math.cos(lat1_rad) * math.cos(lat2_rad) * \
        math.sin(delta_lng/2) * math.sin(delta_lng/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    
    distance = R * c
    return round(distance, 2)

# 生成更多景区数据（确保达到200个）
def generate_extended_scenics():
    """生成扩展的景区数据，确保达到200个"""
    import random
    
    base_scenics = BEIJING_SCENICS.copy()
    categories = ["历史文化", "自然风光", "主题公园", "现代建筑", "宗教文化", "教育科研", "商业休闲", "体育健身"]
    
    # 北京各区县景点
    districts = ["东城区", "西城区", "朝阳区", "海淀区", "丰台区", "石景山区", "门头沟区", "房山区", "通州区", "顺义区", "昌平区", "大兴区", "怀柔区", "平谷区", "密云区", "延庆区"]
    
    # 生成更多景点直到200个
    existing_names = {s["name"] for s in base_scenics}
    counter = 1
    
    while len(base_scenics) < 200:
        district = random.choice(districts)
        category = random.choice(categories)
        
        # 生成随机坐标（北京地区大致范围）
        lat = random.uniform(39.6, 40.2)
        lng = random.uniform(115.8, 116.8)
        
        name = f"{district}景点{counter}"
        if name not in existing_names:
            base_scenics.append({
                "name": name,
                "lat": lat,
                "lng": lng,
                "category": category,
                "address": f"北京市{district}路{counter}号",
                "ticket_price": f"{random.randint(0, 100)}元" if random.random() > 0.3 else "免费",
                "open_time": "08:00-18:00",
                "description": f"{name}是位于北京市{district}的一个{category}类景点。",
                "hotness": round(random.uniform(5.0, 9.0), 1),
                "rating": round(random.uniform(3.5, 4.8), 1)
            })
            existing_names.add(name)
            counter += 1
    
    return base_scenics
