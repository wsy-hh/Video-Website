<template>
  <div style="background-color: white; margin:20px auto" class="main-contain">

    <el-container style="height: 80vh;width: 80%; margin: auto; border: 1px solid #eee;">
      <el-aside width="300px" style="margin-top: 1%">
        <div style="width: 190px;background-color: white;padding: 5px;margin: auto">
          <img v-bind:src="'http://127.0.0.1:8000/static/'+sharedData" width="150px" height="150px" style="border-radius: 300px;margin-left: 8%">
        </div>

        <br>
        <br>
        <el-menu :default-openeds="['1', '2']">
          <el-submenu index="1">
            <template slot="title"><i class="el-icon-message"></i>Information</template>
            <el-menu-item-group>

              <router-link class="alink" to="/userinfo"><el-menu-item index="1-1">Personal
                  information</el-menu-item></router-link>
              <router-link class="alink" to="/subscription"><el-menu-item
                  index="1-2">Subscription</el-menu-item></router-link>
              <router-link class="alink" to="/history"><el-menu-item index="1-3">History</el-menu-item></router-link>
            </el-menu-item-group>

          </el-submenu>
          <el-submenu index="2">
            <template slot="title"><i class="el-icon-menu"></i>Video</template>
            <el-menu-item-group>
              <router-link class="alink" to="/userradio"><el-menu-item index="2-1">Personal
                  Video</el-menu-item></router-link>

            </el-menu-item-group>

          </el-submenu>

        </el-menu>
      </el-aside>

      <el-container style="background-color: white">
        <el-main>
          <router-view />
        </el-main>
      </el-container>

    </el-container>

  </div>
</template>

<script>
export default {

  // 必须登录才能访问此页面
  //   beforeRouteEnter: (to, from, next) => {
  //     console.log("准备进入个人信息页");
  //     let islogin = sessionStorage.getItem("isLogin")
  //     if(!islogin){
  //       next({path:'/login'});
  //     }
  //     next();
  //   },

  data () {
    return {
      user: {
        // userpic: 'https://fuss10.elemecdn.com/3/63/4e7f3a15429bfda99bce42a18cdd1jpeg.jpeg?imageMogr2/thumbnail/360x360/format/webp/quality/100',
        userpic: '',
        username: 'user'
      }
    }
  },
  computed: {
    // 使用getter获取共享数据
    sharedData() {
      return this.$store.getters.getSharedData;

    }
  }

}
</script>

<style scoped>
.el-header {
  background-color: #B3C0D1;
  color: #333;
  line-height: 60px;
}

.el-aside {
  color: #333;
}

.alink {

  text-decoration: none;
}

.main-contain {
  width: 70%;
  display: flex;
  justify-content: center;
}

* {
  font-size: 18px;
}
</style>
