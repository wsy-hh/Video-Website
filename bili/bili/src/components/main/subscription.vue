<template>
  <div id="app">
    <el-card class="box-card" v-for="item in subscribeList">
      <div class="subscription">
        <el-row style="display: flex; align-items: center;">
          <el-col :span="4" style="display: flex; align-items: center;">
            <el-avatar :size="50" :src="circleUrl"></el-avatar>
          </el-col>
          <el-col :span="14">
            <div class="sub-name">
              {{ item.nickname }}
            </div>
            <div class="sub-intro">
              This is introduction. At friday, i'll update this function.
            </div>
          </el-col>
          <el-col :span="6">
            <div class="button-sub">
              <button @click="favor(item.email)" class="my_button" :style="{ backgroundColor: bg_color, color: ft_color, }"
                @mouseenter="change()" @mouseleave="goback()">
                {{ content }}
              </button>

            </div>
          </el-col>
        </el-row>
      </div>
    </el-card>

  </div>
</template>

<script>
import { useRouter } from 'vue-router'
import { Message } from 'element-ui'
import axios from 'axios'

export default {
  name: 'app',
  data () {
    return {
      subscribeList: [],
      circleUrl: 'https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png',
      user: {
        username: 'user',
        intro: 'sfbjbnjfcbe'
      },
      // 关注
      liked: false,
      content: 'Followed',
      bg_color: '#fef0f0',
      ft_color: '#f56c6c'

    }
  },
  mounted () {
    this.getSubscribeList()
  },
  methods: {
    cancel (email) {
      axios.post('http://127.0.0.1:8000/api/cancelsubscribe/', {
        email: email
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
    subscribe (email) {
      axios.post('http://127.0.0.1:8000/api/subscribe/', {
        email: email
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
    getSubscribeList () {
      axios.get('http://127.0.0.1:8000/api/getsubscribelist/', {
        headers: {
          Authorization: 'Bearer ' + sessionStorage.getItem('token'),
          'Content-Type': 'application/json'
        }
      }).then(res => {
        this.subscribeList = res.data
        console.log(res)
      }).catch(err => {
        console.error(err)
      })
    },
    favor (email) {
      this.liked = !this.liked
      if (this.liked) {
        this.content = 'Followed'
        this.bg_color = '#f56c6c'
        this.ft_color = '#fef0f0'
        this.cancel(email)
      } else {
        this.content = '+follow'
        this.bg_color = '#fef0f0'
        this.ft_color = '#f56c6c'
        this.subscribe(email)
      }
      window.location.reload()
    },
    change () {
      this.bg_color = '#ff9999'
      this.ft_color = '#fef0f0'
    },
    goback () {
      if (this.liked) {
        this.bg_color = '#f56c6c'
        this.ft_color = '#fef0f0'
      } else {
        this.bg_color = '#fef0f0'
        this.ft_color = '#f56c6c'
      }
    }
  }

}
</script>
<style>
.el-card {
  width: 800px;
  margin-left: auto;
  margin-right: auto;
}

.sub-name {
  display: flex;
  font-size: 18px;
  padding: 0 0 10px 0;
}

.sub-intro {
  color: gray;
  font-size: 12px;
}

button {
  outline: none;
}

.button-sub {
  display: flex;
  justify-content: flex-end;
}

.my_button {
  color: #f56c6c;
  background: #fef0f0;
  border: #fbc4c4 solid;
  border-radius: 20px;
  padding: 12px 23px;
  text-align: center;
  font-size: 16px;
  -webkit-transform: scale(0.7);
}
</style>
