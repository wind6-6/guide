<template>
  <div id="app">
    <el-container>
      <el-header height="60px">
        <div class="header-container">
          <div class="logo">个性化旅游系统</div>
          <el-menu
            :default-active="activeIndex"
            class="el-menu-demo"
            mode="horizontal"
            @select="handleMenuSelect"
          >
            <el-menu-item index="/">首页</el-menu-item>
            <el-menu-item index="/recommend">景点推荐</el-menu-item>
            <el-menu-item index="/route-plan">路线规划</el-menu-item>
            <el-menu-item index="/place-query">场所查询</el-menu-item>
            <el-menu-item index="/diary">旅游日记</el-menu-item>
            <el-menu-item index="/food">美食推荐</el-menu-item>
            <el-menu-item index="/user" v-if="isLoggedIn">用户中心</el-menu-item>
            <el-menu-item index="/login" v-else>登录</el-menu-item>
          </el-menu>
        </div>
      </el-header>
      <el-main>
        <router-view/>
      </el-main>
    </el-container>
  </div>
</template>

<script>
export default {
  name: 'App',
  data() {
    return {
      activeIndex: '/'
    }
  },
  computed: {
    isLoggedIn() {
      return !!sessionStorage.getItem('token');
    }
  },
  watch: {
    $route() {
      this.activeIndex = this.$route.path;
    }
  },
  methods: {
    handleMenuSelect(key) {
      this.$router.push(key);
    }
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

.header-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 100%;
  padding: 0 20px;
}

.logo {
  font-size: 20px;
  font-weight: bold;
  color: #409eff;
}

.el-menu-demo {
  border-bottom: none;
}

.el-main {
  padding: 20px;
}
</style>
