<template>
    <div id="app">

        <el-container class="container">
            <el-main class="main">
                <el-row>
                    <el-col :span="24">
                        <div class="title">{{ video_detail.video.title }}</div>
                    </el-col>
                </el-row>
                <el-row>
                    <el-col :span="4">
                        <div class="desc" style="margin:10px 10px 10px 0px ;">{{ video_detail.video.create_time }}</div>
                    </el-col>
                    <el-col :span="6">
                        <div class="desc">Reprinting is prohibited without the authorization of the author.</div>
                    </el-col>
                    <el-col :span="6">
                    </el-col>
                    <el-col :span="6">
                    </el-col>
                </el-row>
                <el-row>
                    <el-col :span="24">
                        <video class="video" :src="'http://127.0.0.1:8000/static/' + video_detail.video.file.path" controls
                            @play="handlePlay"></video>
                        <div
                            style="width: 100%; margin-top: 10px; height: 1px; border-bottom: 1px solid rgb(220, 220, 220);;">
                        </div>
                        <div style="margin: 20px 0;">{{ video_detail.video.introduction }}</div>
                        <div style="">
                            <el-tag v-for="item in video_detail.video.labels" :key="item.id"
                                style="margin: 0 10px;  text-align: center;" type="success">{{ item.name }}</el-tag>
                        </div>
                    </el-col>
                </el-row>
            </el-main>
            <el-aside width="400px" style="padding: 20px 0;">
                <div class="user-container">
                    <div class="user-icon">
                        <img src="https://cdn-icons-png.flaticon.com/512/3135/3135715.png" width="56px" height="56px"
                            alt="">
                    </div>
                    <div class="user-info">
                        <el-row>
                            <el-col :span="24">
                                <div style="padding: 5px 0; color: rgb(233, 120, 49); font-size: 20px;">{{
                                    video_detail.video.user.nickname }}</div>
                            </el-col>
                        </el-row>
                        <el-row>
                            <el-col :span="24">
                                <div style="padding: 5px 0; color: rgb(119, 125, 130);font-size: 14px;">
                                    This is introduction part. Later on, i'll update this function.
                                </div>
                            </el-col>
                        </el-row>
                        <el-row>
                            <el-col :span="24" style="margin: 5px 0;">
                                <el-button v-if="subscribe_status"
                                    style="margin: 5px 0;width: 150px; height: 36px; line-height: 0;" type="success"
                                    @click="cancel">Cancel</el-button>
                                <el-button v-else style="margin: 5px 0;width: 150px; height: 36px; line-height: 0;"
                                    type="warning" @click="subscribe">Subscribe</el-button>

                            </el-col>
                        </el-row>
                    </div>
                </div>
                <div class="recommand-list">
                    <div class="recommand-card" v-for="item in creator_video_list" :key="item.id"
                        @click="navToLabelVideo(item)">
                        <div class="recommand-card-left">
                            <img width="100%" height="90px" :src="'http://127.0.0.1:8000/static/' + item.picture.path"
                                alt="">
                        </div>
                        <div class="recommand-card-right">
                            <el-row>
                                <el-col :span="24">
                                    <div
                                        style="display: -webkit-box;-webkit-line-clamp: 2;-webkit-box-orient: vertical;overflow: hidden;text-overflow: ellipsis; margin-bottom: 5px;">
                                        {{ item.title }}
                                    </div>
                                </el-col>
                            </el-row>
                            <el-row>
                                <el-col :span="24" style="font-size: 14px; color:rgb(119, 125, 130);margin: 5px 0;">
                                    {{ item.user.nickname }}
                                </el-col>
                            </el-row>
                            <el-row>
                                <el-col :span="24" style="font-size: 14px; color:rgb(119, 125, 130); ">
                                    2023-06-12 19:00
                                </el-col>
                            </el-row>
                        </div>

                    </div>

                </div>

            </el-aside>
        </el-container>
    </div>
</template>

<script>
// 组件
import Card from '../common/card/Card'
import TopList from '../common/toplist/TopList'
import axios from 'axios'
import { Message } from 'element-ui'

export default {
  name: 'app',
  components: {

  },
  data () {
    return {
      start_play: 0,
      time: '',
      // 视频数据格式
      video_detail: {},
      // 推荐列表测试数据
      recommand_list: [
        {
          id: 1,
          title: '房主依据美国“城堡法”，拒绝让警员进入房屋！E130',
          author: '紧疾出击',
          create_time: '2023-06-09 17:00:00',
          img_url: '../../assets/recommand-card.jpg',
          link: 'https://www.google.com'
        },
        {
          id: 2,
          title: '房主依据美国“城堡法”，拒绝让警员进入房屋！E130',
          author: '紧疾出击',
          create_time: '2023-06-09 17:00:00',
          img_url: '../../assets/recommand-card.jpg',
          link: 'https://www.google.com'
        },
        {
          id: 3,
          title: '房主依据美国“城堡法”，拒绝让警员进入房屋！E130',
          author: '紧疾出击',
          create_time: '2023-06-09 17:00:00',
          img_url: '../../assets/recommand-card.jpg',
          link: 'https://www.google.com'
        }
      ],
      subscribe_status: 0,
      creator_video_list: []
    }
  },
  mounted () {
    const data = localStorage.getItem('video')
    console.log(data)
    this.video_detail = JSON.parse(data)
    console.log(JSON.parse(data))
    this.time = this.getCurrentDateTime()
    this.getSubscribeStatus()
    this.getCreatorVideoList()
  },
  methods: {
    navToLabelVideo (item) {
      console.log(item)
      localStorage.removeItem('video')
      localStorage.setItem('video', JSON.stringify({ video: item }))
      this.$router.push('/radio')
    },
    getCreatorVideoList () {
      axios.post('http://127.0.0.1:8000/api/getcreatorvideolist/', {
        email: this.video_detail.video.user.email
      }, {
        headers: {
          Authorization: 'Bearer ' + sessionStorage.getItem('token'),
          'Content-Type': 'application/json'
        }
      }).then(res => {
        this.creator_video_list = res.data
        console.log(res)
      }).catch(err => {
        console.error(err)
      })
    },

    getSubscribeStatus () {
      axios.post('http://127.0.0.1:8000/api/getsubscribestatus/', {
        email: this.video_detail.video.user.email
      }, {
        headers: {
          Authorization: 'Bearer ' + sessionStorage.getItem('token'),
          'Content-Type': 'application/json'
        }
      }).then(res => {
        console.log(res)
        this.subscribe_status = res.data.status
      }).catch(err => {
        console.error(err)
      })
    },
    cancel () {
      axios.post('http://127.0.0.1:8000/api/cancelsubscribe/', {
        email: this.video_detail.video.user.email
      }, {
        headers: {
          Authorization: 'Bearer ' + sessionStorage.getItem('token'),
          'Content-Type': 'application/json'
        }
      }).then(res => {
        // 处理请求成功的响应
        console.log(res)
        Message({
          message: res.data.message,
          type: 'success'
        })
        this.subscribe_status = 0
      })
        .catch(err => {
          // 处理请求失败的情况
          console.error(err)
        })
    },
    subscribe () {
      axios.post('http://127.0.0.1:8000/api/subscribe/', {
        email: this.video_detail.video.user.email
      }, {
        headers: {
          Authorization: 'Bearer ' + sessionStorage.getItem('token'),
          'Content-Type': 'application/json'
        }
      }).then(res => {
        // 处理请求成功的响应
        console.log(res)
        Message({
          message: res.data.message,
          type: 'success'
        })
        this.subscribe_status = 1
      })
        .catch(err => {
          // 处理请求失败的情况
          console.error(err)
        })
    },
    handlePlay () {
      this.start_play += 1
      if (this.start_play == 1) {
        this.addHistoryRecord()
      }
    },
    addHistoryRecord () {
      axios.post('http://127.0.0.1:8000/api/addhistoryrecord/', {
        video_id: this.video_detail.video.id
      }, {
        headers: {
          Authorization: 'Bearer ' + sessionStorage.getItem('token'),
          'Content-Type': 'application/json'
        }
      }).then(res => {
        // 处理请求成功的响应
        console.log(res)
      })
        .catch(err => {
          // 处理请求失败的情况
          console.error(err)
        })
    },
    getCurrentDateTime () {
      const date = new Date()
      const year = date.getFullYear()
      const month = (date.getMonth() + 1).toString().padStart(2, '0')
      const day = date.getDate().toString().padStart(2, '0')
      const hours = date.getHours().toString().padStart(2, '0')
      const minutes = date.getMinutes().toString().padStart(2, '0')
      const currentDateTime = year + '-' + month + '-' + day + ' ' + hours + ':' + minutes
      return currentDateTime
    }

  }
}
</script>
<style>
#app {
    min-height: 100vh;

}

.container {
    box-sizing: border-box;
    padding: 0 20px;
}

.main {
    padding: 0 20px;
}

.title {
    font-size: 22px;
    padding: 10px 0;
}

.desc {
    margin: 10px;
    height: 22px;
    line-height: 22px;
    color: rgb(119, 125, 130);
}

.video {
    width: 100%;
    height: 50%;
    margin: 10px 0;
}

.user-container {
    display: flex;
    width: 380px;
    margin: auto;

}

.user-icon {
    width: 100px;
    display: flex;
    align-items: center;
    justify-content: center;
}

.user-info {
    width: 260px;
}

.recommand-list {
    width: 380px;
    margin: 20px auto;
}

.recommand-card {
    display: flex;
    justify-content: space-around;
    width: 100%;
    margin-bottom: 18px;
}

.recommand-card-left {
    width: 36%;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: hidden;
    border-radius: 5px;
}

.recommand-card-right {
    width: 60%;
}
</style>
