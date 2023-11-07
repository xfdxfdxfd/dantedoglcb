import { createRouter, createWebHistory } from 'vue-router'
import Home from '/src/views/Home.vue'
import Changelog from '/src/views/Changelog.vue'
import UptieCalculator from '/src/views/UptieCalculator.vue'
const routes = [
    {
        path:'/',
        name:'Home',
        component:Home
    },
    {
        path:'/LCB/Changelog',
        name:'Changelog',
        component:Changelog
    },
    {
        path:'/LCB/UptieCalculator',
        name:'UptieCalculator',
        component:UptieCalculator
    }
]   
const router = createRouter({
    history: createWebHistory(),
    routes,
})
export default router