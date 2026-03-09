const { defineConfig } = require('@vue/cli-service')

module.exports = defineConfig({
  transpileDependencies: true,
  devServer: {
    client: {
      // 禁用ResizeObserver错误覆盖层
      overlay: {
        runtimeErrors: (error) => {
          // 忽略ResizeObserver错误
          if (error.message && error.message.includes('ResizeObserver')) {
            return false;
          }
          return true;
        },
      },
    },
    // 配置代理
    proxy: {
      '/api': {
        target: 'http://localhost:8080',
        changeOrigin: true,
        pathRewrite: {
          '^/api': '/api'
        }
      }
    }
  }
})
