import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import LoginView from '@/views/LoginView.vue'
import SongsView from '@/views/SongsView.vue'
import UploadSongView from '@/views/UploadSongView.vue'
import RegisterView from '@/views/RegisterView.vue'
import CreatorDashboardView from '@/views/CreatorDashboardView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    {path: '/login', component : LoginView},
    {path: '/register', component : RegisterView},
    {path: '/signup', component : RegisterView},
    {path: '/songs', component : SongsView},
    {path: '/creator-dashboard', component:CreatorDashboardView},
    {path: '/songs/upload', component : UploadSongView},
    {
      path: '/about',
      name: 'about',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/AboutView.vue'),
    },
  ],
})

export default router
