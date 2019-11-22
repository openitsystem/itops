<template>
  <div id="app1">
    <el-container>
      <el-header class="header">
        <vheader />
      </el-header>
      <el-container>
        <el-aside width="200px">
          <navmenu></navmenu>
        </el-aside>
        <el-main style="background-color:rgb(246, 250, 251);">
          <router-view></router-view>
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<script>
import NavMenu from '@/components/computer/computerNavMenu'
import Header from '@/components/computer/computerheader'
// import axios from 'axios'
// import Vue from 'vue'

export default {
  name: 'app1',
  components: {
    'navmenu': NavMenu,
    'vheader': Header
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
