// import Vue from 'vue'
// import Router from 'vue-router'
// // import HelloWorld from '@/components/HelloWorld'
// import AccountValue from '@/components/AccountValue'
//
// Vue.use(Router)
// //
// // export default new Router({
// //   routes: [
// //     {
// //       path: '/AccountValue',
// //       name: 'AccountValue',
// //       component: AccountValue
// //     }
// //   ]
// // })
//
// var routes = []
// routes.push({
//   path: `/AccountValue`,
//   name: AccountValue,
//   component: () => import(`@/components/AccountValue`)
// })
//
// export default new Router({ routes })

import Vue from 'vue'
import Router from 'vue-router'
import menus from '@/config/computer-menu-config'

Vue.use(Router)

var routes = []

menus.forEach((item) => {
  routes.push({
    path: `/${item.componentName}`,
    name: item.componentName,
    component: () => import(`@/components/computer/${item.componentName}`)
  })
})

routes.push({
  path: `/`,
  name: 'App',
  component: () => import(`../App`),
  redirect: '/computervalue'
})

export default new Router({
  // mode: 'history',
  routes })
