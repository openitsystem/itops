<template>
  <el-col :span="24">
  <el-table :data="tableData3"  style="width: 100%" :show-header="false" v-cloak>
    <el-table-column width="180">
      <template slot-scope="scope">
        <el-tooltip class="item" effect="light" content="givenName" placement="left-start"><span>&nbsp;名字：</span></el-tooltip>
        <span style="font-size:130%;" v-if="changespanshow.changegivenNameshow" :class="[classname.classSpanFloatRight,classname.classSpancursorpointer]" @click="changegivenName"><i class="el-icon-edit-outline"></i></span>
      </template>
    </el-table-column>
    <el-table-column>
      <template slot-scope="scope">
        <span v-if="changespanshow.changegivenNameshow" v-text="givenName"></span>
        <div v-else >
          <el-col :span="6">
            <el-input size="small" v-model="givenNameChangevalue"></el-input>
          </el-col>
          <el-col :span="6" style="margin-left:auto;margin-right:auto;">
            &nbsp;<span :class="classname.classSpancursorpointer" v-loading.fullscreen.lock="vLoadingShow" @click="savechangegivenName"><i class="el-icon-upload2" style="font-size:150%;"></i></span>
            <span @click="closechangegivenName" :class="classname.classSpancursorpointer"><i class="el-icon-close" style="font-size:150%;"></i></span>
          </el-col>
        </div>
      </template>
    </el-table-column>
  </el-table>
  <el-table :data="tableData3"  style="width: 100%" :show-header="false" v-cloak>
    <el-table-column width="180">
      <template slot-scope="scope">
        <el-tooltip class="item" effect="light" content="initials" placement="left-start"><span>&nbsp;中间名首字母缩写：</span></el-tooltip>
        <span style="font-size:130%;" v-if="changespanshow.changeinitialsshow" :class="[classname.classSpanFloatRight,classname.classSpancursorpointer]" @click="changeinitials"><i class="el-icon-edit-outline"></i></span>
      </template>
    </el-table-column>
    <el-table-column>
      <template slot-scope="scope">
        <span v-if="changespanshow.changeinitialsshow" v-text="initials"></span>
        <div v-else >
          <el-col :span="6">
            <el-input size="small" v-model="initialsChangevalue"></el-input>
          </el-col>
          <el-col :span="6" style="margin-left:auto;margin-right:auto;">
            &nbsp;<span :class="classname.classSpancursorpointer" v-loading.fullscreen.lock="vLoadingShow" @click="savechangeinitials"><i class="el-icon-upload2" style="font-size:150%;"></i></span>
            <span @click="closechangeinitials" :class="classname.classSpancursorpointer"><i class="el-icon-close" style="font-size:150%;"></i></span>
          </el-col>
        </div>
      </template>
    </el-table-column>
  </el-table>
  <el-table :data="tableData3"  style="width: 100%" :show-header="false" v-cloak>
    <el-table-column width="180">
      <template slot-scope="scope">
        <el-tooltip class="item" effect="light" content="sn" placement="left-start"><span>&nbsp;姓氏：</span></el-tooltip>
        <span style="font-size:130%;" v-if="changespanshow.changesnshow" :class="[classname.classSpanFloatRight,classname.classSpancursorpointer]" @click="changesn"><i class="el-icon-edit-outline"></i></span>
      </template>
    </el-table-column>
    <el-table-column>
      <template slot-scope="scope">
        <span v-if="changespanshow.changesnshow"  v-text="sn"></span>
        <div v-else >
          <el-col :span="6">
            <el-input size="small" v-model="snChangevalue"></el-input>
          </el-col>
          <el-col :span="6" style="margin-left:auto;margin-right:auto;">
            &nbsp;<span :class="classname.classSpancursorpointer" v-loading.fullscreen.lock="vLoadingShow" @click="savechangesn"><i class="el-icon-upload2" style="font-size:150%;"></i></span>
            <span @click="closechangesn" :class="classname.classSpancursorpointer"><i class="el-icon-close" style="font-size:150%;"></i></span>
          </el-col>
        </div>
      </template>
    </el-table-column>
  </el-table>
  <el-table :data="tableData3"  style="width: 100%" :show-header="false" v-cloak>
    <el-table-column width="180">
      <template slot-scope="scope">
        <el-tooltip class="item" effect="light" content="cn" placement="left-start"><span>&nbsp;全名：</span></el-tooltip>
        <span style="font-size:130%;" v-if="changespanshow.changecnshow" :class="[classname.classSpanFloatRight,classname.classSpancursorpointer]" @click="changecn"><i class="el-icon-edit-outline"></i></span>
       </template>
    </el-table-column>
    <el-table-column>
      <template slot-scope="scope">
        <span  v-if="changespanshow.changecnshow"  v-text="cn"></span>
        <div v-else >
          <el-col :span="6">
            <el-input size="small" v-model="cnChangevalue"></el-input>
          </el-col>
          <el-col :span="6" style="margin-left:auto;margin-right:auto;">
            &nbsp;<span :class="classname.classSpancursorpointer" v-loading.fullscreen.lock="vLoadingShow" @click="savechangecn"><i class="el-icon-upload2" style="font-size:150%;"></i></span>
            <span @click="closechangecn" :class="classname.classSpancursorpointer"><i class="el-icon-close" style="font-size:150%;"></i></span>
          </el-col>
        </div>
      </template>
    </el-table-column>
  </el-table>
  <el-table :data="tableData3"  style="width: 100%" :show-header="false" v-cloak>
    <el-table-column width="180">
      <template slot-scope="scope">
        <el-tooltip class="item" effect="light" content="sAMAccountName：" placement="left-start"><span>&nbsp;用户登录名：</span></el-tooltip>
          <span style="font-size:130%;" v-if="changespanshow.changesAMAccountNameshow" :class="[classname.classSpanFloatRight,classname.classSpancursorpointer]" @click="changesAMAccountName"><i class="el-icon-edit-outline"></i></span>
      </template>
    </el-table-column>
    <el-table-column>
      <template slot-scope="scope">
        <span  v-if="changespanshow.changesAMAccountNameshow" v-text="sAMAccountName"></span>
        <div v-else >
          <el-col :span="6">
            <el-input size="small" v-model="sAMAccountNameChangevalue"></el-input>
          </el-col>
          <el-col :span="6" style="margin-left:auto;margin-right:auto;">
            &nbsp;<span :class="classname.classSpancursorpointer" v-loading.fullscreen.lock="vLoadingShow" @click="savechangesAMAccountName"><i class="el-icon-upload2" style="font-size:150%;"></i></span>
            <span @click="closechangesAMAccountName" :class="classname.classSpancursorpointer"><i class="el-icon-close" style="font-size:150%;"></i></span>
          </el-col>
        </div>
      </template>
    </el-table-column>
  </el-table>
  <el-table :data="tableData3"  style="width: 100%" :show-header="false" v-cloak>
    <el-table-column width="180">
      <template slot-scope="scope">
        <el-tooltip class="item" effect="light" content="accountExpires" placement="left-start"><span>&nbsp;账户过期：</span></el-tooltip>
          <span style="font-size:130%;" v-if="changespanshow.changeaccountExpiresshow" :class="[classname.classSpanFloatRight,classname.classSpancursorpointer]" @click="changeaccountExpires"><i class="el-icon-edit-outline"></i></span>
      </template>
    </el-table-column>
    <el-table-column>
      <template slot-scope="scope">
        <div v-if="changespanshow.changeaccountExpiresshow" >
          <span v-if="accountExpires == '9999-12-31 23:59:59.999999' || accountExpires == '1601-01-01 00:00:00+00:00'">永不过期</span>
          <span v-else v-text="accountExpires.replace('.999999', '').replace('+00:00', '')">
          </span>
        </div>
        <div v-else>
          <el-col :span="6">
            <span v-if='accountExpirestimeisforever'>
              永不过期
            </span>
            <span v-else>
              过期时间
            </span>
            <el-switch
              v-model="accountExpirestimeisforever">
            </el-switch>
            <el-date-picker
              v-if="!accountExpirestimeisforever"
              v-model="saveaccountExpires"
              type="datetime"
              size="mini"
              value-format="yyyy-MM-dd HH:mm:ss"
              placeholder="选择过期时间">
            </el-date-picker>
          </el-col>
          <el-col :span="6" style="margin-left:auto;margin-right:auto;">
            &nbsp;<span :class="classname.classSpancursorpointer" v-loading.fullscreen.lock="vLoadingShow" @click="savechangeaccountExpires"><i class="el-icon-upload2" style="font-size:150%;"></i></span>
            <span @click="closechangeaccountExpires" :class="classname.classSpancursorpointer"><i class="el-icon-close" style="font-size:150%;"></i></span>
          </el-col>
        </div>
      </template>
    </el-table-column>
  </el-table>
  <el-table :data="tableData3" style="width: 100%" :show-header="false" v-cloak>
    <el-table-column width="180">
      <template slot-scope="scope">
        <el-tooltip class="item" effect="light" content="userAccountConte" placement="left-start"><span>&nbsp;账号禁用状态：</span></el-tooltip>
          <span style="font-size:130%;" v-if="changespanshow.changeuserAccountConteshow" :class="[classname.classSpanFloatRight,classname.classSpancursorpointer]" @click="userAccountContechangevalue = userAccountConte, changespanshow.changeuserAccountConteshow = false"><i class="el-icon-edit-outline"></i></span>
      </template>
    </el-table-column>
    <el-table-column>
      <template slot-scope="scope">
        <div v-if="changespanshow.changeuserAccountConteshow">
          <span v-if="userAccountConte">启用</span>
          <span v-else>禁用</span>
          <el-switch
            v-model="userAccountConte"
            disabled>
          </el-switch>
        </div>
        <div v-else>
          <el-col :span="6">
            <span v-if="userAccountContechangevalue">启用</span>
            <span v-else>禁用</span>
            <el-switch
              v-model="userAccountContechangevalue">
            </el-switch>
          </el-col>
          <el-col :span="6" style="margin-left:auto;margin-right:auto;">
            &nbsp;<span v-if="userAccountContechangevalue !== userAccountConte" :class="classname.classSpancursorpointer" v-loading.fullscreen.lock="vLoadingShow" @click="savechangeuserAccountConte"><i class="el-icon-upload2" style="font-size:150%;"></i></span>
            <span @click="changespanshow.changeuserAccountConteshow = true" :class="classname.classSpancursorpointer"><i class="el-icon-close" style="font-size:150%;"></i></span>
          </el-col>
        </div>
      </template>
    </el-table-column>
  </el-table>
  <el-table :data="tableData3" style="width: 100%" :show-header="false" v-cloak v-if="changespanshow.changeallAccidentallyDeletedshow">
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
  <el-table :data="tableData3" style="width: 100%" :show-header="false" v-cloak>
    <el-table-column width="180">
      <template slot-scope="scope">
        <el-tooltip class="item" effect="light" content="userlock" placement="left-start"><span>&nbsp;账号锁定状态：</span></el-tooltip>
      </template>
    </el-table-column>
    <el-table-column>
      <template slot-scope="scope">
        <span v-if="userlock">锁定</span>
        <span v-else>未锁定</span>
        <el-switch
          v-model="userlock"
          disabled>
        </el-switch>
        <el-button v-if="userlock" type="primary" round @click="unlockuser">解锁</el-button>
      </template>
    </el-table-column>
  </el-table>
  <el-table :data="tableData3"  style="width: 100%" :show-header="false" v-cloak>
    <el-table-column width="180">
      <template slot-scope="scope">
        <el-tooltip class="item" effect="light" content="whenCreated" placement="left-start"><span>&nbsp;账号创建时间：</span></el-tooltip>
      </template>
    </el-table-column>
    <el-table-column>
      <template slot-scope="scope">
        <span v-text="whenCreated"></span>
      </template>
    </el-table-column>
  </el-table>
  <el-table :data="tableData3"  style="width: 100%" :show-header="false" v-cloak>
    <el-table-column width="180">
      <template slot-scope="scope">
        <el-tooltip class="item" effect="light" content="whenChanged" placement="left-start"><span>&nbsp;账号修改时间：</span></el-tooltip>
      </template>
    </el-table-column>
    <el-table-column>
      <template slot-scope="scope">
        <span v-text="whenChanged"></span>
      </template>
    </el-table-column>
  </el-table>
  <el-table :data="tableData3"  style="width: 100%" :show-header="false" v-cloak>
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
  <el-table :data="tableData3"  style="width: 100%" :show-header="false" v-cloak>
    <el-table-column width="180">
      <template slot-scope="scope">
        <el-tooltip class="item" effect="light" content="msDS-UserPasswordExpiryTimeComputed" placement="bottom"><span>&nbsp;密码过期时间：</span></el-tooltip>
          <span style="font-size:130%;" v-if="changespanshow.msDSUserPasswordExpiryTimeComputed" :class="[classname.classSpanFloatRight,classname.classSpancursorpointer]" @click="changepasswordExpiryTimeComputed(), changespanshow.msDSUserPasswordExpiryTimeComputed = false"><i class="el-icon-edit-outline"></i></span>
      </template>
    </el-table-column>
    <el-table-column>
      <template slot-scope="scope">
        <div v-if="changespanshow.msDSUserPasswordExpiryTimeComputed">
        <span v-text="msDSUserPasswordExpiryTimeComputed"></span>&nbsp;&nbsp;
        <el-button tye="primary" @click="dialogVisible = true, changepassword.inputfirtspassword = '', changepassword.inputlastpassword = ''" round>修改密码</el-button>
        </div>
        <div v-else>
          <el-col :span="8">
            <el-checkbox v-model="msDSUserPasswordExpiryTimeComputedchangevalue" label="  密码永不过期"></el-checkbox>
          </el-col>
          <el-col :span="6" style="margin-left:auto;margin-right:auto;" v-if="!changespanshow.msDSUserPasswordExpiryTimeComputed">
            &nbsp;<span :class="classname.classSpancursorpointer" v-if="msDSUserPasswordExpiryTimeComputedchangevaluefirst !== msDSUserPasswordExpiryTimeComputedchangevalue" v-loading.fullscreen.lock="vLoadingShow" @click="savechangemsDSUserPasswordExpiryTimeComputed"><i class="el-icon-upload2" style="font-size:150%;"></i></span>
            <span @click="changespanshow.msDSUserPasswordExpiryTimeComputed = true" :class="classname.classSpancursorpointer"><i class="el-icon-close" style="font-size:150%;"></i></span>
          </el-col>
        </div>
      </template>
    </el-table-column>
  </el-table>
  <el-dialog
  title="修改密码"
  :visible.sync="dialogVisible"
  width="60%">
  <p><el-input type='password' placeholder="请输入密码" v-model="changepassword.inputfirtspassword">
    <template slot="prepend">请输入密码</template>
  </el-input></p>
  <p><el-input type='password' placeholder="请确认密码" v-model="changepassword.inputlastpassword">
    <template slot="prepend">请确认密码</template>
  </el-input></p>
  <span slot="footer" class="dialog-footer">
    <el-button @click="dialogVisible = false">取 消</el-button>
    <el-button type="primary" @click="truechangepassword">确 定</el-button>
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
// import { constants } from 'http2';
axios.defaults.withCredentials = true
export default{
  data () {
    return {
      value1: '',
      value3: true,
      classname: {
        classSpanFloatRight: 'classSpanFloatRight',
        classSpancursorpointer: 'classSpancursorpointer'
      },
      changepassword: {
        inputlastpassword: '',
        inputfirtspassword: ''
      },
      changespanshow: {
        changegivenNameshow: true,
        changesnshow: true,
        changecnshow: true,
        msDSUserPasswordExpiryTimeComputed: true,
        changesAMAccountNameshow: true,
        changeaccountExpiresshow: true,
        changeuserAccountConteshow: true,
        changeAccidentallyDeletedshow: true,
        changeallAccidentallyDeletedshow: false,
        changeinitialsshow: true
      },
      dialogVisible: false,
      changepasswordinputshowvalue: '修改密码',
      accountExpirestimeisforever: false, // 账户是否永不过期
      vLoadingShow: false, // 读条全屏遮罩
      givenName: null, // 名字
      givenNameChangevalue: null, // 名字
      initialsChangevalue: null, 
      snChangevalue: null, 
      cnChangevalue: null, 
      sAMAccountNameChangevalue: null, 
      initials: null, // 中间名首字母缩写
      cn: null, // 姓氏
      DN: null, // DN
      sn: null, // 全名
      userlock: false, // 是否锁定
      sAMAccountName: null, // sAMAccountName
      accountExpires: 'null', // 账户过期
      saveaccountExpires: null, // 保存账户过期时间
      AccidentallyDeleted: false, // 是否防删除
      AccidentallyDeletedchangevalue: false, // 是否防删除变更值
      msDSUserPasswordExpiryTimeComputedchangevalue: false, // 密码是否永不过期
      msDSUserPasswordExpiryTimeComputedchangevaluefirst: false, // 密码是否永不过期(初始对比值)
      displayName: null, // 显示名称
      msDSUserPasswordExpiryTimeComputed: null, // 密码过期
      whenCreated: null, // 账号创建时间
      whenChanged: null, // 账号修改时间
      userAccountConte: false, // 账号是否禁用
      userAccountContechangevalue: false, // 账号是否禁用修改值
      userAccountControl: 0, // 账号状态值
      userDN: null,
      tableData3: [{
        date: 'displayName'
      }]
    }
  },
  async created () {
    this.atsrtmethods()
  },
  methods: {
    async atsrtmethods () {
      const loading = this.$loading({
        lock: true
      })
      let disNameforurl = this.getQueryVariable('disName')
      if (!disNameforurl) {
        let objectDNforurl = this.getQueryVariabledecode('objectDN')
        await this.getsamaccountvaluebydn(objectDNforurl)
      }
      axios
        .get(this.serviceurl() + '/api/GetUserMessage/?CountName=' + disNameforurl)
        .then(response => {
          loading.close()
          if (response.data.isSuccess) {
            this.displayName = response.data.message.displayName
            this.cn = response.data.message.cn
            this.DN = response.data.message.distinguishedName
            this.sn = response.data.message.sn
            this.initials = response.data.message.initials
            this.givenName = response.data.message.givenName
            this.sAMAccountName = response.data.message.sAMAccountName
            this.whenCreated = moment(String(response.data.message.whenCreated)).format('YYYY-MM-DD HH:mm:ss')
            this.whenChanged = moment(String(response.data.message.whenChanged)).format('YYYY-MM-DD HH:mm:ss')
            this.accountExpires = response.data.message.accountExpires
            this.userAccountConte = response.data.message.userAccountConte
            this.userAccountControl = response.data.message.userAccountControl
            this.msDSUserPasswordExpiryTimeComputed = response.data.message.msDSUserPasswordExpiryTimeComputed
            this.tableData3 = [{
              date: 'displayName'
            }]
            var instance = axios.create({
              headers: {'content-type': 'application/x-www-form-urlencoded'}
            })
            let data = {sAMAccountName: disNameforurl}
            this.changespanshow.changeallAccidentallyDeletedshow = false
            instance.post(this.serviceurl() + '/canAccidentallyDeleted/', qs.stringify(data)).then(response => {
              if (response.data.isSuccess) {
                this.changespanshow.changeallAccidentallyDeletedshow = true
                if (response.data.ResultCode === -1 || response.data.ResultCode === '-1') {
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
      this.userlock = false
      let instance = axios.create({
        headers: {'content-type': 'application/x-www-form-urlencoded'}
      })
      let data = {sAMAccountName: disNameforurl}
      instance.post(this.serviceurl() + '/serchLock/', qs.stringify(data))
        .then(response => {
          if (response.data.isSuccess) {
            this.userlock = true
          }
        })
    },
    changepasswordExpiryTimeComputed: function () {
      if (this.msDSUserPasswordExpiryTimeComputed === '密码永不过期') {
        this.msDSUserPasswordExpiryTimeComputedchangevaluefirst = true
        this.msDSUserPasswordExpiryTimeComputedchangevalue = true
      } else {
        this.msDSUserPasswordExpiryTimeComputedchangevaluefirst = false
        this.msDSUserPasswordExpiryTimeComputedchangevalue = false
      }
    },
    async getsamaccountvaluebydn (objectDNforurl) {
      let usermessagevalue = await axios.get(this.serviceurl() + '/api/GetUserMessage/?CountName=' + objectDNforurl + '&objectClass=DN')
      if (usermessagevalue.data.isSuccess) {
        if ((usermessagevalue.data.message.objectClass).sort().toString() === (["top", "person", "organizationalPerson", "user"]).sort().toString()) {
            window.location.search = '?disName=' + usermessagevalue.data.message.sAMAccountName
        }
      }
    },
    unlockuser: function () {
      this.vLoadingShow = true
      let disNameforurl = this.getQueryVariable('disName')
      let instance = axios.create({
        headers: {'content-type': 'application/x-www-form-urlencoded'}
      })
      let data = {sAMAccountName: disNameforurl}
      instance.post(this.serviceurl() + '/unLockuser/', qs.stringify(data))
        .then(response => {
          if (response.data.isSuccess) {
            this.messagealertvalue('解锁成功', 'success')
            this.userlock = false
          } else {
            if (response.data.message === '权限不足') {
              this.messagealertvalue('权限不足', 'error')
            } else {
              this.messagealertvalue('解锁失败', 'error')
            }
          }
        })
    },
    ChangeUserMessagefuction: function (Attributesvalue, ChangeMessagevalue) {
      this.vLoadingShow = true
      axios
        .get(this.serviceurl() + '/api/ChangeUserMessage/?CountName=' + this.sAMAccountName + '&ChangeMessage=' + ChangeMessagevalue + '&Attributes=' + Attributesvalue)
        .then(response => {
          if (response.data.isSuccess) {
            this.messagealertvalue('修改成功', 'success')
            if (Attributesvalue === 'givenName') {
              this.givenName = this.givenNameChangevalue
              this.changespanshow.changegivenNameshow = true
            } else if (Attributesvalue === 'initials') {
              this.initials = this.initialsChangevalue
              this.changespanshow.changeinitialsshow = true
            } else if (Attributesvalue === 'sn') {
              this.sn = this.snChangevalue
              this.changespanshow.changesnshow = true
            } else if (Attributesvalue === 'cn') {
              this.cn = this.cnChangevalue
              this.changespanshow.changecnshow = true
              window.location.search = '?disName=' + this.sAMAccountName
            } else if (Attributesvalue === 'sAMAccountName') {
              this.sAMAccountName = this.sAMAccountNameChangevalue
              this.changespanshow.changesAMAccountNameshow = true
              window.location.search = '?disName=' + this.sAMAccountNameChangevalue
            } else if (Attributesvalue === 'accountExpires') {
              this.accountExpires = '1601-01-01 00:00:00+00:00'
              this.changespanshow.changeaccountExpiresshow = true
            } else if (Attributesvalue === 'userAccountControl') {
              this.atsrtmethods()
              this.changespanshow.changeuserAccountConteshow = true
              this.changespanshow.msDSUserPasswordExpiryTimeComputed = true
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
    ChangeaccountExpiresfuction: function (ChangeMessagevalue) {
      this.vLoadingShow = true
      axios
        .get(this.serviceurl() + '/api/ChangeaccountExpires/?CountName=' + this.sAMAccountName + '&accountExpires=' + ChangeMessagevalue)
        .then(response => {
          if (response.data.isSuccess) {
            this.messagealertvalue('修改成功', 'success')
            this.accountExpires = ChangeMessagevalue
            this.changespanshow.changeaccountExpiresshow = true
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
    Changecnfuction: function (ChangeMessagevalue) {
      this.vLoadingShow = true
      axios
        .get(this.serviceurl() + '/api/ChangeDN/?CountName=' + this.sAMAccountName + '&newName=' + ChangeMessagevalue)
        .then(response => {
          if (response.data.isSuccess) {
            this.messagealertvalue('修改成功', 'success')
            this.cn = this.cnChangevalue
            this.changespanshow.changecnshow = true
            window.location.reload()
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
    changegivenName: function () {
      this.givenNameChangevalue = this.givenName
      this.changespanshow.changegivenNameshow = false
    },
    closechangegivenName: function () {
      this.changespanshow.changegivenNameshow = true
    },
    savechangegivenName: function () {
      this.ChangeUserMessagefuction('givenName', this.givenNameChangevalue)
    },
    changeinitials: function () {
      this.initialsChangevalue = this.initials
      this.changespanshow.changeinitialsshow = false
    },
    closechangeinitials: function () {
      this.changespanshow.changeinitialsshow = true
    },
    savechangeinitials: function () {
      this.ChangeUserMessagefuction('initials', this.initialsChangevalue)
    },
    changesn: function () {
      this.snChangevalue = this.sn
      this.changespanshow.changesnshow = false
    },
    closechangesn: function () {
      this.changespanshow.changesnshow = true
    },
    savechangesn: function () {
      this.ChangeUserMessagefuction('sn', this.snChangevalue)
    },
    changecn: function () {
      this.cnChangevalue = this.cn
      this.changespanshow.changecnshow = false
    },
    closechangecn: function () {
      this.changespanshow.changecnshow = true
    },
    savechangecn: function () {
      this.Changecnfuction(this.cnChangevalue)
    },
    changesAMAccountName: function () {
      this.sAMAccountNameChangevalue = this.sAMAccountName
      this.changespanshow.changesAMAccountNameshow = false
    },
    closechangesAMAccountName: function () {
      this.changespanshow.changesAMAccountNameshow = true
    },
    savechangesAMAccountName: function () {
      this.ChangeUserMessagefuction('sAMAccountName', this.sAMAccountNameChangevalue)
    },
    truechangepassword: function () {
      if (this.changepassword.inputlastpassword !== this.changepassword.inputfirtspassword) {
        this.messagealertvalue('两次密码不一致', 'error')
      } else {
        let instance = axios.create({
          headers: {'content-type': 'application/x-www-form-urlencoded'}
        })
        let data = {distinguishedName: this.DN, newpassword: this.changepassword.inputfirtspassword}
        instance.post(this.serviceurl() + '/resetUserPassword/', qs.stringify(data)).then(response => {
          this.vLoadingShow = false
          if (response.data.isSuccess) {
            this.messagealertvalue('修改成功', 'success')
            this.dialogVisible = false
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
    savechangeuserAccountConte: function () {
      let lastvalue = 0
      if (this.userAccountContechangevalue) {
        lastvalue = Number(this.userAccountControl) - Number(2)
      } else {
        lastvalue = Number(this.userAccountControl) + Number(2)
      }
      this.ChangeUserMessagefuction('userAccountControl', lastvalue)
    },
    savechangemsDSUserPasswordExpiryTimeComputed: function () {
      let lastvalue = 0
      if (this.msDSUserPasswordExpiryTimeComputedchangevalue) {
        lastvalue = Number(this.userAccountControl) + Number(65536)
      } else {
        lastvalue = Number(this.userAccountControl) - Number(65536)
      }
      this.ChangeUserMessagefuction('userAccountControl', lastvalue)
      this.atsrtmethods()
    },
    changeaccountExpires: function () {
      this.accountExpiresChangevalue = this.accountExpires
      this.changespanshow.changeaccountExpiresshow = false
      if (this.accountExpires === '9999-12-31 23:59:59.999999' || this.accountExpires === '1601-01-01 00:00:00+00:00') {
        this.accountExpirestimeisforever = true
        this.saveaccountExpires = null
      } else {
        this.accountExpirestimeisforever = false
        this.saveaccountExpires = this.accountExpires.replace('.999999', '').replace('+00:00', '')
      }
    },
    closechangeaccountExpires: function () {
      this.changespanshow.changeaccountExpiresshow = true
    },
    savechangeaccountExpires: function () {
      if (this.accountExpirestimeisforever) {
        this.ChangeUserMessagefuction('accountExpires', '0')
      } else {
        if (this.saveaccountExpires === null) {
          this.messagealertvalue('请选择一个日期', 'error')
        } else {
          this.ChangeaccountExpiresfuction(this.saveaccountExpires)
        }
      }
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
