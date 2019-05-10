<template>
  <el-col :span="24" v-if="hassmtpvalue">
  <el-menu class="el-menu-demo" mode="horizontal">
    <!-- <el-menu-item @click="addsmtpvalue" index="2">新增smtp地址</el-menu-item> -->
    <el-submenu index="1">
      <template slot="title">邮箱设置</template>
      <el-menu-item @click="addsmtpvalue" index="1-1">新增smtp地址</el-menu-item>
    </el-submenu>
    <!-- <el-menu-item index="4">邮箱功能</el-menu-item> -->
  </el-menu>
  <!-- <el-button round @click="addsmtpvalue">新增smtp地址</el-button> -->
  <el-table :data="tableData2"  style="width: 100%" :show-header="false" v-cloak>
    <el-table-column width="180">
      <template slot-scope="scope">
        <el-tooltip class="item" effect="light" content="Alias" placement="left-start"><span>&nbsp;别名：</span></el-tooltip>
        <span style="font-size:130%;" v-if="changespanshow.changeAliasshow" :class="[classname.classSpanFloatRight,classname.classSpancursorpointer]" @click="changespanshow.changeAliasshow = false, AliasChangevalue = Alias"><i class="el-icon-edit-outline"></i></span>
      </template>
    </el-table-column>
    <el-table-column>
      <template slot-scope="scope">
        <span v-if="changespanshow.changeAliasshow" v-text="Alias"></span>
        <div v-else >
          <el-col :span="6">
            <el-input size="small" v-model="AliasChangevalue"></el-input>
          </el-col>
          <el-col :span="6" style="margin-left:auto;margin-right:auto;">
            &nbsp;<span :class="classname.classSpancursorpointer" v-loading.fullscreen.lock="vLoadingShow" @click="changemailboxvalue('Alias' ,AliasChangevalue)"><i class="el-icon-upload2" style="font-size:150%;"></i></span>
            <span @click="changespanshow.changeAliasshow = true" :class="classname.classSpancursorpointer"><i class="el-icon-close" style="font-size:150%;"></i></span>
          </el-col>
        </div>
      </template>
    </el-table-column>
  </el-table>
  <el-table :data="tableData2"  style="width: 100%" :show-header="false" v-cloak>
    <el-table-column width="180">
      <template slot-scope="scope">
        <el-tooltip class="item" effect="light" content="EmailAddressPolicyEnabled" placement="left-start"><span>&nbsp;是否自动更新地址：</span></el-tooltip>
        <span style="font-size:130%;" v-if="changespanshow.changeEmailAddressPolicyEnabledshow" :class="[classname.classSpanFloatRight,classname.classSpancursorpointer]" @click="changeEmailAddressPolicyEnabledvalue"><i class="el-icon-edit-outline"></i></span>
      </template>
    </el-table-column>
    <el-table-column>
      <template slot-scope="scope">
        <span v-if="changespanshow.changeEmailAddressPolicyEnabledshow" v-text="EmailAddressPolicyEnabled"></span>
        <div v-else >
          <el-col :span="6">
            <span size="small" v-show="!EmailAddressPolicyEnabledChangevalue" v-text="EmailAddressPolicyEnabledchangemessagevalue.falsevmessagevalue"></span>
            <span size="small" v-show="EmailAddressPolicyEnabledChangevalue" v-text="EmailAddressPolicyEnabledchangemessagevalue.truevmessagevalue"></span>
            <el-switch
              v-model="EmailAddressPolicyEnabledChangevalue">
            </el-switch>
          </el-col>
          <el-col :span="6" style="margin-left:auto;margin-right:auto;">
            &nbsp;<span :class="classname.classSpancursorpointer" v-loading.fullscreen.lock="vLoadingShow" @click="changemailboxvalue('EmailAddressPolicyEnabled' ,EmailAddressPolicyEnabledChangevalue)"><i class="el-icon-upload2" style="font-size:150%;"></i></span>
            <span @click="changespanshow.changeEmailAddressPolicyEnabledshow = true" :class="classname.classSpancursorpointer"><i class="el-icon-close" style="font-size:150%;"></i></span>
          </el-col>
        </div>
      </template>
    </el-table-column>
  </el-table>
  <el-table :data="tableData2"  style="width: 100%" :show-header="false" v-cloak v-if="proxyAddresses.length !== 0">
    <el-table-column width="180">
      <template slot-scope="scope">
        <el-tooltip class="item" effect="light" content="SMTP" placement="left-start"><span>&nbsp;SMTP:</span></el-tooltip>
        <span style="font-size:130%;" v-if="!EmailAddressPolicyEnabled && changespanshow.changeSMTPshow" :class="[classname.classSpanFloatRight,classname.classSpancursorpointer]" @click="changespanshow.changeSMTPshow = false, SMTPChangevalue = SMTP"><i class="el-icon-edit-outline"></i></span>
      </template>
    </el-table-column>
    <el-table-column>
      <!-- <template slot-scope="scope">
        <span v-text="SMTP"></span>
      </template> -->
      <template slot-scope="scope">
        <span v-if="changespanshow.changeSMTPshow" v-text="SMTP"></span>
        <div v-else >
          <el-col :span="6">
            <el-input size="small" v-model="SMTPChangevalue"></el-input>
          </el-col>
          <el-col :span="6" style="margin-left:auto;margin-right:auto;">
            &nbsp;<span :class="classname.classSpancursorpointer" v-loading.fullscreen.lock="vLoadingShow" @click="changemailboxvalue('PrimarySmtpAddress' ,SMTPChangevalue)"><i class="el-icon-upload2" style="font-size:150%;"></i></span>
            <span @click="changespanshow.changeSMTPshow = true" :class="classname.classSpancursorpointer"><i class="el-icon-close" style="font-size:150%;"></i></span>
          </el-col>
        </div>
      </template>
    </el-table-column>
  </el-table>
  <el-table :data="tableData2"  v-for="smtpvalue in smtp" :key='smtpvalue' style="width: 100%" :show-header="false" v-cloak>
    <el-table-column width="180">
      <template slot-scope="scope">
        <el-tooltip class="item" effect="light" content="smtp" placement="left-start"><span>&nbsp;smtp:</span></el-tooltip>
      </template>
    </el-table-column>
    <el-table-column>
      <template slot-scope="scope">
          <span v-text="smtpvalue"></span>
          <el-tooltip class="item" effect="light" content="删除smtp" placement="right-start"><span @click="Deletesmtp(smtpvalue)"><i class="el-icon-delete" style="font-size:130%;" :class="classname.classSpancursorpointer"></i></span></el-tooltip>
          <el-tooltip class="item" effect="light" content="设置为主SMTP" placement="right-start" v-if="!EmailAddressPolicyEnabled"><span @click="smtptoSMTP(smtpvalue)"><i class="el-icon-edit-outline" style="font-size:130%;" :class="classname.classSpancursorpointer"></i></span></el-tooltip>
      </template>
    </el-table-column>
  </el-table>
  <el-dialog
    title="接收来自以下发件人的邮件"
    :visible.sync="dialogauthOrig"
    width="60%">
    <el-radio-group v-model="authOrigtypechangevalue">
      <p>
        <el-radio :label="truevalue">所有发件人</el-radio>
      </p>
    </el-radio-group>
    <br>
    <br />
    <el-radio-group v-model="authOrigtypechangevalue">
      <p>
        <el-radio :label="faslevalue">仅限以下列表中的发件人</el-radio>
      </p>
    </el-radio-group>
    <el-table :data="authOriglist" v-if="!authOrigtypechangevalue" id="selectauthOrigtable" style="width: 100%" v-cloak height="250">
      <el-table-column label="DN" prop="DN">
        <template slot="header" slot-scope="scope">
          DN
        </template>
      </el-table-column>
      <el-table-column
        align="right"
        min-width="35%">
        <!-- <template slot="header" slot-scope="scope">
          <el-input
            v-model="search"
            size="mini"
            placeholder="输入关键字搜索"/>
        </template> -->
        <template slot="header" slot-scope="scope">
          <el-button size="mini" type="text" @click="dialogVisiblesearchusershow">添加权限成员</el-button>
        </template>
        <template slot-scope="scope">
          <el-button
            size="mini"
            type="danger"
            @click="deluseroflist(scope.$index, scope.row)">删除权限</el-button>
        </template>
      </el-table-column>
    </el-table>
    <span slot="footer" class="dialog-footer">
      <el-button @click="dialogauthOrig = false">关 闭</el-button>
      <el-button type="primary" @click="savechangeauthOrig">保 存</el-button>
    </span>
  </el-dialog>
  <el-dialog
    title="搜索成员"
    :visible.sync="dialogVisiblesearchuser"
    width="60%"
    center>
    <p>
      <el-input
        type="textarea"
        :autosize="{ minRows: 2, maxRows: 6}"
        placeholder="批量搜索，请以英文“;”分隔"
        style="width: 70%"
        v-model="textarea3">
      </el-input>
      &nbsp;&nbsp;
      <el-button type="info" @click="serarchgroupvalue()" size="mini">检查名称</el-button>
    </p>
    <el-select
    v-model="value9"
    multiple
    filterable
    remote
    placeholder="请输入成员关键信息"
    :remote-method="remoteMethod"
    :loading="loading"
    style="width: 90%">
      <el-option
        v-for="item in options4"
        :key="item.sAMAccountName"
        :label="item.name"
        :value="item.sAMAccountName">
      </el-option>
    </el-select>
    <span slot="footer" class="dialog-footer">
      <el-button @click="dialogVisiblesearchuser = false">取 消</el-button>
      <el-button type="primary" @click="addobjecttoauthOrig">确 定</el-button>
    </span>
  </el-dialog>
</el-col>
<el-col :span="24" v-else>
    <el-button round @click="EnableMailContact">开通邮箱</el-button>
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
        changeEmailAddressPolicyEnabledshow: true,
        changeAliasshow: true,
        changemsExchRequireAuthToSendToshow: true,
        changeSMTPshow: true
      },
      search: '',
      msExchRequireAuthToSendTochangemessagevalue: {
        falsevmessagevalue: '否',
        truevmessagevalue: '是'
      },
      truevalue: true,
      faslevalue: false,
      textarea3: null,
      value9: null,
      dialogVisiblesearchuser: false, // 搜索成员模态框
      vLoadingShow: false, // 读条全屏遮罩
      loading: false, // 读条全屏遮罩
      hassmtpvalue: false, // 读条全屏遮罩
      authOrigtype: false, // authOrigtype选择
      authOrigtypechangevalue: false, // authOrigtype选择
      selectauthOrigtable: false, // 展示所有发件权限
      dialogauthOrig: false, // 展示所有发件权限模态框
      EmailAddressPolicyEnabled: false, // 是否自动更新电子邮件地址
      EmailAddressPolicyEnabledChangevalue: false, // 是否自动更新电子邮件地址更改地址
      cn: null, // cn
      AliasChangevalue: null, // 别名更改值
      Alias: null, // 别名
      description: null, // 描述
      groupType: null, // 组类型
      sAMAccountName: null, // 组sAMAccountName
      SMTP: null, // SMTP
      SMTPChangevalue: null, // SMTP改变值
      whenCreated: null, // whenCreated
      whenChanged: null, // SMTP
      smtp: [], // smtp
      options4: [],
      EmailAddressPolicyEnabledchangemessagevalue: {
        truevmessagevalue: '是',
        falsevmessagevalue: '否'
      },
      proxyAddresses: [], // 所有的电子邮件地址
      msExchRequireAuthToSendTo: null, // 是否开启发件人身份验证
      msExchRequireAuthToSendToChangevalue: null, // 修改是否开启发件人身份验证的值
      authOriglist: [], // 所有发件人权限list
      tableData2: [{
        date: 'displayName'
      }]
    }
  },
  methods: {
    Deletesmtp: function (smtpvalue) {
      let disNameforurl = this.getQueryVariabledecode('disName')
      this.$confirm('此操作将删除' + smtpvalue + '地址, 是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning',
        beforeClose: (action, instance, done) => {
          if (action === 'confirm') {
            instance.confirmButtonLoading = true
            instance.confirmButtonText = '执行中...'
            axios
              .get(this.serviceurl() + '/api/EmUserSmtp/?SmtpValue=' + smtpvalue + '&CountName=' + disNameforurl)
              .then(response => {
                instance.confirmButtonLoading = false
                if (response.data.isSuccess) {
                  (this.smtp).splice(smtpvalue, 1)
                  this.messagealertvalue('SMTP删除成功', 'success')
                } else {
                  if (response.data.message === '权限不足') {
                    this.messagealertvalue('权限不足', 'error')
                  } else {
                    this.messagealertvalue('SMTP删除失败', 'error')
                  }
                }
                done()
              })
          } else {
            done()
          }
        }
      }).then()
    },
    EnableMailContact: function () {
      let disNameforurl = this.getQueryVariabledecode('disName')
      this.$prompt('请输入邮箱地址', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        inputPattern: /[\w!#$%&'*+/=?^_`{|}~-]+(?:\.[\w!#$%&'*+/=?^_`{|}~-]+)*@(?:[\w](?:[\w-]*[\w])?\.)+[\w](?:[\w-]*[\w])?/,
        inputErrorMessage: '邮箱格式不正确',
        beforeClose: (action, instance, done) => {
          if (action === 'confirm') {
            instance.confirmButtonLoading = true
            instance.confirmButtonText = '执行中...'
            axios
              .get(this.serviceurl() + '/api/EnableMailContact/?mailname=' + disNameforurl + '&ExternalEmailAddress=' + instance.inputValue)
              .then(response => {
                instance.confirmButtonLoading = false
                if (response.data.isSuccess) {
                  this.messagealertvalue('邮箱开通成功', 'success')
                  this.getcomputermessagevalue()
                } else {
                  if (response.data.message === '权限不足') {
                    this.messagealertvalue('权限不足', 'error')
                  } else {
                    this.messagealertvalue('邮箱开通失败', 'error')
                  }
                }
                done()
              })
          } else {
            done()
          }
        }
      }).then()
    },
    smtptoSMTP: function (smtpvalue) {
      let disNameforurl = this.getQueryVariabledecode('disName')
      this.$confirm('此操作将' + smtpvalue + '设置为主SMTP, 是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning',
        beforeClose: (action, instance, done) => {
          if (action === 'confirm') {
            instance.confirmButtonLoading = true
            instance.confirmButtonText = '执行中...'
            axios
              // .get(this.serviceurl() + '/api/ChangeMail/?CountName=' + disNameforurl + '&Attributes=PrimarySmtpAddress&ChangeMessage=' + smtpvalue)
              .get(this.serviceurl() + '/api/SetMailContact/?CountName=' + disNameforurl + '&parametername=PrimarySmtpAddress&parametervalue=' + smtpvalue)
              .then(response => {
                instance.confirmButtonLoading = false
                if (response.data.isSuccess) {
                  this.messagealertvalue('设置成功', 'success')
                  this.getcomputermessagevalue()
                } else {
                  if (response.data.message === '权限不足') {
                    this.messagealertvalue('权限不足', 'error')
                  } else {
                    this.messagealertvalue('设置失败', 'error')
                  }
                }
                done()
              })
          } else {
            done()
          }
        }
      }).then(
        this.getcomputermessagevalue())
    },
    deluseroflist: function (index, row) {
      (this.authOriglist).splice(index, 1)
    },
    savechangeauthOrig: function () {
      let disNameforurl = this.getQueryVariabledecode('disName')
      let ChangeMessage = ''
      if (this.authOrigtypechangevalue) {
        ChangeMessage = ''
      } else {
        if (this.authOriglist.length === 0) {
          ChangeMessage = ''
        } else {
          for (let i = 0; i < this.authOriglist.length; i++) {
            ChangeMessage = ChangeMessage + '&ChangeMessage=' + this.authOriglist[i].DN
          }
        }
      }
      axios.get(this.serviceurl() + '/api/ChangeUserMessagebylist/?CountName=' + disNameforurl + '&Attributes=authOrig' + ChangeMessage)
        .then(response => {
          if (response.data.isSuccess) {
            this.messagealertvalue('修改成功', 'success')
            this.dialogauthOrig = false
          } else {
            if (response.data.message === '权限不足') {
              this.messagealertvalue('权限不足', 'error')
            } else {
              this.messagealertvalue('发件权限修改失败', 'error')
            }
          }
        })
    },
    ChangeUserMessagefuction: function (Attributesvalue, ChangeMessagevalue) {
      this.vLoadingShow = true
      axios
        .get(this.serviceurl() + '/api/ChangeUserMessage/?CountName=' + this.sAMAccountName + '&Attributes=' + Attributesvalue + '&ChangeMessage=' + ChangeMessagevalue)
        .then(response => {
          if (response.data.isSuccess) {
            this.messagealertvalue('修改成功', 'success')
            if (Attributesvalue === 'msExchRequireAuthToSendTo') {
              this.msExchRequireAuthToSendTo = this.msExchRequireAuthToSendToChangevalue
              this.changespanshow.changemsExchRequireAuthToSendToshow = true
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
    addobjecttoauthOrig: function () {
      for (let i = 0; i < this.value9.length; i++) {
        let trueorfalsevalue = true
        for (let z = 0; z < this.authOriglist.length; z++) {
          if (this.authOriglist[z].DN === this.value9[i]) {
            trueorfalsevalue = false
          }
        }
        if (trueorfalsevalue) {
          this.authOriglist.push({DN: this.value9[i]})
        }
      }
      this.dialogVisiblesearchuser = false
    },
    dialogVisiblesearchusershow: function () {
      this.dialogVisiblesearchuser = true
      this.options4 = []
      this.textarea3 = null
      this.value9 = []
    },
    changeauthOrigdiagshow: function () {
      let disNameforurl = this.getQueryVariabledecode('disName')
      this.authOriglist = []
      axios
        .get(this.serviceurl() + '/api/GetGroupPreMessage/?CountName=' + disNameforurl)
        .then(response => {
          if (response.data.isSuccess) {
            this.dialogauthOrig = true
            for (let i = 0; i < response.data.message.authOrig.length; i++) {
              this.authOriglist.push({DN: response.data.message.authOrig[i]})
            }
            if (this.authOriglist.length === 0) {
              this.authOrigtypechangevalue = true
              this.authOrigtype = true
            } else {
              this.authOrigtypechangevalue = false
              this.authOrigtype = false
            }
          } else {
            if (response.data.message === '权限不足') {
              this.messagealertvalue('权限不足', 'error')
            } else {
              this.messagealertvalue('联系人邮箱信息获取失败', 'error')
            }
          }
        })
    },
    changemailboxvalue: function (Attributesname, ChangeMessage) {
      let disNameforurl = this.getQueryVariabledecode('disName')
      this.vLoadingShow = true
      axios
        .get(this.serviceurl() + '/api/SetMailContact/?CountName=' + disNameforurl + '&parametername=' + Attributesname + '&parametervalue=' + ChangeMessage)
        .then(response => {
          this.vLoadingShow = false
          if (response.data.isSuccess) {
            if (Attributesname === 'RulesQuota') {
              this.RulesQuota = ChangeMessage
              this.changespanshow.changeRulesQuotashow = true
            } else if (Attributesname === 'RecipientLimits') {
              this.RecipientLimits = ChangeMessage
              this.changespanshow.changeRecipientLimitsshow = true
            } else if (Attributesname === 'Alias') {
              this.Alias = ChangeMessage
              this.changespanshow.changeAliasshow = true
              if (this.EmailAddressPolicyEnabled === 'True' || this.EmailAddressPolicyEnabled === 'true' || this.EmailAddressPolicyEnabled === true) {
                this.getcomputermessagevalue()
              }
            } else if (Attributesname === 'EmailAddressPolicyEnabled') {
              this.EmailAddressPolicyEnabled = ChangeMessage
              this.changespanshow.changeEmailAddressPolicyEnabledshow = true
              this.getcomputermessagevalue()
            } else if (Attributesname === 'PrimarySmtpAddress') {
              this.SMTP = ChangeMessage
              this.changespanshow.changeSMTPshow = true
              this.getcomputermessagevalue()
            }
            this.$message({
              showClose: true,
              message: '修改成功',
              type: 'success'
            })
          } else {
            if (response.data.message === '权限不足') {
              this.messagealertvalue('权限不足', 'error')
            } else {
              this.messagealertvalue('修改失败', 'error')
            }
          }
        })
        .catch(function () {
          this.vLoadingShow = false
          this.$message({
            showClose: true,
            message: '修改失败',
            type: 'error'
          })
        })
    },
    changeEmailAddressPolicyEnabledvalue: function () {
      this.changespanshow.changeEmailAddressPolicyEnabledshow = false
      this.EmailAddressPolicyEnabledChangevalue = this.EmailAddressPolicyEnabled
    },
    addsmtpvalue: function () {
      let disNameforurl = this.getQueryVariabledecode('disName')
      this.$prompt('请输入邮箱地址', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        inputPattern: /[\w!#$%&'*+/=?^_`{|}~-]+(?:\.[\w!#$%&'*+/=?^_`{|}~-]+)*@(?:[\w](?:[\w-]*[\w])?\.)+[\w](?:[\w-]*[\w])?/,
        inputErrorMessage: '邮箱格式不正确',
        beforeClose: (action, instance, done) => {
          if (action === 'confirm') {
            instance.confirmButtonLoading = true
            instance.confirmButtonText = '执行中...'
            axios
              .get(this.serviceurl() + '/api/MailContactSmtpAdd/?CountName=' + disNameforurl + '&SmtpValue=' + instance.inputValue)
              .then(response => {
                instance.confirmButtonLoading = false
                if (response.data.isSuccess) {
                  this.smtp.push(instance.inputValue)
                  this.messagealertvalue('smtp添加成功', 'success')
                } else {
                  if (response.data.message === '权限不足') {
                    this.messagealertvalue('权限不足', 'error')
                  } else {
                    this.messagealertvalue('smtp添加失败', 'error')
                  }
                }
                done()
              })
          } else {
            done()
          }
        }
      }).then()
    },
    async serarchgroupvalue () {
      let textarea3lastvalue = ''
      let groupvaluelist = []
      if (this.textarea3 === null || this.textarea3 === '') {
        this.messagealertvalue('请输入有效值', 'error')
      } else {
        textarea3lastvalue = this.textarea3.replace(/ |\n/g, '') + ';'
        if (textarea3lastvalue === null || textarea3lastvalue === '') {
          this.messagealertvalue('请输入有效值', 'error')
        } else {
          let textarea3lastvaluelistvalue = textarea3lastvalue.split(';')
          for (let i = 0; i < textarea3lastvaluelistvalue.length; i++) {
            if (textarea3lastvaluelistvalue[i] !== '' && textarea3lastvaluelistvalue[i] !== null) {
              groupvaluelist.push(textarea3lastvaluelistvalue[i])
            }
          }
          if (groupvaluelist.length === 0) {
            this.messagealertvalue('请输入有效值', 'error')
          } else {
            textarea3lastvalue = textarea3lastvalue.replace(/;+/g, ';')
            for (let z = 0; z < groupvaluelist.length; z++) {
              if ((this.value9).indexOf(groupvaluelist[z]) === -1) {
                let groupvalemessageone = await axios.get(this.serviceurl() + '/api/GetGroupPreMessage/?CountName=' + groupvaluelist[z])
                let groupvalemessagetwo = await axios.get(this.serviceurl() + '/api/GetUserMessage/?CountName=' + groupvaluelist[z])
                if (groupvalemessageone.data.isSuccess) {
                  if ((this.value9).indexOf(groupvalemessageone.data.message.distinguishedName) === -1) {
                    this.value9.push(groupvalemessageone.data.message.distinguishedName)
                    this.options4.push({name: groupvalemessageone.data.message.cn, sAMAccountName: groupvalemessageone.data.message.distinguishedName})
                    textarea3lastvalue = textarea3lastvalue.replace(groupvaluelist[z] + ';', '')
                  } else {
                    textarea3lastvalue = textarea3lastvalue.replace(groupvaluelist[z] + ';', '')
                  }
                } else if (groupvalemessagetwo.data.isSuccess) {
                  if ((this.value9).indexOf(groupvalemessagetwo.data.message.distinguishedName) === -1) {
                    this.value9.push(groupvalemessagetwo.data.message.distinguishedName)
                    this.options4.push({name: groupvalemessagetwo.data.message.cn, sAMAccountName: groupvalemessagetwo.data.message.distinguishedName})
                    textarea3lastvalue = textarea3lastvalue.replace(groupvaluelist[z] + ';', '')
                  } else {
                    textarea3lastvalue = textarea3lastvalue.replace(groupvaluelist[z] + ';', '')
                  }
                }
              } else {
                textarea3lastvalue = textarea3lastvalue.replace(groupvaluelist[z] + ';', '')
              }
            }
            this.textarea3 = textarea3lastvalue
            if (textarea3lastvalue === '') {
              this.messagealertvalue('成员搜索完毕', 'success')
            } else {
              this.messagealertvalue('部分成员搜索失败，请核实', 'warning')
            }
          }
        }
      }
    },
    remoteMethod (query) {
      if (query !== '') {
        this.loading = true
        axios
          .get(this.serviceurl() + '/api/GetConMessage/?username=' + query)
          .then(response => {
            this.options4 = []
            for (let i = 0; i < response.data.message.length; i++) {
              if (response.data.message[i].proxyAddresses.length) {
                this.options4.push({name: response.data.message[i].name, sAMAccountName: response.data.message[i].distinguishedName})
              }
            }
            this.loading = false
          })
      } else {
        this.options4 = []
      }
    },
    getcomputermessagevalue: function () {
      this.smtp = []
      const loading = this.$loading({
        lock: true
      })
      let disNameforurl = this.getQueryVariabledecode('disName')
      axios
        .get(this.serviceurl() + '/api/GetUserMessage/?CountName=' + disNameforurl + '&objectClass=DN')
        .then(response => {
          if (response.data.isSuccess) {
            this.cn = response.data.message.cn
            if (!response.data.message['proxyAddresses']) {
              this.hassmtpvalue = false
              loading.close()
            } else {
              if (response.data.message['proxyAddresses'].length === 0) {
                this.hassmtpvalue = false
                loading.close()
              } else {
                this.proxyAddresses = response.data.message.proxyAddresses
                if (!response.data.message.msExchRequireAuthToSendTo) {
                  this.msExchRequireAuthToSendTo = false
                } else {
                  if (response.data.message.msExchRequireAuthToSendTo === 'True' || response.data.message.msExchRequireAuthToSendTo === 'true' || response.data.message.msExchRequireAuthToSendTo === true) {
                    this.msExchRequireAuthToSendTo = true
                  } else {
                    this.msExchRequireAuthToSendTo = false
                  }
                }
                this.hassmtpvalue = true
                axios
                  .get(this.serviceurl() + '/api/GetMailContact/?CountName=' + disNameforurl)
                  .then(response => {
                    loading.close()
                    if (response.data.isSuccess) {
                      this.AliasChangevalue = response.data.message.Alias
                      this.Alias = response.data.message.Alias
                      if (response.data.message.EmailAddressPolicyEnabled === 'True' || response.data.message.EmailAddressPolicyEnabled === true) {
                        this.EmailAddressPolicyEnabled = true
                      } else {
                        this.EmailAddressPolicyEnabled = false
                      }
                    } else {
                      if (response.data.message === '权限不足') {
                        this.messagealertvalue('权限不足', 'error')
                      } else {
                        this.messagealertvalue('联系人邮箱信息获取失败', 'error')
                      }
                    }
                  })
              }
            }
            for (let i = 0; i < this.proxyAddresses.length; i++) {
              if (response.data.message.proxyAddresses[i].search('SMTP:') !== -1) {
                this.SMTP = response.data.message.proxyAddresses[i].replace('SMTP:', '')
              } else {
                this.smtp.push(response.data.message.proxyAddresses[i].replace('smtp:', ''))
              }
            }
          } else {
            loading.close()
            if (response.data.message === '权限不足') {
              this.messagealertvalue('权限不足', 'error')
            }
          }
        })
        .catch(function () {
          loading.close()
          this.messagealertvalue('加载失败', 'error')
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
