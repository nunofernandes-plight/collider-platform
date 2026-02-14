import { createRouter, createWebHistory } from 'vue-router'
import EventDisplay from '../views/EventDisplay.vue'
import AnalysisDashboard from '../views/AnalysisDashboard.vue'
import Configuration from '../views/Configuration.vue'

const routes = [
  {
    path: '/',
    name: 'EventDisplay',
    component: EventDisplay
  },
  {
    path: '/analysis',
    name: 'Analysis',
    component: AnalysisDashboard
  },
  {
    path: '/config',
    name: 'Configuration',
    component: Configuration
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
