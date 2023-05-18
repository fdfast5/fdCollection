import { createRouter, createWebHashHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import Auth from '@/components/pages/Auth'
import CollectionAdmin from '@/components/pages/CollectionAdmin'
import UserLogin from '@/components/pages/UserLogin'
import CollectionList from '@/components/pages/CollectionList'

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  {
    path: '/auth',
    name: 'Auth',
    component: Auth
  },
  {
    path: '/collectionadmin',
    name: 'CollectionAdmin',
    component: CollectionAdmin
  },
  {
    path: '/login',
    name: 'Login',
    component: UserLogin
  },
  {
    path: '/collectionlist',
    name: 'CollectionList',
    component: CollectionList
  },
  {
    path: '/about',
    name: 'about',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/AboutView.vue')
  }
]

const router = createRouter({
  history: createWebHashHistory(),
  routes
})

export default router
