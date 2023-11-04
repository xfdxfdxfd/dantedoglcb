import { createRouter, createWebHistory } from 'vue-router'
import Home from '/src/views/Home.vue'
import About from '/src/views/About.vue'
const routes = [
    {
        path:'/LCB/Home',
        name:'Home',
        component:Home
    },
    {
        path:'/LCB/About',
        name:'About',
        component:About
    }
]   
const router = createRouter({
    history: createWebHistory(),
    routes,
})
export default router