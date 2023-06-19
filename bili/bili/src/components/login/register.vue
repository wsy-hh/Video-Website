<template>
  <el-container>

    <div style="display: flex; width: 80%; min-height: 80vh; margin: auto;">
      <div style="width: 60%; min-height: 80vh; display: flex; align-items: center; justify-content: center;">
        <div style="width: 80%; ">
          <div>
            <h1 style="font-size: 50px; margin: 0 0 20px 0;">Welcome to register an account on VideoWebsite.</h1>
          </div>
          <div>
            <p style="font-size: 34px;">Please register using the email and password you used during registration. Please
              make sure the password is entered correctly, with the correct capitalization, and ensure that the password
              is consistent in both entries. Also, ensure that the email format is correct.</p>
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

              <el-form-item style="">
                <el-input style="width: 50%; margin-right: 10%;" placeholder="First name" v-model="first_name">
                </el-input>
                <el-input style="width: 40%;" placeholder="Last name" v-model="last_name">
                </el-input>
              </el-form-item>

              <el-form-item prop="email">
                <el-input placeholder="email" v-model="logintoForm.email"></el-input>
              </el-form-item>
              <el-form-item prop="password">
                <el-input placeholder="password" v-model="logintoForm.pwd" type="password"></el-input>
              </el-form-item>
              <!-- <el-form-item prop="password2">
                <el-input placeholder="password2" v-model="password2" type="password"></el-input>
              </el-form-item> -->
              <el-form-item prop="phone">
                <el-input placeholder="phone number" v-model="logintoForm.phone" type="text"></el-input>
              </el-form-item>
              <!-- 按钮 -->
              <el-form-item class="btns">
                <el-button type="primary" style="font-size: 18px;" @click="loginback">Cancel</el-button>
                <el-button type="primary" style="font-size: 18px;" @click="submit">Sign up</el-button>
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
import { Message } from 'element-ui'
import axios from 'axios'
export default {
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
      first_name: '',
      last_name: '',
      // 这是注册表单的数据绑定对象
      logintoForm: {
        email: '',
        pwd: '',
        phone: ''

      },
      // 登录的规则对象
      addFormRules: {
        email: [
          { reqired: true, message: 'input email', trigger: 'blur' },
          { validator: checkEmail, trigger: 'blur' }
        ],
        pwd: [
          { reqired: true, message: 'input password', trigger: 'blur' },
          {
            min: 6,
            max: 15,
            message: 'The length of the password is between 6 and 15 characters',
            trigger: 'blur'
          }
        ]
      },
      // 注册路由
      registerUrl: ''
    }
  },
  methods: {
    // 点击重置按钮，重置注册表单
    resetLogintoForm () {
      // console.log(this)
      this.$refs.logintoFormRef.resetFields()
    },
    // 点击注册消息弹框
    submit () {
      const data = this.logintoForm
      data.nickname = this.first_name + ' ' + this.last_name
      axios.post('http://127.0.0.1:8000/api/register/', data, {
        headers: {
          Authorization: 'Bearer <token>',
          'Content-Type': 'application/json'
        }
      }).then(res => {
        // 处理请求成功的响应
        console.log(res)
        if (res.data.code == 200) {
          Message({
            message: res.data.message,
            type: 'success'
          })
          setTimeout(() => {
            this.$router.push('/main')
          }, 1000)
        } else {
          Message({
            message: 'register failed!',
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
    },

    // 点击取消
    loginback () {
      this.$router.push('/main')
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
}
</style>
