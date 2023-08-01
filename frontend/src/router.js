import Vue from 'vue'
import Router from 'vue-router'
import HomePage from './components/HomePage.vue'
import CreateTracker from './components/CreateTracker.vue'
import UpdateTracker from './components/UpdateTracker.vue'
import TrackerLogs from './components/TrackerLogs.vue'
import CreateLog from './components/CreateLog.vue'
import LoginPage from './components/LoginPage.vue'
import RegisterPage from './components/RegisterPage.vue'
import UpdateLog from './components/UpdateLog.vue'
import ProfilePage from './components/ProfilePage.vue'

Vue.use(Router)

export default new Router({
    mode: 'history',
    routes: [
        { path: '/', redirect: '/login' },
        { path: '/login', component: LoginPage, name: 'login' },
        { path: '/register', component: RegisterPage, name: 'register' },
        { path: '/profile', component: ProfilePage, name: 'profile' },
        { path: '/dashboard/', component: HomePage, name: 'home' },
        { path: '/tracker/create', component: CreateTracker, name: 'createtracker' },
        { path: '/tracker/:tracker_id/logs', name: 'trackerlogs', component: TrackerLogs, props: true },
        { path: '/tracker/:tracker_id/logs/create', component: CreateLog, name: 'createlog', props: true },
        { path: '/tracker/:tracker_id/update', component: UpdateTracker, name: 'updatetracker', props: true },
        { path: '/tracker/:tracker_id/logs/:log_id/update', component: UpdateLog, name: 'updatelog', props: true },

    ]
})

