"""itops URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
# from django.contrib import admin
from django.views.generic import TemplateView
from rest_framework import routers
from rest_framework_jwt.views import obtain_jwt_token

from apiusers.views import ApiUserViewset
from apps.api.views import apipermissions, getapiuser, modifyapiuser, deletcapiuser, addapiuser, getapiuserpermissions, deluserpermissions, getattributeslevel, addapipermissions, \
    modifyapiattributesleve, itapidocument, apinames
from itapi.exviews import EXEnableMailboxhigh, EXEnableMailboxarchive, EXGetMailboxdatabase, EXNewMoveRequest, EXGetDistributionGroup, \
    EXGetMailboxStatistics, EXGetExchangeServer, EXgetADPermission, EXGetMailContact, EXgetMailboxPermission, EXRemoveMailboxPermission, EXAddMailboxPermission, EXAddADPermission, \
    EXRemoveADPermission, EXEnableMailContact, EXRemoveMoveRequest, EXNewMailContact, EXSetMailContactvalue, EXSetCasMailbox, EXSetMailboxEmailAddresses, EXSetMailbox, EXSetMailbox1, \
    EXSetMailbox2, EXSetDistributionGroup, EXDisableGroup, EXEnableGroup, EXGetCasMailboxhight, EXGetMailbox

from itapi.views import Ldap3Search, Ldap3AddUser, Ldap3AddGroup, Ldap3SetAccount, Ldap3AddComputer, Ldap3AddContact, Ldap3AddOU, Ldap3RenameObject, Ldap3DnMoveToOu, Ldap3DeleteObject, \
    Ldap3inspectObject, Ldap3ResetPassword, Ldap3SerchLock, Ldap3UnlockUser, Ldap3SearchDN, Ldap3CanObject, \
    Ldap3CheckObject, Ldap3UncheckObject, Ldap3AddMembers, Ldap3ReMembers, Ldap3SetAccountLevel1, Ldap3SetAccountLevel2, Ldap3DeleteUser, Ldap3DeleteGroup, Ldap3DeleteContact, \
    Ldap3DeleteComputer, Ldap3DeleteOU, Api_docs, Ldap3GetUser
from ops import views as ops_views

from apps.activedirectory import views as activedirectory_views
from apps.Exchange import views as exchange_views
from apps.record import views as record_views
from apps.admanager import views as admanager_views
from apps.log import views as log_views
from apps.document import views as document_views
from rest_framework.documentation import include_docs_urls



urlpatterns = [
    # url(r'^admin/', admin.site.urls),
    url(r'^searchuser/', TemplateView.as_view(template_name="index.html")),
    url(r'^groupvalue/', TemplateView.as_view(template_name="groupvalue.html")),
    url(r'^contactvalue/', TemplateView.as_view(template_name="contact.html")),
    url(r'^outhervalue/', TemplateView.as_view(template_name="outher.html")),
    url(r'^computervalue/', TemplateView.as_view(template_name="computer.html")),
    url(r'^ouvalue/', TemplateView.as_view(template_name="ou.html")),
    url(r'^intermediate/', TemplateView.as_view(template_name="intermediate.html")),
    url(r'^monitor1111/', TemplateView.as_view(template_name="monitor.html")),
    url(r'^bigindex/', TemplateView.as_view(template_name="bigindex.html"))
]

urlpatterns += [
    url(r'^$|^login/$', ops_views.login, name='login'),
    url(r'^logout/$', ops_views.logout, name="logout"),
    url(r'^home/$', ops_views.home, name="home"),
    url(r'^searchmailstaus/$', ops_views.searchmailstaus, name="searchmailstaus"),
    url(r'^userlogin/$', ops_views.userlogin, name="userlogin"),
    url(r'^gootokenpng/$', ops_views.gootokenpng, name="gootokenpng"),
    url(r'^logingotok/$', ops_views.logingotok, name="logingotok"),
    url(r'^verificationtok/$', ops_views.verificationtok, name="verificationtok"),

    url(r'^basite/$', ops_views.basite, name="basite"),
    url(r'^changadminpwd/$', ops_views.changadminpwd, name="changadminpwd"),
    url(r'^mysqltest/$', ops_views.mysqltest, name="mysqltest"),
    # url(r'^iislinktest/$', ops_views.iislinktest, name="iislinktest"),
    url(r'^exlinktest/$', ops_views.exlinktest, name="exlinktest"),
    url(r'^adldaptest/$', ops_views.adldaptest, name="adldaptest"),
    url(r'^permsetest/$', ops_views.permsetest, name="permsetest"),

    url(r'^restartuwsgi/$', ops_views.restartuwsgi, name="restartuwsgi"),
]

# include  urls
urlpatterns += [
    url(r'^api/', include('ADapi.urls', namespace='api'), ),
    url(r'^monitor/', include('ADapi.urls_monitor', namespace='monitorurl'), ),
]

# urls
urlpatterns += [
    url(r'^directorytree/$', activedirectory_views.directorytree, name="directorytree"),# AD树页面
    url(r'^search/$', activedirectory_views.search, name="search"),# AD搜索页面
    url(r'^downloadcsv/$', activedirectory_views.downloadcsv, name="downloadcsv"),# 导出
    url(r'^userautodow/$', activedirectory_views.userautodow, name='userautodow'),  # 导出权限判断
    url(r'^passwordexp/$', activedirectory_views.passwordexp, name="passwordexp"),#账号过期时间查询页面
    url(r'^leavesearch/$', activedirectory_views.leavesearch, name="leavesearch"),#高级搜索
    url(r'^treesearch/$', activedirectory_views.treesearch, name="treesearch"),# 树搜索页面
    url(r'^groupexport/$', activedirectory_views.groupexport, name="groupexport"),#导出组信息
    url(r'^show_domain/$', activedirectory_views.show_domain, name='show_domain',),# 获取总节点
    url(r'^show_ou_for_dn/$', activedirectory_views.show_ou_for_dn, name='show_ou_for_dn'), #获取OU节点
    url(r'^show_object_for_dn/$', activedirectory_views.show_object_for_dn, name='show_object_for_dn'), #获取下层目录所有对象
    url(r'^setRenameObject/$', activedirectory_views.setRenameObject, name='setRenameObject'), #调用重命名的方法

    url(r'^addUser/$', activedirectory_views.addUser, name='addUser'),#新建USer
    url(r'^addGroup/$', activedirectory_views.addGroup, name='addGroup'),#新建group
    url(r'^addorganizationalUnit/$', activedirectory_views.addorganizationalUnit, name='addorganizationalUnit'),#新建organizationalUnit
    url(r'^addContact/$', activedirectory_views.addContact, name='addContact'),#新建联系人
    url(r'^addComputer/$', activedirectory_views.addComputer, name='addComputer'),#新建Computer
    url(r'^setObjectMoveToOu/$', activedirectory_views.setObjectMoveToOu, name='setObjectMoveToOu'),#右键单击移动到新OU

    url(r'^inspectObject/$', activedirectory_views.inspectObject, name='inspectObject'),#判断容器 OU 内是否有对象
    url(r'^delObject/$', activedirectory_views.delObject, name='delObject'),# 删除对象
    url(r'^exportListToOU/$', activedirectory_views.exportListToOU, name='exportListToOU'),# 导出OU 下成员 列表

    url(r'^setObjectAttributes/$', activedirectory_views.setObjectAttributes, name='setObjectAttributes'),#修改对象属性
    url(r'^resetUserPassword/$', activedirectory_views.resetUserPassword, name='resetUserPassword'),## 修改用户密码 设置 用户下次登陆时须更改密码 解锁用户的账户

    url(r'^moveDnsToOu/$', activedirectory_views.moveDnsToOu, name='moveDnsToOu'),# 多dn 移动到新OU
    url(r'^getMailboxDatebase/$', activedirectory_views.getMailboxDatebase, name='getMailboxDatebase'), ## psot 获取邮箱数据库
    url(r'^serchLock/$', activedirectory_views.serchLock, name='serchLock'),## 查找用户是否被锁定  传入 sAMAccountName or distinguishedNameD
    url(r'^hasmonitorvalueurl/$', activedirectory_views.hasmonitorvalueurl, name='hasmonitorvalueurl'),## 查找是否开启监控
    url(r'^unLockuser/$', activedirectory_views.unLockuser, name='unLockuser'),## 解锁用户  传入 sAMAccountName or distinguishedName
    url(r'^setAccidentallyDeleted/$', activedirectory_views.setAccidentallyDeleted, name='setAccidentallyDeleted'),## 勾选 防止对象被意外删除(P)
    url(r'^canAccidentallyDeleted/$', activedirectory_views.canAccidentallyDeleted, name='canAccidentallyDeleted'),## 判断 勾选 防止对象被意外删除(P)
    url(r'^getExissconfig/$', activedirectory_views.getExissconfig, name='getExissconfig'),## 获取数据库中的邮箱配置

    url(r'^admanager/$', admanager_views.admanager, name='admanager'),# 登录admanager页面
    url(r'^creatusers/$', admanager_views.creatusers, name='creatusers'), # 登录creatusers页面
    url(r'^exportfiletemplate/$', admanager_views.exportfiletemplate, name='exportfiletemplate'),# 导出文件模板
    url(r'^uploadfiletemplate/$', admanager_views.uploadfiletemplate, name='uploadfiletemplate'),# 导入文件模板
    url(r'^creatalluser/$', admanager_views.creatalluser, name='creatalluser'),## 批量创建用户 多进程
    url(r'^modifyuserattributes/$', admanager_views.modifyuserattributes, name='modifyuserattributes'),# 登录批量修改用户属性页面
    url(r'^searchuser_modify/$', admanager_views.searchuser_modify, name='searchuser_modify'),## 查找需要修改的用户属性
    url(r'^modifyuser/$', admanager_views.modifyuser, name='modifyuser'),# 修改用户属性，可修改cn(重命名）
    url(r'^executemodifyuser/$', admanager_views.executemodifyuser, name='executemodifyuser'),# 批量修改文件 多进程
    url(r'^modifypasswd/$', admanager_views.modifypasswd, name='modifypasswd'),# 登录批量修改用户密码页面
    url(r'^searchuser_passwd/$', admanager_views.searchuser_passwd, name='searchuser_passwd'),## 查找需要修改的用户密码属性
    url(r'^executemodifypasswd/$', admanager_views.executemodifypasswd, name='executemodifypasswd'),# 批量修改用户密码 多进程
    url(r'^moveuser/$', admanager_views.moveuser, name='moveuser'),# 登录移动用户页面
    url(r'^executemoveuser/$', admanager_views.executemoveuser, name='executemoveuser'),# 批量移动用户 多进程
    url(r'^creatusermail/$', admanager_views.creatusermail, name='creatusermail'),# 登录批量创建邮箱 页面
    url(r'^executecreatmail/$', admanager_views.executecreatmail, name='executecreatmail'),# 批量新建邮箱 多进程
    url(r'^getsqlldapattributes/$', admanager_views.getsqlldapattributes, name='getsqlldapattributes'),# 获取ldap属性 查找数据库
    url(r'^ladpattributes/$', admanager_views.ladpattributes, name='ladpattributes'),# 登录ldap属性 页面
    url(r'^movecomputer/$', admanager_views.movecomputer, name='movecomputer'),# 登录移动计算机页面

    url(r'^serchlog/$', log_views.serchlog, name='serchlog'),# 日志页面
    url(r'^getsqllog/$', log_views.getsqllog, name='getsqllog'),# 查询日志
    url(r'^gettableslog/$', log_views.gettableslog, name='gettableslog'),# 获取有哪些日志数据表
    url(r'^serchsqllog/$', log_views.serchsqllog, name='serchsqllog'),# 搜索日志
]
#文档
urlpatterns += [
    url(r'^projects/$', document_views.projects, name='projects'),
    url(r'^creatproject/$', document_views.creatproject, name='creatproject'),
    url(r'^findallprojects/$', document_views.findallprojects, name='findallprojects'),
    url(r'^finderroprojects/$', document_views.finderroprojects, name='finderroprojects'),
    url(r'^delprojects/$', document_views.delprojects, name='delprojects'),
    url(r'^delerrprojects/$', document_views.delerrprojects, name='delerrprojects'),
    url(r'^savemess/$', document_views.savemess, name='savemess'),
    url(r'^savemesserro/$', document_views.savemesserro, name='savemesserro'),
    url(r'^upsave/$', document_views.upsave, name='upsave'),
    url(r'^upmesserro/$', document_views.upmesserro, name='upmesserro'),
    url(r'^userauto/$', document_views.userauto, name='userauto'),
    url(r'^lookallmess/$', document_views.lookallmess, name="lookallmess"),
    url(r'^lookerrmess/$', document_views.lookerrmess, name="lookerrmess"),
    url(r'^faultproject/$', document_views.faultproject, name="faultproject"),
    url(r'^findproject/$', document_views.findproject, name="findproject"),
]
# dxw urls
urlpatterns += [
    url(r'^ldapcord/$', record_views.ldaprecord, name="ldapcord"),
    url(r'^dnscord/$', record_views.dnsrecord, name="dnscord"),
    url(r'^insertldap/$', record_views.insert_ldap, name="insertldap"),
    url(r'^deleteldap/$', record_views.delete_ldap, name="deleteldap"),
    url(r'^insertdns/$', record_views.insert_dns, name="insertdns"),
    url(r'^deletedns/$', record_views.delete_dns, name="deletedns"),
    url(r'^getdnsdbvaule/$', record_views.getdnsdbvaule, name="getdnsdbvaule"),
    url(r'^getldapdbvaule/$', record_views.getldapdbvaule, name="getldapdbvaule"),

]

# exchange urls
urlpatterns += [
    url(r'^findmail/$', exchange_views.findmail, name="findmail"),
    url(r'^mailvlafind/$', exchange_views.mailvlafind, name="mailvlafind"),
]

#Api 权限配置页面
urlpatterns += {
    url(r'^apipermissions/$', apipermissions, name="apipermissions"),  # 登录api权限接口页面
    url(r'^getapiuser/$', getapiuser, name="getapiuser", ),  # 获取apiuser权限相关数据
    url(r'^modifyapiuser/$', modifyapiuser, name="modifyapiuser", ),  # 修改apiuser权限相关数据
    url(r'^deletcapiuser/$', deletcapiuser, name="deletcapiuser", ),  # 删除apiuser权限相关数据
    url(r'^addapiuser/$', addapiuser, name="addapiuser", ),  # 新建apiuser权限相关数据
    url(r'^getapiuserpermissions/$', getapiuserpermissions, name="getapiuserpermissions", ),  # 获取apiusers_apinamepermissions权限相关数据
    url(r'^deluserpermissions/$', deluserpermissions, name="deluserpermissions", ),  # 删除apiusers_apinamepermissions权限相关数据
    url(r'^addapipermissions/$', addapipermissions, name="addapipermissions", ),  # 写入apiusers_apinamepermissions权限相关数据
    url(r'^getattributeslevel/$', getattributeslevel, name="getattributeslevel", ),  # 获取attributeslevel
    url(r'^modifyapiattributesleve/$', modifyapiattributesleve, name="modifyapiattributesleve", ),
    url(r'^docs/itapidocument/$', itapidocument, name="itapidocument", ), #打开文档详情
    url(r'^apinames/$', apinames, name="apinames"),  # 登录api方法导航
}

router = routers.DefaultRouter()
# 配置 url
router.register(r'01.API方法调用说明', Api_docs, base_name='Api_docs'),
router.register(r'ApiUserViewset', ApiUserViewset, base_name='ApiUserViewset'),

router.register(r'Ldap3Search', Ldap3Search, base_name='搜索',),
router.register(r'Ldap3SearchDN', Ldap3SearchDN, base_name='根据sAMAccountName属性 搜索对象',),
router.register(r'Ldap3AddUser', Ldap3AddUser, base_name='新建用户',),
router.register(r'Ldap3AddGroup', Ldap3AddGroup, base_name='新建组',),
router.register(r'Ldap3AddComputer', Ldap3AddComputer, base_name='新建计算机',),

router.register(r'Ldap3AddContact', Ldap3AddContact, base_name='新建联系人',),
router.register(r'Ldap3AddOU', Ldap3AddOU, base_name='新建组织单位',),
router.register(r'Ldap3RenameObject', Ldap3RenameObject, base_name='重命名对象',),
router.register(r'Ldap3DnMoveToOu', Ldap3DnMoveToOu, base_name='多dn移动到新OU',),
router.register(r'Ldap3DeleteObject', Ldap3DeleteObject, base_name='删除对象',),

router.register(r'Ldap3DeleteUser', Ldap3DeleteUser, base_name='删除用户',),
router.register(r'Ldap3DeleteGroup', Ldap3DeleteGroup, base_name='删除组',),
router.register(r'Ldap3DeleteContact', Ldap3DeleteContact, base_name='删除联系人',),
router.register(r'Ldap3DeleteComputer', Ldap3DeleteComputer, base_name='删除计算机',),
router.register(r'Ldap3DeleteOU', Ldap3DeleteOU, base_name='删除组织单位',),

router.register(r'Ldap3inspectObject', Ldap3inspectObject, base_name='判断容器或OU内是否有对象',),
router.register(r'Ldap3SetAccount', Ldap3SetAccount, base_name='修改对象属性',),
router.register(r'Ldap3SetAccountLevel1', Ldap3SetAccountLevel1, base_name='修改对象属性',),
router.register(r'Ldap3SetAccountLevel2', Ldap3SetAccountLevel2, base_name='修改对象属性',),
router.register(r'Ldap3ResetPassword', Ldap3ResetPassword, base_name='修改用户密码',),

router.register(r'Ldap3SerchLock', Ldap3SerchLock, base_name='判断用户是否被锁定',),
router.register(r'Ldap3UnlockUser', Ldap3UnlockUser, base_name='解锁用户锁定',),
router.register(r'Ldap3CanObject', Ldap3CanObject, base_name='判断对象是否勾选防止对象被意外删除(P)',),
router.register(r'Ldap3CheckObject', Ldap3CheckObject, base_name='勾选防止对象被意外删除(P)',),
router.register(r'Ldap3UncheckObject', Ldap3UncheckObject, base_name='去除勾选防止对象被意外删除',),

router.register(r'Ldap3AddMembers', Ldap3AddMembers, base_name='批量添加用户(组)到组',),
router.register(r'Ldap3ReMembers', Ldap3ReMembers, base_name='批量删除用户(组)到组',),
router.register(r'Ldap3GetUser', Ldap3GetUser, base_name='获取用户信息',),


router.register(r'EXEnableMailboxhigh', EXEnableMailboxhigh, base_name='启用用户邮箱',),
router.register(r'EXEnableMailboxarchive', EXEnableMailboxarchive, base_name='一般用作启用用户邮箱(启用归档邮箱)',),
router.register(r'EXGetMailboxdatabase', EXGetMailboxdatabase, base_name='获取所有数据库名称/获取单一数据库信息',),
router.register(r'EXNewMoveRequest', EXNewMoveRequest, base_name='迁移用户邮箱和存档数据库',),
router.register(r'EXGetDistributionGroup', EXGetDistributionGroup, base_name='获取邮箱群组信息',),

router.register(r'EXDisableGroup', EXDisableGroup, base_name='禁用邮箱群组',),
router.register(r'EXEnableGroup', EXEnableGroup, base_name='启用邮箱群组',),
router.register(r'EXGetMailboxStatistics', EXGetMailboxStatistics, base_name='用户邮箱信息，一般用作获取用户邮箱大小使用情况',),
router.register(r'EXGetExchangeServer', EXGetExchangeServer, base_name='获取邮箱服务器',),
router.register(r'EXgetADPermission', EXgetADPermission, base_name='获取邮箱用户权限，获取代理发送权限',),

router.register(r'EXGetMailContact', EXGetMailContact, base_name='获取邮箱联系人信息',),
router.register(r'EXgetMailboxPermission', EXgetMailboxPermission, base_name='获取邮箱用户权限',),
router.register(r'EXRemoveMailboxPermission', EXRemoveMailboxPermission, base_name='删除邮箱用户权限，一般用作删除用户完全访问权限',),
router.register(r'EXAddMailboxPermission', EXAddMailboxPermission, base_name='添加邮箱用户权限，添加完全访问权限',),
router.register(r'EXAddADPermission', EXAddADPermission, base_name='添加邮箱用户权限，添加代理发送权限',),

router.register(r'EXRemoveADPermission', EXRemoveADPermission, base_name='删除邮箱用户权限 代理发送权限',),
router.register(r'EXEnableMailContact', EXEnableMailContact, base_name='开启联系人邮箱',),
router.register(r'EXRemoveMoveRequest', EXRemoveMoveRequest, base_name='删除用户邮箱迁移请求',),
router.register(r'EXNewMailContact', EXNewMailContact, base_name='新建联系人',),
router.register(r'EXSetMailContactvalue', EXSetMailContactvalue, base_name='设置联系人邮箱',),

router.register(r'EXSetCasMailbox', EXSetCasMailbox, base_name='设置pop mapi信息',),
router.register(r'EXSetMailboxEmailAddresses', EXSetMailboxEmailAddresses, base_name='新增/删除 用户smtp地址',),
router.register(r'EXSetMailbox', EXSetMailbox, base_name='设置用户邮箱',),
router.register(r'EXSetMailbox1', EXSetMailbox1, base_name='设置用户邮箱level1',),
router.register(r'EXSetMailbox2', EXSetMailbox2, base_name='设置用户邮箱level2',),

router.register(r'EXSetDistributionGroup', EXSetDistributionGroup, base_name='设置群组邮箱',),
router.register(r'EXGetCasMailboxhight', EXGetCasMailboxhight, base_name='获取pop mapi信息',),
router.register(r'EXGetMailbox', EXGetMailbox, base_name='用户邮箱信息',),



urlpatterns += [
    url(r'^', include(router.urls)),
]

urlpatterns += {
    url(r'^docs/', include_docs_urls(title='IT API', authentication_classes=[], permission_classes=[])),
    url(r'^Api-token-auth/', obtain_jwt_token, name='JWT认证'),
    url(r'^api-auth/', include('rest_framework.urls')),
}