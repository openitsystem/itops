<template>
  <el-row>
    <el-col :span="24">
    <div class="head-wrap"><span @click="gobackvalue"><i class="el-icon-back" :class="classname.classSpancursorpointer"></i></span>&nbsp;&nbsp;<span v-text="displaynamevalue"></span></div>
    </el-col>
  </el-row>
</template>

<style scoped>
  .head-wrap{
  }
</style>
<style>
  /* 向右浮动 */
  .classSpanFloatRight{
      float: right;
  }
  /* 鼠标放上去显示手形 */
  .classSpancursorpointer{
      cursor: pointer;
  }
</style>
<script>
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

// 从url获取disName
function getQueryVariable (variable) {
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
export default{
  data () {
    return {
      classname: {
        classSpanFloatRight: 'classSpanFloatRight',
        classSpancursorpointer: 'classSpancursorpointer'
      },
      displaynamevalue: null
    }
  },
  created: function () {
    let disNameforurl = getQueryVariable('disName')
    axios
      .get(serviceurl() + '/api/GetGroupPreMessage/?CountName=' + disNameforurl)
      .then(response => {
        if (response.data.isSuccess) {
          this.displaynamevalue = response.data.message.cn
          this.tableData3 = [{
            date: 'displayName'
          }]
        }
      })
  },
  methods: {
    gobackvalue: function () {
      this.$router.go(-1)
    }
  }
}
</script>
