# 搜索算法
import re
from config.algorithm_config import AlgorithmConfig

class SearchAlgorithm:
    @staticmethod
    def exact_search(items, field, keyword):
        """精确查找"""
        return [item for item in items if getattr(item, field) == keyword]
    
    @staticmethod
    def fuzzy_search(items, field, keyword, threshold=AlgorithmConfig.SEARCH_THRESHOLD):
        """模糊查找"""
        results = []
        keyword = keyword.lower()
        
        for item in items:
            value = str(getattr(item, field)).lower()
            # 计算匹配度
            match = re.search(keyword, value)
            if match:
                # 简单的匹配度计算
                match_ratio = len(keyword) / len(value)
                if match_ratio >= threshold:
                    results.append((match_ratio, item))
        
        # 按匹配度排序
        results.sort(key=lambda x: x[0], reverse=True)
        return [item for _, item in results[:AlgorithmConfig.MAX_SEARCH_RESULTS]]
