import pypsrp
from pypsrp.powershell import PowerShell, RunspacePool
from pypsrp.wsman import WSMan
import xml.etree.cElementTree as ET
# code值对应说明
# 0 =>> 执行成功
# 200 =>> 执行失败，缺少必须参数
# 201 =>> 执行失败，详情见msg
# 202 =>>
from dbinfo.encrypt_decode import encrypt_and_decode
from dbinfo.views import getskey


class exapi():
    def __init__(self):
        # self.wsman = WSMan(server="", port=443, path="/powershell/",ssl=True,username="", password="",auth="basic")
        self.wsman = WSMan(server=getskey()['exserver'], port=80, path="/powershell/",ssl=False,username=getskey()['exdomain'] + "\\" + getskey()['exuser'], password=encrypt_and_decode().decrypted_text(getskey()['expassword']),auth="basic",encryption='never')
        self.msg,self.message,self.isSuccess,self.code,self.count = str(),list(),False,0,0
    def Serializationmessage(self):
        for key,message in enumerate(self.message):
            for item in message:
                if isinstance(message[item],pypsrp.complex_objects.GenericComplexObject):
                    try:
                        self.message[key][item]= [itemxml.text for itemxml in ET.fromstring(message[item].property_sets[0])]
                    except Exception:
                        self.message[key][item] = message[item].adapted_properties
    def returnfuction(self):
        return {"msg": self.msg, "message": self.message, "isSuccess": self.isSuccess, "code": self.code, "count": self.count}
    def connection(self,scriptname,**kwargs):
        try:
            with RunspacePool(self.wsman, configuration_name="Microsoft.Exchange") as pool:
                ps = PowerShell(pool).add_cmdlet(scriptname)
                [ps.add_parameter(i,kwargs[i]) for i in kwargs]
                output = ps.invoke()
                if not ps.had_errors and not ps.streams.error:
                    self.message,self.isSuccess,self.count = [i.adapted_properties for i in output],True,len(output)
                else:
                    self.code,self.msg = 201,"%s".join([str(s) for s in ps.streams.error])
        except Exception as e:
            self.msg,self.code = e,201
    def connectionscript(self,scriptname,**kwargs):
        scriptparameter = list()
        [scriptparameter.extend(["-" + i, kwargs[i]]) for i in kwargs]
        script = scriptname + " " + " ".join(scriptparameter)
        try:
            with RunspacePool(self.wsman, configuration_name="Microsoft.Exchange") as pool:
                ps = PowerShell(pool).add_script(script + " -Confirm:$false")
                output = ps.invoke()
                if not ps.had_errors and not ps.streams.error:
                    self.message,self.isSuccess,self.count = [i.adapted_properties for i in output],True,len(output)
                else:
                    self.code,self.msg = 201,"%s".join([str(s) for s in ps.streams.error])
        except Exception as e:
            self.msg,self.code = e,201
    def connectionscriptall(self,scriptname):
        try:
            with RunspacePool(self.wsman, configuration_name="Microsoft.Exchange") as pool:
                ps = PowerShell(pool).add_script(scriptname)
                output = ps.invoke()
                if not ps.had_errors and not ps.streams.error:
                    self.message,self.isSuccess,self.count = [i.adapted_properties for i in output],True,len(output)
                else:
                    self.code,self.msg = 201,"%s".join([str(s) for s in ps.streams.error])
        except Exception as e:
            self.msg,self.code = e,201

# Enable-Mailbox
# 官方url：https://docs.microsoft.com/en-us/powershell/module/exchange/mailboxes/Enable-Mailbox?view=exchange-ps
#一般用作启用用户邮箱
# identity 用户唯一标识
# alias 邮箱别名
# database 数据库
def EnableMailboxhigh(identity,alias=None,database=None,**kwargs):
    try:
        exchange = exapi()
        if alias:
            exchange.connection('Enable-Mailbox',identity=identity,alias=alias,database=database,**kwargs)
        else:
            exchange.connection('Enable-Mailbox',identity=identity,database=database,**kwargs)
        return  exchange.returnfuction()
    except Exception as e:
        return  {'isSuccess': False, 'count': 0, 'msg': str(e), 'code': 201, 'message': ''}

# Enable-Mailbox
# 官方url：https://docs.microsoft.com/en-us/powershell/module/exchange/mailboxes/Enable-Mailbox?view=exchange-ps
#一般用作启用用户邮箱(启用归档邮箱)
# identity 用户唯一标识
# ArchiveDatabase 数据库
def EnableMailboxarchive(identity,ArchiveDatabase,**kwargs):
    try:
        exchange = exapi()
        kwargs.update(Archive=True)
        exchange.connection('Enable-Mailbox',identity=identity,ArchiveDatabase=ArchiveDatabase,**kwargs)
        return  exchange.returnfuction()
    except Exception as e:
        return  {'isSuccess': False, 'count': 0, 'msg': str(e), 'code': 201, 'message': ''}

# get-mailboxdatabase
#官方url：https://docs.microsoft.com/en-us/powershell/module/exchange/mailbox-databases-and-servers/Get-MailboxDatabase?view=exchange-ps
# 获取所有数据库名称/获取单一数据库信息
def GetMailboxdatabase(**kwargs):
    try:
        exchange = exapi()
        exchange.connection('get-mailboxdatabase',**kwargs)
        return  exchange.returnfuction()
    except Exception as e:
        return  {'isSuccess': False, 'count': 0, 'msg': str(e), 'code': 201, 'message': ''}

#New-MoveRequest
#https://docs.microsoft.com/zh-cn/powershell/module/exchange/move-and-migration/new-moverequest?view=exchange-ps
# 迁移用户邮箱和存档数据库
#identity 用户唯一标识（必须）
#TargetDatabase迁移用户邮箱的目标数据库（和ArchiveTargetDatabase至少要有一个）
#ArchiveTargetDatabase迁移用户归档邮箱的目标数据库（和TargetDatabase至少要有一个）
def NewMoveRequest(identity,TargetDatabase=None,ArchiveTargetDatabase=None,**kwargs):
    try:
        if not TargetDatabase and not ArchiveTargetDatabase:
            return {'isSuccess': False, 'count': 0, 'msg': '缺少必须参数', 'code': 200, 'message': ''}
        exchange = exapi()
        kwargs.update(TargetDatabase=TargetDatabase) if TargetDatabase != None else None
        kwargs.update(ArchiveTargetDatabase=ArchiveTargetDatabase) if ArchiveTargetDatabase != None else None
        exchange.connection('New-MoveRequest', identity=identity, **kwargs)
        return  exchange.returnfuction()
    except Exception as e:
        return  {'isSuccess': False, 'count': 0, 'msg': str(e), 'code': 201, 'message': ''}

# Get-DistributionGroup
# https://docs.microsoft.com/en-us/powershell/module/exchange/users-and-groups/Get-DistributionGroup?view=exchange-ps
# 获取邮箱群组信息
#identity 群组唯一标识（必须）
def GetDistributionGroup(identity,**kwargs):
    try:
        exchange = exapi()
        exchange.connection('Get-DistributionGroup', identity=identity, **kwargs)
        exchange.Serializationmessage()
        return  exchange.returnfuction()
    except Exception as e:
        return  {'isSuccess': False, 'count': 0, 'msg': str(e), 'code': 201, 'message': ''}

# Disable-DistributionGroup
# https://docs.microsoft.com/en-us/powershell/module/exchange/users-and-groups/Disable-DistributionGroup?view=exchange-ps
# 禁用邮箱群组
#identity 群组唯一标识（必须）
def DisableDistributionGroup(identity,**kwargs):
    try:
        exchange = exapi()
        kwargs.update(confirm=False)
        exchange.connection('Disable-DistributionGroup', identity=identity, **kwargs)
        return  exchange.returnfuction()
    except Exception as e:
        return  {'isSuccess': False, 'count': 0, 'msg': str(e), 'code': 201, 'message': ''}

# enable-DistributionGroup
# https://docs.microsoft.com/en-us/powershell/module/exchange/users-and-groups/Enable-DistributionGroup?view=exchange-ps
# 启用邮箱群组
#identity 群组唯一标识（必须）
#alias 别名
def EnableDistributionGroup(identity,alias,**kwargs):
    try:
        exchange = exapi()
        exchange.connection('enable-DistributionGroup', identity=identity,alias=alias, **kwargs)
        return  exchange.returnfuction()
    except Exception as e:
        return  {'isSuccess': False, 'count': 0, 'msg': str(e), 'code': 201, 'message': ''}

# Get-MailboxStatistics
# https://docs.microsoft.com/en-us/powershell/module/exchange/mailboxes/Get-MailboxStatistics?view=exchange-ps
# 用户邮箱信息，一般用作获取用户邮箱大小使用情况
#identity 用户唯一标识（必须）
def GetMailboxStatistics(identity,**kwargs):
    try:
        exchange = exapi()
        exchange.connection('Get-MailboxStatistics', identity=identity, **kwargs)
        exchange.Serializationmessage()
        return  exchange.returnfuction()
    except Exception as e:
        return  {'isSuccess': False, 'count': 0, 'msg': str(e), 'code': 201, 'message': ''}

# Get-Mailbox
# https://docs.microsoft.com/en-us/powershell/module/exchange/mailboxes/get-mailbox?view=exchange-ps
# 用户邮箱信息，获取用户邮箱容量数据库等信息
#identity 用户唯一标识（必须）
def GetMailbox(identity,**kwargs):
    try:
        exchange = exapi()
        exchange.connection('Get-Mailbox', identity=identity, **kwargs)
        exchange.Serializationmessage()
        return  exchange.returnfuction()
    except Exception as e:
        return  {'isSuccess': False, 'count': 0, 'msg': str(e), 'code': 201, 'message': ''}

# Get-ExchangeServer
# https://docs.microsoft.com/en-us/powershell/module/exchange/organization/Get-ExchangeServer?view=exchange-ps
# 获取邮箱服务器
def GetExchangeServer(**kwargs):
    try:
        exchange = exapi()
        exchange.connection('Get-ExchangeServer', **kwargs)
        exchange.Serializationmessage()
        return  exchange.returnfuction()
    except Exception as e:
        return  {'isSuccess': False, 'count': 0, 'msg': str(e), 'code': 201, 'message': ''}

# get-ADPermission
# https://docs.microsoft.com/en-us/powershell/module/exchange/active-directory/Get-ADPermission?view=exchange-ps
# 获取邮箱用户权限，获取代理发送权限
# identity  用户DN，如果有空格，需要用双引号括起来
def getADPermission(identity,**kwargs):
    try:
        exchange = exapi()
        exchange.connection('get-ADPermission',identity=identity , **kwargs)
        exchange.Serializationmessage()
        return  exchange.returnfuction()
    except Exception as e:
        return  {'isSuccess': False, 'count': 0, 'msg': str(e), 'code': 201, 'message': ''}

# Get-MailContact
# https://docs.microsoft.com/en-us/powershell/module/exchange/users-and-groups/Get-MailContact?view=exchange-ps
# 获取邮箱联系人信息
#identity 联系人唯一标识（必须）
def GetMailContacthight(identity,**kwargs):
    try:
        exchange = exapi()
        exchange.connection('Get-MailContact',identity=identity , **kwargs)
        exchange.Serializationmessage()
        return  exchange.returnfuction()
    except Exception as e:
        return  {'isSuccess': False, 'count': 0, 'msg': str(e), 'code': 201, 'message': ''}

# get-MailboxPermission
# https://docs.microsoft.com/en-us/powershell/module/exchange/mailboxes/Get-MailboxPermission?view=exchange-ps
# 获取邮箱用户权限
#identity 用户唯一标识（必须）
def getMailboxPermission(identity,**kwargs):
    try:
        exchange = exapi()
        exchange.connection('get-MailboxPermission',identity=identity , **kwargs)
        exchange.Serializationmessage()
        return  exchange.returnfuction()
    except Exception as e:
        return  {'isSuccess': False, 'count': 0, 'msg': str(e), 'code': 201, 'message': ''}

# Remove-MailboxPermission
# https://docs.microsoft.com/en-us/powershell/module/exchange/mailboxes/Remove-MailboxPermission?view=exchange-ps
# 删除邮箱用户权限，一般用作删除用户完全访问权限
#identity 用户唯一标识（必须）
#User 删除哪个用户的权限（必须）
def RemoveMailboxPermissionhight(identity,User,InheritanceType='All',AccessRights='FullAccess',**kwargs):
    try:
        exchange = exapi()
        kwargs.update(confirm=False)
        exchange.connection('Remove-MailboxPermission',identity=identity , User=User,InheritanceType=InheritanceType,AccessRights=AccessRights,**kwargs)
        return  exchange.returnfuction()
    except Exception as e:
        return  {'isSuccess': False, 'count': 0, 'msg': str(e), 'code': 201, 'message': ''}


# Add-MailboxPermission
# https://docs.microsoft.com/en-us/powershell/module/exchange/mailboxes/Add-MailboxPermission?view=exchange-ps
# 添加邮箱用户权限，添加完全访问权限
#identity 用户唯一标识（必须）
#User 添加哪个用户的权限（必须）
def AddMailboxPermissionhight(identity,User,parametername='AccessRights',parametervalue='FullAccess',**kwargs):
    try:
        exchange = exapi()
        kwargs[parametername]=parametervalue
        exchange.connection('Add-MailboxPermission',identity=identity , User=User,**kwargs)
        return  exchange.returnfuction()
    except Exception as e:
        return  {'isSuccess': False, 'count': 0, 'msg': str(e), 'code': 201, 'message': ''}

# Add-ADPermission
# https://docs.microsoft.com/en-us/powershell/module/exchange/active-directory/Add-ADPermission?view=exchange-ps
# 添加邮箱用户权限，添加代理发送权限
#identity 用户DN
#User 添加哪个用户的权限（必须）
def AddADPermission(identity,User,parametername='ExtendedRights',parametervalue='Send-as',**kwargs):
    try:
        exchange = exapi()
        kwargs[parametername]=parametervalue
        exchange.connection('Add-ADPermission',identity=identity , User=User,**kwargs)
        return  exchange.returnfuction()
    except Exception as e:
        return  {'isSuccess': False, 'count': 0, 'msg': str(e), 'code': 201, 'message': ''}


#Remove-ADPermission
# https://docs.microsoft.com/zh-cn/powershell/module/exchange/active-directory/remove-adpermission?view=exchange-ps
# 删除邮箱用户权限 代理发送权限
#identity 用户DN
#User 删除哪个用户的权限（必须）
def RemoveADPermissionhight(identity,User,parametername='InheritanceType',parametervalue='All',parametername0='ExtendedRights',parametervalue0='send-as',**kwargs):
    try:
        exchange = exapi()
        kwargs.update(confirm=False)
        kwargs[parametername]=parametervalue
        kwargs[parametername0]=parametervalue0
        exchange.connection('Remove-ADPermission',identity=identity , User=User,**kwargs)
        return  exchange.returnfuction()
    except Exception as e:
        return  {'isSuccess': False, 'count': 0, 'msg': str(e), 'code': 201, 'message': ''}

# Enable-MailContact
# https://docs.microsoft.com/en-us/powershell/module/exchange/users-and-groups/Enable-MailContact?view=exchange-ps
# 开启联系人邮箱
#identity 联系人唯一标识
#ExternalEmailAddress   邮箱地址
def EnableMailContacthight(identity,ExternalEmailAddress,**kwargs):
    try:
        exchange = exapi()
        exchange.connection('Enable-MailContact',identity=identity ,ExternalEmailAddress=ExternalEmailAddress,**kwargs)
        return  exchange.returnfuction()
    except Exception as e:
        return  {'isSuccess': False, 'count': 0, 'msg': str(e), 'code': 201, 'message': ''}

# Remove-MoveRequest
# https://docs.microsoft.com/en-us/powershell/module/exchange/move-and-migration/Remove-MoveRequest?view=exchange-ps
#identity 移动请求用户的唯一标识
# 删除用户邮箱迁移请求
def RemoveMoveRequesthight(identity,**kwargs):
    try:
        exchange = exapi()
        kwargs.update(confirm=False)
        exchange.connection('Remove-MoveRequest',identity=identity , **kwargs)
        return  exchange.returnfuction()
    except Exception as e:
        return  {'isSuccess': False, 'count': 0, 'msg': str(e), 'code': 201, 'message': ''}

# New-MailContact
# https://docs.microsoft.com/en-us/powershell/module/exchange/users-and-groups/New-MailContact?view=exchange-ps
# 新建联系人
# New-MailContact -ExternalEmailAddress 'SMTP:contacttest_E@test.com' -Name 'contacttest_M' -Alias 'contacttest_A' -FirstName 'contacttest_F' -Initials 'cont_S' -LastName 'contacttest_L' -OrganizationalUnit 'test.com/Users'
# Name =》CN，（displayname如果不写也会赋此值）  必须
# ExternalEmailAddress  邮件地址  （必须）
def NewMailContacthight(Name,ExternalEmailAddress,**kwargs):
    try:
        exchange = exapi()
        kwargs.update(confirm=False)
        exchange.connection('New-MailContact',Name =Name, ExternalEmailAddress=ExternalEmailAddress,**kwargs)
        return  exchange.returnfuction()
    except Exception as e:
        return  {'isSuccess': False, 'count': 0, 'msg': str(e), 'code': 201, 'message': ''}

# Set-MailContact
# https://docs.microsoft.com/en-us/powershell/module/exchange/users-and-groups/Set-MailContact?view=exchange-ps
# 设置联系人邮箱
# identity  联系人唯一标识
def SetMailContactvalue(identity,**kwargs):
    try:
        exchange = exapi()
        exchange.connectionscript('Set-MailContact',Identity =identity,**kwargs)
        return  exchange.returnfuction()
    except Exception as e:
        return  {'isSuccess': False, 'count': 0, 'msg': str(e), 'code': 201, 'message': ''}

# Set-CasMailbox
# https://docs.microsoft.com/en-us/powershell/module/exchange/client-access/Set-CASMailbox?view=exchange-ps
# 设置pop mapi信息
# identity  用户唯一标识
def SetCasMailboxhight(identity,**kwargs):
    try:
        exchange = exapi()
        exchange.connection('Set-CasMailbox',identity =identity,**kwargs)
        return  exchange.returnfuction()
    except Exception as e:
        return  {'isSuccess': False, 'count': 0, 'msg': str(e), 'code': 201, 'message': ''}

# Get-CasMailbox
# https://docs.microsoft.com/en-us/powershell/module/exchange/client-access/Get-CASMailbox?view=exchange-ps
# 获取pop mapi信息
# identity  用户唯一标识
def GetCasMailboxhight(identity,**kwargs):
    try:
        exchange = exapi()
        exchange.connection('Get-CasMailbox',identity =identity,**kwargs)
        exchange.Serializationmessage()
        return  exchange.returnfuction()
    except Exception as e:
        return  {'isSuccess': False, 'count': 0, 'msg': str(e), 'code': 201, 'message': ''}

# Set-Mailbox
# 新增/删除 用户smtp地址
# Set-Mailbox -Identity wzx -EmailAddresses @{add='hhhh@test.com'}
# Set-Mailbox -Identity wzx -EmailAddresses @{remove='hhhh@test.com'}
def SetMailboxEmailAddresses(identity,EmailAddresses,**kwargs):
    try:
        exchange = exapi()
        exchange.connectionscript('Set-Mailbox',identity =identity,EmailAddresses=EmailAddresses,**kwargs)
        return  exchange.returnfuction()
    except Exception as e:
        return  {'isSuccess': False, 'count': 0, 'msg': str(e), 'code': 201, 'message': ''}


# Set-Mailbox
# 设置用户邮箱
# https://docs.microsoft.com/en-us/powershell/module/exchange/mailboxes/Set-Mailbox?view=exchange-ps
def SetMailbox(identity,script = False,**kwargs):
    try:
        exchange = exapi()
        # exchange.connection('Set-Mailbox',identity =identity,**kwargs)
        exchange.connectionscript('Set-Mailbox', identity=identity, **kwargs) if script else exchange.connection('Set-Mailbox',identity =identity,**kwargs)
        return  exchange.returnfuction()
    except Exception as e:
        return  {'isSuccess': False, 'count': 0, 'msg': str(e), 'code': 201, 'message': ''}


# Set-DistributionGroup
# 设置群组邮箱
# https://docs.microsoft.com/en-us/powershell/module/exchange/users-and-groups/Set-DistributionGroup?view=exchange-ps
def SetDistributionGroup(identity,script = False,**kwargs):
    try:
        exchange = exapi()
        exchange.connectionscript('Set-DistributionGroup', identity=identity, **kwargs) if script else exchange.connection('Set-DistributionGroup',identity =identity,**kwargs)
        return  exchange.returnfuction()
    except Exception as e:
        return  {'isSuccess': False, 'count': 0, 'msg': str(e), 'code': 201, 'message': ''}

# Get-MailboxDatabaseCopyStatus
#官方url：https://docs.microsoft.com/en-us/powershell/module/exchange/mailbox-databases-and-servers/Get-MailboxDatabase?view=exchange-ps
# 获取所有数据库副本信息
def GetMailboxDatabaseCopyStatus(identity,**kwargs):
    try:
        exchange = exapi()
        exchange.connection('Get-MailboxDatabaseCopyStatus',identity=identity,**kwargs)
        exchange.Serializationmessage()
        return  exchange.returnfuction()
    except Exception as e:
        return  {'isSuccess': False, 'count': 0, 'msg': str(e), 'code': 201, 'message': ''}

# Move-ActiveMailboxDatabase
# 官方url：https://docs.microsoft.com/en-us/powershell/module/exchange/database-availability-groups/move-activemailboxdatabase?view=exchange-ps
# 迁移激活邮箱数据库
# identity 数据库名
def MoveActiveMailboxDatabase(identity,**kwargs):
    try:
        exchange = exapi()
        exchange.connection('Move-ActiveMailboxDatabase',identity=identity,**kwargs)
        return  exchange.returnfuction()
    except Exception as e:
        return  {'isSuccess': False, 'count': 0, 'msg': str(e), 'code': 201, 'message': ''}


# set-mailboxdatabase
#官方url：https://docs.microsoft.com/en-us/powershell/module/exchange/mailbox-databases-and-servers/set-mailboxdatabase?view=exchange-ps
# 修改数据库信息
def SetMailboxdatabase(**kwargs):
    try:
        exchange = exapi()
        exchange.connection('set-mailboxdatabase',**kwargs)
        return  exchange.returnfuction()
    except Exception as e:
        return  {'isSuccess': False, 'count': 0, 'msg': str(e), 'code': 201, 'message': ''}

