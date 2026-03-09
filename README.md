# 个性化旅游系统

基于Vue + Flask的前后端分离旅游系统，支持景点推荐、路线规划、场所查询、旅游日记、美食推荐等功能。

## 项目结构

```
tourism-system/
├── frontend/          # 前端（Vue 3）
├── backend/           # 后端（Flask）
├── database/          # 数据库脚本
├── docs/              # 文档
├── test/              # 测试
└── README.md          # 项目说明
```

## 快速开始

### 后端启动

1. 进入后端目录
```bash
cd backend
```

2. 安装依赖
```bash
pip install -r requirements.txt
```

3. 配置数据库
修改 `backend/config/db_config.py` 中的数据库配置

4. 启动服务
```bash
python app.py
```
服务将运行在 http://localhost:8080

### 前端启动

1. 进入前端目录
```bash
cd frontend
```

2. 安装依赖
```bash
npm install
```

3. 启动开发服务器
```bash
npm run serve
```
前端将运行在 http://localhost:8081

## 功能说明

### 后端API

- `/api/user/login` - 用户登录
- `/api/user/register` - 用户注册
- `/api/recommend/list` - 景点推荐
- `/api/route/plan` - 路线规划
- `/api/place/search` - 场所查询
- `/api/diary/list` - 日记列表
- `/api/food/list` - 美食列表

### 前端页面

- `/login` - 登录页
- `/register` - 注册页
- `/` - 首页
- `/recommend` - 景点推荐
- `/route-plan` - 路线规划
- `/place-query` - 场所查询
- `/diary` - 旅游日记
- `/food` - 美食推荐
- `/user` - 用户中心

## 技术栈

- **前端**：Vue 3 + Vue Router + Element Plus + Axios
- **后端**：Flask + SQLAlchemy + JWT + Flask-CORS
- **数据库**：MySQL / SQLite
- **算法**：排序、搜索、最短路径、文本搜索、压缩

## 注意事项

1. 首次启动时会自动创建数据库表并插入初始数据
2. 初始用户账号：
   - 用户名：admin，密码：123456
   - 用户名：user1-9，密码：123456
3. 本地数据库需要提前创建好（MySQL）
