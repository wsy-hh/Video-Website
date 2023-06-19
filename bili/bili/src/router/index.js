import Vue from 'vue'
import VueRouter from 'vue-router'
import Index from '../components'
import Login from '../components/login/login.vue'
import Main from '../components/main/main.vue'
import History from '../components/main/history.vue'
import Subscription from '../components/main/subscription.vue'
import Collection from '../components/main/collection.vue'
import Register from '../components/login/register.vue'
import Search from '../components/main/search.vue'
import Radio from '../components/main/radio.vue'
import Person from '../components/main/person'
import Userinfo from '../components/main/userinfo.vue'
import Userradio from '../components/main/userradio.vue'
import Userradioinfo from '../components/main/userradioinfo.vue'

Vue.use(VueRouter)

const routes = [
  { path: '/', redirect: '/index' },

  {
    path: '/index',
    component: Index,
    redirect: '/main',
    children: [
      { path: '/main', component: Main },
      { path: '/login', component: Login },
      { path: '/register', component: Register },
      { path: '/history', component: History },
      { path: '/subscription', component: Subscription },
      { path: '/collection', component: Collection },
      { path: '/search', component: Search },
      { path: '/radio', component: Radio },
      { path: '/userradioinfo', component: Userradio },
      { path: '/userradio', component: Userradio },
      {
        path: '/person',
        component: Person,
        redirect: '/userinfo',
        children: [
          { path: '/userinfo', component: Userinfo }
        ]
      }
    ]
  }

]

const router = new VueRouter({
  routes
})

export default router
