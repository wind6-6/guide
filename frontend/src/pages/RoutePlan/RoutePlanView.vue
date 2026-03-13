<template>
  <div class="route-plan-container">
    <!-- 页面标题 -->
    <div class="page-header">
      <h1 class="page-title">
        <el-icon><MapLocation /></el-icon>
        智能路线规划
      </h1>
      <p class="page-subtitle">多种策略，智能导航，让出行更便捷</p>
    </div>

    <el-row :gutter="20">
      <!-- 左侧控制面板 -->
      <el-col :span="6">
        <el-card shadow="hover" class="control-card">
          <template #header>
            <div class="card-header">
              <el-icon><Setting /></el-icon>
              <span>规划设置</span>
            </div>
          </template>
          
          <el-form :model="routeForm" label-position="top" class="route-form">
            <el-form-item label="起点">
              <el-select
                v-model="routeForm.start"
                placeholder="请选择起点（可搜索地址）"
                clearable
                filterable
                :filter-method="filterScenicByAddress"
              >
                <el-option
                  v-for="scenic in filteredStartOptions"
                          :key="scenic.id"
                          :label="scenic.name"
                          :value="scenic.name"
                        >
                          <div class="option-content">
                            <span class="option-name">{{ scenic.name }}</span>
                            <div class="option-meta">
                              <span class="option-category">{{ scenic.category }}</span>
                              <span class="option-hotness" v-if="scenic.hotness > 9.0">🔥</span>
                            </div>
                            <span class="option-address">{{ scenic.address }}</span>
                          </div>
                        </el-option>
              </el-select>
            </el-form-item>
            
            <el-form-item label="终点">
              <el-select
                v-model="routeForm.end"
                placeholder="请选择终点（可搜索地址）"
                clearable
                filterable
                :filter-method="filterScenicByAddress"
              >
                <el-option
                  v-for="scenic in filteredEndOptions"
                          :key="scenic.id"
                          :label="scenic.name"
                          :value="scenic.name"
                        >
                          <div class="option-content">
                            <span class="option-name">{{ scenic.name }}</span>
                            <div class="option-meta">
                              <span class="option-category">{{ scenic.category }}</span>
                              <span class="option-hotness" v-if="scenic.hotness > 9.0">🔥</span>
                            </div>
                            <span class="option-address">{{ scenic.address }}</span>
                          </div>
                        </el-option>
              </el-select>
            </el-form-item>
            
            <el-form-item label="规划策略">
              <el-radio-group v-model="routeForm.strategy" class="strategy-group">
                <el-radio-button label="distance">
                  <el-icon><ScaleToOriginal /></el-icon>
                  最短距离
                </el-radio-button>
                <el-radio-button label="time">
                  <el-icon><Timer /></el-icon>
                  最短时间
                </el-radio-button>
              </el-radio-group>
            </el-form-item>
            
            <el-form-item label="交通工具">
              <el-select v-model="routeForm.transport" placeholder="选择交通工具">
                <el-option label="🚶 步行" value="walk">
                  <span>🚶 步行</span>
                  <span style="float: right; color: #8492a6; font-size: 13px">5 km/h</span>
                </el-option>
                <el-option label="🚴 自行车" value="bike">
                  <span>🚴 自行车</span>
                  <span style="float: right; color: #8492a6; font-size: 13px">15 km/h</span>
                </el-option>
                <el-option label="🛵 电瓶车" value="scooter">
                  <span>🛵 电瓶车</span>
                  <span style="float: right; color: #8492a6; font-size: 13px">25 km/h</span>
                </el-option>
                <el-option label="🚗 汽车" value="car">
                  <span>🚗 汽车</span>
                  <span style="float: right; color: #8492a6; font-size: 13px">40 km/h</span>
                </el-option>
              </el-select>
            </el-form-item>
            
            <el-form-item>
              <el-button
                type="primary"
                size="large"
                @click="handlePlan"
                :loading="planning"
                :icon="MapLocation"
                style="width: 100%"
              >
                开始规划
              </el-button>
            </el-form-item>
            
            <el-form-item>
              <el-button
                size="large"
                @click="compareTransport"
                :icon="DataAnalysis"
                style="width: 100%"
              >
                对比交通工具
              </el-button>
            </el-form-item>
          </el-form>
        </el-card>

        <!-- 路线结果 -->
        <el-card v-if="routeResult" shadow="hover" class="result-card">
          <template #header>
            <div class="card-header">
              <el-icon><Check /></el-icon>
              <span>规划结果</span>
            </div>
          </template>
          <div class="route-result">
            <div class="result-item">
              <el-icon><MapLocation /></el-icon>
              <div class="result-info">
                <div class="result-label">路径</div>
                <div class="result-value path-text">{{ routeResult.path.join(' → ') }}</div>
              </div>
            </div>
            <el-divider></el-divider>
            <div class="result-item">
              <el-icon><ScaleToOriginal /></el-icon>
              <div class="result-info">
                <div class="result-label">总距离</div>
                <div class="result-value">{{ formatDistance(routeResult.distance) }}</div>
              </div>
            </div>
            <el-divider></el-divider>
            <div class="result-item">
              <el-icon><Timer /></el-icon>
              <div class="result-info">
                <div class="result-label">预计时间</div>
                <div class="result-value">{{ formatTime(routeResult.time) }}</div>
              </div>
            </div>
            <el-divider></el-divider>
            <div class="result-item">
              <el-icon><Compass /></el-icon>
              <div class="result-info">
                <div class="result-label">规划策略</div>
                <div class="result-value">
                  <el-tag :type="routeResult.strategy === 'distance' ? 'success' : 'primary'">
                    {{ routeResult.strategy === 'distance' ? '最短距离' : '最短时间' }}
                  </el-tag>
                </div>
              </div>
            </div>
          </div>
        </el-card>

        <!-- 交通工具对比 -->
        <el-card v-if="transportComparison.length > 0" shadow="hover" class="comparison-card">
          <template #header>
            <div class="card-header">
              <el-icon><DataAnalysis /></el-icon>
              <span>交通工具对比</span>
            </div>
          </template>
          <div class="comparison-list">
            <div
              v-for="(item, index) in transportComparison"
              :key="index"
              class="comparison-item"
              :class="{ 'best-option': index === 0 }"
            >
              <div class="transport-icon">{{ item.icon }}</div>
              <div class="transport-info">
                <div class="transport-name">{{ item.name }}</div>
                <div class="transport-stats">
                  <span>{{ formatDistance(item.distance) }}</span>
                  <span>{{ formatTime(item.time) }}</span>
                </div>
              </div>
              <el-tag v-if="index === 0" type="success" size="small">推荐</el-tag>
            </div>
          </div>
        </el-card>
      </el-col>

      <!-- 右侧地图区域 -->
      <el-col :span="18">
        <el-card shadow="hover" class="map-card">
          <template #header>
            <div class="card-header">
              <el-icon><MapLocation /></el-icon>
              <span>地图导航</span>
              <el-radio-group v-model="mapType" size="small" style="margin-left: auto">
                <el-radio-button label="standard">标准</el-radio-button>
                <el-radio-button label="satellite">卫星</el-radio-button>
              </el-radio-group>
            </div>
          </template>
          <MapViewer
            :nodes="mapNodes"
            :edges="mapEdges"
            :path="mapPath"
            :path-length="routeResult?.distance || 0"
            :estimated-time="routeResult?.time || 0"
            :transport-type="routeForm.transport"
            @node-click="onNodeClick"
          />
        </el-card>

        <!-- 导航步骤 -->
        <el-card v-if="routeResult && routeResult.steps" shadow="hover" class="steps-card">
          <template #header>
            <div class="card-header">
              <el-icon><List /></el-icon>
              <span>导航步骤</span>
            </div>
          </template>
          <el-timeline>
            <el-timeline-item
              v-for="(step, index) in routeResult.steps"
              :key="index"
              :type="index === 0 ? 'primary' : index === routeResult.steps.length - 1 ? 'success' : ''"
              :icon="index === 0 ? MapLocation : index === routeResult.steps.length - 1 ? Check : ''"
            >
              <div class="step-content">
                <div class="step-title">{{ step.name }}</div>
                <div class="step-address" v-if="step.address">{{ step.address }}</div>
                <div class="step-description">{{ step.description }}</div>
                <div class="step-distance" v-if="step.distance">{{ formatDistance(step.distance) }}</div>
              </div>
            </el-timeline-item>
          </el-timeline>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import { MapLocation, Setting, ScaleToOriginal, Timer, Check, List, DataAnalysis } from '@element-plus/icons-vue'
import MapViewer from '../../components/MapViewer.vue'

export default {
  name: 'RoutePlanView',
  components: {
    MapLocation,
    Setting,
    ScaleToOriginal,
    Timer,
    Check,
    List,
    DataAnalysis,
    MapViewer
  },
  data() {
    return {
      routeForm: {
        start: '',
        end: '',
        strategy: 'distance',
        transport: 'walk'
      },
      routeResult: null,
      transportComparison: [],
      planning: false,
      mapType: 'standard',
      mapNodes: [],
      mapEdges: [],
      mapPath: [],
      realScenics: [], // 存储真实景区数据
      filteredStartOptions: [], // 过滤后的起点选项
      filteredEndOptions: [], // 过滤后的终点选项
      searchQuery: '' // 搜索查询
    }
  },
  mounted() {
    this.loadRealMapData()
  },
  watch: {
    realScenics: {
      handler(newScenics) {
        this.filteredStartOptions = [...newScenics]
        this.filteredEndOptions = [...newScenics]
      },
      deep: true
    }
  },
  methods: {
    async handlePlan() {
      if (!this.routeForm.start || !this.routeForm.end) {
        this.$message.error('起点和终点不能为空')
        return
      }
      
      this.planning = true
      
      try {
        // 映射交通工具类型为中文
        const transportMap = {
          walk: '步行',
          bike: '自行车',
          scooter: '电瓶车',
          car: '汽车'
        }
        
        // 调用真实后端 API
        const response = await this.$http.post('/api/route/plan', {
          start: this.routeForm.start,
          end: this.routeForm.end,
          strategy: this.routeForm.strategy,
          transport_type: transportMap[this.routeForm.transport] || '步行'
        })
        
        console.log('发送的请求参数:', {
          start: this.routeForm.start,
          end: this.routeForm.end,
          strategy: this.routeForm.strategy,
          transport_type: this.routeForm.transport
        })
        
        if (response.data.status === 200) {
          const data = response.data.data
          
          this.routeResult = {
            path: data.path,
            distance: data.distance,
            time: data.estimated_time,
            strategy: data.strategy,
            steps: this.generateSteps(data.path, data.distance)
          }
          
          // 更新地图路径
          this.mapPath = this.convertPathToMapPath(data.path)
          
          // 将路径中的道路节点添加到地图节点列表
          this.addPathNodesToMap()
          
          this.$message.success('路线规划成功！')
        } else {
          this.$message.error('路线规划失败: ' + (response.data.msg || '未知错误'))
        }
      } catch (error) {
        console.error('路线规划失败:', error)
        console.error('错误详情:', error.message, error.response?.data)
        this.$message.error('路线规划失败: ' + (error.message || '网络错误'))
        // 使用模拟数据作为备份
        this.useMockData()
      } finally {
        this.planning = false
      }
    },
    
    // 生成导航步骤
    generateSteps(path, distance) {
      const steps = []
      const stepDistance = distance / (path.length - 1)
      
      for (let i = 0; i < path.length; i++) {
        const nodeName = path[i]
        const node = this.mapNodes.find(n => n.name === nodeName) || this.mapNodes.find(n => n.name.includes(nodeName) || nodeName.includes(n.name))
        const step = {
          name: nodeName,
          address: node?.address || '',
          description: i === 0 ? '起点位置' : i === path.length - 1 ? '到达目的地' : `沿路径前往 ${path[i+1]}`,
          distance: i === 0 ? 0 : Math.round(stepDistance * i)
        }
        steps.push(step)
      }
      
      return steps
    },
    
    // 将路径转换为地图路径
    convertPathToMapPath(path) {
      const mapPath = []
      
      for (let i = 0; i < path.length; i++) {
        const nodeName = path[i]
        
        // 尝试在地图节点中找到对应节点
        let node = this.mapNodes.find(n => n.name === nodeName)
        
        // 如果找不到精确匹配，尝试模糊匹配
        if (!node) {
          node = this.mapNodes.find(n => n.name.includes(nodeName) || nodeName.includes(n.name))
        }
        
        if (node) {
          mapPath.push({
            id: node.id,
            x: node.x,
            y: node.y,
            name: node.name
          })
        } else {
          // 为道路节点生成固定坐标（基于名称哈希）
          const hash = this.stringHash(nodeName)
          const x = 100 + (hash % 600)
          const y = 100 + ((hash / 600) % 400)
          
          // 确保坐标在地图范围内
          const fixedX = Math.max(50, Math.min(750, x))
          const fixedY = Math.max(50, Math.min(550, y))
          
          mapPath.push({
            id: `road-${nodeName}`,
            x: fixedX,
            y: fixedY,
            name: nodeName,
            type: 'road'
          })
        }
      }
      
      return mapPath
    },
    
    // 使用模拟数据作为备份
    useMockData() {
      const speeds = { walk: 5, bike: 15, scooter: 25, car: 40 }
      const speed = speeds[this.routeForm.transport] || 5
      const distance = 2500
      const time = (distance / 1000) / speed * 60
      
      this.routeResult = {
        path: [this.routeForm.start, '节点1', '节点2', '节点3', this.routeForm.end],
        distance: distance,
        time: time,
        strategy: this.routeForm.strategy,
        steps: [
          { name: this.routeForm.start, description: '起点位置', distance: 0 },
          { name: '节点1', description: '沿主干道前行', distance: 500 },
          { name: '节点2', description: '左转进入次干道', distance: 800 },
          { name: '节点3', description: '直行通过路口', distance: 700 },
          { name: this.routeForm.end, description: '到达目的地', distance: 500 }
        ]
      }
      
      // 更新地图路径
      this.mapPath = [
        { id: 'A', x: 100, y: 300 },
        { id: 'B', x: 250, y: 200 },
        { id: 'C', x: 400, y: 300 },
        { id: 'D', x: 550, y: 200 },
        { id: 'E', x: 700, y: 300 }
      ]
    },
    compareTransport() {
      if (!this.routeForm.start || !this.routeForm.end) {
        this.$message.error('请先输入起点和终点')
        return
      }
      
      const distance = 2500
      const transports = [
        { name: '步行', icon: '🚶', speed: 5 },
        { name: '自行车', icon: '🚴', speed: 15 },
        { name: '电瓶车', icon: '🛵', speed: 25 },
        { name: '汽车', icon: '🚗', speed: 40 }
      ]
      
      this.transportComparison = transports.map(t => ({
        ...t,
        distance: distance,
        time: (distance / 1000) / t.speed * 60
      })).sort((a, b) => a.time - b.time)
      
      this.$message.success('交通工具对比完成！')
    },
    onNodeClick(node) {
      this.$message.info(`点击了节点: ${node.name}\n地址: ${node.address}`)
    },
    
    // 根据地址过滤景区
    filterScenicByAddress(query, type = 'start') {
      if (!query) {
        if (type === 'start') {
          this.filteredStartOptions = [...this.realScenics]
        } else {
          this.filteredEndOptions = [...this.realScenics]
        }
        return
      }
      
      const filtered = this.realScenics.filter(scenic => {
        const searchTerm = query.toLowerCase()
        return (
          scenic.name.toLowerCase().includes(searchTerm) ||
          (scenic.address && scenic.address.toLowerCase().includes(searchTerm)) ||
          (scenic.category && scenic.category.toLowerCase().includes(searchTerm))
        )
      })
      
      if (type === 'start') {
        this.filteredStartOptions = filtered
      } else {
        this.filteredEndOptions = filtered
      }
    },
    
    // 计算两点之间的距离（Haversine公式）
    calculateDistance(lat1, lon1, lat2, lon2) {
      const R = 6371e3; // 地球半径（米）
      const φ1 = lat1 * Math.PI / 180;
      const φ2 = lat2 * Math.PI / 180;
      const Δφ = (lat2 - lat1) * Math.PI / 180;
      const Δλ = (lon2 - lon1) * Math.PI / 180;
      
      const a =
        Math.sin(Δφ / 2) * Math.sin(Δφ / 2) +
        Math.cos(φ1) * Math.cos(φ2) * Math.sin(Δλ / 2) * Math.sin(Δλ / 2);
      const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
      
      return R * c;
    },
    
    // 字符串哈希函数（生成固定的哈希值）
    stringHash(str) {
      let hash = 0;
      for (let i = 0; i < str.length; i++) {
        const char = str.charCodeAt(i);
        hash = ((hash << 5) - hash) + char;
        hash = hash & hash; // 转换为32位整数
      }
      return Math.abs(hash);
    },
    
    // 将路径中的道路节点添加到地图节点列表
    addPathNodesToMap() {
      if (!this.mapPath || this.mapPath.length === 0) return;
      
      // 遍历路径中的所有节点
      this.mapPath.forEach(pathNode => {
        // 检查该节点是否已经在地图节点中
        const exists = this.mapNodes.some(node => node.name === pathNode.name);
        
        if (!exists && pathNode.type === 'road') {
          // 添加道路节点到地图节点列表
          this.mapNodes.push({
            id: pathNode.id,
            name: pathNode.name,
            x: pathNode.x,
            y: pathNode.y,
            type: 'node', // 使用 node 类型，对应灰色
            icon: '🚦' // 道路节点使用交通灯图标
          });
        }
      });
    },
    formatDistance(meters) {
      if (meters >= 1000) {
        return (meters / 1000).toFixed(2) + ' km'
      }
      return meters + ' m'
    },
    formatTime(minutes) {
      if (minutes >= 60) {
        const hours = Math.floor(minutes / 60)
        const mins = Math.round(minutes % 60)
        return `${hours}小时${mins}分钟`
      }
      return Math.round(minutes) + '分钟'
    },
    
    // 加载真实地图数据
    async loadRealMapData() {
      try {
        console.log('开始加载地图数据...')
        
        // 获取路径规划使用的所有节点（与后端一致）
        console.log('请求节点数据...')
        const [nodesResponse, roadsResponse] = await Promise.all([
          this.$http.get('/api/route/nodes'),
          this.$http.get('/api/route/roads')
        ])
        
        console.log('节点数据响应:', nodesResponse)
        console.log('道路数据响应:', roadsResponse)
        
        // 处理节点数据（只使用前20个）
        if (nodesResponse.data && nodesResponse.data.data) {
          // 只取前20个节点
          this.realScenics = nodesResponse.data.data.slice(0, 20)
          console.log(`获取到 ${this.realScenics.length} 个景区节点`)
          // 将景区转换为地图节点（使用真实经纬度）
          this.mapNodes = this.convertScenicsToNodes(this.realScenics)
          console.log(`转换了 ${this.mapNodes.length} 个地图节点`)
          
          // 更新起终点选项
          this.filteredStartOptions = [...this.realScenics]
          this.filteredEndOptions = [...this.realScenics]
        } else {
          console.warn('节点数据格式不正确:', nodesResponse.data)
        }
        
        // 处理道路数据
        if (roadsResponse.data && roadsResponse.data.data) {
          this.roads = roadsResponse.data.data
          console.log(`获取到 ${this.roads.length} 条道路`)
        }
        
        // 生成道路网络
        this.mapEdges = this.generateOptimizedRoads()
        console.log(`生成了 ${this.mapEdges.length} 条地图边`)
        
        if (this.mapNodes.length > 0) {
          this.$message.success(`已加载 ${this.mapNodes.length} 个景区和 ${this.mapEdges.length} 条道路`)
        } else {
          throw new Error('没有获取到有效的地图数据')
        }
      } catch (error) {
        console.error('加载地图数据失败:', error)
        console.error('错误详情:', error.message, error.response?.data)
        this.$message.error('加载地图数据失败: ' + (error.message || '网络错误'))
        // 使用默认数据
        this.loadDefaultMapData()
      }
    },
    
    // 将景区数据转换为地图节点 - 使用力导向布局
    convertScenicsToNodes(scenics) {
      // 初始位置：基于经纬度
      const nodes = scenics.map((scenic) => {
        let lat, lng
        
        if (scenic.lat && scenic.lng) {
          lat = scenic.lat
          lng = scenic.lng
        } else {
          const hash = this.stringHash(scenic.name)
          lat = 39.9 + (hash % 100) / 100 * 0.5
          lng = 116.4 + ((hash / 100) % 100) / 100 * 0.5
        }
        
        return {
          id: `scenic-${scenic.id}`,
          name: scenic.name,
          address: scenic.address,
          lat: lat,
          lng: lng,
          x: 400 + (lng - 116.4) * 200,  // 初始x
          y: 300 - (lat - 39.9) * 200,   // 初始y
          type: 'building',
          icon: '🏛️',
          category: scenic.category,
          hotness: scenic.hotness || 5
        }
      })
      
      // 力导向布局算法（简化版）
      const iterations = 50
      const k = 100  // 理想边长
      const width = 800
      const height = 600
      
      for (let iter = 0; iter < iterations; iter++) {
        // 计算斥力
        for (let i = 0; i < nodes.length; i++) {
          for (let j = i + 1; j < nodes.length; j++) {
            const dx = nodes[i].x - nodes[j].x
            const dy = nodes[i].y - nodes[j].y
            const dist = Math.sqrt(dx * dx + dy * dy) + 0.1
            const force = (k * k) / dist
            
            const fx = (dx / dist) * force * 0.05
            const fy = (dy / dist) * force * 0.05
            
            nodes[i].x += fx
            nodes[i].y += fy
            nodes[j].x -= fx
            nodes[j].y -= fy
          }
        }
        
        // 中心引力（防止节点飞散）
        nodes.forEach(node => {
          const dx = width / 2 - node.x
          const dy = height / 2 - node.y
          node.x += dx * 0.01
          node.y += dy * 0.01
        })
        
        // 边界限制
        nodes.forEach(node => {
          node.x = Math.max(60, Math.min(width - 60, node.x))
          node.y = Math.max(60, Math.min(height - 60, node.y))
        })
      }
      
      return nodes
    },
    
    // 生成道路网络 - 只使用从后端加载的真实道路数据
    generateOptimizedRoads() {
      // 如果有从后端加载的道路数据，使用它们
      if (this.roads && this.roads.length > 0) {
        return this.convertRoadsToEdges(this.roads)
      }
      
      // 如果没有道路数据，返回空数组
      return []
    },
    
    // 将道路数据转换为边
    convertRoadsToEdges(roads) {
      const edges = []
      const nodeMap = new Map()
      
      // 创建节点名称到节点的映射
      this.mapNodes.forEach(node => {
        nodeMap.set(node.name, node)
      })
      
      roads.forEach(road => {
        const startNode = nodeMap.get(road.start)
        const endNode = nodeMap.get(road.end)
        
        if (startNode && endNode) {
          // 根据拥挤程度设置颜色
          let color = '#67c23a'  // 绿色 - 畅通
          if (road.crowd_level > 3) color = '#e6a23c'  // 黄色 - 拥挤
          if (road.crowd_level > 4) color = '#f56c6c'  // 红色 - 拥堵
          
          edges.push({
            x1: startNode.x,
            y1: startNode.y,
            x2: endNode.x,
            y2: endNode.y,
            color: color,
            width: road.crowd_level > 3 ? 4 : 3,
            distance: road.distance,
            crowd_level: road.crowd_level,
            transport_type: road.transport_type || '步行'
          })
        }
      })
      
      return edges
    },
    

    
    // 加载默认地图数据（当API失败时使用）
    loadDefaultMapData() {
      this.mapNodes = [
        { id: 'A', name: '故宫博物院', x: 400, y: 300, type: 'building', icon: '🏛️' },
        { id: 'B', name: '颐和园', x: 200, y: 150, type: 'building', icon: '🏛️' },
        { id: 'C', name: '天坛公园', x: 600, y: 400, type: 'building', icon: '🏛️' },
        { id: 'D', name: '北海公园', x: 300, y: 250, type: 'building', icon: '🏛️' },
        { id: 'E', name: '景山公园', x: 380, y: 280, type: 'building', icon: '🏛️' }
      ]
      
      this.mapEdges = [
        { x1: 400, y1: 300, x2: 380, y2: 280, color: '#67c23a' },
        { x1: 380, y1: 280, x2: 300, y2: 250, color: '#67c23a' },
        { x1: 300, y1: 250, x2: 200, y2: 150, color: '#e6a23c' },
        { x1: 400, y1: 300, x2: 600, y2: 400, color: '#f56c6c' }
      ]
    }
  }
}
</script>

<style scoped>
.route-plan-container {
  padding: 20px;
  background: linear-gradient(135deg, #f5f7fa 0%, #e4e7ed 100%);
  min-height: 100vh;
}

/* 页面标题 */
.page-header {
  text-align: center;
  margin-bottom: 30px;
  padding: 30px 0;
  background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
  border-radius: 12px;
  color: white;
}

.page-title {
  font-size: 32px;
  margin: 0 0 10px 0;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
}

.page-subtitle {
  font-size: 16px;
  opacity: 0.9;
  margin: 0;
}

/* 控制卡片 */
.control-card {
  border-radius: 12px;
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: bold;
}

.strategy-group {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.strategy-group .el-radio-button {
  width: 100%;
}

/* 结果卡片 */
.result-card {
  border-radius: 12px;
  margin-bottom: 20px;
}

.route-result {
  padding: 10px 0;
}

.result-item {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  padding: 8px 0;
}

.result-item .el-icon {
  font-size: 20px;
  color: #409eff;
  margin-top: 2px;
}

.result-info {
  flex: 1;
}

.result-label {
  font-size: 12px;
  color: #909399;
  margin-bottom: 4px;
}

.result-value {
  font-size: 16px;
  font-weight: bold;
  color: #303133;
}

.path-text {
  word-break: break-all;
  line-height: 1.6;
}

/* 对比卡片 */
.comparison-card {
  border-radius: 12px;
}

.comparison-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.comparison-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px;
  border-radius: 8px;
  background: #f5f7fa;
  transition: all 0.3s ease;
}

.comparison-item:hover {
  background: #e4e7ed;
}

.comparison-item.best-option {
  background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%);
  border: 1px solid #28a745;
}

.transport-icon {
  font-size: 24px;
}

.transport-info {
  flex: 1;
}

.transport-name {
  font-weight: bold;
  margin-bottom: 4px;
}

.transport-stats {
  display: flex;
  gap: 15px;
  font-size: 13px;
  color: #606266;
}

/* 地图卡片 */
.map-card {
  border-radius: 12px;
  margin-bottom: 20px;
}

.map-card :deep(.el-card__body) {
  padding: 0;
}

/* 步骤卡片 */
.steps-card {
  border-radius: 12px;
}

.step-content {
  padding: 8px 0;
}

.step-title {
  font-weight: bold;
  font-size: 15px;
  margin-bottom: 4px;
}

.step-address {
  color: #909399;
  font-size: 12px;
  margin-bottom: 4px;
  font-style: italic;
}

.step-description {
  color: #606266;
  font-size: 13px;
  margin-bottom: 4px;
}

.step-distance {
  color: #409eff;
  font-size: 12px;
}

/* Dropdown option styles */
.option-content {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 4px;
  padding: 8px 0;
}

.option-name {
  font-weight: 500;
  font-size: 14px;
  width: 100%;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.option-meta {
  display: flex;
  align-items: center;
  gap: 8px;
  width: 100%;
}

.option-category {
  font-size: 12px;
  color: #909399;
  background: #f0f9eb;
  padding: 2px 8px;
  border-radius: 10px;
}

.option-address {
  font-size: 11px;
  color: #606266;
  font-style: italic;
  width: 100%;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.option-hotness {
  font-size: 14px;
}
</style>