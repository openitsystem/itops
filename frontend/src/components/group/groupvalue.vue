<template>
  <el-col :span="24">
  <el-table :data="tableData2"  style="width: 100%" :show-header="false" v-cloak>
    <el-table-column width="180">
      <template slot-scope="scope">
        <el-tooltip class="item" effect="light" content="cn" placement="left-start"><span>&nbsp;组名：</span></el-tooltip>
        <span style="font-size:130%;" v-if="changespanshow.changecnshow" :class="[classname.classSpanFloatRight,classname.classSpancursorpointer]" @click="cnChangevalue = cn, changespanshow.changecnshow = false"><i class="el-icon-edit-outline"></i></span>
      </template>
    </el-table-column>
    <el-table-column>
      <template slot-scope="scope">
        <span v-if="changespanshow.changecnshow" v-text="cn"></span>
        <div v-else >
          <el-col :span="6">
            <el-input size="small" v-model="cnChangevalue"></el-input>
          </el-col>
          <el-col :span="6" style="margin-left:auto;margin-right:auto;">
            &nbsp;<span :class="classname.classSpancursorpointer" v-loading.fullscreen.lock="vLoadingShow" @click="savechangecn"><i class="el-icon-upload2" style="font-size:150%;"></i></span>
            <span @click="changespanshow.changecnshow = true" :class="classname.classSpancursorpointer"><i class="el-icon-close" style="font-size:150%;"></i></span>
          </el-col>
        </div>
      </template>
    </el-table-column>
  </el-table>
  <el-table :data="tableData2"  style="width: 100%" :show-header="false" v-cloak>
    <el-table-column width="180">
      <template slot-scope="scope">
        <el-tooltip class="item" effect="light" content="displayName" placement="left-start"><span>&nbsp;显示名称：</span></el-tooltip>
        <span style="font-size:130%;" v-if="changespanshow.changedisplayNameshow" :class="[classname.classSpanFloatRight,classname.classSpancursorpointer]" @click="displayNameChangevalue = displayName, changespanshow.changedisplayNameshow = false"><i class="el-icon-edit-outline"></i></span>
      </template>
    </el-table-column>
    <el-table-column>
      <template slot-scope="scope">
        <span v-if="changespanshow.changedisplayNameshow" v-text="displayName"></span>
        <div v-else >
          <el-col :span="6">
            <el-input size="small" v-model="displayNameChangevalue"></el-input>
          </el-col>
          <el-col :span="6" style="margin-left:auto;margin-right:auto;">
            &nbsp;<span :class="classname.classSpancursorpointer" v-loading.fullscreen.lock="vLoadingShow" @click="savechangedisplayName"><i class="el-icon-upload2" style="font-size:150%;"></i></span>
            <span @click="changespanshow.changedisplayNameshow = true" :class="classname.classSpancursorpointer"><i class="el-icon-close" style="font-size:150%;"></i></span>
          </el-col>
        </div>
      </template>
    </el-table-column>
  </el-table>
  <el-table :data="tableData2"  style="width: 100%" :show-header="false" v-cloak>
    <el-table-column width="180">
      <template slot-scope="scope">
        <el-tooltip class="item" effect="light" content="sAMAccountName" placement="left-start"><span>&nbsp;组名称：</span></el-tooltip>
        <span style="font-size:130%;" v-if="changespanshow.changeSamAccountNameshow" :class="[classname.classSpanFloatRight,classname.classSpancursorpointer]" @click="SamAccountNameChangevalue = SamAccountName, changespanshow.changeSamAccountNameshow = false"><i class="el-icon-edit-outline"></i></span>
      </template>
    </el-table-column>
    <el-table-column>
      <template slot-scope="scope">
        <span v-if="changespanshow.changeSamAccountNameshow" v-text="SamAccountName"></span>
        <div v-else >
          <el-col :span="6">
            <el-input size="small" v-model="SamAccountNameChangevalue"></el-input>
          </el-col>
          <el-col :span="6" style="margin-left:auto;margin-right:auto;">
            &nbsp;<span :class="classname.classSpancursorpointer" v-loading.fullscreen.lock="vLoadingShow" @click="savechangeSamAccountName"><i class="el-icon-upload2" style="font-size:150%;"></i></span>
            <span @click="changespanshow.changeSamAccountNameshow = true" :class="classname.classSpancursorpointer"><i class="el-icon-close" style="font-size:150%;"></i></span>
          </el-col>
        </div>
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
  <el-table :data="tableData2"  style="width: 100%" :show-header="false" v-cloak>
    <el-table-column width="180">
      <template slot-scope="scope">
        <el-tooltip class="item" effect="light" content="description" placement="left-start"><span>&nbsp;描述：</span></el-tooltip>
        <span style="font-size:130%;" v-if="changespanshow.changedescriptionshow" :class="[classname.classSpanFloatRight,classname.classSpancursorpointer]" @click="descriptionChangevalue = description, changespanshow.changedescriptionshow = false"><i class="el-icon-edit-outline"></i></span>
      </template>
    </el-table-column>
    <el-table-column>
      <template slot-scope="scope">
        <span v-if="changespanshow.changedescriptionshow" v-text="description"></span>
        <div v-else >
          <el-col :span="6">
            <el-input size="small" v-model="descriptionChangevalue"></el-input>
          </el-col>
          <el-col :span="6" style="margin-left:auto;margin-right:auto;">
            &nbsp;<span :class="classname.classSpancursorpointer" v-loading.fullscreen.lock="vLoadingShow" @click="savechangedescription"><i class="el-icon-upload2" style="font-size:150%;"></i></span>
            <span @click="changespanshow.changedescriptionshow = true" :class="classname.classSpancursorpointer"><i class="el-icon-close" style="font-size:150%;"></i></span>
          </el-col>
        </div>
      </template>
    </el-table-column>
  </el-table>
  <el-table :data="tableData2"  style="width: 100%" :show-header="false" v-cloak>
    <el-table-column width="180">
      <template slot-scope="scope">
        <el-tooltip class="item" effect="light" content="info" placement="left-start"><span>&nbsp;注释：</span></el-tooltip>
        <span style="font-size:130%;" v-if="changespanshow.changeinfoshow" :class="[classname.classSpanFloatRight,classname.classSpancursorpointer]" @click="infoChangevalue = info, changespanshow.changeinfoshow = false"><i class="el-icon-edit-outline"></i></span>
      </template>
    </el-table-column>
    <el-table-column>
      <template slot-scope="scope">
        <span v-if="changespanshow.changeinfoshow" v-text="info"></span>
        <div v-else >
          <el-col :span="6">
            <el-input size="small" v-model="infoChangevalue"></el-input>
          </el-col>
          <el-col :span="6" style="margin-left:auto;margin-right:auto;">
            &nbsp;<span :class="classname.classSpancursorpointer" v-loading.fullscreen.lock="vLoadingShow" @click="savechangeinfo"><i class="el-icon-upload2" style="font-size:150%;"></i></span>
            <span @click="changespanshow.changeinfoshow = true" :class="classname.classSpancursorpointer"><i class="el-icon-close" style="font-size:150%;"></i></span>
          </el-col>
        </div>
      </template>
    </el-table-column>
  </el-table>
  <el-table :data="tableData2"  style="width: 100%" :show-header="false" v-cloak>
    <el-table-column width="180">
      <template slot-scope="scope">
        <el-tooltip class="item" effect="light" content="info" placement="left-start"><span>&nbsp;组类型：</span></el-tooltip>
        <span style="font-size:130%;" :class="[classname.classSpanFloatRight,classname.classSpancursorpointer]" @click="changegrouptype"><i class="el-icon-edit-outline"></i></span>
      </template>
    </el-table-column>
    <el-table-column>
      <template slot-scope="scope">
        <span v-if="groupType === 2" v-text="groupTypemessage.groupTypevalue2"></span>
        <span v-else-if="groupType === 4" v-text="groupTypemessage.groupTypevalue4"></span>
        <span v-else-if="groupType === 8" v-text="groupTypemessage.groupTypevalue8"></span>
        <span v-else-if="groupType === -2147483646" v-text="groupTypemessage.groupTypevalue2147483646"></span>
        <span v-else-if="groupType === -2147483644" v-text="groupTypemessage.groupTypevalue2147483644"></span>
        <span v-else-if="groupType === -2147483640" v-text="groupTypemessage.groupTypevalue2147483640"></span>
        <span v-else v-text="groupTypemessage.groupTypevalue"></span>
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
  <el-table :data="tableData2"  style="width: 100%" :show-header="false" v-cloak>
    <el-table-column width="180">
      <template slot-scope="scope">
        <el-tooltip class="item" effect="light" content="whenChanged" placement="left-start"><span>&nbsp;修改时间：</span></el-tooltip>
      </template>
    </el-table-column>
    <el-table-column>
      <template slot-scope="scope">
        <span v-text="whenChanged"></span>
      </template>
    </el-table-column>
  </el-table>
  <el-table :data="tableData2"  style="width: 100%" :show-header="false" v-cloak>
    <el-table-column width="180">
      <template slot-scope="scope">
        <el-tooltip class="item" effect="light" content="whenCreated" placement="left-start"><span>&nbsp;创建时间：</span></el-tooltip>
      </template>
    </el-table-column>
    <el-table-column>
      <template slot-scope="scope">
        <span v-text="whenCreated"></span>
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
  <el-dialog
  title="修改密码"
  :visible.sync="dialogVisible"
  width="60%">
  <p>
    <span>&nbsp;组作用域：</span>
    &nbsp;<el-radio-group v-model="groupdomailvalue">
    <el-radio :label="3" :disabled="grouptypelocalShow">本地域</el-radio>
    <el-radio :label="6" :disabled="grouptypeallShow">全局</el-radio>
    <el-radio :label="9">通用</el-radio>
  </el-radio-group>
  </p>
  <p>
    <span>&nbsp;组类型：</span>
    &nbsp;<el-radio-group v-model="grouptypevaluemessage">
    <el-radio :label="3">安全组</el-radio>
    <el-radio :label="6">通讯组</el-radio>
  </el-radio-group>
  </p>
  <span slot="footer" class="dialog-footer">
    <el-button @click="dialogVisible = false">取 消</el-button>
    <el-button type="primary" @click="savegrouptypechange">确 定</el-button>
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
import qs from 'qs'
import moment from 'moment'
axios.defaults.withCredentials = true
export default{
  data () {
    return {
      classname: {
        classSpanFloatRight: 'classSpanFloatRight',
        classSpancursorpointer: 'classSpancursorpointer'
      },
      groupTypemessage: {
        groupTypevalue2: '通讯组 - 全局',
        groupTypevalue4: '通讯组 - 本地域',
        groupTypevalue8: '通讯组 - 通用',
        groupTypevalue2147483646: '安全组 - 全局',
        groupTypevalue2147483644: '安全组 - 本地域',
        groupTypevalue2147483640: '安全组 - 通用',
        groupTypevalue: '组'
      },
      changespanshow: {
        changecnshow: true,
        changedisplayNameshow: true,
        changemailshow: true,
        changedescriptionshow: true,
        changeSamAccountNameshow: true,
        changeAccidentallyDeletedshow: true,
        changeallAccidentallyDeletedshow: false,
        changeinfoshow: true
      },
      AccidentallyDeleted: false, // 是否防删除
      AccidentallyDeletedchangevalue: false, // 是否防删除变更值
      groupdomailvalue: 0,
      grouptypevaluemessage: 0,
      grouptypelocalShow: true,
      grouptypeallShow: true,
      vLoadingShow: false, // 读条全屏遮罩
      dialogVisible: false, // 更改组类型
      cn: null, // cn
      DN: null, // DN
      displayName: null, // displayName
      cnChangevalue: null, // cn
      displayNameChangevalue: null, // displayName
      SamAccountName: null, // SamAccountName
      SamAccountNameChangevalue: null, // SamAccountName
      mail: null, // mail
      mailChangevalue: null, // mail
      description: null, // 描述
      descriptionChangevalue: null, // 描述
      infoChangevalue: null, // 注释
      info: null, // 注释
      whenCreated: null, // 创建时间
      whenChanged: null, // 修改时间
      groupType: 8, // 修改时间
      tableData2: [{
        date: 'displayName'
      }]
    }
  },
  created: async function () {
    const loading = this.$loading({
      lock: true
    })
    let disNameforurl = this.getQueryVariable('disName')
    await axios
      .get(this.serviceurl() + '/api/GetGroupPreMessage/?CountName=' + disNameforurl)
      .then(response => {
        loading.close()
        if (response.data.isSuccess) {
          this.groupType = response.data.message.groupType
          this.cn = response.data.message.cn
          this.displayName = response.data.message.displayName
          this.SamAccountName = response.data.message.sAMAccountName
          this.mail = response.data.message.mail
          this.info = response.data.message.info
          this.DN = response.data.message.distinguishedName
          this.whenCreated = moment(String(response.data.message.whenCreated)).format('YYYY-MM-DD HH:mm:ss')
          this.whenChanged = moment(String(response.data.message.whenChanged)).format('YYYY-MM-DD HH:mm:ss')
          this.description = response.data.message.description[0]
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
  methods: {
    savegrouptypechange: function () {
      let lastmessagevalue = 0
      if (this.groupdomailvalue === 3) {
        if (this.grouptypevaluemessage === 3) {
          lastmessagevalue = -2147483644
        } else if (this.grouptypevaluemessage === 6) {
          lastmessagevalue = 4
        }
      } else if (this.groupdomailvalue === 6) {
        if (this.grouptypevaluemessage === 3) {
          lastmessagevalue = -2147483646
        } else if (this.grouptypevaluemessage === 6) {
          lastmessagevalue = 2
        }
      } else if (this.groupdomailvalue === 9) {
        if (this.grouptypevaluemessage === 3) {
          lastmessagevalue = -2147483640
        } else if (this.grouptypevaluemessage === 6) {
          lastmessagevalue = 8
        }
      }
      if (lastmessagevalue === 0) {
        this.messagealertvalue('群组类型选择出错', 'error')
      } else {
        axios
          .get(this.serviceurl() + '/api/ChangeUserMessage/?CountName=' + this.SamAccountName + '&Attributes=groupType&ChangeMessage=' + lastmessagevalue)
          .then(response => {
            if (response.data.isSuccess) {
              this.messagealertvalue('修改成功', 'success')
              this.groupType = lastmessagevalue
            } else {
              if (response.data.message === '权限不足') {
                this.messagealertvalue('权限不足', 'error')
              } else {
                this.messagealertvalue('修改失败', 'error')
              }
            }
            this.dialogVisible = false
          })
          .catch(function () {
            this.messagealertvalue('修改失败', 'error')
            this.dialogVisible = false
          })
      }
    },
    changegrouptype: function () {
      this.grouptypelocalShow = false
      this.grouptypeallShow = false
      this.dialogVisible = true
      if (this.groupType === 2) {
        this.groupdomailvalue = 6
        this.grouptypevaluemessage = 6
        this.grouptypelocalShow = true
      } else if (this.groupType === 4) {
        this.groupdomailvalue = 3
        this.grouptypevaluemessage = 6
        this.grouptypeallShow = true
      } else if (this.groupType === 8) {
        this.groupdomailvalue = 9
        this.grouptypevaluemessage = 6
      } else if (this.groupType === -2147483646) {
        this.groupdomailvalue = 6
        this.grouptypevaluemessage = 3
        this.grouptypelocalShow = true
      } else if (this.groupType === -2147483644) {
        this.groupdomailvalue = 3
        this.grouptypevaluemessage = 3
        this.grouptypeallShow = true
      } else if (this.groupType === -2147483640) {
        this.groupdomailvalue = 9
        this.grouptypevaluemessage = 3
      }
    },
    ChangeUserMessagefuction: function (Attributesvalue, ChangeMessagevalue) {
      this.vLoadingShow = true
      axios
        .get(this.serviceurl() + '/api/ChangeUserMessage/?CountName=' + this.SamAccountName + '&Attributes=' + Attributesvalue + '&ChangeMessage=' + ChangeMessagevalue)
        .then(response => {
          if (response.data.isSuccess) {
            this.messagealertvalue('修改成功', 'success')
            if (Attributesvalue === 'givenName') {
              this.givenName = this.givenNameChangevalue
              this.changespanshow.changegivenNameshow = true
            } else if (Attributesvalue === 'description') {
              this.description = this.descriptionChangevalue
              this.changespanshow.changedescriptionshow = true
            } else if (Attributesvalue === 'info') {
              this.info = this.infoChangevalue
              this.changespanshow.changeinfoshow = true
            } else if (Attributesvalue === 'cn') {
              this.cn = this.cnChangevalue
              this.changespanshow.changecnshow = true
              window.location.search = '?disName=' + this.SamAccountName
            } else if (Attributesvalue === 'displayName') {
              this.displayName = this.displayNameChangevalue
              this.changespanshow.changedisplayNameshow = true
            } else if (Attributesvalue === 'SamAccountName') {
              this.SamAccountName = this.SamAccountNameChangevalue
              this.changespanshow.changeSamAccountNameshow = true
              window.location.search = '?disName=' + this.SamAccountNameChangevalue
            } else if (Attributesvalue === 'accountExpires') {
              this.accountExpires = '1601-01-01 00:00:00+00:00'
              this.changespanshow.changeaccountExpiresshow = true
            }
          } else {
            if (response.data.message === '权限不足') {
              this.messagealertvalue('权限不足', 'error')
            } else {
              this.messagealertvalue('修改失败', 'error')
            }
          }
          this.vLoadingShow = false
        })
        .catch(function () {
          this.messagealertvalue('修改失败', 'error')
          this.vLoadingShow = false
        })
    },
    savechangecn: function () {
      this.vLoadingShow = true
      axios
        .get(this.serviceurl() + '/api/ChangeDN/?CountName=' + this.SamAccountName + '&newName=' + this.cnChangevalue)
        .then(response => {
          if (response.data.isSuccess) {
            this.messagealertvalue('修改成功', 'success')
            this.cn = this.cnChangevalue
            this.changespanshow.changecnshow = true
          } else {
            if (response.data.message === '权限不足') {
              this.messagealertvalue('权限不足', 'error')
            } else {
              this.messagealertvalue('修改失败', 'error')
            }
          }
          this.vLoadingShow = false
        })
        .catch(function () {
          this.messagealertvalue('修改失败', 'error')
          this.vLoadingShow = false
        })
    },
    savechangeSamAccountName: function () {
      this.ChangeUserMessagefuction('SamAccountName', this.SamAccountNameChangevalue)
    },
    savechangedisplayName: function () {
      this.ChangeUserMessagefuction('displayName', this.displayNameChangevalue)
    },
    savechangedescription: function () {
      this.ChangeUserMessagefuction('description', this.descriptionChangevalue)
    },
    savechangeinfo: function () {
      this.ChangeUserMessagefuction('info', this.infoChangevalue)
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
  }
}
</script>
<style>
</style>
