<template>
  <div id="app">
    <div class="topradio">
      <el-row :gutter="20">
        <el-col :span="12">
          <!-- 轮播图 -->
          <div class="lunbo">
            <el-carousel height="69vh">
              <el-carousel-item v-for="item in bannerList">
                <img :src="'http://127.0.0.1:8000/static/' + item.video.picture.path" @click="navToVideo(item)"
                  style="cursor: pointer;" class="lunbopic" alt />
                <h3>{{ item.title }}</h3>
              </el-carousel-item>
            </el-carousel>
          </div>
        </el-col>
        <el-col :span="12">
          <!-- 轮播图右侧 -->
          <div class="six">
            <el-row :gutter="20">
              <el-col :span="8" v-for="item in recommandList">
                <!-- 楼层内容 -->
                <div class="right" @click="navToVideo(item)" style="cursor: pointer;">
                  <div class="pic">
                    <img class="rigpic" :src="'http://127.0.0.1:8000/static/' + item.video.picture.path" alt />
                  </div>
                  <div class="rititle" font-size="12px">{{ item.video.title }}</div>
                  <div class="author">{{ item.video.user.nickname }}</div>
                </div>
              </el-col>
            </el-row>
          </div>
        </el-col>
      </el-row>
    </div>
    <div class="tag">
      <el-tag v-for="item in labelList" class="tag-detail" :type="item.id === label_id_confirm ? 'success' : 'info'"  @click="changeTag(item.id)">{{
        item.name }}</el-tag>
    </div>
    <div class="bottomradio">
      <el-row :gutter="20">
        <el-col :span="4" v-for="item in LabelVideoList">
          <div class="right" @click="navToLabelVideo(item)" style="cursor: pointer;">
            <div class="pic">
              <img class="rigpic" :src="'http://127.0.0.1:8000/static/' + item.picture.path" alt />
            </div>
            <div class="rititle">{{ item.title }}</div>
            <div class="author">{{ item.user.nickname }}</div>
          </div>
        </el-col>
      </el-row>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
export default {
  name: 'app',

  data () {
    return {
      // 轮播图数据
      label_id_confirm: 1,
      label_type: 'info',
      lable_selected_type: 'success',
      bannerList: [],
      recommandList: [],
      pic: [{ text: 1 }, { text: 2 }, { text: 3 }, { text: 4 }],

      // 轮播图右边数据
      rightinfo: [
        {
          id: 1,
          title: '房主依据美国“城堡法”，拒绝让警员进入房屋！E130',
          author: '紧疾出击',
          create_time: '2023-06-09 17:00:00',
          img_url:
            'https://shadow.elemecdn.com/app/element/hamburger.9cf7b091-55e9-11e9-a976-7f4d0b07eef6.png',
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
        },
        {
          id: 4,
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
        },
        {
          id: 4,
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
        },
        {
          id: 4,
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

      rainfo: [
        {
          id: 1,
          title: '房主依据美国“城堡法”，拒绝让警员进入房屋！E130',
          author: '紧疾出击',
          create_time: '2023-06-09 17:00:00',
          img_url:
            'https://shadow.elemecdn.com/app/element/hamburger.9cf7b091-55e9-11e9-a976-7f4d0b07eef6.png',
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
        },
        {
          id: 4,
          title: '房主依据美国“城堡法”，拒绝让警员进入房屋！E130',
          author: '紧疾出击',
          create_time: '2023-06-09 17:00:00',
          img_url: '../../assets/recommand-card.jpg',
          link: 'https://www.google.com'
        },
        {
          id: 4,
          title: '房主依据美国“城堡法”，拒绝让警员进入房屋！E130',
          author: '紧疾出击',
          create_time: '2023-06-09 17:00:00',
          img_url: '../../assets/recommand-card.jpg',
          link: 'https://www.google.com'
        },
        {
          id: 4,
          title: '房主依据美国“城堡法”，拒绝让警员进入房屋！E130',
          author: '紧疾出击',
          create_time: '2023-06-09 17:00:00',
          img_url: '../../assets/recommand-card.jpg',
          link: 'https://www.google.com'
        }
      ],
      labelList: [],
      LabelVideoList: []
    }
  },

  methods: {
    changeTag (e) {
      console.log(e)
      this.label_id_confirm = e
      this.getLableVideoList(e)
    },
    navToVideo (item) {
      console.log(item)
      localStorage.removeItem('video')
      localStorage.setItem('video', JSON.stringify(item))
      this.$router.push('/radio')
    },
    navToLabelVideo (item) {
      console.log(item)
      localStorage.removeItem('video')
      localStorage.setItem('video', JSON.stringify({ video: item }))
      this.$router.push('/radio')
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
    getLableVideoList (label_id) {
      axios.post('http://127.0.0.1:8000/api/getlabelvideolist/', {
        label_id: label_id
      }, {
        headers: {
          Authorization: 'Bearer ' + sessionStorage.getItem('token'),
          'Content-Type': 'application/json'
        }
      }).then(res => {
        console.log('video label list')
        // 处理请求成功的响应
        console.log(res.data)
        this.LabelVideoList = res.data
      })
        .catch(err => {
          // 处理请求失败的情况
          console.error(err)
        })
    },
    getBannerList () {
      axios.get('http://127.0.0.1:8000/api/getbannerlist/', {
        headers: {
          Authorization: 'Bearer ' + sessionStorage.getItem('token'),
          'Content-Type': 'application/json'
        }
      }).then(res => {
        // 处理请求成功的响应
        console.log(res)
        this.bannerList = res.data
      })
        .catch(err => {
          // 处理请求失败的情况
          console.error(err)
        })
    },
    getRecommandList () {
      axios.get('http://127.0.0.1:8000/api/getrecommandlist/', {
        headers: {
          Authorization: 'Bearer ' + sessionStorage.getItem('token'),
          'Content-Type': 'application/json'
        }
      }).then(res => {
        // 处理请求成功的响应
        console.log(res)
        this.recommandList = res.data
      })
        .catch(err => {
          // 处理请求失败的情况
          console.error(err)
        })
    }
  },
  created () {
    console.log('hello world')
    this.getLabelList()
    this.getBannerList()
    this.getRecommandList()
    this.getLableVideoList(1)
  }
}
</script>
<style>
.tag {
  width: 100%;
  padding: 10px 0;
}

.topradio {
  margin-bottom: 30px;
}

/* 轮播图 */
.el-carousel__item h3 {
  color: #475669;
  font-size: 14px;
  opacity: 0.75;
  line-height: 150px;
  margin: 0;

}

.el-carousel__item {
  overflow: hidden;
  border-radius: 5px;
}

.lunbopic {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  border-radius: 5px;
  width: auto;
  height: 130%;
}

.el-carousel__item:nth-child(2n) {
  background-color: #99a9bf;
}

.el-carousel__item:nth-child(2n + 1) {
  background-color: #d3dce6;
}

.bottomradio {
  margin-top: 30px;
}

/* 轮播图右侧 */
.pic {
  border-radius: 15px;
  overflow: hidden;
  height: calc(23vh - 85px);
}

.rigpic {
  border-radius: 5px;
  height: 25vh;

  width: auto;
  /* position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%,-50%); */

}

.rititle {
  font-size: 18px;
  box-sizing: border-box;
  padding: 5px;
  width: 100%;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  text-overflow: ellipsis;
  min-height: 52px;
  /* 两行文本的高度 */

  /* 超出两行时显示省略号 */
}

.author {
  color: gray;
  box-sizing: border-box;
  padding: 0 5px 5px 5px;
}

.right {
  margin-bottom: 5px;
}

.tag-detail {
  width: 4vw;
  height: 3vh;
  line-height: 3vh;
  text-align: center;
  margin: 0 20px;
  cursor: pointer;
}
</style>
