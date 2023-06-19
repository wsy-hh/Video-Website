<template>
  <div id="app">
    <div class="b-wrap">
      <!-- 视频内容 -->
      <div v-show="mainDataYes">
        <div class="video-list">
          <el-row :gutter="20" style="width:100%">
            <el-col :span="4" v-for="item in videoList" >
              <div class="right" @click="navToLabelVideo(item)" style="cursor: pointer;">
                <div class="pic">
                  <img class="rigpic" :src="'http://127.0.0.1:8000/static/' + item.picture.path" alt />
                </div>
                <div class="rititle" style="">{{ item.title }}</div>
                <div class="author" style="overflow: hidden;">{{ item.user.nickname }}</div>
              </div>
            </el-col>
          </el-row>
        </div>
        <!-- 分页功能 -->
        <el-pagination :background="true" layout="prev, pager, next" @current-change="handleCurrentChange"
          :current-page="currentPage" :total="500"

          style="position: fixed; bottom: 5%; left: 50%; transform: translateX(-50%);">
        </el-pagination>
      </div>

    </div>
  </div>
</template>

<script>
// 组件
import VideoItem from '../common/videoitem/VideoItem'
import axios from 'axios'

export default {
  name: 'app',
  components: {
    VideoItem
  },
  data () {
    return {

      // 主要内容数据
      mainDataList: [
        {}, {}
      ],
      mainDataListCopy: [],
      // 判断是否有数据 显示没有数据图片
      mainDataYes: true,
      // 鼠标移进的当前item
      currentIndex: null,

      // 当前页码
      currentPage: 1,

      videoList: [],

      keyword: ''

    }
  },
  mounted () {
    const keyword = sessionStorage.getItem('keyword')
    this.keyword = keyword
    this.getKeywordVideoList(keyword)
  },
  methods: {

    handleCurrentChange (e) {
      this.currentPage = e
      const keyword = this.keyword
      this.getKeywordVideoList(keyword)
    },
    navToLabelVideo (item) {
      console.log(item)
      localStorage.removeItem('video')
      localStorage.setItem('video', JSON.stringify({ video: item }))
      this.$router.push('/radio')
    },
    getKeywordVideoList (keyword = '') {
      let input = ''
      console.log(keyword)
      if (keyword != null) {
        input = keyword
      }
      axios.post('http://127.0.0.1:8000/api/getvideolist/', {
        keyword: input,
        page: this.currentPage
      }, {
        headers: {
          Authorization: 'Bearer ' + sessionStorage.getItem('token'),
          'Content-Type': 'application/json'
        }
      }).then(res => {
        this.videoList = res.data.results
        console.log(res)
      }).catch(err => {
        this.videoList = []
        console.error(err)
      })
    },
    // 鼠标事件
    enter (i) {
      this.currentIndex = i
    },
    leave () {
      this.currentIndex = null
    }
  }

}
</script>
<style>
.b-wrap {
  min-height: 80vh;
}

.video-list {
  width: 80vw;
  margin: auto;

}

/* 视频内容 */
.video-list {
  display: flex;
  flex-wrap: wrap;
}

.main-data-item {
  margin-top: 20px;
  margin-right: 25px;
}

.main-data-item:nth-child(5n) {
  margin-right: 0;
}

.video-list-no {
  margin: 50px;
  text-align: center;
}

/* 分页 */
.el-pagination {
  margin-top: 40px;
  text-align: center;
  background: "#00a1d6";
}
</style>
