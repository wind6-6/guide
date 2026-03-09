<template>
  <div class="diary-container">
    <!-- 页面标题 -->
    <div class="page-header">
      <h1 class="page-title">
        <el-icon><Notebook /></el-icon>
        旅游日记
      </h1>
      <p class="page-subtitle">记录美好旅程，分享精彩瞬间</p>
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
        <el-col :span="8">
          <el-input
            v-model="searchForm.keyword"
            placeholder="搜索日记标题、内容..."
            clearable
            @keyup.enter="handleSearch"
          >
            <template #prefix>
              <el-icon><Search /></el-icon>
            </template>
          </el-input>
        </el-col>
        <el-col :span="5">
          <el-select v-model="searchForm.sortBy" placeholder="排序方式" @change="handleSearch">
            <el-option label="最新发布" value="newest"></el-option>
            <el-option label="热度最高" value="hotness"></el-option>
            <el-option label="评分最高" value="rating"></el-option>
          </el-select>
        </el-col>
        <el-col :span="5">
          <el-select v-model="searchForm.scenic" placeholder="目的地" clearable @change="handleSearch">
            <el-option label="全部目的地" value=""></el-option>
            <el-option label="北京" value="beijing"></el-option>
            <el-option label="上海" value="shanghai"></el-option>
            <el-option label="杭州" value="hangzhou"></el-option>
          </el-select>
        </el-col>
        <el-col :span="6">
          <el-button type="primary" @click="handleSearch" :icon="Search">搜索</el-button>
          <el-button type="success" @click="showCreateDialog = true" :icon="Plus">写日记</el-button>
        </el-col>
      </el-row>
    </el-card>

    <!-- 日记列表 -->
    <div class="diary-list" v-loading="loading">
      <el-empty v-if="diaryList.length === 0" description="暂无日记"></el-empty>
      <el-row :gutter="20" v-else>
        <el-col :span="8" v-for="diary in diaryList" :key="diary.id">
          <el-card shadow="hover" class="diary-card">
            <div class="diary-cover">
              <div class="cover-placeholder">
                <el-icon><Picture /></el-icon>
                <span>{{ diary.title }}</span>
              </div>
              <div class="diary-badge" v-if="diary.isTop">
                <el-tag type="danger" size="small" effect="dark">置顶</el-tag>
              </div>
            </div>
            <div class="diary-content">
              <h3 class="diary-title">{{ diary.title }}</h3>
              <p class="diary-excerpt">{{ diary.content }}</p>
              <div class="diary-meta">
                <div class="meta-left">
                  <el-avatar :size="24" :src="diary.authorAvatar"></el-avatar>
                  <span class="author-name">{{ diary.author }}</span>
                  <span class="publish-time">{{ diary.create_time }}</span>
                </div>
              </div>
              <div class="diary-stats">
                <span class="stat-item">
                  <el-icon><View /></el-icon>
                  {{ diary.views || 0 }}
                </span>
                <span class="stat-item">
                  <el-icon><Star /></el-icon>
                  {{ diary.hotness }}
                </span>
                <span class="stat-item">
                  <el-icon><ChatDotRound /></el-icon>
                  {{ diary.comments || 0 }}
                </span>
              </div>
              <div class="diary-rating">
                <el-rate v-model="diary.rating" disabled show-score score-template="{value}分"></el-rate>
              </div>
            </div>
            <div class="diary-actions">
              <el-button type="primary" size="small" @click="viewDetail(diary)">
                <el-icon><View /></el-icon>
                阅读全文
              </el-button>
              <el-button size="small" @click="generateAnimation(diary)">
                <el-icon><VideoPlay /></el-icon>
                生成动画
              </el-button>
            </div>
          </el-card>
        </el-col>
      </el-row>
    </div>

    <!-- 创建日记对话框 -->
    <el-dialog
      title="✍️ 创建新日记"
      v-model="showCreateDialog"
      width="700px"
      class="create-dialog"
    >
      <el-form :model="diaryForm" label-position="top">
        <el-form-item label="标题">
          <el-input
            v-model="diaryForm.title"
            placeholder="给你的日记起个标题"
            maxlength="50"
            show-word-limit
          ></el-input>
        </el-form-item>
        <el-form-item label="目的地">
          <el-select v-model="diaryForm.scenic" placeholder="选择旅游目的地" style="width: 100%">
            <el-option label="北京" value="beijing"></el-option>
            <el-option label="上海" value="shanghai"></el-option>
            <el-option label="杭州" value="hangzhou"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="内容">
          <el-input
            v-model="diaryForm.content"
            type="textarea"
            :rows="6"
            placeholder="记录你的旅行故事..."
            maxlength="2000"
            show-word-limit
          ></el-input>
        </el-form-item>
        <el-form-item label="上传图片">
          <el-upload
            action="#"
            list-type="picture-card"
            :auto-upload="false"
            :on-change="handleImageChange"
            :file-list="diaryForm.images"
          >
            <el-icon><Plus /></el-icon>
          </el-upload>
        </el-form-item>
        <el-form-item label="评分">
          <div class="rating-wrapper">
            <el-rate v-model="diaryForm.rating" :max="5" size="large"></el-rate>
            <span class="rating-text">{{ ratingText }}</span>
          </div>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="showCreateDialog = false">取消</el-button>
          <el-button type="primary" @click="createDiary" :loading="creating">发布日记</el-button>
        </span>
      </template>
    </el-dialog>

    <!-- 日记详情对话框 -->
    <el-dialog
      title="日记详情"
      v-model="detailDialogVisible"
      width="800px"
      class="detail-dialog"
    >
      <div v-if="currentDiary" class="detail-content">
        <div class="detail-header">
          <h2>{{ currentDiary.title }}</h2>
          <div class="detail-meta">
            <el-avatar :size="40" :src="currentDiary.authorAvatar"></el-avatar>
            <div class="meta-info">
              <div class="author-name">{{ currentDiary.author }}</div>
              <div class="publish-time">{{ currentDiary.create_time }}</div>
            </div>
          </div>
        </div>
        <div class="detail-body">
          <p>{{ currentDiary.content }}</p>
        </div>
        <div class="detail-footer">
          <div class="detail-stats">
            <span><el-icon><View /></el-icon> {{ currentDiary.views || 0 }} 浏览</span>
            <span><el-icon><Star /></el-icon> {{ currentDiary.hotness }} 热度</span>
          </div>
          <el-rate v-model="currentDiary.rating" disabled show-score></el-rate>
        </div>
      </div>
    </el-dialog>

    <!-- AIGC动画生成对话框 -->
    <el-dialog
      title="🎬 AIGC生成旅游动画"
      v-model="animationDialogVisible"
      width="600px"
      class="animation-dialog"
    >
      <div v-if="animationLoading" class="animation-loading">
        <el-skeleton :rows="3" animated />
        <div class="loading-text">
          <el-icon class="is-loading"><Loading /></el-icon>
          正在生成旅游动画，请稍候...
        </div>
      </div>
      <div v-else-if="animationResult" class="animation-result">
        <div class="animation-preview">
          <video v-if="animationResult.url" :src="animationResult.url" controls></video>
          <div v-else class="preview-placeholder">
            <el-icon><VideoPlay /></el-icon>
            <span>动画预览</span>
          </div>
        </div>
        <div class="animation-info">
          <h4>{{ animationResult.title }}</h4>
          <p>{{ animationResult.description }}</p>
        </div>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import { Notebook, Search, Plus, Picture, View, Star, ChatDotRound, VideoPlay, Loading } from '@element-plus/icons-vue'

export default {
  name: 'DiaryView',
  components: {
    Notebook,
    Search,
    Plus,
    Picture,
    View,
    Star,
    ChatDotRound,
    VideoPlay,
    Loading
  },
  data() {
    return {
      searchForm: {
        keyword: '',
        sortBy: 'newest',
        scenic: ''
      },
      diaryForm: {
        title: '',
        content: '',
        scenic: '',
        rating: 5,
        images: []
      },
      diaryList: [],
      loading: false,
      creating: false,
      showCreateDialog: false,
      detailDialogVisible: false,
      animationDialogVisible: false,
      animationLoading: false,
      currentDiary: null,
      animationResult: null
    }
  },
  computed: {
    ratingText() {
      const texts = ['', '很差', '较差', '一般', '推荐', '力荐']
      return texts[this.diaryForm.rating] || ''
    }
  },
  mounted() {
    this.getDiaryList()
  },
  methods: {
    async getDiaryList() {
      this.loading = true
      try {
        // 模拟数据
        this.diaryList = [
          {
            id: 1,
            title: '北京之行：故宫一日游',
            content: '今天去了故宫，人很多，但是很值得。太和殿的宏伟壮观让我印象深刻，走在紫禁城的石板路上，仿佛穿越回了明清时代。建议早点去，可以避开人流高峰。',
            hotness: 1280,
            rating: 4.8,
            views: 3560,
            comments: 128,
            author: '旅行达人',
            authorAvatar: '',
            create_time: '2026-03-01',
            isTop: true
          },
          {
            id: 2,
            title: '上海之旅：外滩夜景',
            content: '外滩的夜景真美！黄浦江两岸的灯光璀璨夺目，东方明珠塔在夜色中格外耀眼。晚上在江边散步，吹着江风，感受这座城市的繁华与浪漫。',
            hotness: 980,
            rating: 4.9,
            views: 2890,
            comments: 96,
            author: '夜景控',
            authorAvatar: '',
            create_time: '2026-02-28',
            isTop: false
          },
          {
            id: 3,
            title: '杭州西湖：断桥残雪',
            content: '西湖的美名不虚传，断桥残雪的景色如诗如画。虽然没看到真正的雪，但湖面上的薄雾和远处的山峦构成了一幅水墨画。',
            hotness: 856,
            rating: 4.7,
            views: 2156,
            comments: 78,
            author: '江南游子',
            authorAvatar: '',
            create_time: '2026-02-25',
            isTop: false
          }
        ]
      } catch (error) {
        console.error('获取日记列表失败:', error)
        this.$message.error('获取日记列表失败')
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
    handleImageChange(file, fileList) {
      this.diaryForm.images = fileList
    },
    async createDiary() {
      if (!this.diaryForm.title || !this.diaryForm.content) {
        this.$message.error('标题和内容不能为空')
        return
      }
      
      this.creating = true
      try {
        await new Promise(resolve => setTimeout(resolve, 1000))
        const newDiary = {
          id: Date.now(),
          title: this.diaryForm.title,
          content: this.diaryForm.content,
          hotness: 0,
          rating: this.diaryForm.rating,
          views: 0,
          comments: 0,
          author: '我',
          authorAvatar: '',
          create_time: new Date().toLocaleDateString(),
          isTop: false
        }
        this.diaryList.unshift(newDiary)
        this.showCreateDialog = false
        this.diaryForm = {
          title: '',
          content: '',
          scenic: '',
          rating: 5,
          images: []
        }
        this.$message.success('日记发布成功！')
      } catch (error) {
        console.error('创建日记失败:', error)
        this.$message.error('创建日记失败')
      } finally {
        this.creating = false
      }
    },
    viewDetail(diary) {
      this.currentDiary = diary
      this.detailDialogVisible = true
      // 增加浏览量
      diary.views++
    },
    async generateAnimation(diary) {
      this.animationDialogVisible = true
      this.animationLoading = true
      this.animationResult = null
      
      try {
        await new Promise(resolve => setTimeout(resolve, 3000))
        this.animationResult = {
          title: `${diary.title} - 旅游动画`,
          description: '基于您的照片和文字描述，AI为您生成了这段精美的旅游动画',
          url: ''
        }
        this.$message.success('动画生成成功！')
      } catch (error) {
        console.error('生成动画失败:', error)
        this.$message.error('生成动画失败')
      } finally {
        this.animationLoading = false
      }
    }
  }
}
</script>

<style scoped>
.diary-container {
  padding: 20px;
  background: linear-gradient(135deg, #f5f7fa 0%, #e4e7ed 100%);
  min-height: 100vh;
}

/* 页面标题 */
.page-header {
  text-align: center;
  margin-bottom: 30px;
  padding: 30px 0;
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
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

/* 日记列表 */
.diary-list {
  margin-top: 20px;
}

.diary-card {
  margin-bottom: 20px;
  border-radius: 12px;
  overflow: hidden;
  transition: all 0.3s ease;
}

.diary-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 12px 40px rgba(0, 0, 0, 0.15);
}

.diary-cover {
  height: 180px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  margin: -20px -20px 15px -20px;
  position: relative;
}

.cover-placeholder {
  text-align: center;
  color: white;
}

.cover-placeholder .el-icon {
  font-size: 48px;
  margin-bottom: 10px;
}

.cover-placeholder span {
  display: block;
  font-size: 16px;
  font-weight: bold;
}

.diary-badge {
  position: absolute;
  top: 10px;
  right: 10px;
}

.diary-title {
  font-size: 18px;
  font-weight: bold;
  margin: 0 0 10px 0;
  color: #303133;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.diary-excerpt {
  color: #606266;
  font-size: 14px;
  line-height: 1.6;
  margin-bottom: 15px;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.diary-meta {
  display: flex;
  align-items: center;
  margin-bottom: 10px;
}

.meta-left {
  display: flex;
  align-items: center;
  gap: 8px;
}

.author-name {
  font-size: 13px;
  color: #606266;
}

.publish-time {
  font-size: 12px;
  color: #909399;
}

.diary-stats {
  display: flex;
  gap: 15px;
  margin-bottom: 10px;
  padding: 10px 0;
  border-top: 1px solid #ebeef5;
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 13px;
  color: #606266;
}

.diary-rating {
  margin-bottom: 15px;
}

.diary-actions {
  display: flex;
  gap: 10px;
}

/* 创建对话框 */
.create-dialog :deep(.el-dialog__header) {
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
  color: white;
  padding: 20px;
}

.create-dialog :deep(.el-dialog__title) {
  color: white;
}

.rating-wrapper {
  display: flex;
  align-items: center;
  gap: 15px;
}

.rating-text {
  color: #f7ba2a;
  font-weight: bold;
}

/* 详情对话框 */
.detail-dialog :deep(.el-dialog__header) {
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
  color: white;
}

.detail-content {
  padding: 20px 0;
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

.detail-meta {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
}

.meta-info {
  text-align: left;
}

.author-name {
  font-weight: bold;
  color: #303133;
}

.publish-time {
  font-size: 13px;
  color: #909399;
}

.detail-body {
  margin: 20px 0;
  line-height: 1.8;
  color: #606266;
}

.detail-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 20px;
  border-top: 1px solid #ebeef5;
}

.detail-stats {
  display: flex;
  gap: 20px;
  color: #606266;
}

.detail-stats span {
  display: flex;
  align-items: center;
  gap: 5px;
}

/* 动画对话框 */
.animation-dialog :deep(.el-dialog__header) {
  background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
  color: white;
}

.animation-loading {
  text-align: center;
  padding: 40px;
}

.loading-text {
  margin-top: 20px;
  color: #606266;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
}

.animation-result {
  padding: 20px;
}

.animation-preview {
  background: #f5f7fa;
  border-radius: 8px;
  overflow: hidden;
  margin-bottom: 20px;
}

.animation-preview video {
  width: 100%;
  display: block;
}

.preview-placeholder {
  height: 300px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: #909399;
}

.preview-placeholder .el-icon {
  font-size: 64px;
  margin-bottom: 10px;
}

.animation-info {
  text-align: center;
}

.animation-info h4 {
  margin: 0 0 10px 0;
  color: #303133;
}

.animation-info p {
  color: #606266;
  margin: 0;
}
</style>