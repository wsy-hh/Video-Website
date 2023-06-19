// import Vue from 'vue'
// import Vuex from 'vuex'

// Vue.use(Vuex)

// export default new Vuex.Store({
//   state: {
//   },
//   getters: {
//   },
//   mutations: {
//   },
//   actions: {
//   },
//   modules: {
//   }
// })

// vuex
import Vue from 'vue';
import Vuex from 'vuex';

Vue.use(Vuex);

const store = new Vuex.Store({
  state: {
    // 在这里定义共享的数据
    sharedData: ''
  },
  mutations: {
    // 定义修改共享数据的方法
    setSharedData(state, data) {
      state.sharedData = data;
    }
  },
  actions: {
    // 定义触发mutation的actions
    updateSharedData({ commit }, data) {
      commit('setSharedData', data);
    }
  },
  getters: {
    // 定义获取共享数据的getter
    getSharedData: state => state.sharedData
  }
});

export default store;
