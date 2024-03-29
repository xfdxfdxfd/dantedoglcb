import { createRouter, createWebHistory } from 'vue-router'
import Home from '/src/views/Home.vue'
import Changelog from '/src/views/Changelog.vue'
import UptieCalculator from '/src/views/UptieCalculator.vue'
import StatusSetting from '/src/views/StatusSetting.vue'
import ExpCalculator from '/src/views/ExpCalculator.vue'
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
    },
    {
        path:'/LCB/StatusSetting',
        name:'StatusSetting',
        component:StatusSetting
    },
    {
        path:'/LCB/ExpCalculator',
        name:'ExpCalculator',
        component:ExpCalculator
    },
]   
const router = createRouter({
    history: createWebHistory(),
    routes,
})
export default router