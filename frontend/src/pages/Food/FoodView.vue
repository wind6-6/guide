<template>
  <div class="food-container">
    <el-card shadow="hover" class="search-card">
      <template #header>
        <div class="card-header">
          <span>美食推荐</span>
        </div>
      </template>
      <el-form :inline="true" :model="searchForm" class="search-form">
        <el-form-item label="菜系">
          <el-select v-model="searchForm.cuisine" placeholder="选择菜系">
            <el-option label="全部" value=""></el-option>
            <el-option label="川菜" value="sichuan"></el-option>
            <el-option label="粤菜" value="cantonese"></el-option>
            <el-option label="鲁菜" value="shandong"></el-option>
            <el-option label="淮扬菜" value="huaiyang"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSearch">搜索</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <div class="food-list">
      <el-card
        v-for="food in foodList"
        :key="food.id"
        shadow="hover"
        class="food-card"
      >
        <template #header>
          <div class="food-header">
            <span>{{ food.name }}</span>
            <div class="food-rating">
              <el-rate
                v-model="food.rating"
                :max="5"
                disabled
                show-score
                score-template="{{ value }}"
              ></el-rate>
            </div>
          </div>
        </template>
        <div class="food-content">
          <p>{{ food.description }}</p>
          <div class="food-info">
            <span class="cuisine">{{ getCuisineName(food.cuisine) }}</span>
            <span class="price">价格: ¥{{ food.price }}</span>
          </div>
        </div>
      </el-card>
    </div>
  </div>
</template>

<script>
export default {
  name: 'FoodView',
  data() {
    return {
      searchForm: {
        cuisine: ''
      },
      foodList: []
    }
  },
  mounted() {
    this.getFoodList()
  },
  methods: {
    async getFoodList() {
      try {
        // 这里应该调用后端API，现在使用模拟数据
        this.foodList = [
          {
            id: 1,
            name: '麻婆豆腐',
            description: '四川传统名菜，麻辣鲜香',
            hotness: 90,
            rating: 4.5,
            cuisine: 'sichuan',
            price: 38
          },
          {
            id: 2,
            name: '宫保鸡丁',
            description: '经典川菜，酸甜可口',
            hotness: 85,
            rating: 4.3,
            cuisine: 'sichuan',
            price: 45
          },
          {
            id: 3,
            name: '糖醋里脊',
            description: '酸甜可口，外酥里嫩',
            hotness: 80,
            rating: 4.2,
            cuisine: 'shandong',
            price: 58
          }
        ]
      } catch (error) {
        console.error('获取美食列表失败:', error)
      }
    },
    async handleSearch() {
      try {
        // 这里应该调用后端API，现在使用模拟数据
        this.foodList = [
          {
            id: 1,
            name: '麻婆豆腐',
            description: '四川传统名菜，麻辣鲜香',
            hotness: 90,
            rating: 4.5,
            cuisine: 'sichuan',
            price: 38
          },
          {
            id: 2,
            name: '宫保鸡丁',
            description: '经典川菜，酸甜可口',
            hotness: 85,
            rating: 4.3,
            cuisine: 'sichuan',
            price: 45
          }
        ]
      } catch (error) {
        console.error('搜索失败:', error)
      }
    },
    getCuisineName(cuisine) {
      const cuisineMap = {
        'sichuan': '川菜',
        'cantonese': '粤菜',
        'shandong': '鲁菜',
        'huaiyang': '淮扬菜'
      }
      return cuisineMap[cuisine] || cuisine
    }
  }
}
</script>

<style scoped>
.food-container {
  padding: 20px;
}

.search-card {
  margin-bottom: 20px;
}

.search-form {
  margin-top: 10px;
}

.food-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
}

.food-card {
  height: 100%;
}

.food-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.food-content {
  margin-top: 10px;
}

.food-info {
  margin-top: 15px;
  display: flex;
  justify-content: space-between;
  font-size: 14px;
  color: #606266;
}

.cuisine {
  color: #409eff;
}

.price {
  color: #f56c6c;
  font-weight: bold;
}
</style>