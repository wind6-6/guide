<template>
  <div class="place-query-container">
    <el-card shadow="hover" class="search-card">
      <template #header>
        <div class="card-header">
          <span>场所查询</span>
        </div>
      </template>
      <el-form :inline="true" :model="searchForm" class="search-form">
        <el-form-item label="关键词">
          <el-input v-model="searchForm.keyword" placeholder="请输入关键词"></el-input>
        </el-form-item>
        <el-form-item label="类型">
          <el-select v-model="searchForm.type" placeholder="选择类型">
            <el-option label="全部" value=""></el-option>
            <el-option label="餐厅" value="restaurant"></el-option>
            <el-option label="厕所" value="toilet"></el-option>
            <el-option label="商店" value="shop"></el-option>
            <el-option label="医疗" value="medical"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSearch">搜索</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <div class="facility-list">
      <el-card
        v-for="facility in facilityList"
        :key="facility.id"
        shadow="hover"
        class="facility-card"
      >
        <template #header>
          <div class="facility-header">
            <span>{{ facility.name }}</span>
            <span class="facility-type">{{ getTypeName(facility.type) }}</span>
          </div>
        </template>
        <div class="facility-content">
          <p>{{ facility.description }}</p>
          <div class="facility-info">
            <span class="location">位置: {{ facility.location }}</span>
          </div>
        </div>
      </el-card>
    </div>
  </div>
</template>

<script>
export default {
  name: 'PlaceQueryView',
  data() {
    return {
      searchForm: {
        keyword: '',
        type: ''
      },
      facilityList: []
    }
  },
  mounted() {
    this.getFacilities()
  },
  methods: {
    async getFacilities() {
      try {
        // 这里应该调用后端API，现在使用模拟数据
        this.facilityList = [
          {
            id: 1,
            name: '中餐厅',
            type: 'restaurant',
            location: '景区中心',
            description: '提供各种中式美食'
          },
          {
            id: 2,
            name: '公共厕所',
            type: 'toilet',
            location: '景区入口',
            description: '干净整洁的公共厕所'
          },
          {
            id: 3,
            name: '纪念品商店',
            type: 'shop',
            location: '景区出口',
            description: '出售各种纪念品'
          }
        ]
      } catch (error) {
        console.error('获取设施列表失败:', error)
      }
    },
    async handleSearch() {
      try {
        // 这里应该调用后端API，现在使用模拟数据
        this.facilityList = [
          {
            id: 1,
            name: '中餐厅',
            type: 'restaurant',
            location: '景区中心',
            description: '提供各种中式美食'
          }
        ]
      } catch (error) {
        console.error('搜索失败:', error)
      }
    },
    getTypeName(type) {
      const typeMap = {
        'restaurant': '餐厅',
        'toilet': '厕所',
        'shop': '商店',
        'medical': '医疗'
      }
      return typeMap[type] || type
    }
  }
}
</script>

<style scoped>
.place-query-container {
  padding: 20px;
}

.search-card {
  margin-bottom: 20px;
}

.search-form {
  margin-top: 10px;
}

.facility-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
}

.facility-card {
  height: 100%;
}

.facility-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.facility-type {
  background-color: #ecf5ff;
  color: #409eff;
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 12px;
}

.facility-content {
  margin-top: 10px;
}

.facility-info {
  margin-top: 15px;
  font-size: 14px;
  color: #606266;
}
</style>