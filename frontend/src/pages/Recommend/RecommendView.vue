<template>
  <div class="recommend-container">
    <el-card shadow="hover" class="search-card">
      <template #header>
        <div class="card-header">
          <span>景点推荐</span>
        </div>
      </template>
      <el-form :inline="true" :model="searchForm" class="search-form">
        <el-form-item label="排序方式">
          <el-select v-model="searchForm.sortBy" placeholder="选择排序方式">
            <el-option label="按评分" value="rating"></el-option>
            <el-option label="按热度" value="hotness"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="类别">
          <el-select v-model="searchForm.category" placeholder="选择类别">
            <el-option label="全部" value=""></el-option>
            <el-option label="自然景观" value="natural"></el-option>
            <el-option label="人文景观" value="cultural"></el-option>
            <el-option label="主题公园" value="theme"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSearch">搜索</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <div class="scenic-list">
      <el-card
        v-for="scenic in scenicList"
        :key="scenic.id"
        shadow="hover"
        class="scenic-card"
      >
        <template #header>
          <div class="scenic-header">
            <span>{{ scenic.name }}</span>
            <div class="scenic-rating">
              <el-rate
                v-model="scenic.rating"
                :max="5"
                disabled
                show-score
                score-template="{{ value }}"
              ></el-rate>
            </div>
          </div>
        </template>
        <div class="scenic-content">
          <p>{{ scenic.description }}</p>
          <div class="scenic-info">
            <span class="hotness">热度: {{ scenic.hotness }}</span>
            <span class="category">{{ getCategoryName(scenic.category) }}</span>
          </div>
        </div>
      </el-card>
    </div>
  </div>
</template>

<script>
import { recommendApi } from '../../api/index.js'

export default {
  name: 'RecommendView',
  data() {
    return {
      searchForm: {
        sortBy: 'rating',
        category: ''
      },
      scenicList: []
    }
  },
  mounted() {
    this.getRecommendList()
  },
  methods: {
    async getRecommendList() {
      try {
        const response = await recommendApi.getList()
        this.scenicList = response.data
      } catch (error) {
        console.error('获取推荐列表失败:', error)
      }
    },
    async handleSearch() {
      try {
        const response = await recommendApi.getList(this.searchForm)
        this.scenicList = response.data
      } catch (error) {
        console.error('搜索失败:', error)
      }
    },
    getCategoryName(category) {
      const categoryMap = {
        'natural': '自然景观',
        'cultural': '人文景观',
        'theme': '主题公园'
      }
      return categoryMap[category] || category
    }
  }
}
</script>

<style scoped>
.recommend-container {
  padding: 20px;
}

.search-card {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.search-form {
  margin-top: 10px;
}

.scenic-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
}

.scenic-card {
  height: 100%;
}

.scenic-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.scenic-content {
  margin-top: 10px;
}

.scenic-info {
  margin-top: 15px;
  display: flex;
  justify-content: space-between;
  font-size: 14px;
  color: #606266;
}

.hotness {
  color: #f56c6c;
}

.category {
  color: #409eff;
}
</style>