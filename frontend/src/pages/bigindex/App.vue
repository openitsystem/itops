<template>
  <el-container>
    <el-header class="header">
      <a href="/home/" class="admin-logo" style="text-decoration:none">
        <span style="font-size: 25px;overflow: hidden;white-space: nowrap;text-overflow: ellipsis;text-align: center"> 运维平台</span>
      </a>
      <el-dropdown trigger="click" style="float:right" class="classSpancursorpointer">
        <span class="el-dropdown-link">
          {{ userDisplayname }}<i class="el-icon-caret-bottom el-icon--right"></i>
        </span>
        <el-dropdown-menu slot="dropdown">
          <el-dropdown-item>
            <span  @click="jumpurl_out()">
              退出登录
            </span>
          </el-dropdown-item>
        </el-dropdown-menu>
      </el-dropdown>
    </el-header>
    <el-container>
      <el-aside style="height: calc(100vh - 60px);width:220px">
        <el-menu
          router
          style="height: calc(100vh - 60px)"
          class="el-menu-vertical-demo">
          <el-submenu index="1">
            <template slot="title">
              <i class="el-icon-setting"></i>
              <span>IT记录管理</span>
            </template>
            <el-menu-item index="ldapcord">LDAP账号管理</el-menu-item>
            <el-menu-item index="dnscord">DNS记录管理</el-menu-item>
          </el-submenu>
          <el-submenu index="2">
            <template slot="title">
              <i class="el-icon-s-custom"></i>
              <span>Active Directory</span>
            </template>
            <el-menu-item index="directorytree">用户和计算机</el-menu-item>
            <el-menu-item index="leavesearch">账号搜索</el-menu-item>
            <el-menu-item index="admanager">批量操作</el-menu-item>
            <el-menu-item index="downloadcsv">报表管理</el-menu-item>
          </el-submenu>
          <el-submenu index="3">
            <template slot="title">
              <i class="el-icon-message"></i>
              <span>邮箱</span>
            </template>
            <el-menu-item index="findmail">邮件流查询</el-menu-item>
            <!-- <el-menu-item index="mailboxmessage">邮箱数据库</el-menu-item> -->
          </el-submenu>
          <el-submenu index="4">
            <template slot="title">
              <i class="el-icon-copy-document"></i>
              <span>文档</span>
            </template>
            <el-menu-item index="faultproject">故障报告</el-menu-item>
            <el-menu-item index="findproject">故障回溯</el-menu-item>
            <el-menu-item index="creatproject">新建文档</el-menu-item>
            <el-menu-item index="projects">文档查看</el-menu-item>
          </el-submenu>
          <el-submenu index="5">
            <template slot="title">
              <i class="el-icon-folder-opened"></i>
              <span>API</span>
            </template>
            <el-menu-item @click="jumpurl()">API文档</el-menu-item>
            <el-menu-item index="apipermissions">权限配置</el-menu-item>
            <el-menu-item index="apinames">API方法导航</el-menu-item>
          </el-submenu>
          <el-submenu index="6">
            <template slot="title">
              <i class="el-icon-search"></i>
              <span>日志</span>
            </template>
            <el-menu-item index="serchlog">日志</el-menu-item>
          </el-submenu>
          <!-- <el-submenu index="7">
            <template slot="title">
              <i class="el-icon-view"></i>
              <span>监控</span>
            </template>
            <el-menu-item index="dfsmonitor">DFS监控</el-menu-item>
            <el-menu-item index="casmonitor">邮箱Cas监控</el-menu-item>
            <el-menu-item index="admonitor">AD监控</el-menu-item>
          </el-submenu> -->
        </el-menu>
      </el-aside>
      <el-main style="padding:20px;background-color:#F6FAFB">
        <router-view></router-view>
      </el-main>
    </el-container>
  </el-container>
</template>

<script>
import axios from 'axios'
import serverurlvaluefromjs from '@/config/serverurlvalue'
axios.defaults.withCredentials = true
export default {
  data () {
    return {
      classname: {
        classSpancursorpointer: 'classSpancursorpointer'
      },
      srcurl: '',
      userDisplayname: ''
    }
  },
  created () {
    this.srcurl = window.location.protocol + "//" + window.location.host
    this.checkUserLogin()
  },
  methods: {
    checkUserLogin () {
      axios
        .get(serverurlvaluefromjs.serverurl + '/CheckUserlogin')
        .then(response => {
          if (response.data.username === null) {
            this.jumpurl_out()
          } else {
            this.userDisplayname = response.data.displayname
          }
        })
    },
    jumpurl () {
      window.location = this.srcurl + "/docs/"
    },
    jumpurl_out () {
      window.location = this.srcurl + "/logout/"
    }
  }
}

</script>

<style>
.admin-logo {
    width: auto;
    margin-left: 15px;
}
.admin-logo {
  display: block;
  margin-left: -15px;
  float: left;
  width: 220px;
  text-align: center;
  padding-left: 0px;
  height: 60px;
  line-height: 60px;
}
.admin-logo h1 {
  color: #fff;
  font-size: 28px;
  line-height: 60px;
  text-transform: uppercase;
  font-weight: 800;
  margin: 0px;
}
.admin-logo h1 img {
  margin-top: -4px;
}
.admin-logo sub {
  font-size: 10px;
  font-style: italic;
  color: #fff;
  opacity: 0.8;
  font-weight: 300;
}

  .header {
    /*background-color: #409EFF;*/
    /*color: #fff;*/
    width: 100vw;
    line-height: 60px;
    border-bottom:1px solid #e6e6e6
  }
  .main {
    height: 100vh - 60px;
  }
  /* 鼠标放上去显示手形 */
  .classSpancursorpointer{
      cursor: pointer;
  }  /* 宽度 */
</style>
