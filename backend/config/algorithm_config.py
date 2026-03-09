# 算法配置
class AlgorithmConfig:
    # 排序算法参数
    SORT_TOP_N = 10  # 非完全排序取前10
    SORT_WEIGHTS = {
        'hotness': 0.3,  # 热度权重
        'rating': 0.4,   # 评分权重
        'distance': 0.3  # 距离权重
    }
    
    # 最短路径算法参数
    IDEAL_SPEED = 5.0  # 理想步行速度（km/h）
    MAX_CROWD_LEVEL = 5  # 最大拥挤度
    CROWD_PENALTY = 2.0  # 拥挤度惩罚系数
    
    # 搜索算法参数
    SEARCH_THRESHOLD = 0.6  # 模糊搜索阈值
    MAX_SEARCH_RESULTS = 50  # 最大搜索结果数
    
    # 压缩算法参数
    COMPRESSION_LEVEL = 9  # 压缩级别（1-9）
    MAX_TEXT_SIZE = 10000  # 最大文本大小
    
    # 导航算法参数
    INDOOR_NODE_RADIUS = 1.5  # 室内节点半径（米）
    MAX_NAVIGATION_POINTS = 20  # 最大导航点数量
