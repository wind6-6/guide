#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
重新初始化数据库并导入真实北京地图数据
"""

import os
import sys

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database.db_init import create_tables, insert_initial_data, init_database
from sqlalchemy import text

def reset_database():
    """重置数据库（删除所有表并重新创建）"""
    print("正在重置数据库...")
    
    engine, _ = init_database()
    
    # 删除所有表
    with engine.connect() as conn:
        # 获取所有表名
        result = conn.execute(text("SELECT name FROM sqlite_master WHERE type='table'"))
        tables = [row[0] for row in result if row[0] != 'sqlite_sequence']
        
        # 删除每个表
        for table in tables:
            try:
                conn.execute(text(f"DROP TABLE IF EXISTS {table}"))
                print(f"  删除表: {table}")
            except Exception as e:
                print(f"  删除表 {table} 失败: {e}")
        
        conn.commit()
    
    print("数据库重置完成\n")

def main():
    """主函数"""
    print("=" * 60)
    print("北京旅游导览系统 - 真实地图数据初始化")
    print("=" * 60)
    print()
    
    # 询问是否重置数据库
    response = input("是否重置数据库？这将删除所有现有数据！(y/N): ").strip().lower()
    
    if response == 'y' or response == 'yes':
        reset_database()
    
    # 创建表
    print("正在创建数据库表...")
    create_tables()
    print()
    
    # 插入真实数据
    print("正在导入真实北京地图数据...")
    print("-" * 60)
    insert_initial_data()
    print("-" * 60)
    print()
    
    print("=" * 60)
    print("数据初始化完成！")
    print("=" * 60)
    print()
    print("现在您可以：")
    print("1. 启动后端服务: python run.py")
    print("2. 启动前端服务: npm run serve")
    print("3. 访问系统查看真实地图数据")
    print()

if __name__ == "__main__":
    main()
