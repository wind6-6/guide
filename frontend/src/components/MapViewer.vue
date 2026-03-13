<template>
  <div class="map-container">
    <div ref="mapCanvas" class="map-canvas" @mousedown="startDrag" @mousemove="onDrag" @mouseup="endDrag" @mouseleave="endDrag">
      <svg ref="svgMap" :viewBox="viewBox" preserveAspectRatio="xMidYMid meet">
        <!-- 定义渐变和滤镜 -->
        <defs>
          <!-- 背景渐变 -->
          <linearGradient id="bgGradient" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" style="stop-color:#f8fafc;stop-opacity:1" />
            <stop offset="100%" style="stop-color:#e2e8f0;stop-opacity:1" />
          </linearGradient>
          
          <!-- 节点渐变 -->
          <radialGradient id="nodeGradient" cx="50%" cy="50%" r="50%">
            <stop offset="0%" style="stop-color:#60a5fa;stop-opacity:1" />
            <stop offset="100%" style="stop-color:#3b82f6;stop-opacity:1" />
          </radialGradient>
          
          <!-- 路径节点渐变 -->
          <radialGradient id="pathNodeGradient" cx="50%" cy="50%" r="50%">
            <stop offset="0%" style="stop-color:#fbbf24;stop-opacity:1" />
            <stop offset="100%" style="stop-color:#f59e0b;stop-opacity:1" />
          </radialGradient>
          
          <!-- 阴影滤镜 -->
          <filter id="shadow" x="-50%" y="-50%" width="200%" height="200%">
            <feDropShadow dx="0" dy="2" stdDeviation="3" flood-color="#000000" flood-opacity="0.15"/>
          </filter>
          
          <!-- 发光滤镜 -->
          <filter id="glow" x="-50%" y="-50%" width="200%" height="200%">
            <feGaussianBlur stdDeviation="3" result="coloredBlur"/>
            <feMerge>
              <feMergeNode in="coloredBlur"/>
              <feMergeNode in="SourceGraphic"/>
            </feMerge>
          </filter>
        </defs>
        
        <!-- 背景 -->
        <rect width="100%" height="100%" fill="url(#bgGradient)" rx="12" />
        
        <!-- 装饰性网格点 -->
        <g class="grid-dots" opacity="0.3">
          <circle v-for="n in 100" :key="'dot-'+n" 
            :cx="(n % 10) * 80 + 40" 
            :cy="Math.floor(n / 10) * 60 + 30" 
            r="1.5" 
            fill="#cbd5e1" />
        </g>
        
        <!-- 边（道路）- 45条路线清晰显示 -->
        <g class="edges">
          <line
            v-for="(edge, index) in visibleEdges"
            :key="'edge-'+index"
            :x1="edge.x1"
            :y1="edge.y1"
            :x2="edge.x2"
            :y2="edge.y2"
            :stroke="isPathEdge(edge) ? '#3b82f6' : '#94a3b8'"
            :stroke-width="isPathEdge(edge) ? 4 : 1.5"
            :opacity="isPathEdge(edge) ? 1 : 0.35"
            stroke-linecap="round"
            class="road-line"
          />
        </g>
        
        <!-- 路径 - 更醒目的样式 -->
        <g class="path" v-if="path.length > 1">
          <!-- 路径阴影 -->
          <polyline
            :points="pathPoints"
            fill="none"
            stroke="#1e40af"
            stroke-width="8"
            stroke-linecap="round"
            stroke-linejoin="round"
            opacity="0.2"
          />
          <!-- 主路径 -->
          <polyline
            :points="pathPoints"
            fill="none"
            stroke="url(#pathGradient)"
            stroke-width="5"
            stroke-linecap="round"
            stroke-linejoin="round"
            class="path-line"
            filter="url(#glow)"
          />
          <!-- 路径上的节点高亮 -->
          <circle
            v-for="(point, idx) in pathPointsArray"
            :key="'path-point-'+idx"
            :cx="point.x"
            :cy="point.y"
            r="8"
            fill="url(#pathNodeGradient)"
            stroke="#fff"
            stroke-width="2"
            filter="url(#shadow)"
          />
          <!-- 路径动画点 -->
          <circle r="5" fill="#fbbf24" filter="url(#glow)">
            <animateMotion :dur="animationDuration + 's'" repeatCount="indefinite" :path="pathD" />
          </circle>
        </g>
        
        <!-- 节点 - 极简风格 -->
        <g class="nodes">
          <g
            v-for="node in visibleNodes"
            :key="node.id"
            class="node-group"
            :transform="`translate(${node.x}, ${node.y})`"
            @click="onNodeClick(node)"
            @mouseenter="hoveredNode = node"
            @mouseleave="hoveredNode = null"
          >
            <!-- 路径节点外圈 -->
            <circle
              v-if="isPathNode(node)"
              r="16"
              fill="none"
              stroke="#3b82f6"
              stroke-width="3"
              opacity="0.3"
            />
            <!-- 节点圆圈 -->
            <circle
              :r="isPathNode(node) ? 10 : 8"
              :fill="isPathNode(node) ? '#3b82f6' : '#64748b'"
              stroke="#fff"
              stroke-width="2"
              class="node-circle"
            />
            <!-- 节点标签 - 只显示路径节点和悬停节点 -->
            <text
              v-if="isPathNode(node) || hoveredNode === node"
              y="-18"
              text-anchor="middle"
              font-size="12"
              font-weight="600"
              :fill="isPathNode(node) ? '#1d4ed8' : '#475569'"
              class="node-label"
            >{{ node.name }}</text>
          </g>
        </g>
        
        <!-- 定义路径渐变 -->
        <defs>
          <linearGradient id="pathGradient" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" style="stop-color:#3b82f6;stop-opacity:1" />
            <stop offset="50%" style="stop-color:#60a5fa;stop-opacity:1" />
            <stop offset="100%" style="stop-color:#3b82f6;stop-opacity:1" />
          </linearGradient>
        </defs>
      </svg>
    </div>
    
    <!-- 地图控制面板 -->
    <div class="map-controls">
      <el-button-group vertical>
        <el-button size="small" @click="zoomIn" icon="Plus" circle></el-button>
        <el-button size="small" @click="zoomOut" icon="Minus" circle></el-button>
        <el-button size="small" @click="resetView" icon="RefreshRight" circle></el-button>
      </el-button-group>
    </div>
    
    <!-- 路径信息面板 -->
    <div v-if="path.length > 0" class="path-info-panel">
      <el-card shadow="hover" :body-style="{ padding: '15px' }">
        <div class="path-stats">
          <div class="stat-item">
            <el-icon><MapLocation /></el-icon>
            <span class="stat-label">路径长度</span>
            <span class="stat-value">{{ formatDistance(pathLength) }}</span>
          </div>
          <div class="stat-item">
            <el-icon><Timer /></el-icon>
            <span class="stat-label">预计时间</span>
            <span class="stat-value">{{ formatTime(estimatedTime) }}</span>
          </div>
          <div v-if="transportType" class="stat-item">
            <el-icon><Bicycle /></el-icon>
            <span class="stat-label">交通工具</span>
            <span class="stat-value">{{ transportType }}</span>
          </div>
        </div>
      </el-card>
    </div>
    
    <!-- 图例 -->
    <div class="map-legend">
      <el-card shadow="hover" :body-style="{ padding: '10px' }">
        <div class="legend-title">图例</div>
        <div class="legend-item">
          <span class="legend-dot" style="background: #67c23a;"></span>
          <span>建筑物</span>
        </div>
        <div class="legend-item">
          <span class="legend-dot" style="background: #e6a23c;"></span>
          <span>设施</span>
        </div>
        <div class="legend-item">
          <span class="legend-dot" style="background: #f56c6c;"></span>
          <span>当前位置</span>
        </div>
        <div class="legend-item">
          <span class="legend-line" style="background: #409eff;"></span>
          <span>规划路径</span>
        </div>
      </el-card>
    </div>
  </div>
</template>

<script>
import { MapLocation, Timer, Bicycle } from '@element-plus/icons-vue'

export default {
  name: 'MapViewer',
  components: {
    MapLocation,
    Timer,
    Bicycle
  },
  props: {
    nodes: {
      type: Array,
      default: () => []
    },
    edges: {
      type: Array,
      default: () => []
    },
    path: {
      type: Array,
      default: () => []
    },
    pathLength: {
      type: Number,
      default: 0
    },
    estimatedTime: {
      type: Number,
      default: 0
    },
    transportType: {
      type: String,
      default: ''
    }
  },
  data() {
    return {
      scale: 1,
      offsetX: 0,
      offsetY: 0,
      isDragging: false,
      lastMouseX: 0,
      lastMouseY: 0,
      hoveredNode: null,
      viewBox: '0 0 800 600',
      baseViewBox: '0 0 800 600'
    }
  },
  computed: {
    pathPoints() {
      return this.path.map(p => `${p.x},${p.y}`).join(' ')
    },
    pathPointsArray() {
      return this.path
    },
    pathD() {
      if (this.path.length < 2) return ''
      let d = `M ${this.path[0].x} ${this.path[0].y}`
      for (let i = 1; i < this.path.length; i++) {
        d += ` L ${this.path[i].x} ${this.path[i].y}`
      }
      return d
    },
    animationDuration() {
      return Math.max(3, this.path.length * 0.8)
    },
    pathNodeIds() {
      return new Set(this.path.map(p => p.id))
    },
    visibleNodes() {
      // 只显示前20个节点（与后端一致）
      return this.nodes.slice(0, 20)
    },
    visibleEdges() {
      // 只显示可见节点之间的边
      const visibleNodeIds = new Set(this.visibleNodes.map(n => n.id))
      return this.edges.filter(e => {
        // 找到边对应的节点
        const startNode = this.nodes.find(n => 
          Math.abs(n.x - e.x1) < 1 && Math.abs(n.y - e.y1) < 1
        )
        const endNode = this.nodes.find(n => 
          Math.abs(n.x - e.x2) < 1 && Math.abs(n.y - e.y2) < 1
        )
        return startNode && endNode && 
               visibleNodeIds.has(startNode.id) && 
               visibleNodeIds.has(endNode.id)
      })
    }
  },
  watch: {
    nodes() {
      this.updateViewBox()
    },
    path() {
      this.updateViewBox()
    }
  },
  mounted() {
    this.updateViewBox()
    window.addEventListener('resize', this.updateViewBox)
  },
  beforeUnmount() {
    window.removeEventListener('resize', this.updateViewBox)
  },
  methods: {
    updateViewBox() {
      if (this.nodes.length === 0 && this.path.length === 0) return
      
      // 收集所有节点和路径点的坐标
      const allPoints = [...this.nodes]
      if (this.path.length > 0) {
        allPoints.push(...this.path)
      }
      
      const xs = allPoints.map(p => p.x)
      const ys = allPoints.map(p => p.y)
      const minX = Math.min(...xs) - 50
      const maxX = Math.max(...xs) + 50
      const minY = Math.min(...ys) - 50
      const maxY = Math.max(...ys) + 50
      
      this.baseViewBox = `${minX} ${minY} ${maxX - minX} ${maxY - minY}`
      this.applyTransform()
    },
    getNodeColor(node) {
      if (this.path.length > 0) {
        const pathIds = this.path.map(p => p.id)
        if (pathIds.includes(node.id)) {
          return '#409eff'
        }
      }
      const colors = {
        'building': '#67c23a',
        'facility': '#e6a23c',
        'current': '#f56c6c',
        'node': '#909399'
      }
      return colors[node.type] || '#909399'
    },
    getNodeRadius(node) {
      if (this.isPathNode(node)) return 10
      if (this.hoveredNode === node) return 9
      if (node.type === 'current') return 10
      return 7
    },
    getNodeFill(node) {
      if (this.isPathNode(node)) return 'url(#pathNodeGradient)'
      if (this.hoveredNode === node) return '#60a5fa'
      return 'url(#nodeGradient)'
    },
    isPathNode(node) {
      return this.pathNodeIds.has(node.id)
    },
    shouldShowLabel(node) {
      // 始终显示路径上的节点标签
      if (this.isPathNode(node)) return true
      // 显示悬停的节点标签
      if (this.hoveredNode === node) return true
      // 缩放较大时显示更多标签
      if (this.scale > 1.5) return true
      // 默认只显示部分重要节点
      return node.hotness > 9.0 || node.type === 'current'
    },
    getEdgeColor(edge) {
      // 路径上的边使用蓝色
      if (this.isPathEdge(edge)) return '#3b82f6'
      // 根据拥挤度设置颜色
      if (edge.crowd_level > 4) return '#f87171'
      if (edge.crowd_level > 3) return '#fbbf24'
      return '#94a3b8'
    },
    getEdgeWidth(edge) {
      if (this.isPathEdge(edge)) return 4
      if (edge.crowd_level > 3) return 3
      return 2
    },
    getEdgeOpacity(edge) {
      if (this.isPathEdge(edge)) return 1
      // 非路径边降低透明度，避免杂乱
      return 0.4
    },
    isPathEdge(edge) {
      if (this.path.length < 2) return false
      // 检查这条边是否在路径上
      for (let i = 0; i < this.path.length - 1; i++) {
        const p1 = this.path[i]
        const p2 = this.path[i + 1]
        // 检查边的两个端点是否匹配路径上的两个连续点
        const match1 = Math.abs(p1.x - edge.x1) < 1 && Math.abs(p1.y - edge.y1) < 1 &&
                       Math.abs(p2.x - edge.x2) < 1 && Math.abs(p2.y - edge.y2) < 1
        const match2 = Math.abs(p1.x - edge.x2) < 1 && Math.abs(p1.y - edge.y2) < 1 &&
                       Math.abs(p2.x - edge.x1) < 1 && Math.abs(p2.y - edge.y1) < 1
        if (match1 || match2) return true
      }
      return false
    },
    onNodeClick(node) {
      this.$emit('node-click', node)
    },
    zoomIn() {
      this.scale *= 1.2
      this.applyTransform()
    },
    zoomOut() {
      this.scale /= 1.2
      this.applyTransform()
    },
    resetView() {
      this.scale = 1
      this.offsetX = 0
      this.offsetY = 0
      this.applyTransform()
    },
    applyTransform() {
      // 使用 viewBox 实现缩放，而不是 CSS transform
      // 这样可以确保景点图标大小保持不变
      const [minX, minY, width, height] = this.baseViewBox.split(' ').map(Number)
      
      // 根据缩放比例调整 viewBox
      const newWidth = width / this.scale
      const newHeight = height / this.scale
      
      // 计算中心点偏移
      const centerX = minX + width / 2
      const centerY = minY + height / 2
      
      // 应用偏移量
      const newMinX = centerX - newWidth / 2 + this.offsetX
      const newMinY = centerY - newHeight / 2 + this.offsetY
      
      this.viewBox = `${newMinX} ${newMinY} ${newWidth} ${newHeight}`
    },
    startDrag(e) {
      this.isDragging = true
      this.lastMouseX = e.clientX
      this.lastMouseY = e.clientY
    },
    onDrag(e) {
      if (!this.isDragging) return
      const dx = e.clientX - this.lastMouseX
      const dy = e.clientY - this.lastMouseY
      this.offsetX += dx / this.scale
      this.offsetY += dy / this.scale
      this.lastMouseX = e.clientX
      this.lastMouseY = e.clientY
      this.applyTransform()
    },
    endDrag() {
      this.isDragging = false
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
    getRoadPath(edge) {
      // 生成弯曲的道路路径，而不是直线
      const { x1, y1, x2, y2 } = edge
      
      // 计算中心点
      const cx = (x1 + x2) / 2
      const cy = (y1 + y2) / 2
      
      // 计算偏移量，使道路弯曲
      const dx = x2 - x1
      const dy = y2 - y1
      const length = Math.sqrt(dx * dx + dy * dy)
      const offset = length * 0.1 // 偏移量为道路长度的10%
      
      // 计算控制点，使道路向一侧弯曲
      const controlX = cx + dy * (offset / length)
      const controlY = cy - dx * (offset / length)
      
      // 返回贝塞尔曲线路径
      return `M ${x1} ${y1} Q ${controlX} ${controlY} ${x2} ${y2}`
    }
  }
}
</script>

<style scoped>
.map-container {
  position: relative;
  width: 100%;
  height: 600px;
  background: linear-gradient(135deg, #f5f7fa 0%, #e4e7ed 100%);
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
}

.map-canvas {
  width: 100%;
  height: 100%;
  cursor: grab;
}

.map-canvas:active {
  cursor: grabbing;
}

.map-canvas svg {
  width: 100%;
  height: 100%;
  transition: transform 0.3s ease;
}

/* 极简道路样式 */
.road-line {
  transition: all 0.2s ease;
}

.road-line:hover {
  stroke-width: 3 !important;
  opacity: 0.8 !important;
}

/* 路径样式 - 简洁 */
.path-line {
  filter: drop-shadow(0 2px 4px rgba(59, 130, 246, 0.3));
}

.path-animation {
  filter: drop-shadow(0 0 4px rgba(251, 191, 36, 0.6));
}

/* 节点样式 - 极简 */
.node-group {
  cursor: pointer;
  transition: transform 0.2s ease;
}

.node-circle {
  transition: all 0.2s ease;
}

.node-group:hover .node-circle {
  transform: scale(1.2);
}

.node-label {
  pointer-events: none;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  text-shadow: 0 1px 2px rgba(255, 255, 255, 0.8);
}

/* 脉冲动画 */
.pulse {
  animation: pulse-animation 2s infinite;
}

@keyframes pulse-animation {
  0% {
    box-shadow: 0 0 0 0 rgba(245, 108, 108, 0.7);
  }
  70% {
    box-shadow: 0 0 0 20px rgba(245, 108, 108, 0);
  }
  100% {
    box-shadow: 0 0 0 0 rgba(245, 108, 108, 0);
  }
}

/* 控制面板 */
.map-controls {
  position: absolute;
  top: 20px;
  right: 20px;
  z-index: 10;
}

.map-controls .el-button-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.map-controls .el-button {
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(10px);
  border: none;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

.map-controls .el-button:hover {
  background: #fff;
  transform: translateY(-2px);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
}

/* 路径信息面板 */
.path-info-panel {
  position: absolute;
  bottom: 20px;
  left: 20px;
  z-index: 10;
  max-width: 300px;
}

.path-stats {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 8px 0;
  border-bottom: 1px solid #ebeef5;
}

.stat-item:last-child {
  border-bottom: none;
}

.stat-item .el-icon {
  font-size: 20px;
  color: #409eff;
}

.stat-label {
  color: #606266;
  font-size: 14px;
  flex: 1;
}

.stat-value {
  color: #303133;
  font-size: 16px;
  font-weight: bold;
}

/* 图例 */
.map-legend {
  position: absolute;
  bottom: 20px;
  right: 20px;
  z-index: 10;
}

.legend-title {
  font-weight: bold;
  margin-bottom: 10px;
  color: #303133;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 8px;
  font-size: 13px;
  color: #606266;
}

.legend-dot {
  width: 12px;
  height: 12px;
  border-radius: 50%;
}

.legend-line {
  width: 20px;
  height: 3px;
  border-radius: 2px;
}
</style>