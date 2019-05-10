<template>
  <el-col :span="24" v-show="loadingstopshowall" v-if="hasexchangemailbox" :default-active="activeIndex">
  <el-menu class="el-menu-demo" mode="horizontal">
    <!-- <el-menu-item @click="addsmtpvalue" index="2">新增smtp地址</el-menu-item> -->
    <el-submenu index="3">
      <template slot="title">邮箱设置</template>
      <el-menu-item @click="changeVisiblecapacitydiagshow" index="3-1">容量配额修改</el-menu-item>
      <el-menu-item v-if="ArchiveDatabase !== null" @click="changearchiveVisiblecapacitydiagshow" index="3-2">归档容量配额修改</el-menu-item>
      <el-menu-item v-else @click="changetrueaddarchivemailboxdiagshow" index="3-3">启用归档</el-menu-item>
      <el-menu-item @click="addsmtpvalue" index="3-4">新增smtp地址</el-menu-item>
    </el-submenu>
    <el-menu-item @click="changemailboxfeatures" index="4">邮箱功能</el-menu-item>
    <el-submenu index="5">
      <template slot="title">特殊权限</template>
      <el-menu-item index="5-1" @click="dialogFullAccessshow">管理完全访问权限</el-menu-item>
      <el-menu-item index="5-2" @click="dialogPermissionshow">管理代理发送权限</el-menu-item>
      <el-menu-item index="5-3" @click="dialogpublicDelegatesshow">管理代表发送权限</el-menu-item>
    </el-submenu>
  </el-menu>
  <!-- <el-button round @click="addsmtpvalue">新增smtp地址</el-button>
  <el-button round @click="changeVisiblecapacitydiagshow">容量配额修改</el-button>
  <el-button round v-if="ArchiveDatabase !== ''" @click="changearchiveVisiblecapacitydiagshow">归档容量配额修改</el-button>
  <el-button round v-else @click="changetrueaddarchivemailboxdiagshow">启用归档</el-button>
  <br> -->
  <el-table :data="tableData3"  style="width: 100%" :show-header="false" v-cloak>
    <el-table-column>
      <template slot-scope="scope">
        <span v-if="IssueWarningQuota === 'unlimited'">警告容量使用（总容量：无限制）</span>
        <span v-else>警告容量使用（总容量： <span v-text="IssueWarningQuota.split(' (')[0]"></span>）</span>
      </template>
    </el-table-column>
    <el-table-column>
      <template slot-scope="scope">
        <span v-if="ProhibitSendQuota === 'unlimited'">禁止外发容量使用（总容量：无限制）</span>
        <span v-else>禁止外发容量使用（总容量：<span v-text="ProhibitSendQuota.split(' (')[0]"></span>）</span>
      </template>
    </el-table-column>
    <el-table-column>
      <template slot-scope="scope">
        <span v-if="ProhibitSendReceiveQuota === 'unlimited'">禁止收发容量使用（总容量：无限制）</span>
        <span v-else>禁止收发容量使用（总容量：<span v-text="ProhibitSendReceiveQuota.split(' (')[0]"></span>）</span>
      </template>
    </el-table-column>
    <el-table-column v-if="ArchiveDatabase !== null">
      <template slot-scope="scope">
        <span v-if="ArchiveWarningQuota === 'unlimited'">存档警告容量使用（总容量：无限制）</span>
        <span>存档警告容量使用（总容量：<span v-text="ArchiveWarningQuota.split(' (')[0]"></span>）</span>
      </template>
    </el-table-column>
    <el-table-column v-if="ArchiveDatabase !== null">
      <template slot-scope="scope">
        <span v-if="ArchiveQuota === 'unlimited'">存档容量使用（总容量：无限制）</span>
        <span>存档容量使用（总容量：<span v-text="ArchiveQuota.split(' (')[0]"></span>）</span>
      </template>
    </el-table-column>
  </el-table>
  <el-table :data="tableData3"  style="width: 100%" :show-header="false" v-cloak>
    <el-table-column>
      <template slot-scope="scope">
        <span v-text="TotalItemSize.split(' (')[0]"></span>
        <el-progress :percentage="percentageIssueWarningQuota" style='white-space:nowrap'></el-progress>
      </template>
    </el-table-column>
    <el-table-column>
      <template slot-scope="scope">
        <span v-text="TotalItemSize.split(' (')[0]"></span>
        <el-progress :percentage="percentageProhibitSendQuota" style='white-space:nowrap'></el-progress>
      </template>
    </el-table-column>
    <el-table-column>
      <template slot-scope="scope">
        <span v-text="TotalItemSize.split(' (')[0]"></span>
        <el-progress :percentage="percentageProhibitSendReceiveQuota" style='white-space:nowrap'></el-progress>
      </template>
    </el-table-column>
    <el-table-column v-if="ArchiveDatabase !== null">
      <template slot-scope="scope">
        <span v-text="ArTotalItemSize.split(' (')[0]"></span>
        <el-progress :percentage="percentageArchiveWarningQuota" style='white-space:nowrap'></el-progress>
      </template>
    </el-table-column>
    <el-table-column v-if="ArchiveDatabase !== null">
      <template slot-scope="scope">
        <span v-text="ArTotalItemSize.split(' (')[0]"></span>
        <el-progress :percentage="percentageArchiveQuota" style='white-space:nowrap'></el-progress>
      </template>
    </el-table-column>
  </el-table>
  <el-table :data="tableData3"  style="width: 100%" :show-header="false" v-cloak>
    <el-table-column width="180">
      <template slot-scope="scope">
        <el-tooltip class="item" effect="light" content="RulesQuota" placement="left-start"><span>&nbsp;规则大小：</span></el-tooltip>
        <span style="font-size:130%;" v-if="changespanshow.changeRulesQuotashow" :class="[classname.classSpanFloatRight,classname.classSpancursorpointer]" @click="changespanshow.changeRulesQuotashow = false, RulesQuotaselectfirstvalue = RulesQuota"><i class="el-icon-edit-outline"></i></span>
      </template>
    </el-table-column>
    <el-table-column>
      <template slot-scope="scope">
        <span v-if="changespanshow.changeRulesQuotashow" v-text="RulesQuota"></span>
        <div v-else >
          <el-col :span="6">
              <el-select v-model="RulesQuotaselectfirstvalue" placeholder="请选择" size="mini" style="width: 95%">
                <el-option
                  v-for="item in RulesQuotaselectvalue"
                  :key="item.value"
                  :label="item.label"
                  :value="item.value">
                </el-option>
              </el-select>
          </el-col>
          <el-col :span="6" style="margin-left:auto;margin-right:auto;">
            &nbsp;<span :class="classname.classSpancursorpointer" v-loading.fullscreen.lock="vLoadingShow" @click="changemailboxvalue('RulesQuota' ,RulesQuotaselectfirstvalue)"><i class="el-icon-upload2" style="font-size:150%;"></i></span>
            <span @click="changespanshow.changeRulesQuotashow = true" :class="classname.classSpancursorpointer"><i class="el-icon-close" style="font-size:150%;"></i></span>
          </el-col>
        </div>
      </template>
    </el-table-column>
  </el-table>
  <el-table :data="tableData3"  style="width: 100%" :show-header="false" v-cloak>
    <el-table-column width="180">
      <template slot-scope="scope">
        <el-tooltip class="item" effect="light" content="RecipientLimits" placement="left-start"><span>&nbsp;最大发件人数量：</span></el-tooltip>
        <span style="font-size:130%;" v-if="changespanshow.changeRecipientLimitsshow" :class="[classname.classSpanFloatRight,classname.classSpancursorpointer]" @click="changespanshow.changeRecipientLimitsshow = false"><i class="el-icon-edit-outline"></i></span>
      </template>
    </el-table-column>
    <el-table-column>
      <template slot-scope="scope">
        <div v-if="changespanshow.changeRecipientLimitsshow">
          <div v-if="RecipientLimits === 'unlimited'" >
            <span v-pre>没个人限制</span>
          </div>
          <div v-else >
            <span v-text="RecipientLimits"></span>（个）
          </div>
        </div>
        <div v-else>
          <el-col :span="6">
              <el-select v-model="RecipientLimitsaselectfirstvalue" placeholder="请选择" size="mini" style="width: 95%">
                <el-option
                  v-for="item in RecipientLimitsaselectvalue"
                  :key="item.value"
                  :label="item.label"
                  :value="item.value">
                </el-option>
              </el-select>
          </el-col>
          <el-col :span="6" style="margin-left:auto;margin-right:auto;">
            &nbsp;<span :class="classname.classSpancursorpointer" v-loading.fullscreen.lock="vLoadingShow" @click="changemailboxvalue('RecipientLimits' ,RecipientLimitsaselectfirstvalue)"><i class="el-icon-upload2" style="font-size:150%;"></i></span>
            <span @click="changespanshow.changeRecipientLimitsshow = true" :class="classname.classSpancursorpointer"><i class="el-icon-close" style="font-size:150%;"></i></span>
          </el-col>
        </div>
      </template>
    </el-table-column>
  </el-table>
  <el-table :data="tableData3"  style="width: 100%" :show-header="false" v-cloak>
    <el-table-column width="180">
      <template slot-scope="scope">
        <el-tooltip class="item" effect="light" content="Database" placement="left-start"><span>&nbsp;邮箱数据库：</span></el-tooltip>
        <span style="font-size:130%;" v-if="MailboxMoveStatus === 'None'" :class="[classname.classSpanFloatRight,classname.classSpancursorpointer]" @click="getallmailboxdatabasenameaccount"><i class="el-icon-edit-outline"></i></span>
      </template>
    </el-table-column>
    <el-table-column>
      <template slot-scope="scope">
          <span v-text="Database"></span>
      </template>
    </el-table-column>
  </el-table>
  <el-table :data="tableData3"  style="width: 100%" :show-header="false" v-cloak v-if="ArchiveDatabase !== null">
    <el-table-column width="180">
      <template slot-scope="scope">
        <el-tooltip class="item" effect="light" content="ArchiveDatabase" placement="left-start"><span>&nbsp;邮箱归档数据库：</span></el-tooltip>
        <span style="font-size:130%;" v-if="MailboxMoveStatus === 'None'" :class="[classname.classSpanFloatRight,classname.classSpancursorpointer]" @click="getallmailboxdatabasearchivename"><i class="el-icon-edit-outline"></i></span>
      </template>
    </el-table-column>
    <el-table-column>
      <template slot-scope="scope">
          <span v-text="ArchiveDatabase"></span>
      </template>
    </el-table-column>
  </el-table>
  <el-table :data="tableData3"  style="width: 100%" :show-header="false" v-cloak>
    <el-table-column width="180">
      <template slot-scope="scope">
        <el-tooltip class="item" effect="light" content="MailboxMoveStatus" placement="left-start"><span>&nbsp;邮箱数据库迁移状态：</span></el-tooltip>
      </template>
    </el-table-column>
    <el-table-column>
      <template slot-scope="scope">
          <span v-text="MailboxMoveStatus"></span>
          <span style="font-size:130%;" v-if="MailboxMoveStatus !== 'None'" :class="[classname.classSpancursorpointer]" @click="delmovedatabase"><i class="el-icon-delete"></i></span>
      </template>
    </el-table-column>
  </el-table>
  <el-table :data="tableData3"  style="width: 100%" :show-header="false" v-cloak>
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
  <el-table :data="tableData3"  style="width: 100%" :show-header="false" v-cloak>
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
            <span size="small" v-show="EmailAddressPolicyEnabledChangevalue === 'False' || EmailAddressPolicyEnabledChangevalue === 'false'" v-text="EmailAddressPolicyEnabledchangemessagevalue.falsevmessagevalue"></span>
            <span size="small" v-show="EmailAddressPolicyEnabledChangevalue === 'True' || EmailAddressPolicyEnabledChangevalue === 'true'" v-text="EmailAddressPolicyEnabledchangemessagevalue.truevmessagevalue"></span>
            <el-switch
              active-value = 'true'
              inactive-value = 'false'
              v-model="EmailAddressPolicyEnabledChangevalue">
            </el-switch>
          </el-col>
          <el-col :span="6" style="margin-left:auto;margin-right:auto;">
            &nbsp;<span :class="classname.classSpancursorpointer" v-loading.fullscreen.lock="vLoadingShow" @click="changemailboxvalue('EmailAddressPolicyEnabled' ,EmailAddressPolicyEnabledChangevalue.toLowerCase())"><i class="el-icon-upload2" style="font-size:150%;"></i></span>
            <span @click="changespanshow.changeEmailAddressPolicyEnabledshow = true" :class="classname.classSpancursorpointer"><i class="el-icon-close" style="font-size:150%;"></i></span>
          </el-col>
        </div>
      </template>
    </el-table-column>
  </el-table>
  <el-table :data="tableData3"  style="width: 100%" :show-header="false" v-cloak>
    <el-table-column width="180">
      <template slot-scope="scope">
        <el-tooltip class="item" effect="light" content="SMTP" placement="left-start"><span>&nbsp;SMTP:</span></el-tooltip>
        <span style="font-size:130%;" v-if="changespanshow.changeSMTPshow && (EmailAddressPolicyEnabled === 'False' || EmailAddressPolicyEnabled === 'false')" :class="[classname.classSpanFloatRight,classname.classSpancursorpointer]" @click="changespanshow.changeSMTPshow = false, SMTPChangevalue = SMTP"><i class="el-icon-edit-outline"></i></span>
      </template>
    </el-table-column>
    <el-table-column>
      <template slot-scope="scope">
        <span v-if="changespanshow.changeSMTPshow" v-text="SMTP"></span>
        <div v-if="!changespanshow.changeSMTPshow && (EmailAddressPolicyEnabled === 'False' || EmailAddressPolicyEnabled === 'false')" >
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
  <el-table :data="tableData3"  v-for="smtpvalue in smtp" :key='smtpvalue' style="width: 100%" :show-header="false" v-cloak>
    <el-table-column width="180">
      <template slot-scope="scope">
        <el-tooltip class="item" effect="light" content="smtp" placement="left-start"><span>&nbsp;smtp:</span></el-tooltip>
      </template>
    </el-table-column>
    <el-table-column>
      <template slot-scope="scope">
          <span v-text="smtpvalue"></span>
          <el-tooltip class="item" effect="light" content="删除smtp" placement="right-start"><span @click="Deletesmtp(smtpvalue)"><i class="el-icon-delete" style="font-size:130%;" :class="classname.classSpancursorpointer"></i></span></el-tooltip>
          <el-tooltip v-show="EmailAddressPolicyEnabled === 'False' || EmailAddressPolicyEnabled === 'false'" class="item" effect="light" content="设置为主SMTP" placement="right-start"><span @click="smtptoSMTP(smtpvalue)"><i class="el-icon-edit-outline" style="font-size:130%;" :class="classname.classSpancursorpointer"></i></span></el-tooltip>
      </template>
    </el-table-column>
  </el-table>
<el-dialog
  :visible.sync="dialogVisible"
  width="60%">
  <span>请选择数据库</span>
  <el-select v-model="Databasechangevalue" placeholder="请选择">
    <el-option
      v-for="item in alldatabasename"
      :key="item.danamevalue"
      :label="item.daname"
      :value="item.daname">
    </el-option>
  </el-select>
  <span slot="footer" class="dialog-footer">
    <el-button @click="dialogVisible = false">取 消</el-button>
    <el-button type="primary" @click="truechangemailboxdatabasevalue">确 定</el-button>
  </span>
</el-dialog>
<el-dialog
  :visible.sync="dialogarchiveVisible"
  width="60%">
  <span>请选择归档数据库</span>
  <el-select v-model="Databasearchivechangevalue" placeholder="请选择">
    <el-option
      v-for="item in alldatabasename"
      :key="item.danamevalue"
      :label="item.daname"
      :value="item.daname">
    </el-option>
  </el-select>
  <span slot="footer" class="dialog-footer">
    <el-button @click="dialogarchiveVisible = false">取 消</el-button>
    <el-button type="primary" @click="truechangearchivemailboxdatabasevalue">确 定</el-button>
  </span>
</el-dialog>
<el-dialog
  :visible.sync="dialogaddarchivemailbox"
  width="60%">
  <span>请选择数据库</span>
  <el-select v-model="Databasechangevalue" placeholder="请选择">
    <el-option
      v-for="item in alldatabasename"
      :key="item.danamevalue"
      :label="item.daname"
      :value="item.daname">
    </el-option>
  </el-select>
  <span slot="footer" class="dialog-footer">
    <el-button @click="dialogaddarchivemailbox = false">取 消</el-button>
    <el-button type="primary" @click="trueaddarchivemailboxvalue">确 定</el-button>
  </span>
</el-dialog>
<el-dialog
  title="储存配额"
  :visible.sync="dialogVisiblecapacity"
  width="60%">
  <p>
    <el-checkbox v-model="mailboxsettingcheck">使用邮箱数据库默认设置</el-checkbox>
  </p>
  <br>
  <div v-if="!mailboxsettingcheck">
    <p>
      <span>当邮箱大小超出指定大小时</span>
    </p>
    <p>
      &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<el-checkbox v-model="changeVisiblecapacity.changeisIssueWarningQuotacheckvalue">达到该限度时发出警告 (MB)</el-checkbox>
      <input v-if="changeVisiblecapacity.changeisIssueWarningQuotacheckvalue" v-model="changeisIssueWarningQuotainputvalue" :class="classname.classSpanFloatRight" type="number">
      <input v-else :class="classname.classSpanFloatRight" type="number" v-model="changeisIssueWarningQuotainputvalue" disabled>
    </p>
    <p>
      &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<el-checkbox v-model="changeVisiblecapacity.changeisProhibitSendQuotacheckvalue">达到该限度时禁止发送 (MB)</el-checkbox>
      <input v-if="changeVisiblecapacity.changeisProhibitSendQuotacheckvalue" v-model="changeisProhibitSendQuotainputvalue" :class="classname.classSpanFloatRight" type="number">
      <input v-else :class="classname.classSpanFloatRight" type="number" v-model="changeisProhibitSendQuotainputvalue" disabled>
    </p>
    <p>
      &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<el-checkbox v-model="changeVisiblecapacity.changeisProhibitSendReceiveQuotacheckvalue">达到该限度时禁止发送和接收 (MB)</el-checkbox>
      <input v-if="changeVisiblecapacity.changeisProhibitSendReceiveQuotacheckvalue" v-model="changeisProhibitSendReceiveQuotainputvalue" :class="classname.classSpanFloatRight" type="number">
      <input v-else :class="classname.classSpanFloatRight" type="number" v-model="changeisProhibitSendReceiveQuotainputvalue" disabled>
    </p>
  </div>
  <span slot="footer" class="dialog-footer">
    <el-button @click="dialogVisiblecapacity = false">取 消</el-button>
    <el-button type="primary" @click="saveVisiblecapacitychangevalue">保 存</el-button>
  </span>
</el-dialog>
<el-dialog
  title="储存配额"
  :visible.sync="dialogarchiveVisiblecapacity"
  width="60%">
  <p>
      &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;存档配额 (MB)
      <input v-model="changearchiveisProhibitSendReceiveQuotainputvalue" :class="classname.classSpanFloatRight" type="number">
  </p>
  <br>
  <div v-if="!mailboxsettingcheck">
    <p>
      <span>当存档大小超出指定大小时</span>
    </p>
    <p>
      &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<el-checkbox v-model="changeVisiblecapacity.changearchiveisIssueWarningQuotacheckvalue">达到该限度时发出警告 (MB)</el-checkbox>
      <input v-if="changeVisiblecapacity.changearchiveisIssueWarningQuotacheckvalue" v-model="changearchiveisIssueWarningQuotainputvalue" :class="classname.classSpanFloatRight" type="number">
      <input v-else :class="classname.classSpanFloatRight" type="number" v-model="changearchiveisIssueWarningQuotainputvalue" disabled>
    </p>
  </div>
  <span slot="footer" class="dialog-footer">
    <el-button @click="dialogarchiveVisiblecapacity = false">取 消</el-button>
    <el-button type="primary" @click="savearchiveVisiblecapacitychangevalue">保 存</el-button>
  </span>
</el-dialog>
<el-dialog
  title="邮箱功能"
  :visible.sync="dialogmailboxfeatures"
  width="60%">
  <el-table :data="tableData3" style="width: 100%" :show-header="false" v-cloak>
    <el-table-column width="180">
      <template slot-scope="scope">
        <el-tooltip class="item" effect="light" content="OWAEnabled" placement="left-start"><span>&nbsp;Outlook Web App：</span></el-tooltip>
      </template>
    </el-table-column>
    <el-table-column>
      <template slot-scope="scope">
        <span v-if="OWAEnabled">已启用</span>
        <span v-else>已禁用</span>
        <el-switch
          v-model="OWAEnabled"
          @change="changetest('OWAEnabled', $event)">
        </el-switch>

      </template>
    </el-table-column>
  </el-table>
  <el-table :data="tableData3" style="width: 100%" :show-header="false" v-cloak>
    <el-table-column width="180">
      <template slot-scope="scope">
        <el-tooltip class="item" effect="light" content="ActiveSyncEnabled" placement="left-start"><span>&nbsp;Exchange ActiveSync：</span></el-tooltip>
      </template>
    </el-table-column>
    <el-table-column>
      <template slot-scope="scope">
        <span v-if="ActiveSyncEnabled">已启用</span>
        <span v-else>已禁用</span>
        <el-switch
          v-model="ActiveSyncEnabled"
          @change="changetest('ActiveSyncEnabled', $event)">
        </el-switch>

      </template>
    </el-table-column>
  </el-table>
  <el-table :data="tableData3" style="width: 100%" :show-header="false" v-cloak>
    <el-table-column width="180">
      <template slot-scope="scope">
        <el-tooltip class="item" effect="light" content="MAPIEnabled" placement="left-start"><span>&nbsp;MAPI：</span></el-tooltip>
      </template>
    </el-table-column>
    <el-table-column>
      <template slot-scope="scope">
        <span v-if="MAPIEnabled">已启用</span>
        <span v-else>已禁用</span>
        <el-switch
          v-model="MAPIEnabled"
          @change="changetest('MAPIEnabled', $event)">
        </el-switch>

      </template>
    </el-table-column>
  </el-table>
  <el-table :data="tableData3" style="width: 100%" :show-header="false" v-cloak>
    <el-table-column width="180">
      <template slot-scope="scope">
        <el-tooltip class="item" effect="light" content="PopEnabled" placement="left-start"><span>&nbsp;POP3：</span></el-tooltip>
      </template>
    </el-table-column>
    <el-table-column>
      <template slot-scope="scope">
        <span v-if="PopEnabled">已启用</span>
        <span v-else>已禁用</span>
        <el-switch
          v-model="PopEnabled"
          @change="changetest('PopEnabled', $event)">
        </el-switch>
      </template>
    </el-table-column>
  </el-table>
  <el-table :data="tableData3" style="width: 100%" :show-header="false" v-cloak>
    <el-table-column width="180">
      <template slot-scope="scope">
        <el-tooltip class="item" effect="light" content="ImapEnabled" placement="left-start"><span>&nbsp;IMAP4：</span></el-tooltip>
      </template>
    </el-table-column>
    <el-table-column>
      <template slot-scope="scope">
        <span v-if="ImapEnabled">已启用</span>
        <span v-else>已禁用</span>
        <el-switch
          v-model="ImapEnabled"
          @change="changetest('ImapEnabled', $event)">
        </el-switch>

      </template>
    </el-table-column>
  </el-table>
  <span slot="footer" class="dialog-footer">
    <el-button @click="dialogmailboxfeatures = false">关 闭</el-button>
  </span>
</el-dialog>
<el-dialog
  title="选择要授予或删除完全访问权限的用户或组"
  :visible.sync="dialogFullAccess"
  width="60%">
  <el-table :data="FullAccesslistvalue" style="width: 100%" v-cloak height="250">
    <el-table-column label="Name" prop="DN">
      <template slot="header" slot-scope="scope">
        DN
      </template>
    </el-table-column>
    <el-table-column
      align="right"
      min-width="35%">
      <template slot="header" slot-scope="scope">
        <el-button size="mini" type="text" @click="dialogVisiblesearchusershow">添加权限</el-button>
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
    <el-button @click="dialogFullAccess = false">关 闭</el-button>
    <!-- <el-button type="primary" @click="savechangeauthOrig">保 存</el-button> -->
  </span>
</el-dialog>
<el-dialog
  title="搜索成员"
  :visible.sync="dialogVisiblesearchuser"
  width="60%"
  center>
  <el-select
  v-model="value9"
  multiple
  filterable
  :multiple-limit="onevalue"
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
    <el-button type="primary" @click="addobjecttoFullAccess">添 加</el-button>
  </span>
</el-dialog>
<el-dialog
  title="搜索成员"
  :visible.sync="dialogpublicDelegatessearchusershow"
  width="60%"
  center>
  <el-select
  v-model="value9"
  multiple
  filterable
  remote
  placeholder="请输入成员关键信息"
  :remote-method="remoteMethodpublicDelegates"
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
    <el-button @click="dialogpublicDelegatessearchusershow = false">取 消</el-button>
    <el-button type="primary" @click="addobjecttopublicDelegates">添 加</el-button>
  </span>
</el-dialog>
<el-dialog
  title="搜索成员aaa"
  :visible.sync="dialogPermissionsearchusershow"
  width="60%"
  center>
  <el-select
  v-model="value9"
  multiple
  filterable
  remote
  :multiple-limit="onevalue"
  placeholder="请输入成员关键信息"
  :remote-method="remoteMethodpublicDelegates"
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
    <el-button @click="dialogPermissionsearchusershow = false">取 消</el-button>
    <el-button type="primary" @click="addobjecttoPermission">添 加</el-button>
  </span>
</el-dialog>
<el-dialog
  title="选择要授予或删除代理发送权限的用户或组"
  :visible.sync="dialogPermission"
  width="60%">
  <el-table :data="Permissionlistvalue" style="width: 100%" v-cloak height="250">
    <el-table-column label="Name" prop="DN">
      <template slot="header" slot-scope="scope">
        DN
      </template>
    </el-table-column>
    <el-table-column
      align="right"
      min-width="35%">
      <template slot="header" slot-scope="scope">
        <el-button size="mini" type="text" @click="dialogPermissionsearchuser">添加权限</el-button>
      </template>
      <template slot-scope="scope">
        <el-button
          size="mini"
          type="danger"
          @click="deluserofPermissionlist(scope.$index, scope.row)">删除权限</el-button>
      </template>
    </el-table-column>
  </el-table>
  <span slot="footer" class="dialog-footer">
    <el-button @click="dialogPermission = false">关 闭</el-button>
    <!-- <el-button type="primary" @click="savechangeauthOrig">保 存</el-button> -->
  </span>
</el-dialog>
<el-dialog
  title="代表发送"
  :visible.sync="dialogpublicDelegates"
  width="60%">
  <el-table :data="publicDelegateslistvalue" style="width: 100%" v-cloak height="250">
    <el-table-column label="DN" prop="DN">
      <template slot="header" slot-scope="scope">
        DN
      </template>
    </el-table-column>
    <el-table-column
      align="right"
      min-width="35%">
      <template slot="header" slot-scope="scope">
        <el-button size="mini" type="text" @click="dialogpublicDelegatessearchuser">添加权限</el-button>
      </template>
      <template slot-scope="scope">
        <el-button
          size="mini"
          type="danger"
          @click="deluserofpublicDelegatesonlist(scope.$index, scope.row)">删除权限</el-button>
      </template>
    </el-table-column>
  </el-table>
  <span slot="footer" class="dialog-footer">
    <el-button @click="dialogpublicDelegates = false">关 闭</el-button>
    <el-button type="primary" @click="savechangepublicDelegates">保 存</el-button>
  </span>
</el-dialog>
</el-col>
<el-col :span="24" v-else v-show="loadingstopshowall">
  <el-button round @click="addusertoexmailbox">开通邮箱</el-button>
  <el-dialog
    title="开通邮箱"
    :visible="dialogaddusertoexfixbug"
    :show-close="falsevalue"
    width="60%">
    <span>请选择数据库</span>
    <el-select v-model="Databasechangevalue" placeholder="请选择">
      <el-option
        v-for="item in alldatabasename"
        :key="item.danamevalue"
        :label="item.daname"
        :value="item.daname">
      </el-option>
    </el-select>
    <span slot="footer" class="dialog-footer">
      <el-button @click="dialogaddusertoexfixbug = false">取 消</el-button>
      <el-button type="primary" @click="trueaddusertoexmailbox">确 定</el-button>
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
      falsevalue: false,
      activeIndex: 1,
      classname: {
        classSpanFloatRight: 'classSpanFloatRight',
        classSpancursorpointer: 'classSpancursorpointer'
      },
      changespanshow: {
        changeAliasshow: true,
        changeEmailAddressPolicyEnabledshow: true,
        changeRulesQuotashow: true,
        changeSMTPshow: true,
        changeRecipientLimitsshow: true
      },
      EmailAddressPolicyEnabledchangemessagevalue: {
        truevmessagevalue: '是',
        falsevmessagevalue: '否'
      },
      RulesQuotaselectvalue: [{
        value: '256 KB (262,144 bytes)',
        label: '256 KB'
      }, {
        value: '64 KB (65,536 bytes)',
        label: '64 KB'
      }],
      RecipientLimitsaselectvalue: [{
        value: '100',
        label: '100人'
      }, {
        value: '200',
        label: '200人'
      }, {
        value: '500',
        label: '500人'
      }, {
        value: '1000',
        label: '1000人'
      }, {
        value: 'unlimited',
        label: '不限制'
      }],
      changeVisiblecapacity: {
        changearchiveisIssueWarningQuotacheckvalue: false, // 修改归档储存配额是否勾选发出警告
        changeisIssueWarningQuotacheckvalue: false, // 修改储存配额是否勾选发出警告
        changeisProhibitSendQuotacheckvalue: false, // 修改储存配额是否勾选禁止发送
        changeisProhibitSendReceiveQuotacheckvalue: false // 修改储存配额是否勾选禁止发送和接收
      },
      onevalue: 1, // select只能选择一个
      hasexchangemailbox: false, // 是否开启邮箱功能
      dialogaddusertoex: false, // 新建邮箱模态框
      dialogaddusertoexfixbug: false, // 新建邮箱模态框fixbug版本
      loadingstopshowall: false, // 全部页面加载完毕展示页面
      changeisIssueWarningQuotainputvalue: null, // 修改发出警告配额输入框默认值
      changearchiveisIssueWarningQuotainputvalue: null, // 修改发出警告归档配额输入框默认值
      changearchiveisProhibitSendReceiveQuotainputvalue: null, // 修改禁止发送接收归档配额输入框默认值
      changeisProhibitSendQuotainputvalue: null, // 修改禁止发送配额输入框默认值
      changeisProhibitSendReceiveQuotainputvalue: null, // 修改禁止发送接收配额输入框默认值
      mailboxsettingcheck: false, // 添加smtp、地址模态框
      dialogaddarchivemailbox: false, // 启用归档模态框
      dialogVisible: false, // 添加smtp、地址模态框
      dialogmailboxfeatures: false, // 设置邮箱功能
      dialogarchiveVisible: false, // 迁移归档邮箱数据库
      dialogVisiblecapacity: false, // 修改数据库容量大小模态框
      dialogarchiveVisiblecapacity: false, // 修改归档数据库容量大小模态框
      RulesQuotaselectfirstvalue: null, // 默认规则更改展示规则大小
      AliasChangevalue: null, // 用户邮箱别名修改展示
      EmailAddressPolicyEnabledChangevalue: null, // 是否自动更新地址修改展示
      RecipientLimitsaselectfirstvalue: null, // 默认最大发件人数量展示人数
      SMTPChangevalue: null, // 默认SMTP展示
      UseDatabaseQuotaDefaults: 'False',
      vLoadingShow: false, // 读条全屏遮罩
      TotalItemSize: null, // 用户邮箱大小
      Database: null, // 用户邮箱数据库
      Databasechangevalue: '', // 用户邮箱数据库迁移默认值
      Databasearchivechangevalue: '', // 用户归档邮箱数据库迁移默认值
      Alias: null, // 用户邮箱别名
      EmailAddressPolicyEnabled: null, // 是否自动更新地址
      MailboxMoveStatus: null, // 用户邮箱数据库迁移状态
      intTotalItemSize: false, // 用户邮箱大小(int类型)
      IssueWarningQuota: null, // 发出警告配额
      ProhibitSendQuota: null, // 禁止发送配额
      ProhibitSendReceiveQuota: null, // 禁止发送接收配额
      ArchiveWarningQuota: null, // 存档警告配额
      ArchiveQuota: null, // 存档配额
      ArchiveDatabase: '', // 存档数据库
      ArTotalItemSize: null, // 存档邮箱大小
      percentageIssueWarningQuota: 1, // 发出警告配额使用百分比
      percentageProhibitSendQuota: 1, // 禁止发送配额使用百分比
      percentageProhibitSendReceiveQuota: 1, // 禁止发送配额使用百分比
      percentageArchiveQuota: 1, // 存档配额使用百分比
      percentageArchiveWarningQuota: 1, // 存档警告配额使用百分比
      RulesQuota: null, // 规则大小
      RecipientLimits: null, // 最大发件人数量
      distinguishedName: null, // DN
      SMTP: null, // SMTP
      OWAEnabled: false, // 是否启用owa
      ActiveSyncEnabled: false, // 是否启用手机邮箱
      MAPIEnabled: false, // 是否启用mapi
      PopEnabled: false, // 是否启用pop
      ImapEnabled: false, // 是否启用imap
      loading: false, // 加载
      dialogFullAccess: false, // 管理完全访问权限模态框
      dialogPermission: false, // 管理代理发送权限模态框
      dialogpublicDelegates: false, // 管理代表发送权限模态框
      dialogVisiblesearchuser: false, // 搜索用户和组模态框
      dialogPermissionsearchusershow: false, // 搜索用户和组模态框
      dialogpublicDelegatessearchusershow: false, // 搜索用户和组模态框
      FullAccesslistvalue: [], // 完全访问权限list
      Permissionlistvalue: [], // 代理发送权限list
      publicDelegateslistvalue: [], // 代表发送权限list
      smtp: [], // smtp
      proxyAddresses: [], // 所有电子邮件地址
      tableData3: [],
      options4: [],
      value9: [],
      alldatabasename: [] // 所有邮箱数据库地址
    }
  },
  methods: {
    addobjecttopublicDelegates () {
      for (let i = 0; i < this.value9.length; i++) {
        let trueorfalsevalue = true
        for (let z = 0; z < this.publicDelegateslistvalue.length; z++) {
          if (this.publicDelegateslistvalue[z].DN === this.value9[i]) {
            trueorfalsevalue = false
          }
        }
        if (trueorfalsevalue) {
          this.publicDelegateslistvalue.push({DN: this.value9[i]})
        }
      }
      this.dialogpublicDelegatessearchusershow = false
    },
    dialogpublicDelegatessearchuser () {
      this.dialogpublicDelegatessearchusershow = true
      this.options4 = []
      this.textarea3 = null
      this.value9 = []
    },
    savechangepublicDelegates () {
      let disNameforurl = this.getQueryVariable('disName')
      let ChangeMessage = ''
      if (this.publicDelegateslistvalue.length === 0) {
        ChangeMessage = ''
      } else {
        for (let i = 0; i < this.publicDelegateslistvalue.length; i++) {
          ChangeMessage = ChangeMessage + '&ChangeMessage=' + this.publicDelegateslistvalue[i].DN
        }
      }
      const loading = this.$loading({
        lock: true
      })
      axios.get(this.serviceurl() + '/api/ChangeUserMessagebylist/?CountName=' + disNameforurl + '&Attributes=publicDelegates' + ChangeMessage)
        .then(response => {
          loading.close()
          if (response.data.isSuccess) {
            this.messagealertvalue('修改成功', 'success')
            this.dialogpublicDelegates = false
          } else {
            if (response.data.message === '权限不足') {
              this.messagealertvalue('权限不足', 'error')
            } else {
              this.messagealertvalue('修改失败', 'error')
            }
          }
        })
    },
    dialogpublicDelegatesshow () {
      this.publicDelegateslistvalue = []
      const loading = this.$loading({
        lock: true
      })
      this.dialogpublicDelegates = true
      let disNameforurl = this.getQueryVariable('disName')
      axios.get(this.serviceurl() + '/api/GetUserMessage/?CountName=' + disNameforurl)
        .then(response => {
          loading.close()
          if (response.data.isSuccess) {
            for (let i in response.data.message.publicDelegates) {
              this.publicDelegateslistvalue.push({DN: response.data.message.publicDelegates[i]})
            }
          } else {
            if (response.data.message === '权限不足') {
              this.messagealertvalue('权限不足', 'error')
            } else {
              this.messagealertvalue('邮箱信息获取失败', 'error')
            }
          }
        })
    },
    addobjecttoFullAccess () {
      let disNameforurl = this.getQueryVariable('disName')
      if (!this.value9) {
        this.messagealertvalue('输入为空', 'error')
      } else {
        const loading = this.$loading({
          lock: true
        })
        axios.get(this.serviceurl() + '/api/AddPermission/?CountName=' + this.distinguishedName + '&User=' + this.value9[0] + '&parametername=AccessRights&parametervalue=FullAccess')
          .then(response => {
            loading.close()
            if (response.data.isSuccess) {
              this.dialogVisiblesearchuser = false
              this.messagealertvalue('添加成功', 'success')
              this.dialogFullAccessshow()
            } else {
              if (response.data.message === '权限不足') {
                this.messagealertvalue('权限不足', 'error')
              } else {
                this.messagealertvalue('添加失败', 'error')
              }
            }
          })
      }
    },
    addobjecttoPermission () {
      // let disNameforurl = this.getQueryVariable('disName')
      if (!this.value9) {
        this.messagealertvalue('输入为空', 'error')
      } else {
        const loading = this.$loading({
          lock: true
        })
        axios.get(this.serviceurl() + '/api/AddMailPermission/?CountName=' + this.distinguishedName + '&user=' + this.value9[0] + '&parametername=ExtendedRights&parametervalue=Send-as')
          .then(response => {
            loading.close()
            if (response.data.isSuccess) {
              this.dialogPermissionsearchusershow = false
              this.messagealertvalue('添加成功', 'success')
              this.dialogPermissionshow()
            } else {
              if (response.data.message === '权限不足') {
                this.messagealertvalue('权限不足', 'error')
              } else {
                this.messagealertvalue('添加失败', 'error')
              }
            }
          })
      }
    },
    remoteMethodpublicDelegates (query) {
      if (query !== '') {
        this.loading = true
        axios
          .get(this.serviceurl() + '/api/GetOnlyConMessage/?username=' + query)
          .then(response => {
            this.options4 = []
            for (let i = 0; i < response.data.message.length; i++) {
              this.options4.push({name: response.data.message[i].name, sAMAccountName: response.data.message[i].distinguishedName})
            }
            this.loading = false
          })
      } else {
        this.options4 = []
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
              this.options4.push({name: response.data.message[i].name, sAMAccountName: response.data.message[i].distinguishedName})
            }
            this.loading = false
          })
      } else {
        this.options4 = []
      }
    },
    dialogVisiblesearchusershow: function () {
      this.dialogVisiblesearchuser = true
      this.options4 = []
      this.value9 = []
    },
    dialogPermissionsearchuser: function () {
      this.dialogPermissionsearchusershow = true
      this.options4 = []
      this.value9 = []
    },
    deluserofPermissionlist: function (index, row) {
      const loading = this.$loading({
        lock: true
      })
      // let disNameforurl = this.getQueryVariable('disName')
      axios.get(this.serviceurl() + '/api/RemovePermission/?CountName=' + this.distinguishedName + '&user=' + row.DN + '&parametername=InheritanceType&parametervalue=All&parameternameo=ExtendedRights&parametervalueo=send-as')
        .then(response => {
          loading.close()
          if (response.data.isSuccess) {
            this.messagealertvalue('移除成功', 'success')
            this.dialogPermissionshow()
          } else {
            if (response.data.message === '权限不足') {
              this.messagealertvalue('权限不足', 'error')
            } else {
              this.messagealertvalue('移除失败', 'error')
            }
          }
        })
    },
    deluserofpublicDelegatesonlist: function (index, row) {
      // this.publicDelegateslistvalue
      (this.publicDelegateslistvalue).splice(index, 1)
    },
    deluseroflist: function (index, row) {
      const loading = this.$loading({
        lock: true
      })
      let disNameforurl = this.getQueryVariable('disName')
      axios.get(this.serviceurl() + '/api/ReMailboxPermission/?CountName=' + this.distinguishedName + '&User=' + row.DN + '&InheritanceType=All&AccessRights=FullAccess')
        .then(response => {
          loading.close()
          if (response.data.isSuccess) {
            this.messagealertvalue('移除成功', 'success')
            this.dialogFullAccessshow()
          } else {
            if (response.data.message === '权限不足') {
              this.messagealertvalue('权限不足', 'error')
            } else {
              this.messagealertvalue('移除失败', 'error')
            }
          }
        })
    },
    dialogFullAccessshow () {
      const loading = this.$loading({
        lock: true
      })
      this.FullAccesslistvalue = []
      let disNameforurl = this.getQueryVariable('disName')
      axios.get(this.serviceurl() + '/api/GetPermission/?CountName=' + this.distinguishedName)
        .then(response => {
          loading.close()
          if (response.data.isSuccess) {
            this.dialogFullAccess = true
            for (let i in response.data.message) {
              if ((response.data.message[i].AccessRights[0]).indexOf('FullAccess') !== -1) {
                // if ((response.data.message[i].User).indexOf('\\Domain Admins') === -1 && (response.data.message[i].User).indexOf('\\Enterprise Admins') === -1 && (response.data.message[i].User).indexOf('\\Organization Management') === -1 && (response.data.message[i].User).indexOf('\\Administrator') === -1 && (response.data.message[i].User).indexOf('Domain Admins') === -1 && (response.data.message[i].User).indexOf('\\Enterprise Admins') === -1 && (response.data.message[i].User).indexOf('NT AUTHORITY\\SYSTEM') === -1) {
                this.FullAccesslistvalue.push({DN: response.data.message[i].User})
                // }
              }
            }
          } else {
            if (response.data.message === '权限不足') {
              this.messagealertvalue('权限不足', 'error')
            } else {
              this.messagealertvalue('邮箱信息获取失败', 'error')
            }
          }
        })
    },
    dialogPermissionshow () {
      const loading = this.$loading({
        lock: true
      })
      this.Permissionlistvalue = []
      // let disNameforurl = this.getQueryVariable('disName')
      axios.get(this.serviceurl() + '/api/GetADPermission/?CountName=' + this.distinguishedName)
        .then(response => {
          loading.close()
          if (response.data.isSuccess) {
            this.dialogPermission = true
            for (let i in response.data.message) {
              if (response.data.message[i].ExtendedRights !== null) {
                if ((response.data.message[i].ExtendedRights[0]).indexOf('Send-As') !== -1) {
                  this.Permissionlistvalue.push({DN: response.data.message[i].User})
                }
              }
            }
          } else {
            if (response.data.message === '权限不足') {
              this.messagealertvalue('权限不足', 'error')
            } else {
              this.messagealertvalue('邮箱信息获取失败', 'error')
            }
          }
        })
    },
    async changetest (message, val) {
      const loading = this.$loading({
        lock: true
      })
      let disNameforurl = this.getQueryVariable('disName')
      let mailboxcasvalue = await axios.get(this.serviceurl() + '/api/SetCasMailbox/?CountName=' + disNameforurl + '&parametername=' + message + '&parametervalue=' + val)
      loading.close()
      if (mailboxcasvalue.data.isSuccess) {
        this.messagealertvalue('修改成功', 'success')
      } else {
        this.dialogmailboxfeatures = false
        if (mailboxcasvalue.data.message === '权限不足') {
          this.messagealertvalue('权限不足', 'error')
        } else {
          this.messagealertvalue('邮箱更改失败', 'error')
        }
      }
    },
    async changemailboxfeatures () {
      const loading = this.$loading({
        lock: true
      })
      let disNameforurl = this.getQueryVariable('disName')
      let mailboxcasvalue = await axios.get(this.serviceurl() + '/api/GetCasMailbox/?CountName=' + disNameforurl)
      loading.close()
      if (mailboxcasvalue.data.isSuccess) {
        if (mailboxcasvalue.data.message.OWAEnabled === 'True' || mailboxcasvalue.data.message.OWAEnabled === true) {
          this.OWAEnabled = true
        } else {
          this.OWAEnabled = false
        }
        if (mailboxcasvalue.data.message.ActiveSyncEnabled === 'True' || mailboxcasvalue.data.message.ActiveSyncEnabled === true) {
          this.ActiveSyncEnabled = true
        } else {
          this.ActiveSyncEnabled = false
        }
        if (mailboxcasvalue.data.message.MAPIEnabled === 'True' || mailboxcasvalue.data.message.MAPIEnabled === true) {
          this.MAPIEnabled = true
        } else {
          this.MAPIEnabled = false
        }
        if (mailboxcasvalue.data.message.PopEnabled === 'True' || mailboxcasvalue.data.message.PopEnabled === true) {
          this.PopEnabled = true
        } else {
          this.PopEnabled = false
        }
        if (mailboxcasvalue.data.message.ImapEnabled === 'True' || mailboxcasvalue.data.message.ImapEnabled === true) {
          this.ImapEnabled = true
        } else {
          this.ImapEnabled = false
        }
        this.dialogmailboxfeatures = true
      } else {
        if (mailboxcasvalue.data.message === '权限不足') {
          this.messagealertvalue('权限不足', 'error')
        } else {
          this.messagealertvalue('邮箱信息获取失败', 'error')
        }
      }
    },
    trueaddusertoexmailbox: function () {
      let disNameforurl = this.getQueryVariable('disName')
      if (this.Databasechangevalue === '' || this.Databasechangevalue === null) {
        this.messagealertvalue('请选择一个数据库', 'error')
      } else {
        const loading = this.$loading({
          lock: true
        })
        axios
          .get(this.serviceurl() + '/api/SetUserMail/?CountName=' + this.distinguishedName + '&DBName=' + this.Databasechangevalue)
          .then(response => {
            loading.close()
            this.dialogaddusertoexfixbug = false
            if (response.data.isSuccess) {
              this.messagealertvalue('新建邮箱请求成功', 'success')
              this.searchmailboxvalue()
            } else {
              if (response.data.message === '权限不足') {
                this.messagealertvalue('权限不足', 'error')
              } else {
                this.messagealertvalue('新建邮箱请求失败', 'error')
              }
            }
          })
      }
    },
    getallmailboxdatabasenameaccount () {
      this.dialogVisible = true
      this.getallmailboxdatabasename()
    },
    addusertoexmailbox () {
      this.Databasechangevalue = ''
      this.getallmailboxdatabasename()
      this.dialogaddusertoexfixbug = true
    },
    delmovedatabase: function () {
      let disNameforurl = this.getQueryVariable('disName')
      this.$confirm('此操作将删除' + disNameforurl + '移动请求, 是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning',
        beforeClose: (action, instance, done) => {
          if (action === 'confirm') {
            instance.confirmButtonLoading = true
            instance.confirmButtonText = '执行中...'
            axios
              .get(this.serviceurl() + '/api/RemoveUserRequest/?CountName=' + this.distinguishedName)
              .then(response => {
                instance.confirmButtonLoading = false
                if (response.data.isSuccess) {
                  this.messagealertvalue('移动请求删除成功', 'success')
                  this.searchmailboxvalue()
                } else {
                  if (response.data.message === '权限不足') {
                    this.messagealertvalue('权限不足', 'error')
                  } else {
                    this.messagealertvalue('移动请求删除失败', 'error')
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
    async savearchiveVisiblecapacitychangevalue () {
      let errormessagevalue = true
      if (this.changearchiveisProhibitSendReceiveQuotainputvalue === null || this.changearchiveisProhibitSendReceiveQuotainputvalue === '') {
        this.messagealertvalue('请填写必要信息', 'error')
        errormessagevalue = false
      }
      if (this.changeVisiblecapacity.changearchiveisIssueWarningQuotacheckvalue) {
        if (this.changearchiveisIssueWarningQuotainputvalue === null || this.changearchiveisIssueWarningQuotainputvalue === '') {
          this.messagealertvalue('请填写必要信息', 'error')
          errormessagevalue = false
        }
      }
      if (errormessagevalue) {
        let disNameforurl = this.getQueryVariable('disName')
        const loading = this.$loading({
          lock: true
        })
        await axios
          .get(this.serviceurl() + '/api/ChangeMail/?CountName=' + this.distinguishedName + '&Attributes=ArchiveQuota&ChangeMessage=' + this.changearchiveisProhibitSendReceiveQuotainputvalue + ' MB')
          .then(response => {
            if (response.data.isSuccess) {
              this.messagealertvalue('归档配额配置成功', 'success')
            } else {
              if (response.data.message === '权限不足') {
                this.messagealertvalue('权限不足', 'error')
              } else {
                this.messagealertvalue('归档配额配置失败', 'error')
              }
            }
          })
        if (this.changeVisiblecapacity.changearchiveisIssueWarningQuotacheckvalue) {
          await axios
            .get(this.serviceurl() + '/api/ChangeMail/?CountName=' + this.distinguishedName + '&Attributes=ArchiveWarningQuota&ChangeMessage=' + this.changearchiveisIssueWarningQuotainputvalue + ' MB')
            .then(response => {
              if (response.data.isSuccess) {
                this.messagealertvalue('发出警告归档容量配置成功', 'success')
              } else {
                if (response.data.message === '权限不足') {
                  this.messagealertvalue('权限不足', 'error')
                } else {
                  this.messagealertvalue('发出警告归档容量配置失败', 'error')
                }
              }
            })
        } else {
          await axios
            .get(this.serviceurl() + '/api/ChangeMail/?CountName=' + this.distinguishedName + '&Attributes=ArchiveWarningQuota&ChangeMessage=unlimited')
            .then(response => {
              if (response.data.isSuccess) {
                this.messagealertvalue('发出警告归档容量配置成功', 'success')
              } else {
                if (response.data.message === '权限不足') {
                  this.messagealertvalue('权限不足', 'error')
                } else {
                  this.messagealertvalue('发出警告归档容量配置失败', 'error')
                }
              }
            })
        }
        loading.close()
        this.dialogarchiveVisiblecapacity = false
        this.searchmailboxvalue()
      }
    },
    async saveVisiblecapacitychangevalue () {
      let errormessagevalue = true
      if (!this.mailboxsettingcheck) {
        if (this.changeVisiblecapacity.changeisProhibitSendReceiveQuotacheckvalue) {
          if (this.changeisProhibitSendReceiveQuotainputvalue === null || this.changeisProhibitSendReceiveQuotainputvalue === '') {
            this.messagealertvalue('请填写必要信息', 'error')
            errormessagevalue = false
          }
        }
        if (this.changeVisiblecapacity.changeisProhibitSendQuotacheckvalue) {
          if (this.changeisProhibitSendQuotainputvalue === null || this.changeisProhibitSendQuotainputvalue === '') {
            this.messagealertvalue('请填写必要信息', 'error')
            errormessagevalue = false
          }
        }
        if (this.changeVisiblecapacity.changeisIssueWarningQuotacheckvalue) {
          if (this.changeisIssueWarningQuotainputvalue === null || this.changeisIssueWarningQuotainputvalue === '') {
            this.messagealertvalue('请填写必要信息', 'error')
            errormessagevalue = false
          }
        }
      }
      if (errormessagevalue) {
        let disNameforurl = this.getQueryVariable('disName')
        const loading = this.$loading({
          lock: true
        })
        if (this.mailboxsettingcheck) {
          axios
            .get(this.serviceurl() + '/api/ChangeMail/?CountName=' + this.distinguishedName + '&Attributes=UseDatabaseQuotaDefaults&ChangeMessage=' + this.mailboxsettingcheck)
            .then(response => {
              loading.close()
              if (response.data.isSuccess) {
                this.messagealertvalue('容量配置成功', 'success')
                this.dialogVisiblecapacity = false
                this.searchmailboxvalue()
              } else {
                if (response.data.message === '权限不足') {
                  this.messagealertvalue('权限不足', 'error')
                } else {
                  this.messagealertvalue('容量配置失败', 'error')
                }
              }
            })
        } else {
          await axios
            .get(this.serviceurl() + '/api/ChangeMailcapacity/?CountName="' + this.distinguishedName + '"&UseDatabaseQuotaDefaults=' + this.mailboxsettingcheck + '&ProhibitSendReceiveQuota=' + this.changeVisiblecapacity.changeisProhibitSendReceiveQuotacheckvalue + '&ProhibitSendReceiveQuotamessage=' + this.changeisProhibitSendReceiveQuotainputvalue + 'MB&ProhibitSendQuota=' + this.changeVisiblecapacity.changeisProhibitSendQuotacheckvalue +'&ProhibitSendQuotamessage=' + this.changeisProhibitSendQuotainputvalue + 'MB&IssueWarningQuota=' + this.changeVisiblecapacity.changeisIssueWarningQuotacheckvalue + '&IssueWarningQuotamessage=' + this.changeisIssueWarningQuotainputvalue + 'MB')
            .then(response => {
                if (response.data.isSuccess) {
                  this.messagealertvalue('容量配置成功', 'success')
                  this.dialogVisiblecapacity = false
                  this.searchmailboxvalue()
                } else {
                  this.messagealertvalue('容量配置出错', 'error')
                }
            })
          // if (this.changeVisiblecapacity.changeisProhibitSendReceiveQuotacheckvalue) {
          //   await axios
          //     .get(this.serviceurl() + '/api/ChangeMail/?CountName=' + disNameforurl + '&Attributes=ProhibitSendReceiveQuota&ChangeMessage=' + this.changeisProhibitSendReceiveQuotainputvalue + 'MB')
          //     .then(response => {
          //       if (response.data.isSuccess) {
          //         this.messagealertvalue('禁止接收发送容量配置成功', 'success')
          //       } else {
          //         if (response.data.message === '权限不足') {
          //           this.messagealertvalue('权限不足', 'error')
          //         } else {
          //           this.messagealertvalue('禁止接收发送容量配置失败', 'error')
          //         }
          //       }
          //     })
          // } else {
          //   await axios
          //     .get(this.serviceurl() + '/api/ChangeMail/?CountName=' + disNameforurl + '&Attributes=ProhibitSendReceiveQuota&ChangeMessage=unlimited')
          //     .then(response => {
          //       if (response.data.isSuccess) {
          //         this.messagealertvalue('禁止接收发送容量配置成功', 'success')
          //       } else {
          //         if (response.data.message === '权限不足') {
          //           this.messagealertvalue('权限不足', 'error')
          //         } else {
          //           this.messagealertvalue('禁止接收发送容量配置失败', 'error')
          //         }
          //       }
          //     })
          // }
          // if (this.changeVisiblecapacity.changeisProhibitSendQuotacheckvalue) {
          //   await axios
          //     .get(this.serviceurl() + '/api/ChangeMail/?CountName=' + disNameforurl + '&Attributes=ProhibitSendQuota&ChangeMessage=' + this.changeisProhibitSendQuotainputvalue + 'MB')
          //     .then(response => {
          //       if (response.data.isSuccess) {
          //         this.messagealertvalue('禁止发送容量配置成功', 'success')
          //       } else {
          //         if (response.data.message === '权限不足') {
          //           this.messagealertvalue('权限不足', 'error')
          //         } else {
          //           this.messagealertvalue('禁止发送容量配置失败', 'error')
          //         }
          //       }
          //     })
          // } else {
          //   await axios
          //     .get(this.serviceurl() + '/api/ChangeMail/?CountName=' + disNameforurl + '&Attributes=ProhibitSendQuota&ChangeMessage=unlimited')
          //     .then(response => {
          //       if (response.data.isSuccess) {
          //         this.messagealertvalue('禁止发送容量配置成功', 'success')
          //       } else {
          //         if (response.data.message === '权限不足') {
          //           this.messagealertvalue('权限不足', 'error')
          //         } else {
          //           this.messagealertvalue('禁止发送容量配置失败', 'error')
          //         }
          //       }
          //     })
          // }
          // if (this.changeVisiblecapacity.changeisIssueWarningQuotacheckvalue) {
          //   await axios
          //     .get(this.serviceurl() + '/api/ChangeMail/?CountName=' + disNameforurl + '&Attributes=IssueWarningQuota&ChangeMessage=' + this.changeisIssueWarningQuotainputvalue + 'MB')
          //     .then(response => {
          //       if (response.data.isSuccess) {
          //         this.messagealertvalue('发出警告容量配置成功', 'success')
          //       } else {
          //         if (response.data.message === '权限不足') {
          //           this.messagealertvalue('权限不足', 'error')
          //         } else {
          //           this.messagealertvalue('发出警告容量配置失败', 'error')
          //         }
          //       }
          //     })
          // } else {
          //   await axios
          //     .get(this.serviceurl() + '/api/ChangeMail/?CountName=' + disNameforurl + '&Attributes=IssueWarningQuota&ChangeMessage=unlimited')
          //     .then(response => {
          //       if (response.data.isSuccess) {
          //         this.messagealertvalue('发出警告容量配置成功', 'success')
          //       } else {
          //         if (response.data.message === '权限不足') {
          //           this.messagealertvalue('权限不足', 'error')
          //         } else {
          //           this.messagealertvalue('发出警告容量配置失败', 'error')
          //         }
          //       }
          //     })
          // }
          loading.close()
        }
      }
    },
    changeVisiblecapacitydiagshow: function () {
      this.changeisIssueWarningQuotainputvalue = null
      this.changeisProhibitSendQuotainputvalue = null
      this.changeisProhibitSendReceiveQuotainputvalue = null
      this.dialogVisiblecapacity = true
      if (this.UseDatabaseQuotaDefaults === 'True' || this.UseDatabaseQuotaDefaults === 'true') {
        this.mailboxsettingcheck = true
      } else {
        this.mailboxsettingcheck = false
        // 默认显示发出警告配额信息
        if (this.IssueWarningQuota === 'unlimited') {
          this.changeVisiblecapacity.changeisIssueWarningQuotacheckvalue = false
        } else {
          this.changeVisiblecapacity.changeisIssueWarningQuotacheckvalue = true
          this.changeisIssueWarningQuotainputvalue = Math.round(parseInt(this.IssueWarningQuota.split(' (')[1].split(' bytes)')[0].replace(/,/g, '')) / 1024 / 1024)
        }
        // 默认显示禁止发送配额信息
        if (this.ProhibitSendQuota === 'unlimited') {
          this.changeVisiblecapacity.changeisProhibitSendQuotacheckvalue = false
        } else {
          this.changeVisiblecapacity.changeisProhibitSendQuotacheckvalue = true
          this.changeisProhibitSendQuotainputvalue = Math.round(parseInt(this.ProhibitSendQuota.split(' (')[1].split(' bytes)')[0].replace(/,/g, '')) / 1024 / 1024)
        }
        // 默认显示禁止发送接收配额信息
        if (this.ProhibitSendReceiveQuota === 'unlimited') {
          this.changeVisiblecapacity.changeisProhibitSendReceiveQuotacheckvalue = false
        } else {
          this.changeVisiblecapacity.changeisProhibitSendReceiveQuotacheckvalue = true
          this.changeisProhibitSendReceiveQuotainputvalue = Math.round(parseInt(this.ProhibitSendReceiveQuota.split(' (')[1].split(' bytes)')[0].replace(/,/g, '')) / 1024 / 1024)
        }
      }
    },
    changearchiveVisiblecapacitydiagshow: function () {
      this.changearchiveisIssueWarningQuotainputvalue = null
      this.changearchiveisProhibitSendReceiveQuotainputvalue = null
      this.dialogarchiveVisiblecapacity = true
      // 默认显示归档发出警告配额信息
      this.changearchiveisProhibitSendReceiveQuotainputvalue = Math.round(parseInt(this.ArchiveQuota.split(' (')[1].split(' bytes)')[0].replace(/,/g, '')) / 1024 / 1024)
      // this.changearchiveisIssueWarningQuotainputvalue = Math.round(parseInt(this.ArchiveWarningQuota.split(' (')[1].split(' bytes)')[0].replace(/,/g, '')) / 1024 / 1024)
      // 默认显示归档禁止发送接收配额信息
      if (this.ArchiveWarningQuota === 'unlimited') {
        this.changeVisiblecapacity.changearchiveisIssueWarningQuotacheckvalue = false
      } else {
        this.changeVisiblecapacity.changearchiveisIssueWarningQuotacheckvalue = true
        this.changearchiveisIssueWarningQuotainputvalue = Math.round(parseInt(this.ArchiveWarningQuota.split(' (')[1].split(' bytes)')[0].replace(/,/g, '')) / 1024 / 1024)
      }
    },
    truechangemailboxdatabasevalue: function () {
      let disNameforurl = this.getQueryVariable('disName')
      const loading = this.$loading({
        lock: true
      })
      if (this.Database === this.Databasechangevalue) {
        this.messagealertvalue('当前数据库无法迁移', 'error')
        loading.close()
      } else {
        axios
          .get(this.serviceurl() + '/api/UserDBMove/?CountName=' + this.distinguishedName + '&DBName=' + this.Databasechangevalue)
          .then(response => {
            loading.close()
            if (response.data.isSuccess) {
              this.messagealertvalue('迁移请求添加成功', 'success')
              this.searchmailboxvalue()
            } else {
              if (response.data.message === '权限不足') {
                this.messagealertvalue('权限不足', 'error')
              } else {
                this.messagealertvalue('迁移请求添加失败', 'error')
              }
            }
            this.dialogVisible = false
          })
          .catch(function () {
            this.$message({
              showClose: true,
              message: '加载失败',
              type: 'error'
            })
            this.dialogVisible = false
          })
      }
    },
    truechangearchivemailboxdatabasevalue: function () {
      let disNameforurl = this.getQueryVariable('disName')
      const loading = this.$loading({
        lock: true
      })
      if (this.ArchiveDatabase === this.Databasearchivechangevalue) {
        this.messagealertvalue('当前数据库无法迁移', 'error')
        loading.close()
      } else {
        axios
          .get(this.serviceurl() + '/api/MOUserMailArchive/?CountName=' + this.distinguishedName + '&DBName=' + this.Databasearchivechangevalue)
          .then(response => {
            loading.close()
            if (response.data.isSuccess) {
              this.messagealertvalue('迁移请求添加成功', 'success')
              this.searchmailboxvalue()
            } else {
              if (response.data.message === '权限不足') {
                this.messagealertvalue('权限不足', 'error')
              } else {
                this.messagealertvalue('迁移请求添加失败', 'error')
              }
            }
            this.dialogarchiveVisible = false
          })
          .catch(function () {
            this.$message({
              showClose: true,
              message: '加载失败',
              type: 'error'
            })
            this.dialogarchiveVisible = false
          })
      }
    },
    trueaddarchivemailboxvalue: function () {
      let disNameforurl = this.getQueryVariable('disName')
      const loading = this.$loading({
        lock: true
      })
      axios
        .get(this.serviceurl() + '/api/EnUserMailArchive/?CountName=' + this.distinguishedName + '&DBName=' + this.Databasechangevalue)
        .then(response => {
          loading.close()
          if (response.data.isSuccess) {
            this.messagealertvalue('启用归档请求添加成功', 'success')
            this.searchmailboxvalue()
          } else {
            if (response.data.message === '权限不足') {
              this.messagealertvalue('权限不足', 'error')
            } else {
              this.messagealertvalue('启用归档请求添加失败', 'error')
            }
          }
          this.dialogaddarchivemailbox = false
        })
        .catch(function () {
          this.$message({
            showClose: true,
            message: '加载失败',
            type: 'error'
          })
          this.dialogaddarchivemailbox = false
        })
    },
    getallmailboxdatabasename: function () {
      this.alldatabasename = []
      this.Databasechangevalue = this.Database
      axios
        .get(this.serviceurl() + '/api/GetDBMessage/')
        .then(response => {
          if (response.data.isSuccess) {
            for (let i = 0; i < response.data.message.length; i++) {
              this.alldatabasename.push({'daname': (response.data.message[i]).replace('{\'daname\':\'', '').replace('\'}', ''), 'danamevalue': (response.data.message[i]).replace('{\'daname\':\'', '').replace('\'}', '')})
            }
          } else {
            if (response.data.message === '权限不足') {
              this.messagealertvalue('权限不足', 'error')
            } else {
              this.messagealertvalue('数据库获取失败', 'error')
            }
          }
        })
    },
    getallmailboxdatabasearchivename: function () {
      this.alldatabasename = []
      this.dialogarchiveVisible = true
      this.Databasearchivechangevalue = this.ArchiveDatabase
      axios
        .get(this.serviceurl() + '/api/GetDBMessage/')
        .then(response => {
          if (response.data.isSuccess) {
            for (let i = 0; i < response.data.message.length; i++) {
              this.alldatabasename.push({'daname': (response.data.message[i]).replace('{\'daname\':\'', '').replace('\'}', ''), 'danamevalue': (response.data.message[i]).replace('{\'daname\':\'', '').replace('\'}', '')})
            }
          } else {
            if (response.data.message === '权限不足') {
              this.messagealertvalue('权限不足', 'error')
            } else {
              this.messagealertvalue('数据库获取失败', 'error')
            }
          }
        })
    },
    changetrueaddarchivemailboxdiagshow: function () {
      this.alldatabasename = []
      this.dialogaddarchivemailbox = true
      this.Databasechangevalue = this.Database
      axios
        .get(this.serviceurl() + '/api/GetDBMessage/')
        .then(response => {
          if (response.data.isSuccess) {
            for (let i = 0; i < response.data.message.length; i++) {
              this.alldatabasename.push({'daname': (response.data.message[i]).replace('{\'daname\':\'', '').replace('\'}', ''), 'danamevalue': (response.data.message[i]).replace('{\'daname\':\'', '').replace('\'}', '')})
            }
          } else {
            if (response.data.message === '权限不足') {
              this.messagealertvalue('权限不足', 'error')
            } else {
              this.messagealertvalue('数据库获取失败', 'error')
            }
          }
        })
    },
    addsmtpvalue: function () {
      let disNameforurl = this.getQueryVariable('disName')
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
              .get(this.serviceurl() + '/api/UserSmtpAdd/?CountName="' + this.distinguishedName + '"&SmtpValue=' + instance.inputValue)
              .then(response => {
                instance.confirmButtonLoading = false
                if (response.data.isSuccess) {
                  // this.smtp.push(instance.inputValue)
                  this.messagealertvalue('smtp添加成功', 'success')
                  this.searchmailboxvalue()
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
    Deletesmtp: function (smtpvalue) {
      let disNameforurl = this.getQueryVariable('disName')
      this.$confirm('此操作将删除' + smtpvalue + '地址, 是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning',
        beforeClose: (action, instance, done) => {
          if (action === 'confirm') {
            instance.confirmButtonLoading = true
            instance.confirmButtonText = '执行中...'
            axios
              .get(this.serviceurl() + '/api/EmUserSmtp/?SmtpValue=' + smtpvalue + '&CountName="' + this.distinguishedName + '"')
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
    smtptoSMTP: function (smtpvalue) {
      let disNameforurl = this.getQueryVariable('disName')
      this.$confirm('此操作将' + smtpvalue + '设置为主SMTP, 是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning',
        beforeClose: (action, instance, done) => {
          if (action === 'confirm') {
            instance.confirmButtonLoading = true
            instance.confirmButtonText = '执行中...'
            axios
              .get(this.serviceurl() + '/api/ChangeMail/?CountName=' + this.distinguishedName + '&Attributes=PrimarySmtpAddress&ChangeMessage=' + smtpvalue)
              .then(response => {
                instance.confirmButtonLoading = false
                if (response.data.isSuccess) {
                  this.messagealertvalue('设置成功', 'success')
                  this.searchmailboxvalue()
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
      }).then()
    },
    async searchmailboxvalue () {
      this.loadingstopshowall = false
      const loading = this.$loading({
        lock: true
      })
      let disNameforurl = this.getQueryVariable('disName')
      var responsevalue = await axios.get(this.serviceurl() + '/api/GetUserMessage/?CountName=' + disNameforurl)
      this.smtp = []
      if (responsevalue.data.isSuccess) {
        this.loadingstopshowall = true
        if (!responsevalue.data.message['proxyAddresses'] || responsevalue.data.message['proxyAddresses'].length === 0) {
          loading.close()
          this.hasexchangemailbox = false
        } else {
          this.hasexchangemailbox = true
          this.proxyAddresses = responsevalue.data.message.proxyAddresses
          this.distinguishedName = responsevalue.data.message.distinguishedName
          await axios
            .get(this.serviceurl() + '/api/GetMailMessage/?username=' + this.distinguishedName)
            .then(response => {
              loading.close()
              if (response.data.isSuccess) {
                this.UseDatabaseQuotaDefaults = response.data.message.UseDatabaseQuotaDefaults.toString()
                this.Database = response.data.message.Database
                this.Databasechangevalue = response.data.message.Database
                this.Alias = response.data.message.Alias
                this.EmailAddressPolicyEnabled = response.data.message.EmailAddressPolicyEnabled.toString().toLowerCase()
                this.MailboxMoveStatus = response.data.message.MailboxMoveStatus
                this.ArchiveWarningQuota = response.data.message.ArchiveWarningQuota
                this.ArchiveQuota = response.data.message.ArchiveQuota
                this.ArchiveDatabase = response.data.message.ArchiveDatabase
                // this.TotalItemSize = response.data.message.TotalItemSize
                // if (typeof(this.TotalItemSize) === "undefined") {
                //   this.TotalItemSize = '0 KB (0 bytes)'
                // }
                this.RulesQuota = response.data.message.RulesQuota
                this.RulesQuotaselectfirstvalue = response.data.message.RulesQuota
                this.RecipientLimits = response.data.message.RecipientLimits
                this.RecipientLimitsaselectfirstvalue = response.data.message.RecipientLimits
                if (!response.data.message['TotalItemSize']) {
                  this.intTotalItemSize = 1
                  this.TotalItemSize = '0 KB (0 bytes)'
                } else {
                  this.TotalItemSize = response.data.message.TotalItemSize
                  this.intTotalItemSize = parseInt((((response.data.message.TotalItemSize).split(' (')[1]).split(' bytes)')[0]).replace(/,/g, ''))
                }
                if (response.data.message.UseDatabaseQuotaDefaults === 'False' || response.data.message.UseDatabaseQuotaDefaults === false ) {
                  this.IssueWarningQuota = response.data.message.IssueWarningQuota
                  if (response.data.message.IssueWarningQuota === 'unlimited') {
                    this.percentageIssueWarningQuota = 0
                  } else {
                    this.percentageIssueWarningQuota = (this.intTotalItemSize / parseInt(response.data.message.IssueWarningQuota.split(' (')[1].split(' bytes)')[0].replace(/,/g, '')) * 100).toFixed(1)
                  }
                  if (response.data.message.ProhibitSendQuota === 'unlimited') {
                    this.percentageProhibitSendQuota = 0
                  } else {
                    this.percentageProhibitSendQuota = (this.intTotalItemSize / parseInt(response.data.message.ProhibitSendQuota.split(' (')[1].split(' bytes)')[0].replace(/,/g, '')) * 100).toFixed(1)
                  }
                  if (response.data.message.ProhibitSendReceiveQuota === 'unlimited') {
                    this.percentageProhibitSendReceiveQuota = 0
                  } else {
                    this.percentageProhibitSendReceiveQuota = (this.intTotalItemSize / parseInt(response.data.message.ProhibitSendReceiveQuota.split(' (')[1].split(' bytes)')[0].replace(/,/g, '')) * 100).toFixed(1)
                  }
                  this.ProhibitSendQuota = response.data.message.ProhibitSendQuota
                  this.ProhibitSendReceiveQuota = response.data.message.ProhibitSendReceiveQuota
                } else {
                  this.IssueWarningQuota = response.data.message.DBIssueWarningQuota
                  if (response.data.message.IssueWarningQuota === 'unlimited') {
                    this.percentageIssueWarningQuota = 0
                  } else {
                    this.percentageIssueWarningQuota = (this.intTotalItemSize / parseInt(response.data.message.DBIssueWarningQuota.split(' (')[1].split(' bytes)')[0].replace(/,/g, '')) * 100).toFixed(1)
                  }
                  if (response.data.message.ProhibitSendQuota === 'unlimited') {
                    this.percentageProhibitSendQuota = 0
                  } else {
                    this.percentageProhibitSendQuota = (this.intTotalItemSize / parseInt(response.data.message.DBProhibitSendQuota.split(' (')[1].split(' bytes)')[0].replace(/,/g, '')) * 100).toFixed(1)
                  }
                  if (response.data.message.ProhibitSendReceiveQuota === 'unlimited') {
                    this.percentageProhibitSendReceiveQuota = 0
                  } else {
                    this.percentageProhibitSendReceiveQuota = (this.intTotalItemSize / parseInt(response.data.message.DBProhibitSendReceiveQuota.split(' (')[1].split(' bytes)')[0].replace(/,/g, '')) * 100).toFixed(1)
                  }
                  this.ProhibitSendQuota = response.data.message.DBProhibitSendQuota
                  this.ProhibitSendReceiveQuota = response.data.message.DBProhibitSendReceiveQuota
                }
                this.ArTotalItemSize = response.data.message.ArTotalItemSize
                if (!response.data.message['ArTotalItemSize']) {
                  this.ArTotalItemSize = '0 KB (0 bytes)'
                  this.intArTotalItemSize = 0
                } else {
                  this.ArTotalItemSize = response.data.message.ArTotalItemSize
                  this.intArTotalItemSize = parseInt((((response.data.message.ArTotalItemSize).split(' (')[1]).split(' bytes)')[0]).replace(/,/g, ''))
                }
                if (this.ArchiveDatabase !== null) {
                  if (response.data.message.ArchiveWarningQuota === 'unlimited') {
                    this.percentageArchiveWarningQuota = 0
                  } else {
                    this.percentageArchiveWarningQuota = (this.intArTotalItemSize / parseInt(response.data.message.ArchiveWarningQuota.split(' (')[1].split(' bytes)')[0].replace(/,/g, ''))*100).toFixed(1)
                  }
                  if (response.data.message.ArchiveQuota === 'unlimited') {
                    this.percentageArchiveQuota = 0
                  } else {
                    this.percentageArchiveQuota = (this.intArTotalItemSize / parseInt(response.data.message.ArchiveQuota.split(' (')[1].split(' bytes)')[0].replace(/,/g, '')) * 100).toFixed(1)
                  }
                }
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
            })
            .catch(function () {
              this.$message({
                showClose: true,
                message: '加载失败',
                type: 'error'
              })
            })
        }
        for (let i = 0; i < this.proxyAddresses.length; i++) {
          if (responsevalue.data.message.proxyAddresses[i].search('SMTP:') !== -1) {
            this.SMTP = responsevalue.data.message.proxyAddresses[i].replace('SMTP:', '')
          } else {
            this.smtp.push(responsevalue.data.message.proxyAddresses[i].replace('smtp:', ''))
          }
        }
      } else {
        loading.close()
        if (responsevalue.data.message === '权限不足') {
          this.messagealertvalue('权限不足', 'error')
        } else {
          this.messagealertvalue('加载失败', 'error')
        }
      }
    },
    changemailboxvalue: function (Attributesname, ChangeMessage) {
      let disNameforurl = this.getQueryVariable('disName')
      this.vLoadingShow = true
      axios
        .get(this.serviceurl() + '/api/ChangeMail/?CountName=' + this.distinguishedName + '&Attributes=' + Attributesname + '&ChangeMessage=' + ChangeMessage)
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
              if (this.EmailAddressPolicyEnabled === 'true') {
                this.searchmailboxvalue()
              }
              this.Alias = ChangeMessage
              this.changespanshow.changeAliasshow = true
            } else if (Attributesname === 'EmailAddressPolicyEnabled') {
              this.EmailAddressPolicyEnabled = ChangeMessage
              this.changespanshow.changeEmailAddressPolicyEnabledshow = true
              if (this.EmailAddressPolicyEnabled === 'true') {
                this.searchmailboxvalue()
              }
            } else if (Attributesname === 'PrimarySmtpAddress') {
              this.SMTP = ChangeMessage
              this.changespanshow.changeSMTPshow = true
              this.searchmailboxvalue()
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
    }
  },
  created () {
    this.searchmailboxvalue()
  }
}
</script>
<style>
</style>
