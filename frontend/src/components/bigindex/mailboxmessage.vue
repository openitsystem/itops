<template>
  <div id="app1" ref="elememt" style="height: calc(100vh - 100px);width: calc(100vw -260px)">
    <!-- <iframe scrolling="auto" height="100%" width="100%" frameborder="no" :src="srcurl">
    </iframe> -->
    <el-breadcrumb separator="/" style="margin-bottom:15px;">
      <el-breadcrumb-item :to="{ path: '/index' }">首页</el-breadcrumb-item>
      <el-breadcrumb-item>邮箱数据库</el-breadcrumb-item>
    </el-breadcrumb>
  <el-card shadow="hover" style="margin-bottom:15px;height:60px" class="el-menu-demo">
    <nobr>
    <el-button
      style="margin-left:15px;float:right"
      type="primary"
      size="small"
      @click="configDlog">配置
    </el-button>
    </nobr>
  </el-card>
  <el-card v-loading="mailboxList.loading" shadow="hover" class="el-menu-demo" v-if="mailboxList.tableShow">
    <nobr>
    <el-tag style="margin-left:15px;float:right">{{mailboxList.allMailboxCountTitle}}{{ (mailboxList.tableData).length }} 个</el-tag>
    <el-select
      @change="currentSel"
      style="margin-left:15px;float:right"
      size='small'
      v-model="mailboxList.mailboxSearchSelect.value"
      :remote-method="remoteMethod"
      :multiple-limit="1"
      multiple
      remote
      filterable
      allow-create
      default-first-option
      placeholder="搜索数据库">
      <el-option
        v-for="item in mailboxList.mailboxSearchSelect.options"
        :key="item.databaseGuid"
        :label="item.databaseIdentity"
        :value="item.databaseIdentity">
      </el-option>
    </el-select>
    </nobr>
    <el-table
        v-loading="mailboxList.loading"
        stripe
        @row-dblclick="tabledblClick"
        :data="mailboxList.tableData"
        style="width: 100%">
      <el-table-column
        prop="databaseIdentity"
        label="数据库名"
        width="150px">
        <template slot-scope="scope">
          <span ></span>
          <span>{{ scope.row.databaseIdentity }}</span>
        </template>
      </el-table-column>
      <el-table-column
        prop="databaseSizeInt"
        sortable
        label="数据库大小"
        min-width="250px">
        <template slot-scope="scope">
          <span ></span>
          <el-progress :percentage="parseFloat(((scope.row.databaseSizeInt / configdata.mailboxSizeValueint)*100).toFixed(0))"></el-progress>
          <span>数据库大小：{{ (scope.row.databaseSizeStr).split(' (')[0] }} , 共 {{configdata.mailboxSizeValueStr}} {{configdata.mailboxSizeValueStrCompany}}</span>
        </template>
      </el-table-column>
      <el-table-column
        prop="databaseSpaceProportion"
        sortable
        label="白空间大小"
        min-width="250px">
        <template slot-scope="scope">
          <span ></span>
          <!-- <el-progress :percentage="(scope.row.databaseSizeInt / 2199023255552).toFixed(2)"></el-progress> -->
          <el-progress :percentage="parseFloat(((scope.row.databaseSpaceInt / scope.row.databaseSizeInt)*100).toFixed(0))"></el-progress>
          <span>白空间占：{{ (scope.row.databaseSpaceStr).split(' (')[0] }} , 共 {{ (scope.row.databaseSizeStr).split(' (')[0] }}</span>
        </template>
      </el-table-column>
      <el-table-column
        sortable
        prop="databaseMailboxNumber"
        label="mailbox数量"
        min-width="250px">
        <template slot-scope="scope">
          <span ></span>
          <el-progress :percentage="parseFloat(((scope.row.databaseMailboxNumber / configdata.mailboxNumValueint)*100).toFixed(0))"></el-progress>
          <span>mailbox数量：{{ scope.row.databaseMailboxNumber }} 个 , 共 {{configdata.mailboxNumValueint}} 个</span>
        </template>
      </el-table-column>
    </el-table>
  </el-card>
  <div>
    <el-dialog v-loading="configdata.dialogloading" title="配置管理" :visible.sync="configdata.detailsVisible" width="70%">
      <el-tabs type="border-card" @tab-click="handleClick">
        <el-tab-pane>
          <span slot="label"><i class="el-icon-tickets"></i> 数据库信息配置</span>
          <div>
            <el-table :data="configdata.tableData"  style="width: 100%" :show-header="false" v-cloak>
              <el-table-column width="180">
                <template slot-scope="scope">
                  <span>&nbsp;数据库大小阈值：</span>
                  <span style="font-size:130%;" v-if="configdata.changespanshow.changemailboxsizeshow" :class="[classname.classSpanFloatRight,classname.classSpancursorpointer]" @click="mailboxSizeValueChangeFuction"><i class="el-icon-edit-outline"></i></span>
                </template>
              </el-table-column>
              <el-table-column>
                <template slot-scope="scope">
                  <span v-if="configdata.changespanshow.changemailboxsizeshow"  v-text="configdata.changetextValue.mailboxSizeValue + ' ' + configdata.mailboxSizeCompanySelect.value"></span>
                  <div v-else >
                    <el-col :span="6" style="min-width:250px">
                      <nobr>
                      <!-- <el-input size="small" v-model="configdata.changetextValue.mailboxSizeValueChange"></el-input> -->
                      <el-input-number size="mini" v-model="configdata.changetextValue.mailboxSizeValueChange" controls-position="right" :min="1" :max="configdata.mailboxSizeCompanySelect.inputMaxValue" onkeyup="this.value=this.value.replace(/[^\d.]/g,'');"></el-input-number>
                      <el-select size="mini" style="width:100px" v-model="configdata.mailboxSizeCompanySelect.changeValue" placeholder="请选择">
                        <el-option
                          v-for="item in configdata.mailboxSizeCompanySelect.options"
                          :key="item.value"
                          :label="item.label"
                          :value="item.value">
                        </el-option>
                      </el-select>
                      </nobr>
                    </el-col>
                    <el-col :span="6" style="margin-left:auto;margin-right:auto;">
                      &nbsp;<span size="small" :class="classname.classSpancursorpointer" @click="savechangemailboxSizeValue('mailboxSizeValue')"><i class="el-icon-upload2" style="font-size:150%;"></i></span>
                      <span @click="closechangemailboxSizeValue" :class="classname.classSpancursorpointer"><i class="el-icon-close" style="font-size:150%;"></i></span>
                    </el-col>
                  </div>
                </template>
              </el-table-column>
            </el-table>
            <el-table :data="configdata.tableData"  style="width: 100%" :show-header="false" v-cloak>
              <el-table-column width="180">
                <template slot-scope="scope">
                  <span>&nbsp;mailbox数量阈值：</span>
                  <span style="font-size:130%;" v-if="configdata.changespanshow.changemailboxNumshow" :class="[classname.classSpanFloatRight,classname.classSpancursorpointer]" @click="mailboxNumValueChangeFuction"><i class="el-icon-edit-outline"></i></span>
                </template>
              </el-table-column>
              <el-table-column>
                <template slot-scope="scope">
                  <span v-if="configdata.changespanshow.changemailboxNumshow"  v-text="configdata.changetextValue.mailboxNumValue + '  个'"></span>
                  <div v-else >
                    <el-col :span="6" style="min-width:250px">
                      <nobr>
                      <!-- <el-input size="small" v-model="configdata.changetextValue.mailboxSizeValueChange"></el-input> -->
                      <el-input-number size="mini" v-model="configdata.changetextValue.mailboxNumValueChange" controls-position="right" :min="1"  onkeyup="this.value=this.value.replace(/[^\d.]/g,'');"></el-input-number>
                      </nobr>
                    </el-col>
                    <el-col :span="6" style="margin-left:auto;margin-right:auto;">
                      &nbsp;<span size="small" :class="classname.classSpancursorpointer" @click="savechangemailboxSizeValue('mailboxNumValue')"><i class="el-icon-upload2" style="font-size:150%;"></i></span>
                      <span @click="closechangemailboxNumValue" :class="classname.classSpancursorpointer"><i class="el-icon-close" style="font-size:150%;"></i></span>
                    </el-col>
                  </div>
                </template>
              </el-table-column>
            </el-table>
          </div>
        </el-tab-pane>
      </el-tabs>
    </el-dialog>
    <el-dialog v-loading="databaseMessageDialog.dialogloading" :title="databaseMessageDialog.titleValue" :visible.sync="databaseMessageDialog.detailsVisible" width="70%">
      <div v-show="!databaseMessageDialog.isConfigShow">
        <el-row justify="space-around" :gutter="20">
          <el-button type="primary" size="mini" style="float:right;z-index:9999" @click="databaseMessageconfigFuction()">配置</el-button>
        </el-row>
        <el-row justify="space-around" :gutter="20">
          <el-col :span="8">
            <el-card class="box-card" shadow="never" ref="bar_dv" id="bar_dv" :style="{width: '100%', height: '200px',border:0}">
            </el-card>
          </el-col>
          <el-col :span="8">
            <el-card class="box-card" shadow="never" ref="Size_dv" id="Size_dv" :style="{width: '100%', height: '200px',border:0}">
            </el-card>
          </el-col>
          <el-col :span="8">
            <el-card class="box-card" shadow="never" ref="space_dv" id="space_dv" :style="{width: '100%', height: '200px',border:0}">
            </el-card>
          </el-col>
        </el-row>
        <el-row justify="space-around" v-loading="databaseMessageDialog.mailboxCopyMessageRow.rowLoading" :gutter="20">
          <el-col style="margin-bottom:10px;" :span="6" v-for="itemValue in DatabaseCopyMessage.DatabaseCopyMessageList" :key="itemValue.Identity">
            <el-card class="box-card">
              <div slot="header" class="clearfix">
                <span>{{itemValue.MailboxServer}}</span>
                <!-- <span>{{itemValue.ActiveCopy}}</span> -->
                <el-tag v-if="itemValue.Status.toLowerCase() === 'mounted'" size="mini" style="margin-left:5px;float:right">已装入</el-tag>
                <el-button v-else round size="mini" style="margin-left:5px;float:right" @click="mailboxActivationClick(itemValue.MailboxServer,databaseMessageDialog.titleValue)">激活</el-button>
                <!-- <el-tag v-else type="danger" size="mini" style="margin-left:5px;float:right">异常</el-tag>
                <el-tag size="mini" style="margin-left:5px;float:right">已装入</el-tag> -->
              </div>
              <div class="text item" style="margin-top: 2px">
                激活首选项：{{(itemValue.ActivationPreference)}}
              </div>
              <div class="text item" style="margin-top: 2px">
                复制队列：{{itemValue.CopyQueueLength}}
              </div>
              <div class="text item" style="margin-top: 2px">
                副本磁盘：{{(itemValue.DatabaseVolumeMountPoint).replace(":\\","")}}
              </div>
              <div class="text item" style="margin-top: 2px">
                磁盘大小：{{(itemValue.DiskTotalSpace).split(" (")[0]}}
              </div>
              <el-row :gutter="2">
                <el-col :span="10"><span style="display:inline-block;width:100%;word-wrap:break-word;white-space:normal;">空间比例：</span></el-col>
                <el-col :span="14"><el-progress style="margin-top: 2px" :percentage="100 - itemValue.DiskFreeSpacePercent"></el-progress></el-col>
              </el-row>
              <!-- <el-row :gutter="2" style="margin-top: 8px"> -->
                <!-- <el-col :span="8"> -->
                  <!-- <el-button v-if="itemValue.Status.toLowerCase() !== 'mounted'" round size="mini" style="margin-left:5px;float:right" @click="mailboxActivationClick">激活</el-button> -->
                <!-- </el-col> -->
                <!-- <el-col :span="8">
                  <el-button round size="mini" style="margin-left:5px;float:right">挂起</el-button>
                </el-col>
                <el-col :span="8">
                  <el-button round size="mini" style="margin-left:5px;float:right">删除</el-button>
                </el-col> -->
              <!-- </el-row> -->
            </el-card>
          </el-col>
        </el-row>
      </div>
      <div v-show="databaseMessageDialog.isConfigShow">
        <el-row justify="space-around" :gutter="20">
          <el-button type="primary" size="mini" style="float:right;z-index:9999" @click="databaseMessageDialog.isConfigShow = false">返回</el-button>
        </el-row>
        <el-row justify="space-around" :gutter="20" style="padding-top: 20px;">
          <el-tabs type="border-card" @tab-click="handleClick">
            <el-tab-pane>
              <span slot="label"><i class="el-icon-tickets"></i> 数据库限制配置</span>
              <div v-loading="databaseMessageDialog.databaseMessageConfigSize.tagLoading">
                <el-table :data="configdata.tableData"  style="width: 100%" :show-header="false" v-cloak>
                  <el-table-column width="200">
                    <template slot-scope="scope">
                      <span>&nbsp;达到该限度时发出警告：</span>
                      <span style="font-size:130%;" v-if="databaseMessageDialog.databaseMessageConfigSize.changespanshow.warningchangemailboxsizeshow" :class="[classname.classSpanFloatRight,classname.classSpancursorpointer]" @click="mailboxSizelimitValuewarningChangeFuction(false)"><i class="el-icon-edit-outline"></i></span>
                    </template>
                  </el-table-column>
                  <el-table-column>
                    <template slot-scope="scope">
                      <span v-if="databaseMessageDialog.databaseMessageConfigSize.changespanshow.warningchangemailboxsizeshow"  v-text="databaseMessageDialog.databaseMessageConfigSize.mailboxsizelimitValue.IssueWarning"></span>
                      <div v-else >
                        <el-col :span="6" style="min-width:250px">
                          <nobr>
                          <el-input-number size="mini" v-model="databaseMessageDialog.databaseMessageConfigSize.mailboxsizelimitValue.IssueWarningInt" controls-position="right" :min="1" :max="configdata.mailboxSizeCompanySelect.inputMaxValue" onkeyup="this.value=this.value.replace(/[^\d.]/g,'');"></el-input-number>
                          <el-select size="mini" style="width:100px" v-model="databaseMessageDialog.databaseMessageConfigSize.mailboxsizelimitValue.IssueWarningCompany" placeholder="请选择">
                            <el-option
                              v-for="item in configdata.mailboxSizeCompanySelect.options"
                              :key="item.value"
                              :label="item.label"
                              :value="item.value">
                            </el-option>
                          </el-select>
                          </nobr>
                        </el-col>
                        <el-col :span="6" style="margin-left:auto;margin-right:auto;">
                          &nbsp;<span size="small" :class="classname.classSpancursorpointer" @click="savechangemailboxLimitSizeValue('IssueWarningQuota',databaseMessageDialog.databaseMessageConfigSize.mailboxsizelimitValue.IssueWarningCompany,databaseMessageDialog.databaseMessageConfigSize.mailboxsizelimitValue.IssueWarningInt)"><i class="el-icon-upload2" style="font-size:150%;"></i></span>
                          <span @click="mailboxSizelimitValuewarningChangeFuction(true)" :class="classname.classSpancursorpointer"><i class="el-icon-close" style="font-size:150%;"></i></span>
                        </el-col>
                      </div>
                    </template>
                  </el-table-column>
                </el-table>
                <el-table :data="configdata.tableData"  style="width: 100%" :show-header="false" v-cloak>
                  <el-table-column width="200">
                    <template slot-scope="scope">
                      <span>&nbsp;达到该限度时禁止发送：</span>
                      <span style="font-size:130%;" v-if="databaseMessageDialog.databaseMessageConfigSize.changespanshow.ProhibitSendchangemailboxsizeshow" :class="[classname.classSpanFloatRight,classname.classSpancursorpointer]" @click="mailboxSizelimitValueProhibitSendChangeFuction(false)"><i class="el-icon-edit-outline"></i></span>
                    </template>
                  </el-table-column>
                  <el-table-column>
                    <template slot-scope="scope">
                      <span v-if="databaseMessageDialog.databaseMessageConfigSize.changespanshow.ProhibitSendchangemailboxsizeshow"  v-text="databaseMessageDialog.databaseMessageConfigSize.mailboxsizelimitValue.ProhibitSend"></span>
                      <div v-else >
                        <el-col :span="6" style="min-width:250px">
                          <nobr>
                          <el-input-number size="mini" v-model="databaseMessageDialog.databaseMessageConfigSize.mailboxsizelimitValue.ProhibitSendInt" controls-position="right" :min="1" :max="configdata.mailboxSizeCompanySelect.inputMaxValue" onkeyup="this.value=this.value.replace(/[^\d.]/g,'');"></el-input-number>
                          <el-select size="mini" style="width:100px" v-model="databaseMessageDialog.databaseMessageConfigSize.mailboxsizelimitValue.ProhibitSendCompany" placeholder="请选择">
                            <el-option
                              v-for="item in configdata.mailboxSizeCompanySelect.options"
                              :key="item.value"
                              :label="item.label"
                              :value="item.value">
                            </el-option>
                          </el-select>
                          </nobr>
                        </el-col>
                        <el-col :span="6" style="margin-left:auto;margin-right:auto;">
                          &nbsp;<span size="small" :class="classname.classSpancursorpointer" @click="savechangemailboxLimitSizeValue('ProhibitSendQuota',databaseMessageDialog.databaseMessageConfigSize.mailboxsizelimitValue.ProhibitSendCompany,databaseMessageDialog.databaseMessageConfigSize.mailboxsizelimitValue.ProhibitSendInt)"><i class="el-icon-upload2" style="font-size:150%;"></i></span>
                          <span @click="mailboxSizelimitValueProhibitSendChangeFuction(true)" :class="classname.classSpancursorpointer"><i class="el-icon-close" style="font-size:150%;"></i></span>
                        </el-col>
                      </div>
                    </template>
                  </el-table-column>
                </el-table>
                <el-table :data="configdata.tableData"  style="width: 100%" :show-header="false" v-cloak>
                  <el-table-column width="240">
                    <template slot-scope="scope">
                      <span>&nbsp;达到该限度时禁止发送和接收：</span>
                      <span style="font-size:130%;" v-if="databaseMessageDialog.databaseMessageConfigSize.changespanshow.ProhibitSendReceivechangemailboxsizeshow" :class="[classname.classSpanFloatRight,classname.classSpancursorpointer]" @click="mailboxSizelimitValueProhibitSendReceiveChangeFuction(false)"><i class="el-icon-edit-outline"></i></span>
                    </template>
                  </el-table-column>
                  <el-table-column>
                    <template slot-scope="scope">
                      <span v-if="databaseMessageDialog.databaseMessageConfigSize.changespanshow.ProhibitSendReceivechangemailboxsizeshow"  v-text="databaseMessageDialog.databaseMessageConfigSize.mailboxsizelimitValue.ProhibitSendReceive"></span>
                      <div v-else >
                        <el-col :span="6" style="min-width:250px">
                          <nobr>
                          <el-input-number size="mini" v-model="databaseMessageDialog.databaseMessageConfigSize.mailboxsizelimitValue.ProhibitSendReceiveInt" controls-position="right" :min="1" :max="configdata.mailboxSizeCompanySelect.inputMaxValue" onkeyup="this.value=this.value.replace(/[^\d.]/g,'');"></el-input-number>
                          <el-select size="mini" style="width:100px" v-model="databaseMessageDialog.databaseMessageConfigSize.mailboxsizelimitValue.ProhibitSendReceiveCompany" placeholder="请选择">
                            <el-option
                              v-for="item in configdata.mailboxSizeCompanySelect.options"
                              :key="item.value"
                              :label="item.label"
                              :value="item.value">
                            </el-option>
                          </el-select>
                          </nobr>
                        </el-col>
                        <el-col :span="6" style="margin-left:auto;margin-right:auto;">
                          &nbsp;<span size="small" :class="classname.classSpancursorpointer" @click="savechangemailboxLimitSizeValue('ProhibitSendReceiveQuota',databaseMessageDialog.databaseMessageConfigSize.mailboxsizelimitValue.ProhibitSendReceiveCompany,databaseMessageDialog.databaseMessageConfigSize.mailboxsizelimitValue.ProhibitSendReceiveInt)"><i class="el-icon-upload2" style="font-size:150%;"></i></span>
                          <span @click="mailboxSizelimitValueProhibitSendReceiveChangeFuction(true)" :class="classname.classSpancursorpointer"><i class="el-icon-close" style="font-size:150%;"></i></span>
                        </el-col>
                      </div>
                    </template>
                  </el-table-column>
                </el-table>
              </div>
            </el-tab-pane>
          </el-tabs>
        </el-row>
      </div>
    </el-dialog>
  </div>
  </div>
</template>

<style>
  .el-dialog__body{
    padding-top: 0px;
  }
  /* 向右浮动 */
  .classSpanFloatRight{
      float: right;
  }
  /* 鼠标放上去显示手形 */
  .classSpancursorpointer{
      cursor: pointer;
  }
   .el-progress{width:100%;} 
</style>
<script>
import axios from 'axios'
import qs from 'qs'
import serverurlvaluefromjs from '@/config/serverurlvalue'
// import Vue from 'vue'


//取消下面注释使用本地模块echarts
// 引入 ECharts 主模块
var echarts = require('echarts/lib/echarts')
// // 引入柱状图
require('echarts/lib/chart/line')
// // 引入提示框和标题组件
require('echarts/lib/component/tooltip')
require('echarts/lib/component/title')

export default {
  name: 'app1',
  data () {
    return {
      srcurl: '',
      mailboxList: {
        allMailboxCountTitle:'数据库共：',
        tableData: [],
        tableShow: true,
        tableListModule: [{'label':'数据库名','value':'databaseIdentity'},{'label':'数据库大小','value':'databaseSizeStr'},{'label':'白空间大小','value':'databaseSpaceStr'}],
        loading: true,
        mailboxSearchSelect: {
          options: [],
          value: []
        }
      },
      configdata:{
        mailboxSizeValueStr:'',
        mailboxSizeValueint:0,
        mailboxNumValueint:0,
        mailboxSizeValueStrCompany:'',
        dialogloading:false,
        tableData:[{date: 'displayName'}],
        detailsVisible:false,
        changespanshow:{
          changemailboxsizeshow:true,
          changemailboxNumshow:true
        },
        changetextValue:{
          mailboxNumValue:0,
          mailboxNumValueChange:0,
          mailboxSizeValue:0,
          mailboxSizeValueChange:0
        },
        mailboxSizeCompanySelect:{
          options:[{value: 'TB',label: 'TB'}, {value: 'GB',label: 'GB'},{value: 'MB',label: 'MB'}],
          value:'',
          changeValue:'',
          inputMaxValue:1024
        }
      },
      classname: {
        classSpanFloatRight: 'classSpanFloatRight',
        classSpancursorpointer: 'classSpancursorpointer'
      },
      databaseMessageDialog:{
        isConfigShow:false,
        mailboxCopyMessageRow:{
          rowLoading:false
        },
        databaseMessageConfigSize:{
          tagLoading:false,
          mailboxsizelimitValue:{
            ProhibitSend:'',
            ProhibitSendInt:0,
            ProhibitSendCompany:'',
            ProhibitSendReceive:'',
            ProhibitSendReceiveInt:0,
            ProhibitSendReceiveCompany:'',
            IssueWarning:'',
            IssueWarningInt:0,
            IssueWarningCompany:'',
          },
          changespanshow:{
            warningchangemailboxsizeshow:true,
            ProhibitSendchangemailboxsizeshow:true,
            ProhibitSendReceivechangemailboxsizeshow:true,
          },
        },
        echartsRowValue:{},
        titleValue:'',
        dialogloading: false,
        detailsVisible: false
      },
      DatabaseCopyMessage:{
        count:0,
        DatabaseCopyMessageList:[]
      }
    }
  },
  created () {
    this.srcurl = window.location.protocol + "//" + window.location.host + "/mailboxmessage"
    this.searchMailboxMessageconfig()
    this.searchMailboxMessage()
  },
  watch:{
    'databaseMessageDialog.detailsVisible' : {
      handler(val, oldVal){
        this.$nextTick(function () {
          if(val){
            let that = this
            that.trendClickDosth()
          }
        })
      },
      deep:true //true 深度监听
    }
  },
  methods: {
    async databaseMessageconfigFuction() {
      let that = this
      that.databaseMessageDialog.databaseMessageConfigSize.tagLoading = true
      that.databaseMessageDialog.isConfigShow = true
      that.databaseMessageDialog.databaseMessageConfigSize.changespanshow = {
            warningchangemailboxsizeshow:true,
            ProhibitSendchangemailboxsizeshow:true,
            ProhibitSendReceivechangemailboxsizeshow:true,
          }
      let data = {'mailboxIdentity': that.databaseMessageDialog.echartsRowValue.databaseIdentity}
      let instance = axios.create({
        timeout: 1000000,
        headers: {'content-type': 'application/x-www-form-urlencoded'}
      })
      await instance.post(serverurlvaluefromjs.serverurl + '/exchange/getmailboxSizelimitMessage/', qs.stringify(data)).then(response => {
        if (response.data.isSuccess) {
          that.databaseMessageDialog.databaseMessageConfigSize.mailboxsizelimitValue.IssueWarning = (response.data.message.IssueWarningQuota).split(" (")[0]
          that.databaseMessageDialog.databaseMessageConfigSize.mailboxsizelimitValue.ProhibitSend = (response.data.message.ProhibitSendQuota).split(" (")[0]
          that.databaseMessageDialog.databaseMessageConfigSize.mailboxsizelimitValue.ProhibitSendReceive = (response.data.message.ProhibitSendReceiveQuota).split(" (")[0]
          that.databaseMessageDialog.databaseMessageConfigSize.mailboxsizelimitValue.IssueWarningInt =parseFloat((that.databaseMessageDialog.databaseMessageConfigSize.mailboxsizelimitValue.IssueWarning).split(" ")[0])
          that.databaseMessageDialog.databaseMessageConfigSize.mailboxsizelimitValue.ProhibitSendInt =parseFloat((that.databaseMessageDialog.databaseMessageConfigSize.mailboxsizelimitValue.ProhibitSend).split(" ")[0])
          that.databaseMessageDialog.databaseMessageConfigSize.mailboxsizelimitValue.ProhibitSendReceiveInt =parseFloat((that.databaseMessageDialog.databaseMessageConfigSize.mailboxsizelimitValue.ProhibitSendReceive).split(" ")[0])
          that.databaseMessageDialog.databaseMessageConfigSize.mailboxsizelimitValue.IssueWarningCompany =(that.databaseMessageDialog.databaseMessageConfigSize.mailboxsizelimitValue.IssueWarning).split(" ")[1]
          that.databaseMessageDialog.databaseMessageConfigSize.mailboxsizelimitValue.ProhibitSendCompany =(that.databaseMessageDialog.databaseMessageConfigSize.mailboxsizelimitValue.ProhibitSend).split(" ")[1]
          that.databaseMessageDialog.databaseMessageConfigSize.mailboxsizelimitValue.ProhibitSendReceiveCompany =(that.databaseMessageDialog.databaseMessageConfigSize.mailboxsizelimitValue.ProhibitSendReceive).split(" ")[1]
        } else {
          that.databaseMessageDialog.databaseMessageConfigSize.mailboxsizelimitValue = {
            ProhibitSend:'',
            ProhibitSendInt:0,
            ProhibitSendCompany:'',
            ProhibitSendReceive:'',
            ProhibitSendReceiveInt:0,
            ProhibitSendReceiveCompany:'',
            IssueWarning:'',
            IssueWarningInt:0,
            IssueWarningCompany:'',
          }
          this.$message({
            type: 'error',
            showClose: true,
            message: '获取配置失败'
          });
        }
      })
      that.databaseMessageDialog.databaseMessageConfigSize.tagLoading = false
    },
    async mailboxActivationClick(ActivateOnServer,identity) {
      let that = this
      this.$msgbox({
          type: 'warning',
          title: '警告',
          message: '是否要激活数据库副本 '+ActivateOnServer+'\\'+identity+'?',
          showCancelButton: true,
          closeOnPressEscape: false,
          closeOnClickModal: false,
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          beforeClose: (action, instance, done) => {
            if (action === 'confirm') {
              instance.confirmButtonLoading = true;
              instance.confirmButtonText = '执行中...';
              let data = {'identity': identity,'ActivateOnServer': ActivateOnServer}
              let instanceUrl = axios.create({
                timeout: 1000000,
                headers: {'content-type': 'application/x-www-form-urlencoded'}
              })
              instanceUrl.post(serverurlvaluefromjs.serverurl + '/exchange/moveDatabaseActiveOperation/', qs.stringify(data)).then(response => {
                instance.confirmButtonLoading = false
                done();
                if (response.data.isSuccess) {
                  this.$message({
                    type: 'success',
                    showClose: true,
                    message: '激活操作成功！'
                  });
                  that.hasDatabaseCopyMessageValue()
                } else {
                  this.$message({
                    type: 'error',
                    showClose: true,
                    duration: 0,
                    message: response.data.msg
                  });
                }
              })
            } else {
              done();
            }
          }
        }).then();
    },
    async hasDatabaseCopyMessageValue(){
      let that = this
      that.databaseMessageDialog.mailboxCopyMessageRow.rowLoading = true
      that.DatabaseCopyMessage.count = 0
      let data = {'mailboxIdentity': that.databaseMessageDialog.echartsRowValue.databaseIdentity}
      let instance = axios.create({
        timeout: 1000000,
        headers: {'content-type': 'application/x-www-form-urlencoded'}
      })
      await instance.post(serverurlvaluefromjs.serverurl + '/exchange/getmailboxStatusMessage/', qs.stringify(data)).then(response => {
        if (response.data.isSuccess) {
          that.DatabaseCopyMessage.DatabaseCopyMessageList = response.data.message.message
          that.DatabaseCopyMessage.count = response.data.message.count
        } else {
          that.DatabaseCopyMessage.DatabaseCopyMessageList = []
        }
      })
      that.databaseMessageDialog.mailboxCopyMessageRow.rowLoading = false
    },
    async trendClickDosth(){
      let that = this
      var myChart = echarts.init(document.getElementById('bar_dv'))
      var Size_dv = echarts.init(document.getElementById('Size_dv'))
      var space_dv = echarts.init(document.getElementById('space_dv'))
      myChart.showLoading({
        text: '数据正在努力加载...',
        textStyle: {fontSize: 30, color: '#444'},
        effectOption: {backgroundColor: 'rgba(0, 0, 0, 0)'}
      })
      Size_dv.showLoading({
        text: '数据正在努力加载...',
        textStyle: {fontSize: 30, color: '#444'},
        effectOption: {backgroundColor: 'rgba(0, 0, 0, 0)'}
      })
      space_dv.showLoading({
        text: '数据正在努力加载...',
        textStyle: {fontSize: 30, color: '#444'},
        effectOption: {backgroundColor: 'rgba(0, 0, 0, 0)'}
      })
      let data = {'mailboxGuid': that.databaseMessageDialog.echartsRowValue.databaseGuid}
      let instance = axios.create({
        timeout: 1000000,
        headers: {'content-type': 'application/x-www-form-urlencoded'}
      })
      let xData_myChart = []
      let yData_myChart = []
      let yData_Size_dv = []
      let yData_space_dv = []
      await instance.post(serverurlvaluefromjs.serverurl + '/exchange/getmailboxaccounttrend/', qs.stringify(data)).then(response => {
        if (response.data.isSuccess) {
          xData_myChart = response.data.message['datetimeValueList']
          yData_myChart = response.data.message['accountList']
          yData_Size_dv = response.data.message['databaseSizeIntList']
          yData_space_dv = response.data.message['databaseSpaceProportion']
        }
      })
      myChart.setOption({
        title: { text: '邮箱数趋势' },
        tooltip: {
          trigger: 'axis',
          formatter:function(params){
            var msg=(params[0].name).replace('/','月') +' <br /> ';
            msg+=params[0].seriesName + " ：" + (params[0].value) + " 个"
            return msg;
          }
        },
        xAxis: {
          data: xData_myChart
        },
        grid: {
          top:"40px",
          left:"10px",
          right:"30px",
          bottom:"20px",
          containLabel : true
        },
        yAxis: {
          axisLine: {
            show: false
          },
        },
        series: [{
          name: '数量',
          type: 'line',
          data: yData_myChart
        }]
      })
      Size_dv.setOption({
        title: { text: '数据库大小趋势' },
        tooltip: {
          trigger: 'axis',
          formatter:function(params){
            var msg=(params[0].name).replace('/','月') +' <br /> ';
            for(let x in params){
              if((params[x].value/(1024*1024*1024*1024))>=1){
                msg+=params[x].seriesName+" : "+(params[x].value/(1024*1024*1024*1024)).toFixed(2)+' TB <br />';
              }else if((params[x].value/(1024*1024*1024))>=1){
                msg+=params[x].seriesName+" : "+(params[x].value/(1024*1024*1024)).toFixed(2)+' GB <br />';
              }else if((params[x].value/(1024*1024))>=1){
                msg+=params[x].seriesName+" : " +(params[x].value/(1024*1024)).toFixed(2)+' MB <br />';
              }else if((params[x].value/(1024))>=1){
                msg+=params[x].seriesName+" : "+(params[x].value/(1024)).toFixed(2)+" KB <br />";
              }else if((params[x].value/(1024))<1&&(params[x].value/(1024))>0){
                msg+=params[x].seriesName+" : "+params[x].value+" byte<br />";
              }else{
                msg+=params[x].seriesName+" : 0 byte<br />";
              }
            }
            return msg;
          }
        },
        xAxis: {
          data: xData_myChart
        },
        grid: {
          top:"40px",
          left:"10px",
          right:"30px",
          bottom:"20px",
          containLabel : true
        },
        yAxis: {
          axisLine: {
            show: false
          },
           axisLabel: {
            formatter: function(value,index){
                if((value/(1024*1024*1024*1024))>1){
                return (value/(1024*1024*1024*1024)).toFixed(2)+" TB";
                }else if((value/(1024*1024*1024))>1){
                return (value/(1024*1024*1024)).toFixed(2)+" GB";
                }else if((value/(1024*1024))>1){
                return (value/(1024*1024)).toFixed(2)+" MB";
                }else if((value/(1024))>1){
                return (value/(1024)).toFixed(2)+" KB";
                }else{
                return value+" byte";
                }
               }
           },
        },
        series: [{
          name: '大小',
          type: 'line',
          data: yData_Size_dv
        }]
      })
      space_dv.setOption({
        title: { text: '白空间占比趋势' },
        tooltip: {
          trigger: 'axis',
          formatter:function(params){
            var msg=(params[0].name).replace('/','月') +' <br /> ';
            msg+=params[0].seriesName + " ：" + ((params[0].value)/(10)).toFixed(2) + " %"
            return msg;
          }
        },
        xAxis: {
          data: xData_myChart
        },
        grid: {
          top:"40px",
          left:"10px",
          right:"30px",
          bottom:"20px",
          containLabel : true
        },
        yAxis: {
          axisLine: {
            show: false
          },
           axisLabel: {
            formatter: function(value,index){
                return (value/(10)).toFixed(2)+" %";
               }
           },
        },
        series: [{
          name: '占比',
          type: 'line',
          data: yData_space_dv
        }]
      })
      myChart.hideLoading()
      Size_dv.hideLoading()
      space_dv.hideLoading()
      that.hasDatabaseCopyMessageValue()
    },
    async tabledblClick(row, column, event) {
      let that = this
      that.databaseMessageDialog.echartsRowValue = row
      that.databaseMessageDialog.detailsVisible = true
      that.databaseMessageDialog.isConfigShow = false
      that.databaseMessageDialog.titleValue = row.databaseIdentity
    },
    async configDlog() {
      let that = this
      that.closechangemailboxSizeValue()
      that.closechangemailboxNumValue()
      that.configdata.detailsVisible = true
      that.configdata.dialogloading = true
      let instance = axios.create({
        timeout: 1000000,
        headers: {'content-type': 'application/x-www-form-urlencoded'}
      })
      let data = {}
      await instance.post(serverurlvaluefromjs.serverurl + '/exchange/searchmailboxconfig/', qs.stringify(data)).then(response => {
        if (response.data.isSuccess) {
          that.configdata.mailboxSizeCompanySelect.changeValue = response.data.message.mailboxSizeThresholdCompanyValue
          that.configdata.mailboxSizeCompanySelect.value = response.data.message.mailboxSizeThresholdCompanyValue
          that.configdata.changetextValue.mailboxSizeValue = response.data.message.mailboxSizeThresholdIntValue
          that.configdata.changetextValue.mailboxSizeValueChange = response.data.message.mailboxSizeThresholdIntValue
          that.configdata.changetextValue.mailboxNumValue = response.data.message.mailboxNumThresholdIntValue
          that.configdata.changetextValue.mailboxNumValueChange = response.data.message.mailboxNumThresholdIntValue
        }
      })
      that.configdata.dialogloading = false
    },
    closechangemailboxSizeValue() {
      let that = this
      that.configdata.changespanshow.changemailboxsizeshow = true
    },
    closechangemailboxNumValue() {
      let that = this
      that.configdata.changespanshow.changemailboxNumshow = true
    },
    async savechangemailboxSizeValue(saveType) {
      let that = this
      let instance = axios.create({
        timeout: 1000000,
        headers: {'content-type': 'application/x-www-form-urlencoded'}
      })
      let data = {'saveType':saveType,
      'mailboxSizeValueStr':that.configdata.changetextValue.mailboxSizeValueChange,'mailboxSizeValueCompany':that.configdata.mailboxSizeCompanySelect.changeValue,
      'mailboxNumValueStr':that.configdata.changetextValue.mailboxNumValueChange
      }
      await instance.post(serverurlvaluefromjs.serverurl + '/exchange/savemailboxconfig/', qs.stringify(data)).then(response => {
        if (response.data.isSuccess) {
          this.$message.success('保存成功');
          that.configDlog()
        } else {
          this.$message.error('保存失败');
        }
      })
    },
    async savechangemailboxLimitSizeValue(saveType,valueCompany,valueInt) {
      let that = this
      that.databaseMessageDialog.databaseMessageConfigSize.tagLoading = true
      let instance = axios.create({
        timeout: 1000000,
        headers: {'content-type': 'application/x-www-form-urlencoded'}
      })
      let data = {'saveType':saveType,'valueCompany':valueCompany,'valueInt':valueInt,'dbname':that.databaseMessageDialog.titleValue}
      await instance.post(serverurlvaluefromjs.serverurl + '/exchange/savemailboxSizelimit/', qs.stringify(data)).then(response => {
        if (response.data.isSuccess) {
          this.$message.success('保存成功');
          that.databaseMessageDialog.databaseMessageConfigSize.tagLoading = false
          that.databaseMessageconfigFuction();
        } else {
          this.$message({
            type: 'error',
            showClose: true,
            duration: 0,
            message: response.data.message
          });
          that.databaseMessageDialog.databaseMessageConfigSize.tagLoading = false
        }
      })
    },
    mailboxSizelimitValuewarningChangeFuction(typeValue) {
      let that = this
      that.databaseMessageDialog.databaseMessageConfigSize.changespanshow.warningchangemailboxsizeshow = typeValue
    },
    mailboxSizelimitValueProhibitSendChangeFuction(typeValue) {
      let that = this
      that.databaseMessageDialog.databaseMessageConfigSize.changespanshow.ProhibitSendchangemailboxsizeshow = typeValue
    },
    mailboxSizelimitValueProhibitSendReceiveChangeFuction(typeValue) {
      let that = this
      that.databaseMessageDialog.databaseMessageConfigSize.changespanshow.ProhibitSendReceivechangemailboxsizeshow = typeValue
    },
    mailboxSizeValueChangeFuction() {
      let that = this
      that.configdata.changespanshow.changemailboxsizeshow = false
    },
    mailboxNumValueChangeFuction() {
      let that = this
      that.configdata.changespanshow.changemailboxNumshow = false
    },
    async currentSel(selVal) {
      let that = this
      if (selVal.length) {
        that.mailboxList.allMailboxCountTitle = '查询到数据库：'
        that.mailboxList.tableData = []
        that.mailboxList.loading = true
        let instance = axios.create({
          timeout: 1000000,
          headers: {'content-type': 'application/x-www-form-urlencoded'}
        })
        let data = {'mailboxName':selVal[0],'typeValue':false}
        await instance.post(serverurlvaluefromjs.serverurl + '/exchange/searchmailboxvalue/', qs.stringify(data)).then(response => {
          if (response.data.isSuccess) {
            that.mailboxList.tableData = response.data.message
          }
        })
        that.mailboxList.loading = false
      } else{
        that.mailboxList.allMailboxCountTitle = '数据库共：'
        that.searchMailboxMessage()
      }
    },
    async remoteMethod(query) {
      let that = this
      if (query !== '') {
        let instance = axios.create({
          timeout: 1000000,
          headers: {'content-type': 'application/x-www-form-urlencoded'}
        })
        let data = {'mailboxName':query,'typeValue':true}
        await instance.post(serverurlvaluefromjs.serverurl + '/exchange/searchmailboxvalue/', qs.stringify(data)).then(response => {
          if (response.data.isSuccess) {
            that.mailboxList.mailboxSearchSelect.options = response.data.message
          }
        })
      }
    },
    async searchMailboxMessage () {
      let that = this
      that.mailboxList.tableData = []
      that.mailboxList.loading = true
      let instance = axios.create({
        timeout: 1000000,
        headers: {'content-type': 'application/x-www-form-urlencoded'}
      })
      let data = {}
      await instance.post(serverurlvaluefromjs.serverurl + '/exchange/searchmailboxmessage/', qs.stringify(data)).then(response => {
        if (response.data.isSuccess) {
          that.mailboxList.tableData = response.data.message
          that.mailboxList.loading = false
        } else {
          that.mailboxList.loading = false
        }
      })
    },
    async searchMailboxMessageconfig () {
      let that = this
      that.mailboxList.loading = true
      let instance = axios.create({
        timeout: 1000000,
        headers: {'content-type': 'application/x-www-form-urlencoded'}
      })
      let data = {}
      await instance.post(serverurlvaluefromjs.serverurl + '/exchange/searchmailboxconfig/', qs.stringify(data)).then(response => {
        if (response.data.isSuccess) {
          that.configdata.mailboxSizeValueStr = response.data.message['mailboxSizeThresholdIntValue']
          that.configdata.mailboxSizeValueint = Number(response.data.message['mailboxSizeThresholdInt'])
          that.configdata.mailboxNumValueint = Number(response.data.message['mailboxNumThresholdIntValue'])
          that.configdata.mailboxSizeValueStrCompany = response.data.message['mailboxSizeThresholdCompanyValue']
        }
      })
      that.mailboxList.loading = false
    },
    handleClick (tab) {
      // let that = this
      // if (tab.index === "0") {
      //   that.toconfigure()
      // } else if (tab.index === "1") {
      //   that.selectblackusername()
      // } else if (tab.index === "2") {
      //   that.selectblackip()
      // } else if (tab.index === "3") {
      //   that.selectblackuseragent()
      // }
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
