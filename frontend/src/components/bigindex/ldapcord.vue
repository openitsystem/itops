<template>
  <div id="app1" ref="elememt" style="height: calc(100vh - 100px);width: calc(100vw -260px)">
    <iframe height="100%" width="100%" frameborder="no" :src="srcurl">
    </iframe>
  </div>
</template>

<script>
// import axios from 'axios'
// import Vue from 'vue'

export default {
  name: 'app1',
  data () {
      return {
          srcurl: ''
      }
  },
  created () {
    this.srcurl = window.location.protocol + "//" + window.location.host + "/ldapcord"
  }
}

</script>

<style>
  .header {
    /*background-color: #409EFF;*/
    /*color: #fff;*/
    line-height: 60px;
    border-bottom:1px solid #e6e6e6
  }
  .main {
    border-left:1px dashed #e6e6e6
  }
</style>
