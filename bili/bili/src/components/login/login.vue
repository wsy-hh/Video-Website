<template>
  <el-container>

    <div style="display: flex; width: 80%; min-height: 80vh; margin: auto;">
      <div style="width: 60%; min-height: 80vh; display: flex; align-items: center; justify-content: center;">
        <div style="width: 80%; ">
          <div>
            <h1 style="font-size: 50px; margin: 0 0 20px 0;">Welcome to VideoWebsite!</h1>
          </div>
          <div>
            <p style="font-size: 34px;">Please log in using the email and password you used during registration. Please
              ensure that the password is entered correctly, with the correct capitalization.</p>
          </div>
        </div>

      </div>
      <div style="width: 40%; min-height: 80vh; display: flex; align-items: center; ">
        <div class="loginto_container" style="width: 60%;">
          <!-- 框内区域 -->
          <div class="loginto_box">
            <!-- <div class="avatar_box">
            </div> -->
            <!-- 注册区域 -->
            <el-form ref="logintoFormRef" :model="logintoForm" :rules="addFormRules" label-width="0px"
              class="loginto_form">
              <el-form-item prop="email">
                <el-input placeholder="please input your email" v-model="logintoForm.email" class="input">
                </el-input>
              </el-form-item>

              <el-form-item prop="password">
                <el-input placeholder="please input your password" class="input" v-model="logintoForm.password"
                  type="password">
                </el-input>
              </el-form-item>
              <!-- 按钮 -->
              <el-form-item class="btns">

                <el-button type="primary" style="font-size: 18px;" @click="login">Log in</el-button>
                <el-button type="primary" style="font-size: 18px;" @click="loginto">Sign up</el-button>
                <el-button type="info" style="font-size: 18px;" @click="resetLogintoForm">Reset</el-button>
              </el-form-item>
            </el-form>
          </div>
        </div>
      </div>
    </div>
  </el-container>
</template>

<script>
import axios from 'axios'
import { Message } from 'element-ui'
export default {
  name: 'app',
  data () {
    // 验证邮箱的规则
    const checkEmail = (rule, value, cb) => {
      // 验证邮箱的正则表达式
      const regEmail = /^([a-zA-Z0-9_-])+@([a-zA-Z0-9_-])+(\.[a-zA-Z0-9_-])+/
      if (regEmail.test(value)) {
        // 合法的邮箱
        return cb()
      }

      cb(new Error('please input valid email'))
    }

    return {
      // 这是注册表单的数据绑定对象
      logintoForm: {
        email: '',
        password: ''
      },

      // 登录信息
      loginUrl: '',
      // 登录的规则对象
      addFormRules: {
        email: [
          { reqired: true, message: 'please input your email', trigger: 'blur' },
          { validator: checkEmail, trigger: 'blur' }
        ],
        password: [
          { reqired: true, message: 'please input your password', trigger: 'blur' },
          {
            min: 6,
            max: 15,
            message: 'The length of the password is between 6 and 15 characters',
            trigger: 'blur'
          }
        ]
      }
    }
  },

  methods: {
    // 点击重置按钮，重置登录表单
    resetLogintoForm () {
      // console.log(this)
      this.$refs.logintoFormRef.resetFields()
    },
    // 跳转到注册页面
    loginto () {
      // 2. 通过编程式导航跳转到登录，路由地址是 /register
      this.$router.push('/register')
    },
    login () {
      const data = this.logintoForm
      console.log(data)
      axios.post('http://127.0.0.1:8000/api/login/', data, {
        headers: {
          Authorization: 'Bearer <token>',
          'Content-Type': 'application/json'
        }
      }).then(res => {
        // 处理请求成功的响应
        console.log(res)
        if (res.data.code == 200) {
          sessionStorage.setItem('token', res.data.token)
          sessionStorage.setItem('nickname', res.data.nickname)
          Message({
            message: res.data.message,
            type: 'success'
          })
          setTimeout(() => {
            this.$router.push('/main')
          }, 1000)
        } else {
          Message({
            message: res.data.message,
            type: 'warning'
          })
        }
      })
        .catch(err => {
          // 处理请求失败的情况
          console.error(err)
        })
      console.log(this.$globalVariable)
      console.log(this.logintoForm)
    }
  }

}
</script>
<style lang="less" scoped>
/deep/ .el-input__inner {
  padding: 10px;
  height: 60px;
  font-size: 18px;
}

.el-header {
  opacity: 0.8;
  color: #eee;
  text-align: center;

}

.loginto_box {
  width: 100%;
  padding: 20px;
  border-radius: 6px;

  .avatar_box {
    border: 1px solid #eee;
    border-radius: 50%;
    height: 138px;
    width: 138px;
    padding: 8px;
    box-shadow: 0 0 10px #edd;
    position: absolute;

    left: 50%;
    transform: translate(-50%, -50%);
    background-color: #fff;

    .icon_img {
      width: 100%;
      height: 100%;
      border-radius: 50%;
      background-color: #eee;
    }

  }

  .loginto_form {
    justify-content: center;

    width: 100%;
    padding: 0 20px;
    box-sizing: border-box;
    opacity: 0.7;
  }

  .btns {
    padding-top: 8px;
    float: right;
  }

  .el-steps {
    box-sizing: border-box;
    justify-content: center;
    margin-bottom: 10px;
  }
}</style>
