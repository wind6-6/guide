<template>
  <div class="home-container">
    <div class="header">
      <h1>个性化旅游系统</h1>
      <div class="user-info">
        <span v-if="user">{{ user.name }}</span>
        <el-button v-else @click="goToLogin">登录</el-button>
      </div>
    </div>
    <div class="nav">
      <el-menu :default-active="activeIndex" mode="horizontal">
        <el-menu-item index="1" @click="goTo('/recommend')">景点推荐</el-menu-item>
        <el-menu-item index="2" @click="goTo('/route-plan')">路线规划</el-menu-item>
        <el-menu-item index="3" @click="goTo('/place-query')">场所查询</el-menu-item>
        <el-menu-item index="4" @click="goTo('/diary')">旅游日记</el-menu-item>
        <el-menu-item index="5" @click="goTo('/food')">美食推荐</el-menu-item>
        <el-menu-item index="6" @click="goTo('/user')" v-if="user">个人中心</el-menu-item>
      </el-menu>
    </div>
    <div class="content">
      <el-carousel :interval="5000" type="card" height="400px">
        <el-carousel-item v-for="item in banners" :key="item.id">
          <div class="carousel-item">
            <h3>{{ item.title }}</h3>
            <p>{{ item.description }}</p>
          </div>
        </el-carousel-item>
      </el-carousel>
      <div class="recommend-section">
        <h2>热门推荐</h2>
        <div class="recommend-list">
          <el-card v-for="scenic in recommendedScenics" :key="scenic.id" class="recommend-card">
            <template #header>
              <div class="card-header">
                <span>{{ scenic.name }}</span>
                <el-rate v-model="scenic.rating" :max="5" disabled />
              </div>
            </template>
            <div class="card-body">
              <p>{{ scenic.description }}</p>
              <div class="card-footer">
                <span class="hotness">热度: {{ scenic.hotness }}</span>
                <el-button type="primary" size="small">查看详情</el-button>
              </div>
            </div>
          </el-card>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { recommendApi } from '../../api'

export default {
  name: 'HomeView',
  data() {
    return {
      activeIndex: '1',
      user: JSON.parse(sessionStorage.getItem('user')),
      banners: [
        { id: 1, title: '颐和园', description: '皇家园林，历史文化遗产' },
        { id: 2, title: '故宫', description: '明清皇宫，世界文化遗产' },
        { id: 3, title: '长城', description: '万里长城，中华民族象征' }
      ],
      recommendedScenics: []
    }
  },
  mounted() {
    this.fetchRecommendedScenics()
  },
  methods: {
    goTo(path) {
      this.$router.push(path)
    },
    goToLogin() {
      this.$router.push('/login')
    },
    async fetchRecommendedScenics() {
      try {
        const response = await recommendApi.getList()
        if (response.status === 200) {
          this.recommendedScenics = response.data.slice(0, 6)
        }
      } catch (error) {
        console.error('获取推荐景点失败:', error)
      }
    }
  }
}
</script>

<style scoped>
.home-container {
  min-height: 100vh;
  background: #f5f5f5;
}

.header {
  background: white;
  padding: 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.header h1 {
  color: #333;
  margin: 0;
}

.nav {
  background: white;
  margin-top: 10px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.content {
  padding: 20px;
}

.carousel-item {
  height: 400px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  color: white;
  text-align: center;
  padding: 0 40px;
}

.carousel-item h3 {
  font-size: 36px;
  margin-bottom: 20px;
}

.carousel-item p {
  font-size: 18px;
}

.recommend-section {
  margin-top: 40px;
}

.recommend-section h2 {
  color: #333;
  margin-bottom: 20px;
}

.recommend-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
}

.recommend-card {
  height: 100%;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-body {
  padding: 20px;
}

.card-footer {
  margin-top: 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.hotness {
  color: #f56c6c;
  font-weight: bold;
}
</style>
