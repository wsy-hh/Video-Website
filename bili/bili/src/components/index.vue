<template>
  <el-container>
    <!-- header -->
    <el-header style=" ">
      <el-row :gutter="20" style="display: flex; align-items: center;">
        <el-col :span="3" style="display: flex; justify-content: center; align-items: center;">
          <el-avatar style="margin: 0;" :size="50" :src="circleUrl"></el-avatar>
        </el-col>
        <el-col :span="3" style="text-align: left;">
          <div class="grid-content bg-purple" @click="index" style="cursor: pointer;">
            <h1>Video Website</h1>
          </div>
        </el-col>
        <el-col :span="8">
          <div class="top-input">
            <el-input style="padding: 10px 0; width: 60%;" v-model="input" placeholder="Search"></el-input>
            <el-button icon="el-icon-search" @click="search"></el-button>
          </div>
        </el-col>
        <el-col :span="6">
          <div class="top-select">
            <el-menu :default-active="this.$router.path" style="" router class="el-menu-demo" mode="horizontal"
              active-text-color="#ffd04b">
              <el-menu-item index="/history" style="font-size: 20px; color: black;">History</el-menu-item>
              <el-menu-item index="/subscription" style="font-size: 20px; color: black;">Subscription</el-menu-item>
              <el-menu-item index="/userinfo" style="font-size: 20px; color: black;">Userinfo</el-menu-item>

            </el-menu>
          </div>
        </el-col>
        <el-col :span="4">
          <div class="top-login">
            <div v-if="status" style="display: flex; align-items: center; justify-content: center; margin: 0 20px;"> {{ nickname }} </div>
            <el-button v-if="status" type="warning" @click="logout">Log out</el-button>
            <el-button v-if="status == 0" type="warning" disabled>Log out</el-button>
            <el-button v-if="status == 0" type="warning" @click="login">Sign in</el-button>
          </div>

        </el-col>
      </el-row>
    </el-header>
    <el-main>
      <!-- 路由占位符 -->
      <router-view></router-view>
    </el-main>
  </el-container>
</template>

<script>

export default {
  watch: {
    '$route.path' (newPath, oldPath) {
      console.log('路由路径变化:', newPath, oldPath)
      if (newPath == '/main' && oldPath == '/login') {
        location.reload()
      }
      // 在这里可以执行你想要的操作
      // 例如更新数据、发送请求等
    }
  },
  data () {
    return {
      circleUrl: 'https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png',
      input: '',
      status: 0,
      token: null,
      nickname: null
    }
  },

  methods: {
    search () {
      this.$router.push('/search')
      sessionStorage.removeItem('keyword')
      sessionStorage.setItem('keyword', this.input)
    },
    login () {
      this.$router.push('/login')
    },
    index () {
      this.$router.push('/index')
    },
    logout () {
      sessionStorage.removeItem('token')
      sessionStorage.removeItem('nickname')
      this.status = 0
      this.$router.push('/index')
    }
  },

  created () {
    const token = sessionStorage.getItem('token')
    this.token = token
    console.log(token)
    const nickname = sessionStorage.getItem('nickname')
    console.log(nickname)
    this.nickname = nickname
    if (token) {
      this.status = 1
    } else {
      this.status = 0
    }
    console.log(this.status)
  }
}
</script>
<style lang="less" scoped>
* {
  padding: 0;
  margin: 0;
  font-family: "Google Sans",Roboto,Arial,sans-serif;
}

.el-header {
  margin: 20px
}

.el-row {

  margin-bottom: 20px;

  &:last-child {
    margin-bottom: 0;
  }
}

h1 {
  color: black
}

.el-avatar {
  display: flex;
  align-items: center;
  margin-top: 10px
}

.el-input {
  width: 400px
}

.top-input {}

.top-login {
  display: flex;
  justify-content: flex-end;

}</style>
