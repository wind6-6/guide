import axios from 'axios'
import base from './base'
import { ElMessage } from 'element-plus'

// 创建 axios 实例
const api = axios.create({
  baseURL: base.baseUrl,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// 请求拦截器
api.interceptors.request.use(
  config => {
    const token = sessionStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  error => {
    return Promise.reject(error)
  }
)

// 响应拦截器
api.interceptors.response.use(
  response => {
    const res = response.data
    if (res.status !== 200) {
      ElMessage.error(res.msg || '请求失败')
      return Promise.reject(new Error(res.msg))
    }
    return res
  },
  error => {
    ElMessage.error(error.response?.data?.msg || '网络错误')
    return Promise.reject(error)
  }
)

// 用户相关 API
export const userApi = {
  login: (data) => api.post(base.login, data),
  register: (data) => api.post(base.register, data),
  getInfo: () => api.get(base.userInfo)
}

// 推荐相关 API
export const recommendApi = {
  getList: (params) => api.get(base.recommendList, { params })
}

export default api
