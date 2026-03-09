<template>
  <div class="user-center-container">
    <el-card shadow="hover" class="user-card">
      <template #header>
        <div class="card-header">
          <span>用户中心</span>
        </div>
      </template>
      <div class="user-info">
        <div class="user-avatar">
          <el-avatar :size="100" :src="userInfo.avatar || defaultAvatar">
            {{ userInfo.name?.charAt(0) || 'U' }}
          </el-avatar>
        </div>
        <div class="user-details">
          <h3>{{ userInfo.name || '未设置' }}</h3>
          <p><strong>用户名:</strong> {{ userInfo.username }}</p>
          <p><strong>手机号:</strong> {{ userInfo.phone || '未设置' }}</p>
          <p><strong>邮箱:</strong> {{ userInfo.email || '未设置' }}</p>
        </div>
      </div>
      <div class="user-actions">
        <el-button type="primary" @click="handleLogout">退出登录</el-button>
      </div>
    </el-card>
  </div>
</template>

<script>
export default {
  name: 'UserCenterView',
  data() {
    return {
      defaultAvatar: '',
      userInfo: {
        username: 'admin',
        name: '管理员',
        phone: '13800138000',
        email: 'admin@example.com'
      }
    }
  },
  mounted() {
    this.getUserInfo()
  },
  methods: {
    async getUserInfo() {
      try {
        // 这里应该调用后端API，现在使用模拟数据
        this.userInfo = {
          username: 'admin',
          name: '管理员',
          phone: '13800138000',
          email: 'admin@example.com'
        }
      } catch (error) {
        console.error('获取用户信息失败:', error)
      }
    },
    handleLogout() {
      sessionStorage.removeItem('token');
      this.$router.push('/login');
      this.$message.success('退出登录成功');
    }
  }
}
</script>

<style scoped>
.user-center-container {
  padding: 20px;
}

.user-info {
  display: flex;
  align-items: center;
  margin-bottom: 30px;
}

.user-avatar {
  margin-right: 30px;
}

.user-details h3 {
  margin: 0 0 15px 0;
}

.user-details p {
  margin: 10px 0;
  font-size: 16px;
}

.user-actions {
  margin-top: 20px;
}
</style>