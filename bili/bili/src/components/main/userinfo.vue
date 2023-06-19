<template>
  <div>
    <el-card class="box-card" shadow="never">
      <div slot="header" class="clearfix">
        <span>Basic info</span>
        <el-button
          style="float: right; padding: 3px 0"
          type="text"
          @click="dialogFormVisible = true"
        >modify</el-button>
      </div>
      <el-row style="padding: 14px;">
        <el-col :span="8">
          <div style="font-size: 18px;">Nickname</div>
        </el-col>
        <el-col :span="16">
          <div>{{ userinfo.nickname }}</div>
        </el-col>
      </el-row>
      <el-divider></el-divider>
      <el-row style="padding: 14px;">
        <el-col :span="8">
          <div style="font-size: 18px;">Introduction</div>
        </el-col>
        <el-col :span="16">
          <div>{{ userinfo.introduction }}</div>
        </el-col>
      </el-row>
      <el-divider></el-divider>
      <el-row style="padding: 14px;">
        <el-col :span="8">
          <div style="font-size: 18px;">Gender</div>
        </el-col>
        <el-col :span="16">
          <div>{{ userinfo.gender }}</div>
        </el-col>
      </el-row>
      <!-- <div class="text item">
        nickname:{{ user.username }}
      </div>
      <div class="text item">
        Gender:{{ user.username }}
      </div>
      <div class="text item">
        Introduction:{{ user.username }}
      </div>-->

      <!-- 修改信息 -->
      <el-dialog title="Modify information" :visible.sync="dialogFormVisible">
        <el-form :model="userinfo">
          <el-form-item label="Avatar" :label-width="formLabelWidth">
            <!-- 上传头像 -->
            <el-button size="small" type="primary" @click="openPicturePicker">upload</el-button>
            <!-- <div slot="tip" class="el-upload__tip">only jpg/png,less than 500kb</div> -->
            <div style="width: 80px; height: 80px; border-radius: 80px; overflow: hidden;">
              <img
                width="80px"
                height="80px"
                :src="'http://127.0.0.1:8000/static/' + userinfo.avatar"
                alt
              />
            </div>
          </el-form-item>
          <el-form-item label="Nickname" :label-width="formLabelWidth">
            <el-input v-model="userinfo.nickname" autocomplete="off"></el-input>
          </el-form-item>
          <el-form-item label="Gender" :label-width="formLabelWidth">
            <el-input v-model="userinfo.gender" autocomplete="off"></el-input>
          </el-form-item>
          <el-form-item label="Introduction" :label-width="formLabelWidth">
            <el-input v-model="userinfo.introduction" autocomplete="off" type="textarea"></el-input>
          </el-form-item>
        </el-form>
        <div slot="footer" class="dialog-footer">
          <el-button @click="dialogFormVisible = false">cancel</el-button>
          <el-button type="primary" @click="update">Update</el-button>
        </div>
      </el-dialog>
    </el-card>

    <el-card class="box-card" shadow="never" style="margin-top: 40px;">
      <div slot="header" class="clearfix">
        <span>Contact info</span>
      </div>
      <el-row style="padding: 14px;">
        <el-col :span="8">
          <div style="font-size: 18px;">Email</div>
        </el-col>
        <el-col :span="16">
          <div>{{ userinfo.email }}</div>
        </el-col>
      </el-row>
      <el-divider></el-divider>
      <el-row style="padding: 14px;">
        <el-col :span="8">
          <div style="font-size: 18px;">Phone</div>
        </el-col>
        <el-col :span="16">
          <div>{{ userinfo.phone }}</div>
        </el-col>
      </el-row>
    </el-card>
  </div>
</template>

<script>
import axios from "axios";
import { Message } from "element-ui";
export default {
  data() {
    return {
      // 上传头像
      fileList: [],
      userinfo: {},
      user: {
        username: "user",
        introduction:
          "hello everyone, my name is qixuan huang. welcome to my channel",
        phone: "148206516",
        email: "tma3919@163.com"
      },
      dialogTableVisible: false,
      dialogFormVisible: false,
      form: {
        name: "",
        gender: "",
        introduction: ""
      },
      formLabelWidth: "100px",
      picture_path: ""
    };
  },
  mounted() {
    this.getUserInfo();
  },
  methods: {
    // 共享数据
    sendDataToSecondPage() {
      // 通过dispatch action来修改共享数据
      this.$store.dispatch("updateSharedData", "Hello from Page 1");
    },
    update() {
      axios
        .post("http://127.0.0.1:8000/api/updateuserinfo/", this.userinfo, {
          headers: {
            Authorization: "Bearer " + sessionStorage.getItem("token"),
            "Content-Type": "application/json"
          }
        })
        .then(res => {
          console.log(res);
          if (res.data.code == 200) {
            this.status = 1;
            setTimeout(() => {
              location.reload();
            }, 1000);
            Message({
              message: res.data.message,
              type: "success"
            });
          }
        })
        .catch(err => {
          console.error(err);
        });
    },

    openPicturePicker() {
      // 创建一个隐藏的<input>元素
      const input = document.createElement("input");
      input.type = "file";
      input.style.display = "none";
      // 添加change事件监听器
      input.addEventListener("change", this.handlePictureUpload);
      // 将<input>元素添加到DOM中
      document.body.appendChild(input);
      // 触发文件选择对话框
      input.click();
    },
    handlePictureUpload(event) {
      const file = event.target.files[0];
      console.log(file);
      // 在这里可以处理上传文件的逻辑，例如使用FormData对象发送到服务器
      // 可以使用axios或其他库来发送POST请求
      const formData = new FormData();
      formData.append("file", file);
      this.uploadImage(formData, file.name);
    },
    uploadImage(formData, filename) {
      axios
        .post("http://127.0.0.1:8000/api/uploadfile/", formData, {
          headers: {
            "Content-Type": "image/png",
            "Content-Disposition": `attachment; filename="${filename}"`
          }
        })
        .then(res => {
          console.log(res);
          this.userinfo.avatar = res.data.file_name;

          if (res.data.code == 200) {
            this.status = 1;
            Message({
              message: res.data.message,
              type: "success"
            });
            // 共享头像
          }
        })
        .catch(err => {
          console.error(err);
        });
    },
    // 上传文件
    handleRemove(file, fileList) {
      console.log(file, fileList);
    },
    handlePreview(file) {
      console.log(file);
    },
    getUserInfo() {
      axios
        .get("http://127.0.0.1:8000/api/getuserinfo/", {
          headers: {
            Authorization: "Bearer " + sessionStorage.getItem("token"),
            "Content-Type": "application/json"
          }
        })
        .then(res => {
          // 处理请求成功的响应
          this.userinfo = res.data;
          console.log(res);
          this.$store.dispatch("updateSharedData", res.data.avatar);
        })
        .catch(err => {
          // 处理请求失败的情况
          console.error(err);
        });
    }
  }
};
</script>

<style scoped>
* {
  font-size: 22px;
  font-family: "Google Sans", Roboto, Arial, sans-serif;
}

.text {
  font-size: 22px;
}

.item {
  margin-bottom: 18px;
}

.clearfix:before,
.clearfix:after {
  display: table;
  content: "";
}

.clearfix:after {
  clear: both;
}

.box-card {
  width: 80%;
}

/* 上传头像 */

.avatar-uploader .el-upload {
  border: 1px dashed #d9d9d9;
  border-radius: 6px;
  cursor: pointer;
  position: relative;
  overflow: hidden;
}

.avatar-uploader .el-upload:hover {
  border-color: #409eff;
}

.avatar-uploader-icon {
  font-size: 28px;
  color: #8c939d;
  width: 178px;
  height: 178px;
  line-height: 178px;
  text-align: center;
}

.avatar {
  width: 178px;
  height: 178px;
  display: block;
}
</style>
