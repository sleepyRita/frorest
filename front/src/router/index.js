import { createRouter, createWebHistory } from 'vue-router'
import Left from '../views/Left.vue'
import Right from '../views/Right.vue'
import Top from '../views/Top.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      components: {
        top: Top,
        left: Left,
        right: Right
      }
    }
  ]
})

export default router
