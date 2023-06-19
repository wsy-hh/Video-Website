<template>
  <div id="app">
    <div class="b-wrap">
      <!-- 视频内容 -->
      <div v-show="mainDataYes">
        <div class="video-list">
          <video-item
            class="main-data-item"
            :class="currentIndex == index ? 'item-hover' : ''"
            v-for="(item, index) in mainDataList"
            :key="index"
            :main-data="item"
            @mouseenter.native="enter(index)"
            @mouseleave.native="leave()"
          ></video-item>
        </div>
        <!-- 分页功能 -->
        <el-pagination
          :background="true"
          layout="prev, pager, next"
          @current-change="handleCurrentChange"
          :current-page="currentPage"
          :total="500"
        >
        </el-pagination>
      </div>

    </div>
  </div>
</template>

<script>
// 组件
import VideoItem from '../common/videoitem/VideoItem'

export default {
  name: 'app',
  components: {
    VideoItem
  },
  data () {
    return {

      // 主要内容数据
      mainDataList: [],
      mainDataListCopy: [],
      // 判断是否有数据 显示没有数据图片
      mainDataYes: true,
      // 鼠标移进的当前item
      currentIndex: null,

      // 当前页码
      currentPage: 1

    }
  },
  mounted () {},
  methods: {
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
