# 排序算法
import heapq
from config.algorithm_config import AlgorithmConfig

class SortAlgorithm:
    @staticmethod
    def top_n_sort(items, key_func, n=AlgorithmConfig.SORT_TOP_N):
        """非完全排序取前N个"""
        if len(items) <= n:
            return sorted(items, key=key_func, reverse=True)
        
        # 使用堆来高效获取前N个
        heap = []
        for item in items:
            value = key_func(item)
            if len(heap) < n:
                heapq.heappush(heap, (value, item))
            elif value > heap[0][0]:
                heapq.heappushpop(heap, (value, item))
        
        return [item for _, item in sorted(heap, key=lambda x: x[0], reverse=True)]
    
    @staticmethod
    def weighted_sort(items, weights=None):
        """带权重的排序"""
        if weights is None:
            weights = AlgorithmConfig.SORT_WEIGHTS
        
        def key_func(item):
            score = 0
            if hasattr(item, 'hotness') and 'hotness' in weights:
                score += item.hotness * weights['hotness']
            if hasattr(item, 'rating') and 'rating' in weights:
                score += item.rating * weights['rating']
            if hasattr(item, 'distance') and 'distance' in weights:
                # 距离越近得分越高
                score += (1.0 / (item.distance + 1)) * weights['distance']
            return score
        
        return sorted(items, key=key_func, reverse=True)
