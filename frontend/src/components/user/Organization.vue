<template>
  <el-col :span="24">
  <el-table :data="tableData3"  style="width: 100%" :show-header="false" v-cloak>
    <el-table-column width="180">
      <template slot-scope="scope">
        <el-tooltip class="item" effect="light" content="displayName" placement="left-start"><span>&nbsp;显示名称：</span></el-tooltip>
        <span style="font-size:130%;" v-if="changespanshow.changedisplayNameshow" :class="[classname.classSpanFloatRight,classname.classSpancursorpointer]" @click="changedisplayName"><i class="el-icon-edit-outline"></i></span>
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
            <span @click="closechangedisplayName" :class="classname.classSpancursorpointer"><i class="el-icon-close" style="font-size:150%;"></i></span>
          </el-col>
        </div>
      </template>
    </el-table-column>
  </el-table>
  <el-table :data="tableData3"  style="width: 100%" :show-header="false" v-cloak>
    <el-table-column width="180">
      <template slot-scope="scope">
        <el-tooltip class="item" effect="light" content="physicalDeliveryOfficeName" placement="left-start"><span>&nbsp;办公室：</span></el-tooltip>
        <span style="font-size:130%;" v-if="changespanshow.changephysicalDeliveryOfficeNameshow" :class="[classname.classSpanFloatRight,classname.classSpancursorpointer]" @click="changephysicalDeliveryOfficeName"><i class="el-icon-edit-outline"></i></span>
      </template>
    </el-table-column>
    <el-table-column>
      <template slot-scope="scope">
        <span v-if="changespanshow.changephysicalDeliveryOfficeNameshow" v-text="physicalDeliveryOfficeName"></span>
        <div v-else >
          <el-col :span="6">
            <el-input size="small" v-model="physicalDeliveryOfficeNameChangevalue"></el-input>
          </el-col>
          <el-col :span="6" style="margin-left:auto;margin-right:auto;">
            &nbsp;<span :class="classname.classSpancursorpointer" v-loading.fullscreen.lock="vLoadingShow" @click="savechangephysicalDeliveryOfficeName"><i class="el-icon-upload2" style="font-size:150%;"></i></span>
            <span @click="closechangephysicalDeliveryOfficeName" :class="classname.classSpancursorpointer"><i class="el-icon-close" style="font-size:150%;"></i></span>
          </el-col>
        </div>
      </template>
    </el-table-column>
  </el-table>
  <el-table :data="tableData3"  style="width: 100%" :show-header="false" v-cloak>
    <el-table-column width="180">
      <template slot-scope="scope">
        <el-tooltip class="item" effect="light" content="mail" placement="left-start"><span>&nbsp;电子邮件：</span></el-tooltip>
        <!-- <span style="font-size:130%;" v-if="changespanshow.changemailshow" :class="[classname.classSpanFloatRight,classname.classSpancursorpointer]" @click="changemailName"><i class="el-icon-edit-outline"></i></span> -->
      </template>
    </el-table-column>
    <el-table-column>
      <template slot-scope="scope">
        <span v-text="mail"></span>
        <!-- <span v-if="changespanshow.changemailshow" v-text="mail"></span> -->
        <!-- <div v-else >
          <el-col :span="6">
            <el-input size="small" v-model="mailChangevalue"></el-input>
          </el-col>
          <el-col :span="6" style="margin-left:auto;margin-right:auto;">
            &nbsp;<span :class="classname.classSpancursorpointer" v-loading.fullscreen.lock="vLoadingShow" @click="savechangemailName"><i class="el-icon-upload2" style="font-size:150%;"></i></span>
            <span @click="closechangemailName" :class="classname.classSpancursorpointer"><i class="el-icon-close" style="font-size:150%;"></i></span>
          </el-col>
        </div> -->
      </template>
    </el-table-column>
  </el-table>
  <el-table :data="tableData3"  style="width: 100%" :show-header="false" v-cloak>
    <el-table-column width="180">
      <template slot-scope="scope">
        <el-tooltip class="item" effect="light" content="wWWHomePage" placement="left-start"><span>&nbsp;网页：</span></el-tooltip>
        <span style="font-size:130%;" v-if="changespanshow.changewWWHomePageshow" :class="[classname.classSpanFloatRight,classname.classSpancursorpointer]" @click="changewWWHomePageName"><i class="el-icon-edit-outline"></i></span>
      </template>
    </el-table-column>
    <el-table-column>
      <template slot-scope="scope">
        <span v-if="changespanshow.changewWWHomePageshow" v-text="wWWHomePage"></span>
        <div v-else >
          <el-col :span="6">
            <el-input size="small" v-model="wWWHomePageChangevalue"></el-input>
          </el-col>
          <el-col :span="6" style="margin-left:auto;margin-right:auto;">
            &nbsp;<span :class="classname.classSpancursorpointer" v-loading.fullscreen.lock="vLoadingShow" @click="savechangewWWHomePageName"><i class="el-icon-upload2" style="font-size:150%;"></i></span>
            <span @click="closechangewWWHomePageName" :class="classname.classSpancursorpointer"><i class="el-icon-close" style="font-size:150%;"></i></span>
          </el-col>
        </div>
      </template>
    </el-table-column>
  </el-table>
  <el-table :data="tableData3"  style="width: 100%" :show-header="false" v-cloak>
    <el-table-column width="180">
      <template slot-scope="scope">
        <el-tooltip class="item" effect="light" content="telephoneNumber" placement="left-start"><span>&nbsp;电话号码：</span></el-tooltip>
        <span style="font-size:130%;" v-if="changespanshow.changetelephoneNumbershow" :class="[classname.classSpanFloatRight,classname.classSpancursorpointer]" @click="changetelephoneNumberName"><i class="el-icon-edit-outline"></i></span>
      </template>
    </el-table-column>
    <el-table-column>
      <template slot-scope="scope">
        <span v-if="changespanshow.changetelephoneNumbershow" v-text="telephoneNumber"></span>
        <div v-else >
          <el-col :span="6">
            <el-input size="small" v-model="telephoneNumberChangevalue"></el-input>
          </el-col>
          <el-col :span="6" style="margin-left:auto;margin-right:auto;">
            &nbsp;<span :class="classname.classSpancursorpointer" v-loading.fullscreen.lock="vLoadingShow" @click="savechangetelephoneNumberName"><i class="el-icon-upload2" style="font-size:150%;"></i></span>
            <span @click="closechangetelephoneNumberName" :class="classname.classSpancursorpointer"><i class="el-icon-close" style="font-size:150%;"></i></span>
          </el-col>
        </div>
      </template>
    </el-table-column>
  </el-table>
  <el-table :data="tableData3"  style="width: 100%" :show-header="false" v-cloak>
    <el-table-column width="180">
      <template slot-scope="scope">
        <el-tooltip class="item" effect="light" content="homePhone" placement="left-start"><span>&nbsp;主页：</span></el-tooltip>
        <span style="font-size:130%;" v-if="changespanshow.changehomePhoneshow" :class="[classname.classSpanFloatRight,classname.classSpancursorpointer]" @click="changehomePhoneName"><i class="el-icon-edit-outline"></i></span>
      </template>
    </el-table-column>
    <el-table-column>
      <template slot-scope="scope">
        <span v-if="changespanshow.changehomePhoneshow" v-text="homePhone"></span>
        <div v-else >
          <el-col :span="6">
            <el-input size="small" v-model="homePhoneChangevalue"></el-input>
          </el-col>
          <el-col :span="6" style="margin-left:auto;margin-right:auto;">
            &nbsp;<span :class="classname.classSpancursorpointer" v-loading.fullscreen.lock="vLoadingShow" @click="savechangehomePhoneName"><i class="el-icon-upload2" style="font-size:150%;"></i></span>
            <span @click="closechangehomePhoneName" :class="classname.classSpancursorpointer"><i class="el-icon-close" style="font-size:150%;"></i></span>
          </el-col>
        </div>
      </template>
    </el-table-column>
  </el-table>
  <el-table :data="tableData3"  style="width: 100%" :show-header="false" v-cloak>
    <el-table-column width="180">
      <template slot-scope="scope">
        <el-tooltip class="item" effect="light" content="mobile" placement="left-start"><span>&nbsp;移动电话号码：</span></el-tooltip>
        <span style="font-size:130%;" v-if="changespanshow.changemobileshow" :class="[classname.classSpanFloatRight,classname.classSpancursorpointer]" @click="changemobileName"><i class="el-icon-edit-outline"></i></span>
      </template>
    </el-table-column>
    <el-table-column>
      <template slot-scope="scope">
        <span v-if="changespanshow.changemobileshow" v-text="mobile"></span>
        <div v-else >
          <el-col :span="6">
            <el-input size="small" v-model="mobileChangevalue"></el-input>
          </el-col>
          <el-col :span="6" style="margin-left:auto;margin-right:auto;">
            &nbsp;<span :class="classname.classSpancursorpointer" v-loading.fullscreen.lock="vLoadingShow" @click="savechangemobileName"><i class="el-icon-upload2" style="font-size:150%;"></i></span>
            <span @click="closechangemobileName" :class="classname.classSpancursorpointer"><i class="el-icon-close" style="font-size:150%;"></i></span>
          </el-col>
        </div>
      </template>
    </el-table-column>
  </el-table>
  <el-table :data="tableData3"  style="width: 100%" :show-header="false" v-cloak>
    <el-table-column width="180">
      <template slot-scope="scope">
        <el-tooltip class="item" effect="light" content="facsimileTelephoneNumber" placement="left-start"><span>&nbsp;传真：</span></el-tooltip>
        <span style="font-size:130%;" v-if="changespanshow.changefacsimileTelephoneNumbershow" :class="[classname.classSpanFloatRight,classname.classSpancursorpointer]" @click="changefacsimileTelephoneNumberName"><i class="el-icon-edit-outline"></i></span>
      </template>
    </el-table-column>
    <el-table-column>
      <template slot-scope="scope">
        <span v-if="changespanshow.changefacsimileTelephoneNumbershow" v-text="facsimileTelephoneNumber"></span>
        <div v-else >
          <el-col :span="6">
            <el-input size="small" v-model="facsimileTelephoneNumberChangevalue"></el-input>
          </el-col>
          <el-col :span="6" style="margin-left:auto;margin-right:auto;">
            &nbsp;<span :class="classname.classSpancursorpointer" v-loading.fullscreen.lock="vLoadingShow" @click="savechangefacsimileTelephoneNumberName"><i class="el-icon-upload2" style="font-size:150%;"></i></span>
            <span @click="closechangefacsimileTelephoneNumberName" :class="classname.classSpancursorpointer"><i class="el-icon-close" style="font-size:150%;"></i></span>
          </el-col>
        </div>
      </template>
    </el-table-column>
  </el-table>
  <el-table :data="tableData3"  style="width: 100%" :show-header="false" v-cloak>
    <el-table-column width="180">
      <template slot-scope="scope">
        <el-tooltip class="item" effect="light" content="pager" placement="left-start"><span>&nbsp;寻呼机：</span></el-tooltip>
        <span style="font-size:130%;" v-if="changespanshow.changepagershow" :class="[classname.classSpanFloatRight,classname.classSpancursorpointer]" @click="changepagerName"><i class="el-icon-edit-outline"></i></span>
      </template>
    </el-table-column>
    <el-table-column>
      <template slot-scope="scope">
        <span v-if="changespanshow.changepagershow" v-text="pager"></span>
        <div v-else >
          <el-col :span="6">
            <el-input size="small" v-model="pagerChangevalue"></el-input>
          </el-col>
          <el-col :span="6" style="margin-left:auto;margin-right:auto;">
            &nbsp;<span :class="classname.classSpancursorpointer" v-loading.fullscreen.lock="vLoadingShow" @click="savechangepagerName"><i class="el-icon-upload2" style="font-size:150%;"></i></span>
            <span @click="closechangepagerName" :class="classname.classSpancursorpointer"><i class="el-icon-close" style="font-size:150%;"></i></span>
          </el-col>
        </div>
      </template>
    </el-table-column>
  </el-table>
  <el-table :data="tableData3"  style="width: 100%" :show-header="false" v-cloak>
    <el-table-column width="180">
      <template slot-scope="scope">
        <el-tooltip class="item" effect="light" content="ipPhone" placement="left-start"><span>&nbsp;IP电话：</span></el-tooltip>
        <span style="font-size:130%;" v-if="changespanshow.changeipPhoneshow" :class="[classname.classSpanFloatRight,classname.classSpancursorpointer]" @click="changeipPhoneName"><i class="el-icon-edit-outline"></i></span>
      </template>
    </el-table-column>
    <el-table-column>
      <template slot-scope="scope">
        <span v-if="changespanshow.changeipPhoneshow" v-text="ipPhone"></span>
        <div v-else >
          <el-col :span="6">
            <el-input size="small" v-model="ipPhoneChangevalue"></el-input>
          </el-col>
          <el-col :span="6" style="margin-left:auto;margin-right:auto;">
            &nbsp;<span :class="classname.classSpancursorpointer" v-loading.fullscreen.lock="vLoadingShow" @click="savechangeipPhoneName"><i class="el-icon-upload2" style="font-size:150%;"></i></span>
            <span @click="closechangeipPhoneName" :class="classname.classSpancursorpointer"><i class="el-icon-close" style="font-size:150%;"></i></span>
          </el-col>
        </div>
      </template>
    </el-table-column>
  </el-table>
  <el-table :data="tableData3"  style="width: 100%" :show-header="false" v-cloak>
    <el-table-column width="180">
      <template slot-scope="scope">
        <el-tooltip class="item" effect="light" content="description" placement="left-start"><span>&nbsp;描述：</span></el-tooltip>
        <span style="font-size:130%;" v-if="changespanshow.changedescriptionshow" :class="[classname.classSpanFloatRight,classname.classSpancursorpointer]" @click="changedescriptionName"><i class="el-icon-edit-outline"></i></span>
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
            &nbsp;<span :class="classname.classSpancursorpointer" v-loading.fullscreen.lock="vLoadingShow" @click="savechangedescriptionName"><i class="el-icon-upload2" style="font-size:150%;"></i></span>
            <span @click="closechangedescriptionName" :class="classname.classSpancursorpointer"><i class="el-icon-close" style="font-size:150%;"></i></span>
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
        changedisplayNameshow: true,
        // changemailshow: true,
        changetelephoneNumbershow: true,
        changehomePhoneshow: true,
        changemobileshow: true,
        changeipPhoneshow: true,
        changepagershow: true,
        changedescriptionshow: true,
        changefacsimileTelephoneNumbershow: true,
        changewWWHomePageshow: true,
        changephysicalDeliveryOfficeNameshow: true
      },
      vLoadingShow: false, // 读条全屏遮罩
      displayName: null, // 显示名称
      physicalDeliveryOfficeName: null, // 办公室
      displayNameChangevalue: null, 
      physicalDeliveryOfficeNameChangevalue: null, 
      wWWHomePageChangevalue: null,
      telephoneNumberChangevalue: null,
      homePhoneChangevalue: null,
      mobileChangevalue: null,
      facsimileTelephoneNumberChangevalue: null,
      pagerChangevalue: null,
      ipPhoneChangevalue: null,
      descriptionChangevalue: null,
      mail: null, // 电子邮件地址
      wWWHomePage: null, // 网页
      telephoneNumber: null, // 电话号码
      homePhone: null, // 主页
      mobile: null, // 移动电话号码
      facsimileTelephoneNumber: null, // 传真
      ipPhone: null, //  IP电话
      pager: null, //  寻呼机
      description: null, //  描述
      tableData3: []
    }
  },
  created: function () {
    const loading = this.$loading({
      lock: true
    })
    let disNameforurl = this.getQueryVariable('disName')
    axios
      .get(this.serviceurl() + '/api/GetUserMessage/?CountName=' + disNameforurl)
      .then(response => {
        loading.close()
        if (response.data.isSuccess) {
          this.displayName = response.data.message.displayName
          this.sAMAccountName = response.data.message.sAMAccountName
          this.physicalDeliveryOfficeName = response.data.message.physicalDeliveryOfficeName
          this.mail = response.data.message.mail
          this.wWWHomePage = response.data.message.wWWHomePage
          this.telephoneNumber = response.data.message.telephoneNumber
          this.homePhone = response.data.message.homePhone
          this.mobile = response.data.message.mobile
          this.facsimileTelephoneNumber = response.data.message.facsimileTelephoneNumber
          this.pager = response.data.message.pager
          this.ipPhone = response.data.message.ipPhone
          this.description = response.data.message.description[0]
          this.tableData3 = [{
            date: 'displayName'
          }]
        } else {
          if (response.data.message === '权限不足') {
            this.messagealertvalue('权限不足', 'error')
          } else {
            this.messagealertvalue('加载失败', 'error')
          }
        }
        // this.tableData = [{name: response.data.message.userPrincipalName}]
      })
      .catch(function () {
        this.messagealertvalue('加载失败', 'error')
      })
  },
  methods: {
    ChangeUserMessagefuction: function (Attributesvalue, ChangeMessagevalue) {
      this.vLoadingShow = true
      axios
        .get(this.serviceurl() + '/api/ChangeUserMessage/?CountName=' + this.sAMAccountName + '&Attributes=' + Attributesvalue + '&ChangeMessage=' + ChangeMessagevalue)
        .then(response => {
          if (response.data.isSuccess) {
            this.messagealertvalue('修改成功', 'success')
            if (Attributesvalue === 'displayName') {
              this.displayName = this.displayNameChangevalue
              this.changespanshow.changedisplayNameshow = true
            } else if (Attributesvalue === 'initials') {
              this.initials = this.initialsChangevalue
              this.changespanshow.changeinitialsshow = true
            } else if (Attributesvalue === 'physicalDeliveryOfficeName') {
              this.physicalDeliveryOfficeName = this.physicalDeliveryOfficeNameChangevalue
              this.changespanshow.changephysicalDeliveryOfficeNameshow = true
            // } else if (Attributesvalue === 'mail') {
            //   this.mail = this.mailChangevalue
            //   this.changespanshow.changemailshow = true
            } else if (Attributesvalue === 'wWWHomePage') {
              this.wWWHomePage = this.wWWHomePageChangevalue
              this.changespanshow.changewWWHomePageshow = true
            } else if (Attributesvalue === 'telephoneNumber') {
              this.telephoneNumber = this.telephoneNumberChangevalue
              this.changespanshow.changetelephoneNumbershow = true
            } else if (Attributesvalue === 'homePhone') {
              this.homePhone = this.homePhoneChangevalue
              this.changespanshow.changehomePhoneshow = true
            } else if (Attributesvalue === 'mobile') {
              this.mobile = this.mobileChangevalue
              this.changespanshow.changemobileshow = true
            } else if (Attributesvalue === 'facsimileTelephoneNumber') {
              this.facsimileTelephoneNumber = this.facsimileTelephoneNumberChangevalue
              this.changespanshow.changefacsimileTelephoneNumbershow = true
            } else if (Attributesvalue === 'pager') {
              this.pager = this.pagerChangevalue
              this.changespanshow.changepagershow = true
            } else if (Attributesvalue === 'ipPhone') {
              this.ipPhone = this.ipPhoneChangevalue
              this.changespanshow.changeipPhoneshow = true
            } else if (Attributesvalue === 'description') {
              this.description = this.descriptionChangevalue
              this.changespanshow.changedescriptionshow = true
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
    changedisplayName: function () {
      this.displayNameChangevalue = this.displayName
      this.changespanshow.changedisplayNameshow = false
    },
    closechangedisplayName: function () {
      this.changespanshow.changedisplayNameshow = true
    },
    savechangedisplayName: function () {
      this.ChangeUserMessagefuction('displayName', this.displayNameChangevalue)
    },
    changephysicalDeliveryOfficeName: function () {
      this.physicalDeliveryOfficeNameChangevalue = this.physicalDeliveryOfficeName
      this.changespanshow.changephysicalDeliveryOfficeNameshow = false
    },
    closechangephysicalDeliveryOfficeName: function () {
      this.changespanshow.changephysicalDeliveryOfficeNameshow = true
    },
    savechangephysicalDeliveryOfficeName: function () {
      this.ChangeUserMessagefuction('physicalDeliveryOfficeName', this.physicalDeliveryOfficeNameChangevalue)
    },
    changewWWHomePageName: function () {
      this.wWWHomePageChangevalue = this.wWWHomePage
      this.changespanshow.changewWWHomePageshow = false
    },
    closechangewWWHomePageName: function () {
      this.changespanshow.changewWWHomePageshow = true
    },
    savechangewWWHomePageName: function () {
      this.ChangeUserMessagefuction('wWWHomePage', this.wWWHomePageChangevalue)
    },
    changetelephoneNumberName: function () {
      this.telephoneNumberChangevalue = this.telephoneNumber
      this.changespanshow.changetelephoneNumbershow = false
    },
    closechangetelephoneNumberName: function () {
      this.changespanshow.changetelephoneNumbershow = true
    },
    savechangetelephoneNumberName: function () {
      this.ChangeUserMessagefuction('telephoneNumber', this.telephoneNumberChangevalue)
    },
    changehomePhoneName: function () {
      this.homePhoneChangevalue = this.homePhone
      this.changespanshow.changehomePhoneshow = false
    },
    closechangehomePhoneName: function () {
      this.changespanshow.changehomePhoneshow = true
    },
    savechangehomePhoneName: function () {
      this.ChangeUserMessagefuction('homePhone', this.homePhoneChangevalue)
    },
    changemobileName: function () {
      this.mobileChangevalue = this.mobile
      this.changespanshow.changemobileshow = false
    },
    closechangemobileName: function () {
      this.changespanshow.changemobileshow = true
    },
    savechangemobileName: function () {
      this.ChangeUserMessagefuction('mobile', this.mobileChangevalue)
    },
    changefacsimileTelephoneNumberName: function () {
      this.facsimileTelephoneNumberChangevalue = this.facsimileTelephoneNumber
      this.changespanshow.changefacsimileTelephoneNumbershow = false
    },
    closechangefacsimileTelephoneNumberName: function () {
      this.changespanshow.changefacsimileTelephoneNumbershow = true
    },
    savechangefacsimileTelephoneNumberName: function () {
      this.ChangeUserMessagefuction('facsimileTelephoneNumber', this.facsimileTelephoneNumberChangevalue)
    },
    changepagerName: function () {
      this.pagerChangevalue = this.pager
      this.changespanshow.changepagershow = false
    },
    closechangepagerName: function () {
      this.changespanshow.changepagershow = true
    },
    savechangepagerName: function () {
      this.ChangeUserMessagefuction('pager', this.pagerChangevalue)
    },
    changeipPhoneName: function () {
      this.ipPhoneChangevalue = this.ipPhone
      this.changespanshow.changeipPhoneshow = false
    },
    closechangeipPhoneName: function () {
      this.changespanshow.changeipPhoneshow = true
    },
    savechangeipPhoneName: function () {
      this.ChangeUserMessagefuction('ipPhone', this.ipPhoneChangevalue)
    },
    changedescriptionName: function () {
      this.descriptionChangevalue = this.description
      this.changespanshow.changedescriptionshow = false
    },
    closechangedescriptionName: function () {
      this.changespanshow.changedescriptionshow = true
    },
    savechangedescriptionName: function () {
      this.ChangeUserMessagefuction('description', this.descriptionChangevalue)
    }
  }
}
</script>
<style>
</style>
