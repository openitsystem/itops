import Vue from 'vue'
import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'
import App from './App'
import router from './router'
import serverurlvaluefromjs from '@/config/serverurlvalue'

Vue.config.productionTip = false

Vue.use(ElementUI)
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
