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
        <el-main>
          <router-view></router-view>
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<script>
import NavMenu from '@/components/user/NavMenu'
import Header from '@/components/user/Header'
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
