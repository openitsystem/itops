<template>
  <div id="app">
    <P></P>
    <el-row :inline="true" :gutter="15" style="min-width:1200px; margin-bottom: 10px;">
      <el-col :span="classValue.pictureSpanWidth" style="min-width:300px; margin-bottom: 10px;">
        <el-card shadow="hover">
          <el-row>
            <el-col :span="6">
              <i style="font-size:250%;" class="iconfont icon-yonghu">
                <el-divider style="hight:80px" direction="vertical"></el-divider>
              </i>
            </el-col>
            <el-col :span="12">
              <span style="font-size:13px">
                所有用户
              </span>
                <br>
              <span style="font-size:20px">
                <vns :start="0" :end="parseInt(allusercountvalue)" :times="15" :speed="80"/>
              </span>
              <span style="font-size:9px"> 个</span>
            </el-col>
          </el-row>
        </el-card>
      </el-col>
      <el-col :span="classValue.pictureSpanWidth" style="min-width:300px; margin-bottom: 10px;">
        <el-card shadow="hover">
          <el-row>
            <el-col :span="6">
              <i style="font-size:250%;" class="iconfont icon-zu">
                <el-divider style="hight:80px" direction="vertical"></el-divider>
              </i>
            </el-col>
            <el-col :span="12">
              <span style="font-size:13px">
                所有组
              </span>
                <br>
              <span style="font-size:20px">
                <vns :start="0" :end="parseInt(allgroupcountvalue)" :times="15" :speed="80"/>
              </span>
              <span style="font-size:9px"> 个</span>
            </el-col>
          </el-row>
        </el-card>
      </el-col>
      <el-col :span="classValue.pictureSpanWidth" style="min-width:300px; margin-bottom: 10px;">
        <el-card shadow="hover">
          <el-row>
            <el-col :span="6">
              <i style="font-size:250%;" class="iconfont icon-jisuanjicomputer160">
                <el-divider style="hight:80px" direction="vertical"></el-divider>
              </i>
            </el-col>
            <el-col :span="12">
              <span style="font-size:13px">
                所有计算机
              </span>
                <br>
              <span style="font-size:20px">
                <vns :start="0" :end="parseInt(allcomputercountvalue)" :times="15" :speed="80"/>
              </span>
              <span style="font-size:9px"> 个</span>
            </el-col>
          </el-row>
        </el-card>
      </el-col>
      <el-col v-if="tableexchangeshow" :span="6" style="min-width:300px; margin-bottom: 10px;">
        <el-card shadow="hover">
          <el-row>
            <el-col :span="6">
              <i style="font-size:250%;" class="iconfont icon-youxiang1">
                <el-divider style="hight:80px" direction="vertical"></el-divider>
              </i>
            </el-col>
            <el-col :span="12">
              <span style="font-size:13px">
                所有用户邮箱
              </span>
                <br>
              <span style="font-size:20px">
                <vns :start="0" :end="parseInt(allexchangeusercountvalue)" :times="15" :speed="80"/>
              </span>
              <span style="font-size:9px"> 个</span>
            </el-col>
          </el-row>
        </el-card>
      </el-col>
    </el-row>
    <el-row>
      <el-col :span="12">
        <el-card shadow="always" class="box-card" :class="[classname.classSpanFloatmid, classname.classkuandu]" :style="{width: '95%'}">
          <div slot="header" class="clearfix">
            <span>用户报表</span>
            <span style="float: right; padding: 3px 0" type="text" @click="alluserLine()" :class="[classname.classSpancursorpointer]"><i class="el-icon-refresh"></i></span>
          </div>
          <div id="alluserLineChart" :style="{width: '90%', height: '300px'}"></div>
          <el-table :data="tableDataalluser" style="width: 100%" :show-header="false" v-show="allusertableshowvalue" size='mini'>
            <el-table-column
              label="色块"
              width="180">
              <template slot-scope="scope">
                <div :style="{width: '12px', height: '12px', background: scope.row.colorvalue}"></div>
              </template>
            </el-table-column>
            <el-table-column
              prop="name"
              label="名称"
              width="180">
            </el-table-column>
            <el-table-column
              prop="messagevalue"
              label="值">
            </el-table-column>
          </el-table>
        </el-card>
      </el-col>
      <el-col :span="12">
        <el-card shadow="always" class="box-card" :class="[classname.classSpanFloatmid, classname.classkuandu]" :style="{width: '95%'}">
          <div slot="header" class="clearfix">
            <span>群组报表</span>
            <span style="float: right; padding: 3px 0" type="text" @click="allgroupLine()" :class="[classname.classSpancursorpointer]"><i class="el-icon-refresh"></i></span>
          </div>
          <div id="allgroupLineChart" :style="{width: '90%', height: '300px'}"></div>
          <el-table :data="tableDataallgroup" style="width: 100%" :show-header="false" v-show="allgrouptableshowvalue" size='mini'>
            <el-table-column
              label="色块"
              width="180">
              <template slot-scope="scope">
                <div :style="{width: '12px', height: '12px', background: scope.row.colorvalue}"></div>
              </template>
            </el-table-column>
            <el-table-column
              prop="name"
              label="名称"
              width="180">
            </el-table-column>
            <el-table-column
              prop="messagevalue"
              label="值">
            </el-table-column>
          </el-table>
        </el-card>
      </el-col>
    </el-row>
    <p></p>
    <el-row>
      <el-col :span="12">
        <el-card shadow="always" class="box-card" :class="[classname.classSpanFloatmid, classname.classkuandu]" :style="{width: '95%'}">
          <div slot="header" class="clearfix">
            <span>计算机报表</span>
            <span style="float: right; padding: 3px 0" type="text" @click="allcomputerLine()" :class="[classname.classSpancursorpointer]"><i class="el-icon-refresh"></i></span>
          </div>
          <div id="allcomputerLineChart" :style="{width: '90%', height: '300px'}"></div>
          <el-table :data="tableDataallcomputer" style="width: 100%" :show-header="false" v-show="allcomputertableshowvalue" size='mini'>
            <el-table-column
              label="色块"
              width="180">
              <template slot-scope="scope">
                <div :style="{width: '12px', height: '12px', background: scope.row.colorvalue}"></div>
              </template>
            </el-table-column>
            <el-table-column
              prop="name"
              label="名称"
              width="180">
            </el-table-column>
            <el-table-column
              prop="messagevalue"
              label="值">
            </el-table-column>
          </el-table>
        </el-card>
      </el-col>
      <el-col :span="12" v-if="tableexchangeshow">
        <el-card shadow="always" class="box-card" :class="[classname.classSpanFloatmid, classname.classkuandu]" :style="{width: '95%'}">
          <div slot="header" class="clearfix">
            <span>exchange报表</span>
            <span style="float: right; padding: 3px 0" type="text" @click="allexchangeLine()" :class="[classname.classSpancursorpointer]"><i class="el-icon-refresh"></i></span>
          </div>
          <div id="allexchangeLineChart" :style="{width: '90%', height: '300px'}"></div>
          <el-table :data="tableDataallexchange" style="width: 100%" :show-header="false" v-show="allexchangetableshowvalue" size='mini'>
            <el-table-column
              label="色块"
              width="180">
              <template slot-scope="scope">
                <div :style="{width: '12px', height: '12px', background: scope.row.colorvalue}"></div>
              </template>
            </el-table-column>
            <el-table-column
              prop="name"
              label="名称"
              width="180">
            </el-table-column>
            <el-table-column
              prop="messagevalue"
              label="值">
            </el-table-column>
          </el-table>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>
<style>
  /* 向右浮动 */
  .classSpanFloatRight{
      float: right;
  }
  /* 居中 */
  .classSpanFloatmid{
      margin: auto;
  }
  /* 鼠标放上去显示手形 */
  .classSpancursorpointer{
      cursor: pointer;
  }  /* 宽度 */
  .classkuandu{
      width: calc(100vh*0.95);
  }
</style>
<script>
import axios from 'axios'
import serverurlvaluefromjs from '@/config/serverurlvalue'
import vns from 'vue-number-scroll'
// import echarts from 'https://cdn.bootcss.com/echarts/4.2.1-rc1/echarts.min.js'

//取消下面注释使用本地模块echarts
// 引入 ECharts 主模块
var echarts = require('echarts/lib/echarts')
// // 引入柱状图
require('echarts/lib/chart/bar')
// // 引入提示框和标题组件
require('echarts/lib/component/tooltip')
require('echarts/lib/component/title')

axios.defaults.withCredentials = true
export default {
  name: 'eCharts',
  components: {
    'vns' : vns
  },
  data () {
    return {
      classValue: {
        pictureSpanWidth: 6
      },
      classname: {
        classSpanFloatRight: 'classSpanFloatRight',
        classSpanFloatmid: 'classSpanFloatmid',
        classkuandu: 'classSpanFloatmid',
        classSpancursorpointer: 'classSpancursorpointer'
      },
      // 用户
      tableDataalluser: [],
      allusercountvalue: 0, // 所有用户数量
      alldisableusercountvalue: 0, // 禁用用户数量
      allexpiredpasswordusercountvalue: 0, // 密码已过期用户数量
      alllockusercountvalue: 0, // 锁定用户数量
      nologoinusercountvalue: 0, // 账号30天之内未登录的账号数量
      allusertableshowvalue: false, // table是否显示
      // 群组
      tableDataallgroup: [],
      allgrouptableshowvalue: false, // 群组table是否显示
      allgroupcountvalue: 0, // 所有群组数量
      allgrouptalkgroupcountvalue: 0, // 通讯组数量
      allgroupsavegroupcpuntvalue: 0, // 安全组数量
      allgroupnomembercountvalue: 0, // 没有成员的组数量
      allgrouphasmailcountvalue: 0, // 启用邮箱的组数量
      // 计算机
      tableDataallcomputer: [],
      allcomputertableshowvalue: false, // 计算机table是否显示
      allcomputercountvalue: 0, // 所有计算机数量
      allcomputernologoincountvalue: 0, // 超过30天没有登录的计算机数量
      allcomputernodisablecpuntvalue: 0, // 启用的计算机数量
      allcomputerdisablecountvalue: 0, // 禁用的计算机数量
      // 邮箱
      tableexchangeshow: true,
      tableDataallexchange: [],
      allexchangetableshowvalue: false, // 邮箱table是否显示
      allexchangeusercountvalue: 0, // 所有启用邮箱的用户数量
      allnoexchangeusercountvalue: 0, // 所有未启用邮箱的用户数量
      allexchangehasarchivecpuntvalue: 0, // 已启用归档的账户数量
      allexchangenodizhicountvalue: 0, // 不显示在exchange地址簿的用户数量
      allexchangenoarchivecountvalue: 0 // 禁用归档的账户数量
    }
  },
  async created () {
    await axios
      .get(serverurlvaluefromjs.serverurl + '/getExissconfig/')
      .then(response => {
        if (!response.data.isSuccess) {
          this.tableexchangeshow = false
          this.classValue.pictureSpanWidth = 8
        } else {
          this.tableexchangeshow = true
          this.classValue.pictureSpanWidth = 6
        }
      })
  },
  mounted () {
    this.alluserLine()
    this.allgroupLine()
    this.allcomputerLine()
    this.allexchangeLine()
  },
  methods: {
    async allexchangeLine () {
      this.tableDataallexchange = []
      this.allexchangetableshowvalue = false // 邮箱table是否显示
      this.allexchangeusercountvalue = 0 // 所有启用邮箱的用户数量
      this.allnoexchangeusercountvalue = 0 // 所有未启用邮箱的用户数量
      this.allexchangehasarchivecpuntvalue = 0 // 已启用归档的账户数量
      this.allexchangenodizhicountvalue = 0 // 使用默认的数据库存储限制的用户数量
      this.allexchangenoarchivecountvalue = 0 // 禁用归档的账户数量
      // 基于准备好的dom，初始化echarts实例
      var myChart = echarts.init(document.getElementById('allexchangeLineChart'))
      // 绘制图表
      myChart.showLoading({
        text: '数据正在努力加载...',
        textStyle: {fontSize: 30, color: '#444'},
        effectOption: {backgroundColor: 'rgba(0, 0, 0, 0)'}
      })
      // 启用邮箱的用户数量
      let getallmailmessagenummber = await axios.get(serverurlvaluefromjs.serverurl + '/api/getallmessagenummber/?idtyes=已启用邮箱的用户&datevalue=1&checkval=true')
      this.allexchangeusercountvalue = getallmailmessagenummber.data.message[0].allexchangeusercountvalue // 所有启用邮箱的用户数量
      this.allnoexchangeusercountvalue = getallmailmessagenummber.data.message[0].allnoexchangeusercountvalue // 所有未启用邮箱的用户数量
      this.allexchangehasarchivecpuntvalue = getallmailmessagenummber.data.message[0].allexchangehasarchivecpuntvalue // 已启用归档的账户数量
      this.allexchangenodizhicountvalue = getallmailmessagenummber.data.message[0].allexchangenodizhicountvalue // 使用默认的数据库存储限制的用户数量
      this.allexchangenoarchivecountvalue = getallmailmessagenummber.data.message[0].allexchangenoarchivecountvalue // 禁用归档的账户数量
      this.allexchangetableshowvalue = true
      this.tableDataallexchange = [{colorvalue: '#5e7e54', name: '启用邮箱的用户', messagevalue: this.allexchangeusercountvalue},
        {colorvalue: '#e44f2f', name: '未启用邮箱的用户', messagevalue: this.allnoexchangeusercountvalue},
        {colorvalue: '#81b6b2', name: '已启用归档的账户', messagevalue: this.allexchangehasarchivecpuntvalue},
        {colorvalue: '#FF0033', name: '使用默认容量限制的用户', messagevalue: this.allexchangenodizhicountvalue},
        {colorvalue: '#eba422', name: '禁用归档的账户', messagevalue: this.allexchangenoarchivecountvalue}]
      myChart.setOption({
        // title: { text: '用户统计' },
        tooltip: {},
        xAxis: {
          data: ['启用邮箱的用户', '未启用邮箱的用户', '已启用归档的账户', '使用默认容量限制的用户', '禁用归档的账户']
        },
        grid: {
          containLabel : true
        },
        yAxis: {},
        series: [{
          name: '数量',
          type: 'bar',
          itemStyle: {
            normal: {
              color: function (params) {
                let colorList = ['#5e7e54', '#e44f2f', '#81b6b2', '#FF0033', '#eba422']
                return colorList[params.dataIndex]
              }
            }
          },
          data: [this.allexchangeusercountvalue, this.allnoexchangeusercountvalue, this.allexchangehasarchivecpuntvalue, this.allexchangenodizhicountvalue, this.allexchangenoarchivecountvalue]
          // data: [allusercountvalue, allusercountvalue, allusercountvalue, allusercountvalue]
        }]
      })
      myChart.hideLoading()
    },
    async allcomputerLine () {
      this.tableDataallcomputer = []
      this.allcomputertableshowvalue = false // 计算机table是否显示
      this.allcomputercountvalue = 0 // 所有计算机数量
      this.allcomputernologoincountvalue = 0 // 超过30天没有登录的计算机数量
      this.allcomputernodisablecpuntvalue = 0 // 启用的计算机数量
      this.allcomputerdisablecountvalue = 0 // 禁用的计算机数量
      // 基于准备好的dom，初始化echarts实例
      var myChart = echarts.init(document.getElementById('allcomputerLineChart'))
      // 绘制图表
      myChart.showLoading({
        text: '数据正在努力加载...',
        textStyle: {fontSize: 30, color: '#444'},
        effectOption: {backgroundColor: 'rgba(0, 0, 0, 0)'}
      })
      // 所有计算机数量
      let getallcomputermessagenummber = await axios.get(serverurlvaluefromjs.serverurl + '/api/getallmessagenummber/?idtyes=所有计算机&datevalue=1&checkval=true')
      this.allcomputercountvalue = getallcomputermessagenummber.data.message[0].allcomputercountvalue // 所有计算机数量
      this.allcomputernologoincountvalue = getallcomputermessagenummber.data.message[0].allcomputernologoincountvalue // 超过30天没有登录的计算机数量
      this.allcomputernodisablecpuntvalue = getallcomputermessagenummber.data.message[0].allcomputernodisablecpuntvalue // 启用的计算机数量
      this.allcomputerdisablecountvalue = getallcomputermessagenummber.data.message[0].allcomputerdisablecountvalue // 禁用的计算机数量
      this.allcomputertableshowvalue = true
      this.tableDataallcomputer = [{colorvalue: '#5e7e54', name: '所有计算机', messagevalue: this.allcomputercountvalue},
        {colorvalue: '#e44f2f', name: '启用的计算机', messagevalue: this.allcomputernodisablecpuntvalue},
        {colorvalue: '#81b6b2', name: '禁用的计算机', messagevalue: this.allcomputerdisablecountvalue},
        {colorvalue: '#eba422', name: '超过30天没有登录的计算机', messagevalue: this.allcomputernologoincountvalue}]
      myChart.setOption({
        // title: { text: '用户统计' },
        tooltip: {},
        xAxis: {
          data: ['所有计算机', '启用的计算机', '禁用的计算机', '超过30天没有登录的计算机']
        },
        grid: {
          containLabel : true
        },
        yAxis: {},
        series: [{
          name: '数量',
          type: 'bar',
          itemStyle: {
            normal: {
              color: function (params) {
                let colorList = ['#5e7e54', '#e44f2f', '#81b6b2', '#eba422']
                return colorList[params.dataIndex]
              }
            }
          },
          data: [this.allcomputercountvalue, this.allcomputernodisablecpuntvalue, this.allcomputerdisablecountvalue, this.allcomputernologoincountvalue]
          // data: [allusercountvalue, allusercountvalue, allusercountvalue, allusercountvalue]
        }]
      })
      myChart.hideLoading()
    },
    async allgroupLine () {
      this.tableDataallgroup = []
      this.allgrouptableshowvalue = false // 群组table是否显示
      this.allgroupcountvalue = 0 // 所有群组数量
      this.allgrouptalkgroupcountvalue = 0 // 通讯组数量
      this.allgroupsavegroupcpuntvalue = 0 // 安全组数量
      this.allgroupnomembercountvalue = 0 // 没有成员的组数量
      this.allgrouphasmailcountvalue = 0 // 启用邮箱的组数量
      // 基于准备好的dom，初始化echarts实例
      var myChart = echarts.init(document.getElementById('allgroupLineChart'))
      // 绘制图表
      myChart.showLoading({
        text: '数据正在努力加载...',
        textStyle: {fontSize: 30, color: '#444'},
        effectOption: {backgroundColor: 'rgba(0, 0, 0, 0)'}
      })
      // 所有组数量
      let getallgroupmessagenummber = await axios.get(serverurlvaluefromjs.serverurl + '/api/getallmessagenummber/?idtyes=所有组&datevalue=30&checkval=true')
      this.allgroupcountvalue = getallgroupmessagenummber.data.message[0].allgroupcountvalue // 所有群组数量
      this.allgrouptalkgroupcountvalue = getallgroupmessagenummber.data.message[0].allgrouptalkgroupcountvalue // 通讯组数量
      this.allgroupsavegroupcpuntvalue = getallgroupmessagenummber.data.message[0].allgroupsavegroupcpuntvalue // 安全组数量
      this.allgroupnomembercountvalue = getallgroupmessagenummber.data.message[0].allgroupnomembercountvalue // 没有成员的组数量
      this.allgrouphasmailcountvalue = getallgroupmessagenummber.data.message[0].allgrouphasmailcountvalue // 启用邮箱的组数量
      this.allgrouptableshowvalue = true
      this.tableDataallgroup = [{colorvalue: '#5e7e54', name: '所有组', messagevalue: this.allgroupcountvalue},
        {colorvalue: '#e44f2f', name: '安全组', messagevalue: this.allgroupsavegroupcpuntvalue},
        {colorvalue: '#81b6b2', name: '通讯组', messagevalue: this.allgrouptalkgroupcountvalue},
        {colorvalue: '#FF0033', name: '没有成员的组', messagevalue: this.allgroupnomembercountvalue},
        {colorvalue: '#eba422', name: '已启用邮箱的组', messagevalue: this.allgrouphasmailcountvalue}]
      myChart.setOption({
        // title: { text: '用户统计' },
        tooltip: {},
        xAxis: {
          data: ['所有组', '安全组', '通讯组', '没有成员的组', '已启用邮箱的组']
        },
        grid: {
          containLabel : true
        },
        yAxis: {},
        series: [{
          name: '数量',
          type: 'bar',
          itemStyle: {
            normal: {
              color: function (params) {
                let colorList = ['#5e7e54', '#e44f2f', '#81b6b2', '#FF0033', '#eba422']
                return colorList[params.dataIndex]
              }
            }
          },
          data: [this.allgroupcountvalue, this.allgroupsavegroupcpuntvalue, this.allgrouptalkgroupcountvalue, this.allgroupnomembercountvalue, this.allgrouphasmailcountvalue]
          // data: [allusercountvalue, allusercountvalue, allusercountvalue, allusercountvalue]
        }]
      })
      myChart.hideLoading()
    },
    async alluserLine () {
      this.tableDataalluser = []
      this.allusercountvalue = 0 // 所有用户数量
      this.alldisableusercountvalue = 0 // 禁用用户数量
      this.allexpiredpasswordusercountvalue = 0 // 密码已过期用户数量
      this.alllockusercountvalue = 0 // 锁定用户数量
      this.nologoinusercountvalue = 0 // 账号30天之内未登录的账号数量
      this.allusertableshowvalue = false
      // 基于准备好的dom，初始化echarts实例
      var myChart = echarts.init(document.getElementById('alluserLineChart'))
      // 绘制图表
      myChart.showLoading({
        text: '数据正在努力加载...',
        textStyle: {fontSize: 30, color: '#444'},
        effectOption: {backgroundColor: 'rgba(0, 0, 0, 0)'}
      })
      // 账号30天之内未登录的账号数量
      let getallmessagenummber = await axios.get(serverurlvaluefromjs.serverurl + '/api/getallmessagenummber/?idtyes=账号某些天之内未登录的账号&datevalue=30&checkval=true')
      this.allusercountvalue = getallmessagenummber.data.message[0].allusercountvalue // 所有用户数量
      this.alldisableusercountvalue = getallmessagenummber.data.message[0].alldisableusercountvalue // 禁用用户数量
      this.allexpiredpasswordusercountvalue = getallmessagenummber.data.message[0].allexpiredpasswordusercountvalue // 密码已过期用户数量
      this.alllockusercountvalue = getallmessagenummber.data.message[0].alllockusercountvalue // 锁定用户数量
      this.nologoinusercountvalue = getallmessagenummber.data.message[0].nologoinusercountvalue // 账号30天之内未登录的账号数量
      this.allusertableshowvalue = true
      this.tableDataalluser = [{colorvalue: '#5e7e54', name: '所有用户', messagevalue: this.allusercountvalue},
        {colorvalue: '#e44f2f', name: '禁用的用户', messagevalue: this.alldisableusercountvalue},
        {colorvalue: '#81b6b2', name: '密码已过期的用户', messagevalue: this.allexpiredpasswordusercountvalue},
        {colorvalue: '#FF0033', name: '账号30天之内未登录的账号', messagevalue: this.nologoinusercountvalue},
        {colorvalue: '#eba422', name: '锁定的用户', messagevalue: this.alllockusercountvalue}]
      myChart.setOption({
        // title: { text: '用户统计' },
        tooltip: {},
        xAxis: {
          data: ['所有用户', '禁用用户', '密码过期用户', '账号30天之内未登录的账号', '锁定用户']
        },
        grid: {
          containLabel : true
        },
        yAxis: {},
        series: [{
          name: '数量',
          type: 'bar',
          itemStyle: {
            normal: {
              color: function (params) {
                let colorList = ['#5e7e54', '#e44f2f', '#81b6b2', '#FF0033', '#eba422']
                return colorList[params.dataIndex]
              }
            }
          },
          data: [this.allusercountvalue, this.alldisableusercountvalue, this.allexpiredpasswordusercountvalue, this.nologoinusercountvalue, this.alllockusercountvalue]
          // data: [allusercountvalue, allusercountvalue, allusercountvalue, allusercountvalue]
        }]
      })
      myChart.hideLoading()
    }
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
