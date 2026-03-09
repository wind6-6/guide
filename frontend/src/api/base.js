/**
 * API 基础配置
 * 存放所有后端接口地址
 */
const base = {
  baseUrl: "http://localhost:8080",     // 后端服务地址
  
  // 用户相关
  login: "/api/user/login",             // 登录
  register: "/api/user/register",       // 注册
  userInfo: "/api/user/info",           // 获取用户信息
  
  // 景点推荐
  recommendList: "/api/recommend/list",     // 推荐列表
  recommendSort: "/api/recommend/sort",     // 排序
  
  // 路线规划
  routePlan: "/api/route/plan",         // 路线规划（最短路径）
  routeNavigate: "/api/route/navigate", // 多点导航
  
  // 场所查询
  placeSearch: "/api/place/search",     // 场所搜索
  placeNearby: "/api/place/nearby",     // 附近设施
  
  // 旅游日记
  diaryList: "/api/diary/list",         // 日记列表
  diaryCreate: "/api/diary/create",     // 创建日记
  
  // 美食推荐
  foodList: "/api/food/list",           // 美食列表
  foodRecommend: "/api/food/recommend"  // 美食推荐
}

export default base
