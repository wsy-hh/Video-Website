<template>
  <div class="card-list">

    <!-- 楼层内容 -->
    <div class="storey-content">
      <div
        class="s-c-item"
        v-for="(item, i) in maindataItem"
        :key="i"
        @click="jumpPath(item.title)"
      >
        <!-- 图片 -->
        <div class="item-pic">
          <!-- 3.图片懒加载修改img :src -> v-lazy -->
          <img v-lazy="item.pic" alt="" />
        </div>
        <!-- 标题 -->
        <div class="item-title">
          <a href="#">{{ item.title }}</a>
        </div>
        <!-- up主 -->
        <div class="item-up">
          <a href="#">
            {{ item.name }}
          </a>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'CardList',
  props: {
    maindataItem: {
      type: Array,
      default () {
        return []
      }
    },
    mdnameItem: {
      type: String,
      default: ''
    }
  },
  data () {
    return {}
  },
  created () {},
  mouthed () {
    this.getName()
  },

  methods: {
    // 获取标题名字
    getName () {
      // 如果 this.maindataItem 里面有 tname 这个属性就 return ture取反(false)
      // every() 如果数组中检测到有一个元素不满足，则整个表达式返回 false ，且剩余的元素不会再进行检测。
      if (this.maindataItem.every((item) => !('tname' in item))) {
        return
      }
      return this.maindataItem[0].tname
    },

    // 点击跳转
    jumpPath (keyword) {
      this.$router.push(`/search?keyword=${keyword}`)
    }
  }
}
</script>

<style scoped>
.card-list {
  width: 100%;
  font: 12px Helvetica Neue, Helvetica, Arial, Microsoft Yahei, Hiragino Sans GB,
    Heiti SC, WenQuanYi Micro Hei, sans-serif;
}

/* 楼层内容区域 */
.storey-content {
  display: flex;
  justify-content: space-between;
  flex-wrap: wrap;
}
.s-c-item {
  width: 19%;
  margin-bottom: 10px;
}
.item-pic {
  position: relative;
  width: 100%;
  max-height: 116px;
  border-radius: 5px;
  overflow: hidden;
  /* box-shadow: 0 0 5px rgba(0, 0, 0, 0.2); */
}
.item-pic img {
  display: block;
  width: 100%;
}
.item-pic .count {
  position: absolute;
  left: 0;
  bottom: 0;
  font-size: 12px;
  padding: 3px 5px;
  color: #fff;
  background-image: linear-gradient(
    to top,
    rgba(0, 0, 0, 0.6),
    rgba(119, 119, 119, 0.1)
  );
  width: 100%;
  /* 一行显示 */
  display: -webkit-box;
  -webkit-box-orient: vertical;
  -webkit-line-clamp: 1;
  overflow: hidden;
}
.duration {
  position: absolute;
  right: 0;
  top: 0;
  padding: 3px 5px;
  color: #fff;
  background-image: linear-gradient(
    to left bottom,
    rgba(0, 0, 0, 0.6),
    rgba(255, 255, 255, 0.1)
  );
  border-bottom-left-radius: 8px;
}

.item-title {
  height: 21%;
  margin-top: 5px;
  margin-bottom: 10px;
  font-size: 14px;
  /* 两行显示 */
  display: -webkit-box;
  -webkit-box-orient: vertical;
  -webkit-line-clamp: 2;
  overflow: hidden;
  color: #4d4d4d;
}
.item-up {
  padding-left: 5px;
}
.item-up a {
  font-size: 12px;
  color: #999;
}
</style>
