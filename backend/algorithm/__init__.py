# 算法模块初始化
from .sort_algorithm import SortAlgorithm
from .search_algorithm import SearchAlgorithm
from .shortest_path import ShortestPath
from .multi_point_path import MultiPointPath
from .indoor_navigation import IndoorNavigation
from .text_search import TextSearch
from .lossless_compression import LosslessCompression

__all__ = ['SortAlgorithm', 'SearchAlgorithm', 'ShortestPath', 'MultiPointPath',
           'IndoorNavigation', 'TextSearch', 'LosslessCompression']
