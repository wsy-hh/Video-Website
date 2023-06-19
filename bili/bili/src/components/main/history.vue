<template>
  <div id="app">
    <el-card v-for="item in radioList" :key="item.id">
      <el-row :gutter="20">
        <el-col :span="6">
          <div class="con-his">
            <div class="vedio">
              <img :src="'http://127.0.0.1:8000/static/' + item.video.picture.path" width="100%" height="100%" alt />
            </div>
          </div>
        </el-col>
        <el-col :span="18">
          <div class="con-info">
            <div class="title">{{ item.video.title }}</div>
            <div class="time-name">
              <div class="time">{{ item.video.create_time }}</div>
              <div class="name">{{ item.user.nickname }}</div>
            </div>
          </div>
        </el-col>
      </el-row>
    </el-card>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'app',

  data () {
    return {
      // 主要内容数据
      radioList: []
    }
  },
  mounted () {
    this.getHistoryRecordList()
  },
  methods: {
    getHistoryRecordList () {
      axios.get('http://127.0.0.1:8000/api/gethistoryrecordlist/', {
        headers: {
          Authorization: 'Bearer ' + sessionStorage.getItem('token'),
          'Content-Type': 'application/json'
        }
      }).then(res => {
        // 处理请求成功的响应
        console.log(res)
        this.radioList = res.data
      })
        .catch(err => {
          // 处理请求失败的情况
          console.error(err)
        })
    }

  }
}
</script>
<style>
.el-card {
  margin-bottom: 10px;
}

.con-info {
  height: 100%;
}

.time-name {
  display: inline-block;
  width: 100%;
  height: 100%;
}

.title {
  display: inline-block;
  width: 100%;
  font-style: normal;
  text-overflow: ellipsis;
  white-space: nowrap;
  overflow: hidden;
  color: orange;
}

.time {
  float: left;
}

.name {
  float: right;
}
</style>
