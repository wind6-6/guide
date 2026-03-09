<template>
  <div class="route-plan-container">
    <el-card shadow="hover" class="route-card">
      <template #header>
        <div class="card-header">
          <span>路线规划</span>
        </div>
      </template>
      <el-form :model="routeForm" class="route-form">
        <el-form-item label="起点">
          <el-input v-model="routeForm.start" placeholder="请输入起点"></el-input>
        </el-form-item>
        <el-form-item label="终点">
          <el-input v-model="routeForm.end" placeholder="请输入终点"></el-input>
        </el-form-item>
        <el-form-item label="策略">
          <el-radio-group v-model="routeForm.strategy">
            <el-radio label="distance">最短距离</el-radio>
            <el-radio label="time">最短时间</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handlePlan">规划路线</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <el-card v-if="routeResult" shadow="hover" class="result-card">
      <template #header>
        <div class="card-header">
          <span>路线结果</span>
        </div>
      </template>
      <div class="route-result">
        <p><strong>路径:</strong> {{ routeResult.path.join(' → ') }}</p>
        <p><strong>距离:</strong> {{ routeResult.distance }} 米</p>
        <p><strong>策略:</strong> {{ routeResult.strategy === 'distance' ? '最短距离' : '最短时间' }}</p>
      </div>
    </el-card>
  </div>
</template>

<script>
export default {
  name: 'RoutePlanView',
  data() {
    return {
      routeForm: {
        start: '',
        end: '',
        strategy: 'distance'
      },
      routeResult: null
    }
  },
  methods: {
    async handlePlan() {
      if (!this.routeForm.start || !this.routeForm.end) {
        this.$message.error('起点和终点不能为空');
        return;
      }
      
      try {
        // 这里应该调用后端API，现在使用模拟数据
        this.routeResult = {
          path: [this.routeForm.start, 'A', 'B', this.routeForm.end],
          distance: 5000,
          strategy: this.routeForm.strategy
        };
        this.$message.success('路线规划成功');
      } catch (error) {
        console.error('路线规划失败:', error);
        this.$message.error('路线规划失败');
      }
    }
  }
}
</script>

<style scoped>
.route-plan-container {
  padding: 20px;
}

.route-card {
  margin-bottom: 20px;
}

.route-form {
  margin-top: 10px;
}

.result-card {
  margin-top: 20px;
}

.route-result {
  padding: 10px;
}

.route-result p {
  margin: 10px 0;
}
</style>