import Vue from 'vue'
import { Card, Row, Col, TableColumn, Table } from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'
import App from './App'
import router from './router'
import serverurlvaluefromjs from '@/config/serverurlvalue'

Vue.config.productionTip = false

new Vue({
  el: '#app',
  router,
  template: '<App/>',
  components: { App }
})

Vue.prototype.serviceurl = function () {
  let serviceurlvalue = serverurlvaluefromjs.serverurl
  return serviceurlvalue
}

// 从url获取disName
Vue.prototype.getQueryVariable = function (variable) {
  let query = window.location.search.substring(1)
  let vars = query.split('&')
  for (let i = 0; i < vars.length; i++) {
    let pair = vars[i].split('=')
    if (pair[0] === variable) {
      return decodeURI(pair[1])
    }
  }
  return (false)
}
// 从url获取DN,需要decode
Vue.prototype.getQueryVariabledecode = function (variable) {
  let query = window.location.search.substring(1)
  let vars = query.split('&')
  for (let i = 0; i < vars.length; i++) {
    let pair = vars[i].split('=')
    if (pair[0] === variable) {
      return decodeURIComponent(pair[1])
    }
  }
  return (false)
}
