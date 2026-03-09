<template>
  <div class="diary-container">
    <el-card shadow="hover" class="diary-card">
      <template #header>
        <div class="card-header">
          <span>旅游日记</span>
          <el-button type="primary" @click="showCreateDialog = true">创建日记</el-button>
        </div>
      </template>
      <div class="diary-list">
        <el-card
          v-for="diary in diaryList"
          :key="diary.id"
          shadow="hover"
          class="diary-item"
        >
          <template #header>
            <div class="diary-header">
              <span>{{ diary.title }}</span>
              <span class="diary-time">{{ diary.create_time }}</span>
            </div>
          </template>
          <div class="diary-content">
            <p>{{ diary.content }}</p>
            <div class="diary-info">
              <span class="hotness">热度: {{ diary.hotness }}</span>
              <el-rate
                v-model="diary.rating"
                :max="5"
                disabled
                show-score
                score-template="{{ value }}"
              ></el-rate>
            </div>
          </div>
        </el-card>
      </div>
    </el-card>

    <!-- 创建日记对话框 -->
    <el-dialog
      title="创建日记"
      v-model="showCreateDialog"
      width="500px"
    >
      <el-form :model="diaryForm">
        <el-form-item label="标题">
          <el-input v-model="diaryForm.title" placeholder="请输入标题"></el-input>
        </el-form-item>
        <el-form-item label="内容">
          <el-input
            v-model="diaryForm.content"
            type="textarea"
            :rows="4"
            placeholder="请输入内容"
          ></el-input>
        </el-form-item>
        <el-form-item label="评分">
          <el-rate v-model="diaryForm.rating" :max="5"></el-rate>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="showCreateDialog = false">取消</el-button>
          <el-button type="primary" @click="createDiary">确定</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script>
export default {
  name: 'DiaryView',
  data() {
    return {
      showCreateDialog: false,
      diaryForm: {
        title: '',
        content: '',
        rating: 5
      },
      diaryList: []
    }
  },
  mounted() {
    this.getDiaryList()
  },
  methods: {
    async getDiaryList() {
      try {
        // 这里应该调用后端API，现在使用模拟数据
        this.diaryList = [
          {
            id: 1,
            title: '北京之行',
            content: '今天去了故宫，人很多，但是很值得...',
            hotness: 100,
            rating: 4.5,
            create_time: '2026-03-01 10:00:00'
          },
          {
            id: 2,
            title: '上海之旅',
            content: '外滩的夜景真美...',
            hotness: 80,
            rating: 4.8,
            create_time: '2026-02-28 15:00:00'
          }
        ]
      } catch (error) {
        console.error('获取日记列表失败:', error)
      }
    },
    async createDiary() {
      if (!this.diaryForm.title || !this.diaryForm.content) {
        this.$message.error('标题和内容不能为空');
        return;
      }
      
      try {
        // 这里应该调用后端API，现在使用模拟数据
        const newDiary = {
          id: Date.now(),
          title: this.diaryForm.title,
          content: this.diaryForm.content,
          hotness: 0,
          rating: this.diaryForm.rating,
          create_time: new Date().toLocaleString()
        };
        this.diaryList.unshift(newDiary);
        this.showCreateDialog = false;
        this.diaryForm = {
          title: '',
          content: '',
          rating: 5
        };
        this.$message.success('日记创建成功');
      } catch (error) {
        console.error('创建日记失败:', error);
        this.$message.error('创建日记失败');
      }
    }
  }
}
</script>

<style scoped>
.diary-container {
  padding: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.diary-list {
  margin-top: 20px;
}

.diary-item {
  margin-bottom: 20px;
}

.diary-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.diary-time {
  font-size: 12px;
  color: #909399;
}

.diary-content {
  margin-top: 10px;
}

.diary-info {
  margin-top: 15px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 14px;
  color: #606266;
}

.hotness {
  color: #f56c6c;
}

.dialog-footer {
  width: 100%;
  display: flex;
  justify-content: flex-end;
}
</style>