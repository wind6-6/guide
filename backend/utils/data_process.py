# 数据处理工具
import json
import datetime

class DataProcess:
    @staticmethod
    def update_hotness(items, base_hotness=0.1):
        """更新热度"""
        for item in items:
            if hasattr(item, 'hotness'):
                item.hotness += base_hotness
        return items
    
    @staticmethod
    def format_datetime(dt):
        """格式化时间"""
        if isinstance(dt, datetime.datetime):
            return dt.strftime('%Y-%m-%d %H:%M:%S')
        return dt
    
    @staticmethod
    def to_dict(obj, exclude=None):
        """对象转字典"""
        if exclude is None:
            exclude = []
        
        result = {}
        for attr in dir(obj):
            if not attr.startswith('_') and attr not in exclude:
                value = getattr(obj, attr)
                if not callable(value):
                    if isinstance(value, datetime.datetime):
                        result[attr] = DataProcess.format_datetime(value)
                    else:
                        result[attr] = value
        return result
