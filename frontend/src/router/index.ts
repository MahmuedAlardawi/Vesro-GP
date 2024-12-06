import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router'
import HomeView from '@/views/HomeView.vue'
import AboutView from '@/views/AboutView.vue'
import documentation from '@/views/DocumentationView.vue'
import poemExplanation from '@/views/PoemExplanationView.vue'


const routes: Array<RouteRecordRaw> = [
  {path: '/', name: 'home', component: HomeView},
  {path: '/about', name: 'about', component: AboutView},
  {path: '/documentation', name: 'documentation', component: documentation},
  {path: '/poemExplanation', name: 'poemExplanation', component: poemExplanation},
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
