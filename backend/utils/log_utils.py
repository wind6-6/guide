# 日志工具
import logging
import os
from datetime import datetime

class LogUtils:
    @staticmethod
    def setup_logger(name='tourism_system', log_file='app.log'):
        """设置日志"""
        # 确保日志目录存在
        log_dir = 'logs'
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        
        # 日志文件名
        log_path = os.path.join(log_dir, f'{log_file}_{datetime.now().strftime("%Y%m%d")}.log')
        
        # 创建logger
        logger = logging.getLogger(name)
        logger.setLevel(logging.DEBUG)
        
        # 创建文件处理器
        file_handler = logging.FileHandler(log_path, encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)
        
        # 创建控制台处理器
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        # 设置格式
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        # 添加处理器
        if not logger.handlers:
            logger.addHandler(file_handler)
            logger.addHandler(console_handler)
        
        return logger
    
    @staticmethod
    def get_logger(name='tourism_system'):
        """获取logger"""
        return logging.getLogger(name)
