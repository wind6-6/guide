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
        # 使用计数器来确保元组可比较（避免对象直接比较）
        counter = 0
        heap = []
        for item in items:
            value = key_func(item)
            if len(heap) < n:
                # 使用负值实现最大堆效果，并添加计数器确保唯一性
                heapq.heappush(heap, (-value, counter, item))
                counter += 1
            elif -value < heap[0][0]:  # 比较负值（即原值更大）
                heapq.heappushpop(heap, (-value, counter, item))
                counter += 1
        
        # 返回排序后的结果（从高到低）
        return [item for _, _, item in sorted(heap, key=lambda x: x[0])]
    
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
    
    @staticmethod
    def quick_sort(items, key_func=None):
        """快速排序"""
        if key_func is None:
            key_func = lambda x: x
        
        if len(items) <= 1:
            return items
        
        pivot = items[len(items) // 2]
        pivot_key = key_func(pivot)
        
        left = [x for x in items if key_func(x) < pivot_key]
        middle = [x for x in items if key_func(x) == pivot_key]
        right = [x for x in items if key_func(x) > pivot_key]
        
        return SortAlgorithm.quick_sort(left, key_func) + middle + SortAlgorithm.quick_sort(right, key_func)
    
    @staticmethod
    def merge_sort(items, key_func=None):
        """归并排序"""
        if key_func is None:
            key_func = lambda x: x
        
        if len(items) <= 1:
            return items
        
        mid = len(items) // 2
        left = SortAlgorithm.merge_sort(items[:mid], key_func)
        right = SortAlgorithm.merge_sort(items[mid:], key_func)
        
        return SortAlgorithm._merge(left, right, key_func)
    
    @staticmethod
    def _merge(left, right, key_func):
        """合并两个有序列表"""
        result = []
        i = j = 0
        
        while i < len(left) and j < len(right):
            if key_func(left[i]) <= key_func(right[j]):
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1
        
        result.extend(left[i:])
        result.extend(right[j:])
        return result
