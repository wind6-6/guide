<template>
  <div class="recommend-container">
    <!-- 页面标题 -->
    <div class="page-header">
      <h1 class="page-title">
        <el-icon><Location /></el-icon>
        景点推荐
      </h1>
      <p class="page-subtitle">发现精彩景点，开启美好旅程</p>
    </div>

    <!-- 搜索和筛选区域 -->
    <el-card shadow="hover" class="search-card">
      <template #header>
        <div class="card-header">
          <span>
            <el-icon><Search /></el-icon>
            搜索筛选
          </span>
        </div>
      </template>
      <el-row :gutter="20">
        <el-col :span="8">
          <el-input
            v-model="searchForm.keyword"
            placeholder="搜索景点名称、描述..."
            clearable
            @keyup.enter="handleSearch"
          >
            <template #prefix>
              <el-icon><Search /></el-icon>
            </template>
          </el-input>
        </el-col>
        <el-col :span="5">
          <el-select v-model="searchForm.sortBy" placeholder="排序方式" @change="handleSearch">
            <el-option label="综合推荐" value="comprehensive">
              <el-icon><Star /></el-icon> 综合推荐
            </el-option>
            <el-option label="评分最高" value="rating">
              <el-icon><Trophy /></el-icon> 评分最高
            </el-option>
            <el-option label="热度最高" value="hotness">
              <el-icon><Fire /></el-icon> 热度最高
            </el-option>
          </el-select>
        </el-col>
        <el-col :span="5">
          <el-select v-model="searchForm.category" placeholder="景点类别" clearable @change="handleSearch">
            <el-option label="全部类别" value=""></el-option>
            <el-option label="历史文化" value="历史文化"></el-option>
            <el-option label="自然风光" value="自然风光"></el-option>
            <el-option label="主题公园" value="主题公园"></el-option>
            <el-option label="现代建筑" value="现代建筑"></el-option>
            <el-option label="宗教文化" value="宗教文化"></el-option>
          </el-select>
        </el-col>
        <el-col :span="6">
          <el-button type="primary" @click="handleSearch" :icon="Search">搜索</el-button>
          <el-button @click="resetSearch" :icon="RefreshRight">重置</el-button>
        </el-col>
      </el-row>
    </el-card>

    <!-- 统计信息 -->
    <div class="stats-bar">
      <el-row :gutter="20">
        <el-col :span="6">
          <div class="stat-item">
            <el-icon><OfficeBuilding /></el-icon>
            <div class="stat-info">
              <div class="stat-value">{{ totalCount }}</div>
              <div class="stat-label">景点总数</div>
            </div>
          </div>
        </el-col>
        <el-col :span="6">
          <div class="stat-item">
            <el-icon><Star /></el-icon>
            <div class="stat-info">
              <div class="stat-value">{{ avgRating }}</div>
              <div class="stat-label">平均评分</div>
            </div>
          </div>
        </el-col>
        <el-col :span="6">
          <div class="stat-item">
            <el-icon><Fire /></el-icon>
            <div class="stat-info">
              <div class="stat-value">{{ avgHotness }}</div>
              <div class="stat-label">平均热度</div>
            </div>
          </div>
        </el-col>
        <el-col :span="6">
          <div class="stat-item">
            <el-icon><Collection /></el-icon>
            <div class="stat-info">
              <div class="stat-value">{{ categoryCount }}</div>
              <div class="stat-label">类别数量</div>
            </div>
          </div>
        </el-col>
      </el-row>
    </div>

    <!-- 景点列表 -->
    <div class="scenic-list" v-loading="loading">
      <el-empty v-if="scenicList.length === 0" description="暂无景点数据"></el-empty>
      <el-row :gutter="20" v-else>
        <el-col :span="8" v-for="(scenic, index) in scenicList" :key="scenic.id">
          <el-card
            shadow="hover"
            class="scenic-card"
            :class="{ 'top-three': index < 3 }"
          >
            <div class="scenic-rank" v-if="index < 3">
              <el-tag :type="index === 0 ? 'danger' : index === 1 ? 'warning' : 'success'" effect="dark">
                TOP {{ index + 1 }}
              </el-tag>
            </div>
            <div class="scenic-image">
              <div class="image-placeholder">
                <el-icon><Picture /></el-icon>
                <span>{{ scenic.name }}</span>
              </div>
            </div>
            <div class="scenic-content">
              <h3 class="scenic-name">{{ scenic.name }}</h3>
              <div class="scenic-rating">
                <el-rate
                  v-model="scenic.rating"
                  :max="5"
                  disabled
                  show-score
                  :colors="['#99A9BF', '#F7BA2A', '#FF9900']"
                ></el-rate>
              </div>
              <p class="scenic-description">{{ scenic.description }}</p>
              <div class="scenic-tags">
                <el-tag size="small" type="info">{{ scenic.category }}</el-tag>
                <el-tag size="small" type="success" v-if="scenic.ticket_price">{{ scenic.ticket_price }}</el-tag>
              </div>
              <div class="scenic-stats">
                <span class="stat">
                  <el-icon><Fire /></el-icon>
                  {{ scenic.hotness }} 热度
                </span>
                <span class="stat">
                  <el-icon><View /></el-icon>
                  {{ scenic.views || 0 }} 浏览
                </span>
              </div>
            </div>
            <div class="scenic-actions">
              <el-button type="primary" size="small" @click="viewDetail(scenic)">
                <el-icon><View /></el-icon>
                查看详情
              </el-button>
              <el-button size="small" @click="planRoute(scenic)">
                <el-icon><MapLocation /></el-icon>
                规划路线
              </el-button>
            </div>
          </el-card>
        </el-col>
      </el-row>
    </div>

    <!-- 景点详情对话框 -->
    <el-dialog
      v-model="detailDialogVisible"
      title="景点详情"
      width="600px"
      class="detail-dialog"
    >
      <div v-if="currentScenic" class="detail-content">
        <div class="detail-header">
          <h2>{{ currentScenic.name }}</h2>
          <el-rate
            v-model="currentScenic.rating"
            disabled
            show-score
            score-template="{value} 分"
          ></el-rate>
        </div>
        <el-descriptions :column="2" border>
          <el-descriptions-item label="类别">
            <el-tag>{{ currentScenic.category }}</el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="热度">
            <el-tag type="danger">{{ currentScenic.hotness }}</el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="门票" :span="2">
            {{ currentScenic.ticket_price || '免费' }}
          </el-descriptions-item>
          <el-descriptions-item label="开放时间" :span="2">
            {{ currentScenic.open_time || '08:00-18:00' }}
          </el-descriptions-item>
          <el-descriptions-item label="地址" :span="2">
            {{ currentScenic.address || '北京市区' }}
          </el-descriptions-item>
        </el-descriptions>
        <div class="detail-section">
          <h4>景点介绍</h4>
          <p>{{ currentScenic.description }}</p>
        </div>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import { Location, Search, Star, Trophy, Fire, OfficeBuilding, Collection, Picture, View, MapLocation } from '@element-plus/icons-vue'

export default {
  name: 'RecommendView',
  components: {
    Location,
    Search,
    Star,
    Trophy,
    Fire,
    OfficeBuilding,
    Collection,
    Picture,
    View,
    MapLocation
  },
  data() {
    return {
      searchForm: {
        keyword: '',
        sortBy: 'comprehensive',
        category: ''
      },
      scenicList: [],
      loading: false,
      detailDialogVisible: false,
      currentScenic: null
    }
  },
  computed: {
    totalCount() {
      return this.scenicList.length
    },
    avgRating() {
      if (this.scenicList.length === 0) return 0
      const sum = this.scenicList.reduce((acc, item) => acc + item.rating, 0)
      return (sum / this.scenicList.length).toFixed(1)
    },
    avgHotness() {
      if (this.scenicList.length === 0) return 0
      const sum = this.scenicList.reduce((acc, item) => acc + item.hotness, 0)
      return Math.round(sum / this.scenicList.length)
    },
    categoryCount() {
      const categories = new Set(this.scenicList.map(item => item.category))
      return categories.size
    }
  },
  mounted() {
    this.getRecommendList()
  },
  methods: {
    async getRecommendList() {
      this.loading = true
      try {
        // 模拟数据
        this.scenicList = [
          {
            id: 1,
            name: '颐和园',
            description: '中国清朝时期皇家园林，保存最完整的一座皇家行宫御苑，被誉为"皇家园林博物馆"。',
            hotness: 95,
            rating: 4.8,
            category: '历史文化',
            ticket_price: '30元',
            open_time: '06:00-20:00',
            address: '北京市海淀区新建宫门路19号',
            views: 12580
          },
          {
            id: 2,
            name: '故宫博物院',
            description: '中国明清两代的皇家宫殿，旧称紫禁城，是世界上现存规模最大、保存最为完整的木质结构古建筑之一。',
            hotness: 98,
            rating: 4.9,
            category: '历史文化',
            ticket_price: '60元',
            open_time: '08:30-17:00',
            address: '北京市东城区景山前街4号',
            views: 25600
          },
          {
            id: 3,
            name: '天坛公园',
            description: '明清两代皇帝祭天的场所，是中国现存最大的古代祭祀性建筑群。',
            hotness: 88,
            rating: 4.7,
            category: '历史文化',
            ticket_price: '15元',
            open_time: '06:00-22:00',
            address: '北京市东城区天坛东里甲1号',
            views: 8900
          }
        ]
      } catch (error) {
        console.error('获取推荐列表失败:', error)
        this.$message.error('获取推荐列表失败')
      } finally {
        this.loading = false
      }
    },
    async handleSearch() {
      this.loading = true
      try {
        // 模拟搜索
        await new Promise(resolve => setTimeout(resolve, 500))
        this.$message.success('搜索完成')
      } catch (error) {
        console.error('搜索失败:', error)
        this.$message.error('搜索失败')
      } finally {
        this.loading = false
      }
    },
    resetSearch() {
      this.searchForm = {
        keyword: '',
        sortBy: 'comprehensive',
        category: ''
      }
      this.getRecommendList()
    },
    viewDetail(scenic) {
      this.currentScenic = scenic
      this.detailDialogVisible = true
    },
    planRoute(scenic) {
      this.$router.push({
        path: '/route-plan',
        query: { destination: scenic.name }
      })
    }
  }
}
</script>

<style scoped>
.recommend-container {
  padding: 20px;
  background: linear-gradient(135deg, #f5f7fa 0%, #e4e7ed 100%);
  min-height: 100vh;
}

/* 页面标题 */
.page-header {
  text-align: center;
  margin-bottom: 30px;
  padding: 30px 0;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
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

/* 搜索卡片 */
.search-card {
  margin-bottom: 20px;
  border-radius: 12px;
}

.card-header {
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: bold;
}

/* 统计栏 */
.stats-bar {
  margin-bottom: 20px;
}

.stat-item {
  background: white;
  padding: 20px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  gap: 15px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
}

.stat-item:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
}

.stat-item .el-icon {
  font-size: 40px;
  color: #409eff;
}

.stat-info {
  flex: 1;
}

.stat-value {
  font-size: 24px;
  font-weight: bold;
  color: #303133;
}

.stat-label {
  font-size: 14px;
  color: #909399;
  margin-top: 5px;
}

/* 景点列表 */
.scenic-list {
  margin-top: 20px;
}

.scenic-card {
  margin-bottom: 20px;
  border-radius: 12px;
  overflow: hidden;
  transition: all 0.3s ease;
  position: relative;
}

.scenic-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 12px 40px rgba(0, 0, 0, 0.15);
}

.scenic-card.top-three {
  border: 2px solid #ffd700;
}

.scenic-rank {
  position: absolute;
  top: 10px;
  left: 10px;
  z-index: 10;
}

.scenic-image {
  height: 180px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  margin: -20px -20px 15px -20px;
}

.image-placeholder {
  text-align: center;
  color: white;
}

.image-placeholder .el-icon {
  font-size: 48px;
  margin-bottom: 10px;
}

.image-placeholder span {
  display: block;
  font-size: 18px;
  font-weight: bold;
}

.scenic-name {
  font-size: 18px;
  font-weight: bold;
  margin: 0 0 10px 0;
  color: #303133;
}

.scenic-rating {
  margin-bottom: 10px;
}

.scenic-description {
  color: #606266;
  font-size: 14px;
  line-height: 1.6;
  margin-bottom: 15px;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.scenic-tags {
  margin-bottom: 15px;
}

.scenic-tags .el-tag {
  margin-right: 8px;
}

.scenic-stats {
  display: flex;
  gap: 20px;
  margin-bottom: 15px;
  padding: 10px 0;
  border-top: 1px solid #ebeef5;
  border-bottom: 1px solid #ebeef5;
}

.scenic-stats .stat {
  display: flex;
  align-items: center;
  gap: 5px;
  color: #606266;
  font-size: 13px;
}

.scenic-actions {
  display: flex;
  gap: 10px;
}

/* 详情对话框 */
.detail-dialog :deep(.el-dialog__header) {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 20px;
}

.detail-dialog :deep(.el-dialog__title) {
  color: white;
}

.detail-content {
  padding: 20px 0;
}

.detail-header {
  text-align: center;
  margin-bottom: 20px;
  padding-bottom: 20px;
  border-bottom: 2px solid #ebeef5;
}

.detail-header h2 {
  margin: 0 0 15px 0;
  color: #303133;
}

.detail-section {
  margin-top: 20px;
}

.detail-section h4 {
  color: #409eff;
  margin-bottom: 10px;
  padding-left: 10px;
  border-left: 4px solid #409eff;
}

.detail-section p {
  line-height: 1.8;
  color: #606266;
}
</style>