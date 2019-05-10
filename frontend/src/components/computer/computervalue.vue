<template>
  <el-col :span="24">
  <el-table :data="tableData2"  style="width: 100%" :show-header="false" v-cloak>
    <el-table-column width="180">
      <template slot-scope="scope">
        <el-tooltip class="item" effect="light" content="cn" placement="left-start"><span>&nbsp;计算机名：</span></el-tooltip>
      </template>
    </el-table-column>
    <el-table-column>
      <template slot-scope="scope">
        <span v-text="cn"></span>
      </template>
    </el-table-column>
  </el-table>
  <el-table :data="tableData2"  style="width: 100%" :show-header="false" v-cloak>
    <el-table-column width="180">
      <template slot-scope="scope">
        <el-tooltip class="item" effect="light" content="dNSHostName" placement="left-start"><span>&nbsp;DNS 名称：</span></el-tooltip>
      </template>
    </el-table-column>
    <el-table-column>
      <template slot-scope="scope">
        <span v-text="dNSHostName"></span>
      </template>
    </el-table-column>
  </el-table>
  <el-table :data="tableData2"  style="width: 100%" :show-header="false" v-cloak>
    <el-table-column width="180">
      <template slot-scope="scope">
        <el-tooltip class="item" effect="light" content="operatingSystem" placement="left-start"><span>&nbsp;操作系统名称：</span></el-tooltip>
      </template>
    </el-table-column>
    <el-table-column>
      <template slot-scope="scope">
        <span v-text="operatingSystem"></span>
      </template>
    </el-table-column>
  </el-table>
  <el-table :data="tableData2"  style="width: 100%" :show-header="false" v-cloak>
    <el-table-column width="180">
      <template slot-scope="scope">
        <el-tooltip class="item" effect="light" content="operatingSystemVersion" placement="left-start"><span>&nbsp;操作系统版本：</span></el-tooltip>
      </template>
    </el-table-column>
    <el-table-column>
      <template slot-scope="scope">
        <span v-text="operatingSystemVersion"></span>
      </template>
    </el-table-column>
  </el-table>
  <el-table :data="tableData2"  style="width: 100%" :show-header="false" v-cloak>
    <el-table-column width="180">
      <template slot-scope="scope">
        <el-tooltip class="item" effect="light" content="operatingSystemServicePack" placement="left-start"><span>&nbsp;Service Pack：</span></el-tooltip>
      </template>
    </el-table-column>
    <el-table-column>
      <template slot-scope="scope">
        <span v-text="operatingSystemServicePack"></span>
      </template>
    </el-table-column>
  </el-table>
  <el-table :data="tableData2"  style="width: 100%" :show-header="false" v-cloak>
    <el-table-column width="180">
      <template slot-scope="scope">
        <el-tooltip class="item" effect="light" content="distinguishedName" placement="left-start"><span>&nbsp;DN：</span></el-tooltip>
      </template>
    </el-table-column>
    <el-table-column>
      <template slot-scope="scope">
        <span v-text="DN"></span>
      </template>
    </el-table-column>
  </el-table>
  <el-table :data="tableData2" style="width: 100%" :show-header="false" v-cloak v-if="changespanshow.changeallAccidentallyDeletedshow">
    <el-table-column width="180">
      <template slot-scope="scope">
        <el-tooltip class="item" effect="light" content="AccidentallyDeleted" placement="left-start"><span>&nbsp;防删除：</span></el-tooltip>
          <span style="font-size:130%;" v-if="changespanshow.changeAccidentallyDeletedshow" :class="[classname.classSpanFloatRight,classname.classSpancursorpointer]" @click="changespanshow.changeAccidentallyDeletedshow = false,  AccidentallyDeletedchangevalue = AccidentallyDeleted"><i class="el-icon-edit-outline"></i></span>
      </template>
    </el-table-column>
    <el-table-column>
      <template slot-scope="scope">
        <div>
          <el-col :span="8">
            <!-- <el-checkbox v-model="AccidentallyDeletedchangevalue" :disabled="changespanshow.changeAccidentallyDeletedshow"></el-checkbox>&nbsp;&nbsp;防止对象被意外删除 -->
            <el-checkbox v-model="AccidentallyDeletedchangevalue" v-if="!changespanshow.changeAccidentallyDeletedshow" label="防止对象被意外删除"></el-checkbox>
            <el-checkbox v-model="AccidentallyDeletedchangevalue" v-else onclick="return false" label="  防止对象被意外删除"></el-checkbox>
          </el-col>
          <el-col :span="6" style="margin-left:auto;margin-right:auto;" v-if="!changespanshow.changeAccidentallyDeletedshow">
            &nbsp;<span :class="classname.classSpancursorpointer" v-loading.fullscreen.lock="vLoadingShow" @click="savechangeAccidentallyDeleted"><i class="el-icon-upload2" style="font-size:150%;"></i></span>
            <span @click="changespanshow.changeAccidentallyDeletedshow = true, AccidentallyDeletedchangevalue = AccidentallyDeleted" :class="classname.classSpancursorpointer"><i class="el-icon-close" style="font-size:150%;"></i></span>
          </el-col>
        </div>
      </template>
    </el-table-column>
  </el-table>
</el-col>
</template>
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
// import Vue from 'vue'
import qs from 'qs'
axios.defaults.withCredentials = true
export default{
  data () {
    return {
      classname: {
        classSpanFloatRight: 'classSpanFloatRight',
        classSpancursorpointer: 'classSpancursorpointer'
      },
      changespanshow: {
        changeAccidentallyDeletedshow: true,
        changeallAccidentallyDeletedshow: false
      },
      AccidentallyDeleted: false, // 是否防删除
      AccidentallyDeletedchangevalue: false, // 是否防删除变更值
      vLoadingShow: false, // 读条全屏遮罩
      cn: null, // cn
      DN: null, // DN
      dNSHostName: null, // dNSHostName
      operatingSystem: null, // operatingSystem  操作系统
      operatingSystemVersion: null, // operatingSystemVersion  操作系统版本
      operatingSystemServicePack: null, // operatingSystemServicePack  ServicePack
      tableData2: [{
        date: 'displayName'
      }]
    }
  },
  methods: {
    getcomputermessagevalue: function () {
      const loading = this.$loading({
        lock: true
      })
      let disNameforurl = this.getQueryVariable('disName')
      axios
        .get(this.serviceurl() + '/api/GetCompMessage/?CountName=' + disNameforurl)
        .then(response => {
          loading.close()
          if (response.data.isSuccess) {
            this.dNSHostName = response.data.message.dNSHostName
            this.cn = response.data.message.cn
            this.DN = response.data.message.distinguishedName
            this.operatingSystem = response.data.message.operatingSystem
            this.operatingSystemVersion = response.data.message.operatingSystemVersion
            this.operatingSystemServicePack = response.data.message.operatingSystemServicePack
            var instance = axios.create({
              headers: {'content-type': 'application/x-www-form-urlencoded'}
            })
            let data = {sAMAccountName: disNameforurl}
            this.changespanshow.changeallAccidentallyDeletedshow = false
            instance.post(this.serviceurl() + '/canAccidentallyDeleted/', qs.stringify(data)).then(response => {
              if (response.data.isSuccess) {
                this.changespanshow.changeallAccidentallyDeletedshow = true
                if (response.data.ResultCode === -1 || response.data.ResultCode === '-1') {
                // if (response.data.message.ResultCode === -1) {
                  this.AccidentallyDeleted = false
                  this.AccidentallyDeletedchangevalue = false
                } else {
                  this.AccidentallyDeleted = true
                  this.AccidentallyDeletedchangevalue = true
                }
              } else {
                this.changespanshow.changeallAccidentallyDeletedshow = false
              }
            })
          } else {
            if (response.data.message === '权限不足') {
              this.messagealertvalue('权限不足', 'error')
            } else {
              this.messagealertvalue('加载失败', 'error')
            }
          }
        })
        .catch(function () {
          this.messagealertvalue('加载失败', 'error')
        })
    },
    savechangeAccidentallyDeleted: function () {
      this.vLoadingShow = true
      let disNameforurl = this.getQueryVariable('disName')
      var instance = axios.create({
        headers: {'content-type': 'application/x-www-form-urlencoded'}
      })
      let data = {sAMAccountName: disNameforurl, prevent: this.AccidentallyDeletedchangevalue}
      instance.post(this.serviceurl() + '/setAccidentallyDeleted/', qs.stringify(data)).then(response => {
        this.vLoadingShow = false
        if (response.data.isSuccess) {
          this.messagealertvalue('修改成功', 'success')
          this.AccidentallyDeleted = this.AccidentallyDeletedchangevalue
          this.changespanshow.changeAccidentallyDeletedshow = true
        } else {
          if (response.data.message === '权限不足') {
            this.messagealertvalue('权限不足', 'error')
          } else {
            this.messagealertvalue('修改失败', 'error')
          }
        }
      })
    }
  },
  created: function () {
    this.getcomputermessagevalue()
  }
}
</script>
<style>
</style>
