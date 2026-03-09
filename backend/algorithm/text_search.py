# 文本搜索算法
import re
from collections import Counter

class TextSearch:
    @staticmethod
    def keyword_search(text, keywords):
        """关键词搜索"""
        results = []
        text_lower = text.lower()
        
        for keyword in keywords:
            keyword_lower = keyword.lower()
            matches = re.finditer(keyword_lower, text_lower)
            for match in matches:
                start = max(0, match.start() - 50)
                end = min(len(text), match.end() + 50)
                snippet = text[start:end]
                results.append({
                    'keyword': keyword,
                    'position': match.start(),
                    'snippet': snippet
                })
        
        return results
    
    @staticmethod
    def similarity_search(texts, query, top_n=10):
        """文本相似度搜索"""
        results = []
        
        for text in texts:
            # 简单的词频相似度计算
            text_words = set(re.findall(r'\w+', text.lower()))
            query_words = set(re.findall(r'\w+', query.lower()))
            
            # 计算交集
            intersection = text_words & query_words
            similarity = len(intersection) / (len(text_words) + len(query_words) - len(intersection)) if text_words or query_words else 0
            
            results.append((similarity, text))
        
        # 按相似度排序
        results.sort(key=lambda x: x[0], reverse=True)
        return [text for _, text in results[:top_n]]
