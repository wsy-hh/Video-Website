<template>
  <el-card>
    <el-container>
      <!-- header -->
      <el-header>
        <el-row :gutter="20">
          <!-- <el-col :span="8">
        <div class="top-input">
          <el-input v-model="input" placeholder="Search"></el-input>
          <el-button icon="el-icon-search"></el-button>
        </div>
          </el-col>-->
          <el-col :span="24">
            <div class="top-login">
              <el-button type="warning" @click="dialogFormVisible = true">upload</el-button>
            </div>
            <el-divider></el-divider>
          </el-col>
        </el-row>
      </el-header>
      <el-main>

        <div id="app">
          <el-card v-for="item in videoList">
            <el-row :gutter="20" style="">
              <el-col :span="6">
                <div class="con-his">
                  <div class="vedio">
                    <img :src="'http://127.0.0.1:8000/static/' + item.picture.path" width="100%" height="100%"
                      alt />
                  </div>
                </div>
              </el-col>
              <el-col :span="18">
                <div class="con-info">
                  <div class="title" style="font-size: 28px;">{{ item.title }}</div>
                  <div class="introduction" style="padding: 10px 0; font-size: 24px;">{{ item.introduction }}</div>
                  <div class="time-name" style="padding: 180px 0 0 0; font-size: 24px;">
                    <div class="time">{{ item.create_time }}</div>
                    <div class="name">{{ item.user.nickname }}</div>
                  </div>
                </div>
              </el-col>
            </el-row>
          </el-card>
        </div>
      </el-main>
    </el-container>
    <!--上传视频 -->
    <el-dialog title="Upload video" :visible.sync="dialogFormVisible">
      <el-steps :active="active" finish-status="success">
        <el-step title="step 1" icon="el-icon-upload"></el-step>
        <el-step title="step 2" icon="el-icon-edit"></el-step>
      </el-steps>
      <!-- 上传视频步骤一 -->
      <div v-if="active === 0"
        style="width: 60%; height: 200px; margin: 20px auto; display: flex; align-items: center; justify-content: center; border: 1px dotted black;">
        <div style="text-align: center;" @dragenter="dragEnter" @dragover="dragOver" @dragleave="dragLeave" @drop="drop">
          <img style="display: block; margin: auto; margin-bottom: 20px;" width="90px" height="45px"
            src="../../assets/WX20230610-122234@2x.png" alt />
          <div v-if="status == 0"><span @click="openFilePicker" style="cursor: pointer; color:steelblue;">upload
              file</span>
          </div>
          <div v-else>{{ file_name }}</div>
        </div>
      </div>

      <!-- 上传视频步骤二 -->
      <div v-if="active === 1">
        <el-form ref="form" :model="form" label-width="100px" style="margin:20px">
          <!-- 标题 -->
          <el-form-item label="Title">
            <el-input v-model="form.title"></el-input>
          </el-form-item>
          <!-- 标签 -->

          <el-form-item label="Tag1">
            <el-checkbox-group v-model="checkList">
              <el-checkbox v-for="item in labelList" :label="item.name" name="type"></el-checkbox>
            </el-checkbox-group>
          </el-form-item>
          <!-- 封面 -->
          <el-form-item label="Image">
            <el-button type="primary" @click="openPicturePicker">select Cover image</el-button>
            <div style="margin: 5px 0;"><img :src="'http://127.0.0.1:8000/static/' + picture_path" alt=""></div>
          </el-form-item>
          <!-- 介绍 -->
          <el-form-item label="Introduction">
            <el-input type="textarea" v-model="form.introduction"></el-input>
          </el-form-item>
        </el-form>
      </div>

      <div slot="footer" class="dialog-footer">
        <el-button @click="cancel">Cancel</el-button>
        <el-button @click="previous" v-if="active === 1">Previous</el-button>
        <el-button type="primary" v-if="active === 0" @click="submit">Next</el-button>
        <el-button type="primary" v-if="active === 1" @click="submit">Submit</el-button>

      </div>
    </el-dialog>
  </el-card>
</template>

<script>
import { Message } from 'element-ui'
import axios from 'axios'
export default {
  data () {
    return {
      // 上传步骤
      active: 0,
      disabled: true,
      // 上传封面
      fileList: [],
      // 上传细节数据
      form: {
        title: '',
        introduction: ''
      },
      // 标签
      dynamicTags: [],
      inputVisible: false,
      inputValue: '',
      dialogTableVisible: false,
      dialogFormVisible: false,
      videoForm: {
        storageurl: '' // 视频地址
      },
      dragging: false,
      formLabelWidth: '100px',
      file_name: '',
      status: 0,
      checkList: [],
      labelList: [],
      picture_path: '',
      videoList: []
    }
  },
  mounted () {
    this.getVideoList()
    this.getLabelList()
  },
  methods: {
    getVideoList () {
      axios.post('http://127.0.0.1:8000/api/getuploadvideolist/', {}, {
        headers: {
          Authorization: 'Bearer ' + sessionStorage.getItem('token'),
          'Content-Type': 'application/json'
        }
      }).then(res => {
        // 处理请求成功的响应
        console.log(res)
        this.videoList = res.data
      })
        .catch(err => {
          // 处理请求失败的情况
          console.error(err)
        })
    },
    uploadImage (formData, filename) {
      axios.post('http://127.0.0.1:8000/api/uploadfile/', formData, {
        headers: {
          'Content-Type': 'image/png',
          'Content-Disposition': `attachment; filename="${filename}"`

        }
      }).then(res => {
        console.log(res)
        this.picture_path = res.data.file_name
        if (res.data.code == 200) {
          this.status = 1
          Message({
            message: res.data.message,
            type: 'success'
          })
        }
      }).catch(err => {
        console.error(err)
      })
    },
    upload (formData, filename) {
      axios.post('http://127.0.0.1:8000/api/uploadfile/', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
          'Content-Disposition': `attachment; filename="${filename}"`

        }
      }).then(res => {
        console.log(res)
        this.file_name = res.data.file_name
        if (res.data.code == 200) {
          this.status = 1
          Message({
            message: res.data.message,
            type: 'success'
          })
        }
      }).catch(err => {
        console.error(err)
      })
    },
    openPicturePicker () {
      // 创建一个隐藏的<input>元素
      const input = document.createElement('input')
      input.type = 'file'
      input.style.display = 'none'
      // 添加change事件监听器
      input.addEventListener('change', this.handlePictureUpload)
      // 将<input>元素添加到DOM中
      document.body.appendChild(input)
      // 触发文件选择对话框
      input.click()
    },
    handlePictureUpload (event) {
      const file = event.target.files[0]
      console.log(file)
      // 在这里可以处理上传文件的逻辑，例如使用FormData对象发送到服务器
      // 可以使用axios或其他库来发送POST请求
      const formData = new FormData()
      formData.append('file', file)
      this.uploadImage(formData, file.name)
    },
    handleFileUpload (event) {
      const file = event.target.files[0]
      console.log(file)
      // 在这里可以处理上传文件的逻辑，例如使用FormData对象发送到服务器
      // 可以使用axios或其他库来发送POST请求
      const formData = new FormData()
      formData.append('file', file)
      this.upload(formData, file.name)
      // 发送请求...
      // axios.post('/upload', formData, ...)
    },
    openFilePicker () {
      // 创建一个隐藏的<input>元素
      const input = document.createElement('input')
      input.type = 'file'
      input.style.display = 'none'
      // 添加change事件监听器
      input.addEventListener('change', this.handleFileUpload)
      // 将<input>元素添加到DOM中
      document.body.appendChild(input)
      // 触发文件选择对话框
      input.click()
    },
    handleFileUpload (event) {
      const file = event.target.files[0]
      console.log(file)
      // 在这里可以处理上传文件的逻辑，例如使用FormData对象发送到服务器
      // 可以使用axios或其他库来发送POST请求
      const formData = new FormData()
      formData.append('file', file)
      this.upload(formData, file.name)
      // 发送请求...
      // axios.post('/upload', formData, ...)
    },
    getLabelList () {
      axios.get('http://127.0.0.1:8000/api/labels/', {
        headers: {
          Authorization: 'Bearer ' + sessionStorage.getItem('token'),
          'Content-Type': 'application/json'
        }
      }).then(res => {
        // 处理请求成功的响应
        console.log(res)
        this.labelList = res.data
      })
        .catch(err => {
          // 处理请求失败的情况
          console.error(err)
        })
    },
    // cancel
    cancel () {
      this.active = 0
      this.dialogFormVisible = false
    },
    // previous
    previous () {
      this.active = 0
    },
    // 点击下一步及提交
    submit () {
      // this.dialogFormVisible = false
      if (this.active == 1) {
        const data = {
          file_path: this.file_name,
          picture_path: this.picture_path,
          introduction: this.form.introduction,
          title: this.form.title,
          tags: this.checkList
        }
        console.log(data)

        axios.post('http://127.0.0.1:8000/api/addvideo/', data, {
          headers: {
            Authorization: 'Bearer ' + sessionStorage.getItem('token'),
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
              location.reload()
            }, 1000)
          }
          // this.labelList = res.data
        })
          .catch(err => {
            // 处理请求失败的情况
            console.error(err)
          })
      }
      this.active++
      // if (this.active++ > 2) this.active = 0;
    },
    // 上传封面
    handleRemove (file, fileList) {
      console.log(file, fileList)
    },
    handlePreview (file) {
      console.log(file)
    },
    // //标签
    // handleClose(tag) {
    //   this.dynamicTags.splice(this.dynamicTags.indexOf(tag), 1);
    // },

    showInput () {
      this.inputVisible = true
      this.$nextTick(_ => {
        this.$refs.saveTagInput.$refs.input.focus()
      })
    },

    // handleInputConfirm() {
    //   let inputValue = this.inputValue;
    //   if (inputValue) {
    //     this.dynamicTags.push(inputValue);
    //   }
    //   this.inputVisible = false;
    //   this.inputValue = '';
    // },

    update () { },

    dragEnter (event) {
      event.preventDefault()
      this.dragging = true
    },
    dragOver (event) {
      event.preventDefault()
    },
    dragLeave () {
      this.dragging = false
    },
    drop (event) {
      event.preventDefault()
      this.dragging = false
      const files = event.dataTransfer.files
      this.uploadFiles(files)
    }
  }
}
</script>
<style lang="less" scoped>
.el-header {
  margin: 20px;
}

.drop-area {
  width: 200px;
  height: 200px;
  border: 2px dashed gray;
  text-align: center;
}

.el-row {
  margin-bottom: 20px;

  &:last-child {
    margin-bottom: 0;
  }
}

h1 {
  color: black;
}

.el-avatar {
  display: flex;
  align-items: center;
  margin-top: 10px;
}

.el-input {
  width: 400px;
}

.top-input {
  display: flex;
  align-items: center;
  justify-content: center;
}

.top-login {
  display: flex;
  justify-content: flex-end;
  margin-top: 15px;
}

.el-card {
  width: 100%;
}

// 上传视频
.avatar-uploader-icon {
  border: 1px dashed #d9d9d9 !important;
}

.avatar-uploader .el-upload {
  border: 1px dashed #d9d9d9 !important;
  border-radius: 6px !important;
  position: relative !important;
  overflow: hidden !important;
}

.avatar-uploader .el-upload:hover {
  border: 1px dashed #d9d9d9 !important;
  border-color: #409eff;
}

.avatar-uploader-icon {
  font-size: 28px;
  color: #8c939d;
  width: 300px;
  height: 178px;
  line-height: 178px;
  text-align: center;
}

.avatar {
  width: 300px;
  height: 178px;
  display: block;
}

// 标签
.el-tag+.el-tag {
  margin-left: 10px;
}

.button-new-tag {
  margin-left: 10px;
  height: 32px;
  line-height: 30px;
  padding-top: 0;
  padding-bottom: 0;
}

.input-new-tag {
  width: 90px;
  margin-left: 10px;
  vertical-align: bottom;
}
</style>
