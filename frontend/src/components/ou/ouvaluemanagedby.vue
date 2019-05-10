<template>
  <el-col :span="24">
  <el-table :data="tableData2"  style="width: 100%" :show-header="false" v-cloak>
    <el-table-column width="180">
      <template slot-scope="scope">
        <el-tooltip class="item" effect="light" content="managedBy" placement="left-start"><span>&nbsp;管理者：</span></el-tooltip>
        <el-tooltip class="item" effect="light" content="修改管理者" placement="top">
          <span style="font-size:130%;" :class="[classname.classSpanFloatRight,classname.classSpancursorpointer]" @click="dialogVisible = true ,value9 = []"><i class="el-icon-edit-outline"></i></span>
        </el-tooltip>
      </template>
    </el-table-column>
    <el-table-column>
      <template slot-scope="scope">
        <span v-text="managedBy"></span>
      </template>
    </el-table-column>
  </el-table>
  <el-table :data="tableData2"  style="width: 100%" :show-header="false" v-cloak>
    <el-table-column width="180">
      <template slot-scope="scope">
        <el-tooltip class="item" effect="light" content="telephoneNumber" placement="left-start"><span>&nbsp;电话号码：</span></el-tooltip>
      </template>
    </el-table-column>
    <el-table-column>
      <template slot-scope="scope">
        <span v-text="telephoneNumber"></span>
      </template>
    </el-table-column>
  </el-table>
  <el-table :data="tableData2"  style="width: 100%" :show-header="false" v-cloak>
    <el-table-column width="180">
      <template slot-scope="scope">
        <el-tooltip class="item" effect="light" content="sAMAccountName" placement="left-start"><span>&nbsp;用户登录名：</span></el-tooltip>
      </template>
    </el-table-column>
    <el-table-column>
      <template slot-scope="scope">
        <span v-text="sAMAccountName"></span>
      </template>
    </el-table-column>
  </el-table>
  <el-table :data="tableData2"  style="width: 100%" :show-header="false" v-cloak>
    <el-table-column width="180">
      <template slot-scope="scope">
        <el-tooltip class="item" effect="light" content="cn" placement="left-start"><span>&nbsp;全名：</span></el-tooltip>
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
        <el-tooltip class="item" effect="light" content="physicalDeliveryOfficeName" placement="left-start"><span>&nbsp;办公室：</span></el-tooltip>
      </template>
    </el-table-column>
    <el-table-column>
      <template slot-scope="scope">
        <span v-text="physicalDeliveryOfficeName"></span>
      </template>
    </el-table-column>
  </el-table>
  <el-table :data="tableData2"  style="width: 100%" :show-header="false" v-cloak>
    <el-table-column width="180">
      <template slot-scope="scope">
        <el-tooltip class="item" effect="light" content="mail" placement="left-start"><span>&nbsp;电子邮件：</span></el-tooltip>
      </template>
    </el-table-column>
    <el-table-column>
      <template slot-scope="scope">
        <span v-text="mail"></span>
      </template>
    </el-table-column>
  </el-table>
  <el-dialog
    title="更改管理者"
    :visible.sync="dialogVisible"
    width="60%"
    center>
    <el-select
    v-model="value9"
    multiple
    filterable
    remote
    :multiple-limit = 1
    placeholder="请输入管理者关键信息"
    :remote-method="remoteMethod"
    :loading="loading"
    style="width: 90%">
      <el-option
        v-for="item in options4"
        :key="item.sAMAccountName"
        :label="item.sAMAccountName + ' (' + item.displayName + ')'"
        :value="item.distinguishedName">
      </el-option>
    </el-select>
    <span slot="footer" class="dialog-footer">
      <el-button @click="dialogVisible = false">取 消</el-button>
      <el-button type="primary" @click="changemanagergroup">确 定</el-button>
    </span>
  </el-dialog>
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
// import qs from 'qs'
axios.defaults.withCredentials = true
export default{
  data () {
    return {
      classname: {
        classSpanFloatRight: 'classSpanFloatRight',
        classSpancursorpointer: 'classSpancursorpointer'
      },
      changespanshow: {
        changecnshow: true
      },
      dialogVisible: false,
      loading: false,
      options4: [],
      value9: [],
      vLoadingShow: false, // 读条全屏遮罩
      managedBy: null, // managedBy管理者
      telephoneNumber: null, // 电话号码
      sAMAccountName: null, // 用户登录名
      cn: null, // 全名
      physicalDeliveryOfficeName: null, // 办公室
      mail: null, // 电子邮件
      tableData2: [{
        date: 'displayName'
      }]
    }
  },
  methods: {
    getmanagermessagevalue: function () {
      const loading = this.$loading({
        lock: true
      })
      let disNameforurl = this.getQueryVariabledecode('disName')
      axios
        .get(this.serviceurl() + '/api/GetUserMessage/?CountName=' + disNameforurl + '&objectClass=DN')
        .then(response => {
          loading.close()
          if (response.data.isSuccess) {
            this.managedBy = response.data.message.managedBy
            axios
              .get(this.serviceurl() + '/api/GetUserMessage/?CountName=' + response.data.message.managedBy + '&objectClass=DN')
              .then(response => {
                if (response.data.isSuccess) {
                  this.telephoneNumber = response.data.message.telephoneNumber
                  this.sAMAccountName = response.data.message.sAMAccountName
                  this.cn = response.data.message.cn
                  this.physicalDeliveryOfficeName = response.data.message.physicalDeliveryOfficeName
                  this.mail = response.data.message.mail
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
    savechangecn: function () {
      console.log()
    },
    remoteMethod: function (query) {
      if (query !== '') {
        this.loading = true
        axios
          .get(this.serviceurl() + '/api/GetOnlyConMessage/?username=' + query)
          .then(response => {
            if (response.data.isSuccess) {
              this.options4 = response.data.message
            } else {
              this.options4 = []
            }
            this.loading = false
          })
          .catch(function () {
            this.options4 = []
            this.loading = false
          })
      } else {
        this.options4 = []
      }
    },
    changemanagergroup: function () {
      this.loading = true
      let disNameforurl = this.getQueryVariable('disName')
      axios
        .get(this.serviceurl() + '/api/ChangeUserMessage/?CountName=' + disNameforurl + '&Attributes=managedBy&types=ou&ChangeMessage=' + this.value9)
        .then(response => {
          if (response.data.isSuccess) {
            this.messagealertvalue('修改成功', 'success')
            this.getmanagermessagevalue()
            this.dialogVisible = false
          } else {
            if (response.data.message === '权限不足') {
              this.messagealertvalue('权限不足', 'error')
            } else {
              this.messagealertvalue('修改失败', 'error')
            }
          }
          this.loading = false
        })
        .catch(function () {
          this.messagealertvalue('修改失败', 'error')
          this.loading = false
        })
    }
  },
  created: function () {
    this.getmanagermessagevalue()
  }
}
</script>
<style>
</style>
