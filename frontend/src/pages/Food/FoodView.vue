<template>
  <div class="food-container">
    <!-- 页面标题 -->
    <div class="page-header">
      <h1 class="page-title">
        <el-icon><Food /></el-icon>
        美食推荐
      </h1>
      <p class="page-subtitle">探索各地美食，品味舌尖文化</p>
    </div>

    <!-- 搜索和筛选 -->
    <el-card shadow="hover" class="search-card">
      <template #header>
        <div class="card-header">
          <el-icon><Search /></el-icon>
          <span>搜索筛选</span>
        </div>
      </template>
      <el-row :gutter="20">
        <el-col :span="6">
          <el-input
            v-model="searchForm.keyword"
            placeholder="搜索美食、饭店..."
            clearable
            @keyup.enter="handleSearch"
          >
            <template #prefix>
              <el-icon><Search /></el-icon>
            </template>
          </el-input>
        </el-col>
        <el-col :span="4">
          <el-select v-model="searchForm.cuisine" placeholder="菜系" clearable @change="handleSearch">
            <el-option label="全部菜系" value=""></el-option>
            <el-option label="川菜" value="sichuan"></el-option>
            <el-option label="粤菜" value="cantonese"></el-option>
            <el-option label="鲁菜" value="shandong"></el-option>
            <el-option label="淮扬菜" value="huaiyang"></el-option>
            <el-option label="湘菜" value="hunan"></el-option>
            <el-option label="浙菜" value="zhejiang"></el-option>
          </el-select>
        </el-col>
        <el-col :span="4">
          <el-select v-model="searchForm.sortBy" placeholder="排序方式" @change="handleSearch">
            <el-option label="综合推荐" value="comprehensive"></el-option>
            <el-option label="评分最高" value="rating"></el-option>
            <el-option label="热度最高" value="hotness"></el-option>
            <el-option label="距离最近" value="distance"></el-option>
          </el-select>
        </el-col>
        <el-col :span="4">
          <el-select v-model="searchForm.priceRange" placeholder="价格区间" clearable @change="handleSearch">
            <el-option label="全部价格" value=""></el-option>
            <el-option label="¥0-50" value="0-50"></el-option>
            <el-option label="¥50-100" value="50-100"></el-option>
            <el-option label="¥100-200" value="100-200"></el-option>
            <el-option label="¥200+" value="200+"></el-option>
          </el-select>
        </el-col>
        <el-col :span="6">
          <el-button type="primary" @click="handleSearch" :icon="Search">搜索</el-button>
          <el-button @click="resetSearch" :icon="RefreshRight">重置</el-button>
        </el-col>
      </el-row>
    </el-card>

    <!-- 热门菜系标签 -->
    <div class="cuisine-tags">
      <span class="tags-label">热门菜系：</span>
      <el-tag
        v-for="cuisine in hotCuisines"
        :key="cuisine.value"
        :type="searchForm.cuisine === cuisine.value ? 'primary' : 'info'"
        class="cuisine-tag"
        @click="selectCuisine(cuisine.value)"
      >
        {{ cuisine.label }}
      </el-tag>
    </div>

    <!-- 美食列表 -->
    <div class="food-list" v-loading="loading">
      <el-empty v-if="foodList.length === 0" description="暂无美食数据"></el-empty>
      <el-row :gutter="20" v-else>
        <el-col :span="6" v-for="(food, index) in foodList" :key="food.id">
          <el-card shadow="hover" class="food-card" :class="{ 'top-three': index < 3 }">
            <div class="food-rank" v-if="index < 3">
              <el-tag :type="index === 0 ? 'danger' : index === 1 ? 'warning' : 'success'" effect="dark">
                TOP {{ index + 1 }}
              </el-tag>
            </div>
            <div class="food-image">
              <div class="image-placeholder">
                <el-icon><Dish /></el-icon>
                <span>{{ food.name }}</span>
              </div>
            </div>
            <div class="food-content">
              <h3 class="food-name">{{ food.name }}</h3>
              <div class="food-rating">
                <el-rate v-model="food.rating" disabled show-score score-template="{value}分"></el-rate>
              </div>
              <p class="food-description">{{ food.description }}</p>
              <div class="food-tags">
                <el-tag size="small" type="success">{{ getCuisineName(food.cuisine) }}</el-tag>
                <el-tag size="small" type="warning">¥{{ food.price }}</el-tag>
                <el-tag size="small" type="info" v-if="food.distance">{{ food.distance }}m</el-tag>
              </div>
              <div class="food-stats">
                <span class="stat-item">
                  <el-icon><Fire /></el-icon>
                  {{ food.hotness }} 热度
                </span>
                <span class="stat-item">
                  <el-icon><View /></el-icon>
                  {{ food.views || 0 }} 浏览
                </span>
              </div>
            </div>
            <div class="food-actions">
              <el-button type="primary" size="small" @click="viewDetail(food)">
                <el-icon><View /></el-icon>
                查看详情
              </el-button>
              <el-button size="small" @click="navigateTo(food)">
                <el-icon><MapLocation /></el-icon>
                导航前往
              </el-button>
            </div>
          </el-card>
        </el-col>
      </el-row>
    </div>

    <!-- 美食详情对话框 -->
    <el-dialog
      title="美食详情"
      v-model="detailDialogVisible"
      width="600px"
      class="detail-dialog"
    >
      <div v-if="currentFood" class="detail-content">
        <div class="detail-image">
          <div class="image-placeholder large">
            <el-icon><Dish /></el-icon>
            <span>{{ currentFood.name }}</span>
          </div>
        </div>
        <div class="detail-header">
          <h2>{{ currentFood.name }}</h2>
          <el-rate v-model="currentFood.rating" disabled show-score></el-rate>
        </div>
        <el-descriptions :column="2" border>
          <el-descriptions-item label="菜系">
            <el-tag type="success">{{ getCuisineName(currentFood.cuisine) }}</el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="价格">
            <span class="price-tag">¥{{ currentFood.price }}</span>
          </el-descriptions-item>
          <el-descriptions-item label="热度" :span="2">
            <el-tag type="danger">{{ currentFood.hotness }}</el-tag>
          </el-descriptions-item>
        </el-descriptions>
        <div class="detail-section">
          <h4>菜品介绍</h4>
          <p>{{ currentFood.description }}</p>
        </div>
        <div class="detail-actions">
          <el-button type="primary" size="large" @click="navigateTo(currentFood)">
            <el-icon><MapLocation /></el-icon>
            导航前往
          </el-button>
          <el-button size="large" @click="shareFood(currentFood)">
            <el-icon><Share /></el-icon>
            分享
          </el-button>
        </div>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import { Food, Search, Dish, Fire, View, MapLocation, Share } from '@element-plus/icons-vue'

export default {
  name: 'FoodView',
  components: {
    Food,
    Search,
    Dish,
    Fire,
    View,
    MapLocation,
    Share
  },
  data() {
    return {
      searchForm: {
        keyword: '',
        cuisine: '',
        sortBy: 'comprehensive',
        priceRange: ''
      },
      foodList: [],
      loading: false,
      detailDialogVisible: false,
      currentFood: null,
      hotCuisines: [
        { label: '川菜', value: 'sichuan' },
        { label: '粤菜', value: 'cantonese' },
        { label: '鲁菜', value: 'shandong' },
        { label: '湘菜', value: 'hunan' },
        { label: '江浙菜', value: 'zhejiang' }
      ]
    }
  },
  mounted() {
    this.getFoodList()
  },
  methods: {
    async getFoodList() {
      this.loading = true
      try {
        // 模拟数据
        this.foodList = [
          {
            id: 1,
            name: '麻婆豆腐',
            description: '四川传统名菜，麻辣鲜香，豆腐嫩滑，肉末酥香，是川菜中的经典之作。',
            hotness: 1280,
            rating: 4.8,
            cuisine: 'sichuan',
            price: 38,
            distance: 500,
            views: 3560
          },
          {
            id: 2,
            name: '宫保鸡丁',
            description: '经典川菜，酸甜可口，鸡肉嫩滑，花生酥脆，是一道老少皆宜的美食。',
            hotness: 1156,
            rating: 4.7,
            cuisine: 'sichuan',
            price: 45,
            distance: 800,
            views: 2890
          },
          {
            id: 3,
            name: '糖醋里脊',
            description: '鲁菜经典，酸甜可口，外酥里嫩，色泽红亮，深受食客喜爱。',
            hotness: 980,
            rating: 4.6,
            cuisine: 'shandong',
            price: 58,
            distance: 1200,
            views: 2156
          },
          {
            id: 4,
            name: '白切鸡',
            description: '粤菜代表，皮黄肉白，肥嫩鲜美，滋味异常鲜美，十分可口。',
            hotness: 890,
            rating: 4.5,
            cuisine: 'cantonese',
            price: 68,
            distance: 600,
            views: 1890
          }
        ]
      } catch (error) {
        console.error('获取美食列表失败:', error)
        this.$message.error('获取美食列表失败')
      } finally {
        this.loading = false
      }
    },
    async handleSearch() {
      this.loading = true
      try {
        await new Promise(resolve => setTimeout(resolve, 500))
        this.$message.success('搜索完成')
      } catch (error) {
        console.error('搜索失败:', error)
      } finally {
        this.loading = false
      }
    },
    resetSearch() {
      this.searchForm = {
        keyword: '',
        cuisine: '',
        sortBy: 'comprehensive',
        priceRange: ''
      }
      this.getFoodList()
    },
    selectCuisine(cuisine) {
      this.searchForm.cuisine = this.searchForm.cuisine === cuisine ? '' : cuisine
      this.handleSearch()
    },
    viewDetail(food) {
      this.currentFood = food
      this.detailDialogVisible = true
    },
    navigateTo(food) {
      this.$router.push({
        path: '/route-plan',
        query: { destination: food.name }
      })
    },
    shareFood(food) {
      this.$message.success(`已分享：${food.name}`)
    },
    getCuisineName(cuisine) {
      const cuisineMap = {
        'sichuan': '川菜',
        'cantonese': '粤菜',
        'shandong': '鲁菜',
        'huaiyang': '淮扬菜',
        'hunan': '湘菜',
        'zhejiang': '江浙菜'
      }
      return cuisineMap[cuisine] || cuisine
    }
  }
}
</script>

<style scoped>
.food-container {
  padding: 20px;
  background: linear-gradient(135deg, #f5f7fa 0%, #e4e7ed 100%);
  min-height: 100vh;
}

/* 页面标题 */
.page-header {
  text-align: center;
  margin-bottom: 30px;
  padding: 30px 0;
  background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
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

/* 菜系标签 */
.cuisine-tags {
  margin-bottom: 20px;
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 10px;
}

.tags-label {
  font-weight: bold;
  color: #606266;
}

.cuisine-tag {
  cursor: pointer;
  transition: all 0.3s ease;
}

.cuisine-tag:hover {
  transform: scale(1.05);
}

/* 美食列表 */
.food-list {
  margin-top: 20px;
}

.food-card {
  margin-bottom: 20px;
  border-radius: 12px;
  overflow: hidden;
  transition: all 0.3s ease;
  position: relative;
}

.food-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 12px 40px rgba(0, 0, 0, 0.15);
}

.food-card.top-three {
  border: 2px solid #ffd700;
}

.food-rank {
  position: absolute;
  top: 10px;
  left: 10px;
  z-index: 10;
}

.food-image {
  height: 160px;
  background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
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
  font-size: 40px;
  margin-bottom: 8px;
}

.image-placeholder span {
  display: block;
  font-size: 14px;
  font-weight: bold;
}

.image-placeholder.large .el-icon {
  font-size: 64px;
}

.image-placeholder.large span {
  font-size: 18px;
}

.food-name {
  font-size: 18px;
  font-weight: bold;
  margin: 0 0 8px 0;
  color: #303133;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.food-rating {
  margin-bottom: 8px;
}

.food-description {
  color: #606266;
  font-size: 13px;
  line-height: 1.5;
  margin-bottom: 12px;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.food-tags {
  margin-bottom: 10px;
}

.food-tags .el-tag {
  margin-right: 6px;
  margin-bottom: 6px;
}

.food-stats {
  display: flex;
  gap: 15px;
  margin-bottom: 12px;
  padding: 8px 0;
  border-top: 1px solid #ebeef5;
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 12px;
  color: #606266;
}

.food-actions {
  display: flex;
  gap: 8px;
}

/* 详情对话框 */
.detail-dialog :deep(.el-dialog__header) {
  background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
  color: white;
  padding: 20px;
}

.detail-dialog :deep(.el-dialog__title) {
  color: white;
}

.detail-content {
  padding: 20px 0;
}

.detail-image {
  margin: -20px -20px 20px -20px;
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

.price-tag {
  color: #f56c6c;
  font-size: 20px;
  font-weight: bold;
}

.detail-section {
  margin-top: 20px;
}

.detail-section h4 {
  color: #fa709a;
  margin-bottom: 10px;
  padding-left: 10px;
  border-left: 4px solid #fa709a;
}

.detail-section p {
  line-height: 1.8;
  color: #606266;
}

.detail-actions {
  margin-top: 20px;
  display: flex;
  gap: 15px;
  justify-content: center;
}
</style>