<template>
      <el-menu
        class="el-menu-vertical-demo"
        router
        unique-opened
        @open="handleOpen"
        @close="handleClose">
          <el-menu-item-group class="over-hide" v-for="sub in menu" :key="sub.componentName">
            <el-menu-item :index="sub.componentName" v-text="sub.name" :address.sync="sub.name">
            </el-menu-item>
          </el-menu-item-group>

      </el-menu>
</template>

<style scoped>
  .over-hide{
    overflow: hidden;
  }
  .el-menu-vertical-demo:not(.el-menu--collapse)  {
    height:calc(100vh - 60px)
  }
</style>

<script>
import menu from '@/config/contact-menu-config'
import axios from 'axios'
import serverurlvaluefromjs from '@/config/serverurlvalue'

axios.defaults.withCredentials = true
// 本地服务器地址
function serviceurl () {
  // 正式环境value值取空
  // let serviceurlvalue = ''
  let serviceurlvalue = serverurlvaluefromjs.serverurl
  return serviceurlvalue
}
export default {
  data () {
    return {
      menu: menu
    }
  },
  created () {
    axios
      .get(serviceurl() + '/getExissconfig/')
      .then(response => {
        if (!response.data.isSuccess) {
          for (let i = 0; i < this.menu.length; i++) {
            if (this.menu[i]['componentName'] === 'contactexchangevalue') {
              this.menu.splice(i, 1)
              }
          }
        }
    })
  },
  methods: {
    handleOpen (key, keyPath) {
    },
    handleClose (key, keyPath) {
    }
  }
}
</script>
