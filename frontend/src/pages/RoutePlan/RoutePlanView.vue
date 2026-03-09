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
              <el-input
                v-model="routeForm.start"
                placeholder="请输入起点"
                clearable
              >
                <template #prefix>
                  <el-icon><Location /></el-icon>
                </template>
              </el-input>
            </el-form-item>
            
            <el-form-item label="终点">
              <el-input
                v-model="routeForm.end"
                placeholder="请输入终点"
                clearable
              >
                <template #prefix>
                  <el-icon><Flag /></el-icon>
                </template>
              </el-input>
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
              :icon="index === 0 ? Location : index === routeResult.steps.length - 1 ? Flag : ''"
            >
              <div class="step-content">
                <div class="step-title">{{ step.name }}</div>
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
import { MapLocation, Setting, Location, Flag, ScaleToOriginal, Timer, Check, Compass, DataAnalysis, List } from '@element-plus/icons-vue'
import MapViewer from '../../components/MapViewer.vue'

export default {
  name: 'RoutePlanView',
  components: {
    MapLocation,
    Setting,
    Location,
    Flag,
    ScaleToOriginal,
    Timer,
    Check,
    Compass,
    DataAnalysis,
    List,
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
      mapNodes: [
        { id: 'A', name: '起点', x: 100, y: 300, type: 'current', icon: '📍' },
        { id: 'B', name: '节点1', x: 250, y: 200, type: 'node' },
        { id: 'C', name: '节点2', x: 400, y: 300, type: 'node' },
        { id: 'D', name: '节点3', x: 550, y: 200, type: 'node' },
        { id: 'E', name: '终点', x: 700, y: 300, type: 'building', icon: '🏁' }
      ],
      mapEdges: [
        { x1: 100, y1: 300, x2: 250, y2: 200, color: '#ccc' },
        { x1: 250, y1: 200, x2: 400, y2: 300, color: '#ccc' },
        { x1: 400, y1: 300, x2: 550, y2: 200, color: '#ccc' },
        { x1: 550, y1: 200, x2: 700, y2: 300, color: '#ccc' },
        { x1: 100, y1: 300, x2: 400, y2: 300, color: '#ddd', dashed: true },
        { x1: 250, y1: 200, x2: 550, y2: 200, color: '#ddd', dashed: true }
      ],
      mapPath: []
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
        // 模拟规划
        await new Promise(resolve => setTimeout(resolve, 1000))
        
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
        
        this.$message.success('路线规划成功！')
      } catch (error) {
        console.error('路线规划失败:', error)
        this.$message.error('路线规划失败')
      } finally {
        this.planning = false
      }
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
      this.$message.info(`点击了节点: ${node.name}`)
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

.step-description {
  color: #606266;
  font-size: 13px;
  margin-bottom: 4px;
}

.step-distance {
  color: #409eff;
  font-size: 12px;
}
</style>