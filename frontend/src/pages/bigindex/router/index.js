import Vue from 'vue'
import Router from 'vue-router'
import menus from '@/config/bigindex-menu-config'

Vue.use(Router)

var routes = []

menus.forEach((item) => {
  routes.push({
    path: `/${item.componentName}`,
    name: item.componentName,
    component: () => import(`@/components/bigindex/${item.componentName}`)
  })
})

routes.push({
  path: `/`,
  name: 'App',
  component: () => import(`../App`),
  redirect: '/bigindex'
})

export default new Router({
  routes })
