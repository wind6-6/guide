<template>
  <div class="map-container">
    <div ref="mapCanvas" class="map-canvas" @mousedown="startDrag" @mousemove="onDrag" @mouseup="endDrag" @mouseleave="endDrag">
      <svg ref="svgMap" :viewBox="viewBox" preserveAspectRatio="xMidYMid meet">
        <!-- 网格背景 -->
        <defs>
          <pattern id="grid" width="50" height="50" patternUnits="userSpaceOnUse">
            <path d="M 50 0 L 0 0 0 50" fill="none" stroke="#e0e0e0" stroke-width="1"/>
          </pattern>
        </defs>
        <rect width="100%" height="100%" fill="url(#grid)" />
        
        <!-- 边（道路） -->
        <g class="edges">
          <path
            v-for="(edge, index) in edges"
            :key="'edge-'+index"
            :d="getRoadPath(edge)"
            :stroke="edge.color || '#ccc'"
            :stroke-width="edge.width || 3"
            :stroke-dasharray="edge.dashed ? '5,5' : '0'"
            fill="none"
            class="road-line"
          />
        </g>
        
        <!-- 路径 -->
        <g class="path" v-if="path.length > 1">
          <polyline
            :points="pathPoints"
            fill="none"
            stroke="#409eff"
            stroke-width="5"
            stroke-linecap="round"
            stroke-linejoin="round"
            class="path-line"
          />
          <!-- 路径动画点 -->
          <circle r="6" fill="#409eff" class="path-animation">
            <animateMotion :dur="animationDuration + 's'" repeatCount="indefinite" :path="pathD" />
          </circle>
        </g>
        
        <!-- 节点 -->
        <g class="nodes">
          <g
            v-for="node in nodes"
            :key="node.id"
            class="node-group"
            :transform="`translate(${node.x}, ${node.y})`"
            @click="onNodeClick(node)"
            @mouseenter="hoveredNode = node"
            @mouseleave="hoveredNode = null"
          >
            <!-- 节点圆圈 -->
            <circle
              :r="getNodeRadius(node)"
              :fill="getNodeColor(node)"
              :stroke="hoveredNode === node ? '#fff' : 'none'"
              stroke-width="3"
              class="node-circle"
              :class="{ 'pulse': node.type === 'current' }"
            />
            <!-- 节点图标 -->
            <text
              v-if="node.icon"
              text-anchor="middle"
              dominant-baseline="central"
              font-size="12"
              fill="#fff"
              class="node-icon"
            >{{ node.icon }}</text>
            <!-- 节点标签 -->
            <text
              v-if="scale > 1.2 || hoveredNode === node"
              y="-15"
              text-anchor="middle"
              :font-size="hoveredNode === node ? 12 : 10"
              :font-weight="hoveredNode === node ? 'bold' : 'normal'"
              fill="#333"
              class="node-label"
            >{{ node.name }}</text>
          </g>
        </g>
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
import { MapLocation, Timer, Bicycle, Plus, Minus, RefreshRight } from '@element-plus/icons-vue'

export default {
  name: 'MapViewer',
  components: {
    MapLocation,
    Timer,
    Bicycle,
    Plus,
    Minus,
    RefreshRight
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
    pathD() {
      if (this.path.length < 2) return ''
      let d = `M ${this.path[0].x} ${this.path[0].y}`
      for (let i = 1; i < this.path.length; i++) {
        d += ` L ${this.path[i].x} ${this.path[i].y}`
      }
      return d
    },
    animationDuration() {
      // 根据路径长度计算动画时长
      return Math.max(2, this.path.length * 0.5)
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
      if (node.type === 'current') return 10
      if (this.hoveredNode === node) return 8
      return 6
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

/* 道路样式 */
.road-line {
  transition: all 0.3s ease;
}

.road-line:hover {
  stroke-width: 5 !important;
  filter: drop-shadow(0 0 3px rgba(0, 0, 0, 0.3));
}

/* 路径样式 */
.path-line {
  filter: drop-shadow(0 0 5px rgba(64, 158, 255, 0.5));
  animation: dash 2s linear infinite;
}

@keyframes dash {
  to {
    stroke-dashoffset: -20;
  }
}

.path-animation {
  filter: drop-shadow(0 0 5px rgba(64, 158, 255, 0.8));
}

/* 节点样式 */
.node-group {
  cursor: pointer;
  transition: all 0.3s ease;
}

.node-circle {
  transition: all 0.3s ease;
  filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.2));
}

.node-group:hover .node-circle {
  filter: drop-shadow(0 4px 8px rgba(0, 0, 0, 0.3));
  transform: scale(1.2);
}

.node-label {
  transition: all 0.3s ease;
  text-shadow: 0 1px 2px rgba(255, 255, 255, 0.8);
  pointer-events: none;
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