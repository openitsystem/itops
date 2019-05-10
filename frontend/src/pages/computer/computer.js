import Vue from 'vue'
import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'
import 'normalize.css'
import 'vue-awesome/icons'
import Icon from 'vue-awesome/components/Icon'

import App from './App'
import router from './router'
import serverurlvaluefromjs from '@/config/serverurlvalue'
// import getCombBySum from '@/config/useraccountvalue.js'

Vue.config.productionTip = false

Vue.use(ElementUI)
Vue.component('icon', Icon)

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  template: '<App/>',
  components: { App }
})

// 本地服务器地址
Vue.prototype.serviceurl = function () {
  // 正式环境value值取空
  // let serviceurlvalue = ''
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

// alert弹窗，type：[‘success’，‘error’]
Vue.prototype.messagealertvalue = function (message, type) {
  this.$message({
    showClose: true,
    message: message,
    type: type
  })
}
