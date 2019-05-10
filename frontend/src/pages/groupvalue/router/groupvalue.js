
import Vue from 'vue'
import Router from 'vue-router'
import menus from '@/config/group-menu-config'

Vue.use(Router)

var routes = []

menus.forEach((item) => {
  routes.push({
    path: `/${item.componentName}`,
    name: item.componentName,
    component: () => import(`@/components/group/${item.componentName}`)
    // component: () => import(`../../../components/${item.componentName}`)
  })
})

routes.push({
  path: `/`,
  name: 'groupsearch',
  component: () => import(`../App`),
  redirect: '/groupvalue'
})

export default new Router({
  // mode: 'history',
  routes })
