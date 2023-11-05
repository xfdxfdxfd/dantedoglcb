import { createRouter, createWebHistory } from 'vue-router'
import Home from '/src/views/Home.vue'
import About from '/src/views/About.vue'
import Thread from '/src/views/Thread.vue'
const routes = [
    {
        path:'/',
        name:'Home',
        component:Home
    },
    {
        path:'/LCB/About',
        name:'About',
        component:About
    },
    {
        path:'/LCB/Thread',
        name:'Thread',
        component:Thread
    }
]   
const router = createRouter({
    history: createWebHistory(),
    routes,
})
export default router