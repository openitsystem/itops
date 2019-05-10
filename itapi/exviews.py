# -*- coding: utf-8 -*-
# @Time    : 2019/3/28 19:25
# @Author  :
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response

from dbinfo.views import insert_drf_api_log
from itapi.exapi import SetMailbox, EnableMailboxhigh, EnableMailboxarchive, GetMailboxdatabase, NewMoveRequest, GetDistributionGroup, DisableDistributionGroup, EnableDistributionGroup, \
    GetMailboxStatistics, GetExchangeServer, getADPermission, GetMailContacthight, getMailboxPermission, RemoveMailboxPermissionhight, AddMailboxPermissionhight, AddADPermission, RemoveADPermissionhight, \
    EnableMailContacthight, RemoveMoveRequesthight, NewMailContacthight, SetMailContactvalue, SetCasMailboxhight, SetDistributionGroup, SetMailboxEmailAddresses, GetCasMailboxhight, \
    GetMailbox
from itapi.exserializers import *

# 获取传入的其他值 kwargs
def getkwargs(data,initial_data):
    try:
        initial_data_copy = initial_data.copy()
        for i in data.keys():
            initial_data_copy.pop(i)
        return initial_data_copy
    except:
        return {}

#一般用作启用用户邮箱
class EXEnableMailboxhigh(mixins.CreateModelMixin, viewsets.GenericViewSet):
    '''
    '''
    # permission_classes = (ReadOnly,)
    serializer_class = EnableMailboxhighSerializers

    def create(self, request, *args, **kwargs):
        '''
        * Enable-Mailbox
        * 官方url：https://docs.microsoft.com/en-us/powershell/module/exchange/mailboxes/Enable-Mailbox?view=exchange-ps
        * 启用用户邮箱
            - identity 用户唯一标识（Name，Distinguished name (DN)，Canonical DN，GUID）
            - alias 邮箱别名
            - database 数据库
            - **kwargs 表示函数接收可变长度的关键字参数字典作为函数的输入
        '''
        try:
            # 1. 反序列化 将其他格式（字典、JSON、XML等）转换为程序中的数据，例如将JSON字符串转换为Django中的模型类对象
            serializer = self.get_serializer(data=request.data)
            # 验证数据
            serializer.is_valid(raise_exception=True)
            headers = self.get_success_headers(serializer.data)
            data = serializer.data
            initial_data = serializer.initial_data
            kwargs = getkwargs(data, initial_data)
            result = EnableMailboxhigh(data['identity'], data['alias'], data['database'], **kwargs)
        except Exception as e:
            result = {"isSuccess": False, "message": '', 'count': 0, 'msg': str(e), 'code': 2}
        insert_drf_api_log(request, str(result['isSuccess']), str(result))
        return Response(result, status=status.HTTP_200_OK)

#一般用作启用用户邮箱(启用归档邮箱)
class EXEnableMailboxarchive(mixins.CreateModelMixin, viewsets.GenericViewSet):
    '''
    '''
    # permission_classes = (ReadOnly,)
    serializer_class = EnableMailboxarchiveSerializers

    def create(self, request, *args, **kwargs):
        '''
        * Enable-Mailbox
        * 官方url：https://docs.microsoft.com/en-us/powershell/module/exchange/mailboxes/Enable-Mailbox?view=exchange-ps
        * 启用用户邮箱(启用归档邮箱)
            - identity 用户唯一标识（Name，Distinguished name (DN)，Canonical DN，GUID）
            - ArchiveDatabase 数据库
            - **kwargs 表示函数接收可变长度的关键字参数字典作为函数的输入
        '''
        try:
            # 1. 反序列化 将其他格式（字典、JSON、XML等）转换为程序中的数据，例如将JSON字符串转换为Django中的模型类对象
            serializer = self.get_serializer(data=request.data)
            # 验证数据
            serializer.is_valid(raise_exception=True)
            headers = self.get_success_headers(serializer.data)
            data = serializer.data
            initial_data = serializer.initial_data
            kwargs = getkwargs(data, initial_data)
            result = EnableMailboxarchive(data['identity'], data['ArchiveDatabase'], **kwargs)
        except Exception as e:
            result = {"isSuccess": False, "message": '', 'count': 0, 'msg': str(e), 'code': 2}
        insert_drf_api_log(request, str(result['isSuccess']), str(result))
        return Response(result, status=status.HTTP_200_OK)

#获取所有数据库名称/获取单一数据库信息
class EXGetMailboxdatabase(mixins.CreateModelMixin, viewsets.GenericViewSet):
    '''
    '''
    # permission_classes = (ReadOnly,)
    serializer_class = serializers.Serializer

    def create(self, request, *args, **kwargs):
        '''
        * get-mailboxdatabase
        * 官方url：https://docs.microsoft.com/en-us/powershell/module/exchange/mailbox-databases-and-servers/Get-MailboxDatabase?view=exchange-ps
        * 获取所有数据库名称/获取单一数据库信息
            - **kwargs 表示函数接收可变长度的关键字参数字典作为函数的输入
        '''
        try:
            # 1. 反序列化 将其他格式（字典、JSON、XML等）转换为程序中的数据，例如将JSON字符串转换为Django中的模型类对象
            serializer = self.get_serializer(data=request.data)
            # 验证数据
            # serializer.is_valid(raise_exception=True)
            # headers = self.get_success_headers(serializer.data)
            # data = serializer.data
            kwargs = serializer.initial_data
            result = GetMailboxdatabase(**kwargs)
        except Exception as e:
            result = {"isSuccess": False, "message": '', 'count': 0, 'msg': str(e), 'code': 2}
        insert_drf_api_log(request, str(result['isSuccess']), str(result))
        return Response(result, status=status.HTTP_200_OK)

#迁移用户邮箱和存档数据库
class EXNewMoveRequest(mixins.CreateModelMixin, viewsets.GenericViewSet):
    '''
    '''
    # permission_classes = (ReadOnly,)
    serializer_class = NewMoveRequestSerializers

    def create(self, request, *args, **kwargs):
        '''
        * New-MoveRequest
        * https://docs.microsoft.com/zh-cn/powershell/module/exchange/move-and-migration/new-moverequest?view=exchange-ps
        * 迁移用户邮箱和存档数据库
            - identity 用户唯一标识（必须）（GUID，Distinguished name (DN)，Domain\Account，User principal name (UPN)，LegacyExchangeDN，SMTP address，Alias）
            - TargetDatabase迁移用户邮箱的目标数据库（和ArchiveTargetDatabase至少要有一个）
            - ArchiveTargetDatabase迁移用户归档邮箱的目标数据库（和TargetDatabase至少要有一个）
            - **kwargs 表示函数接收可变长度的关键字参数字典作为函数的输入
        '''
        try:
            # 1. 反序列化 将其他格式（字典、JSON、XML等）转换为程序中的数据，例如将JSON字符串转换为Django中的模型类对象
            serializer = self.get_serializer(data=request.data)
            # 验证数据
            serializer.is_valid(raise_exception=True)
            headers = self.get_success_headers(serializer.data)
            data = serializer.data
            initial_data = serializer.initial_data
            kwargs = getkwargs(data, initial_data)
            result = NewMoveRequest(data.get('identity'), data.get('TargetDatabase', None), data.get('ArchiveTargetDatabase', None), **kwargs)
        except Exception as e:
            result = {"isSuccess": False, "message": '', 'count': 0, 'msg': str(e), 'code': 2}
        insert_drf_api_log(request, str(result['isSuccess']), str(result))
        return Response(result, status=status.HTTP_200_OK)

#获取邮箱群组信息
class EXGetDistributionGroup(mixins.CreateModelMixin, viewsets.GenericViewSet):
    '''
    '''
    # permission_classes = (ReadOnly,)
    serializer_class = IdentitySerializers

    def create(self, request, *args, **kwargs):
        '''
        * Get-DistributionGroup
        * https://docs.microsoft.com/en-us/powershell/module/exchange/users-and-groups/Get-DistributionGroup?view=exchange-ps
        * 获取邮箱群组信息
            - identity 用户唯一标识（必须）（Name，Alias，Distinguished name (DN)，Canonical DN，Email address，GUID）
            - **kwargs 表示函数接收可变长度的关键字参数字典作为函数的输入
        '''
        try:
            # 1. 反序列化 将其他格式（字典、JSON、XML等）转换为程序中的数据，例如将JSON字符串转换为Django中的模型类对象
            serializer = self.get_serializer(data=request.data)
            # 验证数据
            serializer.is_valid(raise_exception=True)
            headers = self.get_success_headers(serializer.data)
            data = serializer.data
            initial_data = serializer.initial_data
            kwargs = getkwargs(data, initial_data)
            result = GetDistributionGroup(data.get('identity'), **kwargs)
        except Exception as e:
            result = {"isSuccess": False, "message": '', 'count': 0, 'msg': str(e), 'code': 2}
        insert_drf_api_log(request, str(result['isSuccess']), str(result))
        return Response(result, status=status.HTTP_200_OK)

#禁用邮箱群组
class EXDisableGroup(mixins.CreateModelMixin, viewsets.GenericViewSet):
    '''
    '''
    # permission_classes = (ReadOnly,)
    serializer_class = IdentitySerializers

    def create(self, request, *args, **kwargs):
        '''
        * Disable-DistributionGroup
        * https://docs.microsoft.com/en-us/powershell/module/exchange/users-and-groups/Disable-DistributionGroup?view=exchange-ps
        * 禁用邮箱群组
            - identity 用户唯一标识（必须）（Name，Alias，Distinguished name (DN)，Canonical DN，Email address，GUID）
            - **kwargs 表示函数接收可变长度的关键字参数字典作为函数的输入
        '''
        try:
            # 1. 反序列化 将其他格式（字典、JSON、XML等）转换为程序中的数据，例如将JSON字符串转换为Django中的模型类对象
            serializer = self.get_serializer(data=request.data)
            # 验证数据
            serializer.is_valid(raise_exception=True)
            headers = self.get_success_headers(serializer.data)
            data = serializer.data
            initial_data = serializer.initial_data
            kwargs = getkwargs(data, initial_data)
            result = DisableDistributionGroup(data.get('identity'), **kwargs)
        except Exception as e:
            result = {"isSuccess": False, "message": '', 'count': 0, 'msg': str(e), 'code': 2}
        insert_drf_api_log(request, str(result['isSuccess']), str(result))
        return Response(result, status=status.HTTP_200_OK)

#启用邮箱群组
class EXEnableGroup(mixins.CreateModelMixin, viewsets.GenericViewSet):
    '''
    '''
    # permission_classes = (ReadOnly,)
    serializer_class = EnableDistributionGroupSerializers

    def create(self, request, *args, **kwargs):
        '''
        * enable-DistributionGroup
        * https://docs.microsoft.com/en-us/powershell/module/exchange/users-and-groups/Enable-DistributionGroup?view=exchange-ps
        * 启用邮箱群组
            - identity 用户唯一标识（必须）（Name，Distinguished name (DN)，Canonical DN，GUID）
            - alias 别名
            - **kwargs 表示函数接收可变长度的关键字参数字典作为函数的输入
        '''
        try:
            # 1. 反序列化 将其他格式（字典、JSON、XML等）转换为程序中的数据，例如将JSON字符串转换为Django中的模型类对象
            serializer = self.get_serializer(data=request.data)
            # 验证数据
            serializer.is_valid(raise_exception=True)
            headers = self.get_success_headers(serializer.data)
            data = serializer.data
            initial_data = serializer.initial_data
            kwargs = getkwargs(data, initial_data)
            result = EnableDistributionGroup(data.get('identity'), data.get('alias'), **kwargs)
        except Exception as e:
            result = {"isSuccess": False, "message": '', 'count': 0, 'msg': str(e), 'code': 2}
        insert_drf_api_log(request, str(result['isSuccess']), str(result))
        return Response(result, status=status.HTTP_200_OK)

#用户邮箱信息，一般用作获取用户邮箱大小使用情况
class EXGetMailboxStatistics(mixins.CreateModelMixin, viewsets.GenericViewSet):
    '''
    '''
    # permission_classes = (ReadOnly,)
    serializer_class = IdentitySerializers

    def create(self, request, *args, **kwargs):
        '''
        * Get-MailboxStatistics
        * https://docs.microsoft.com/en-us/powershell/module/exchange/mailboxes/Get-MailboxStatistics?view=exchange-ps
        * 用户邮箱信息，一般用作获取用户邮箱大小使用情况
            - identity 用户唯一标识（必须）（Name，Alias，Distinguished name (DN)，Canonical DN，domain name\\account name，Email address，GUID，LegacyExchangeDN，SamAccountName，User ID or user principal name (UPN)）
            - **kwargs 表示函数接收可变长度的关键字参数字典作为函数的输入
        '''
        try:
            # 1. 反序列化 将其他格式（字典、JSON、XML等）转换为程序中的数据，例如将JSON字符串转换为Django中的模型类对象
            serializer = self.get_serializer(data=request.data)
            # 验证数据
            serializer.is_valid(raise_exception=True)
            headers = self.get_success_headers(serializer.data)
            data = serializer.data
            initial_data = serializer.initial_data
            kwargs = getkwargs(data, initial_data)
            result = GetMailboxStatistics(data.get('identity'), **kwargs)
        except Exception as e:
            result = {"isSuccess": False, "message": '', 'count': 0, 'msg': str(e), 'code': 2}
        insert_drf_api_log(request, str(result['isSuccess']), str(result))
        return Response(result, status=status.HTTP_200_OK)


#获取邮箱服务器
class EXGetExchangeServer(mixins.CreateModelMixin, viewsets.GenericViewSet):
    '''
    '''
    # permission_classes = (ReadOnly,)
    serializer_class = serializers.Serializer

    def create(self, request, *args, **kwargs):
        '''
        * Get-ExchangeServer
        * https://docs.microsoft.com/en-us/powershell/module/exchange/organization/Get-ExchangeServer?view=exchange-ps
        * 获取邮箱服务器
            - **kwargs 表示函数接收可变长度的关键字参数字典作为函数的输入
        '''
        try:
            # 1. 反序列化 将其他格式（字典、JSON、XML等）转换为程序中的数据，例如将JSON字符串转换为Django中的模型类对象
            serializer = self.get_serializer(data=request.data)
            kwargs = serializer.initial_data
            result = GetExchangeServer(**kwargs)
        except Exception as e:
            result = {"isSuccess": False, "message": '', 'count': 0, 'msg': str(e), 'code': 2}
        insert_drf_api_log(request, str(result['isSuccess']), str(result))
        return Response(result, status=status.HTTP_200_OK)

#获取邮箱用户权限，获取代理发送权限
class EXgetADPermission(mixins.CreateModelMixin, viewsets.GenericViewSet):
    '''
    '''
    # permission_classes = (ReadOnly,)
    serializer_class = getADPermissionSerializers

    def create(self, request, *args, **kwargs):
        '''
        * get-ADPermission
        * https://docs.microsoft.com/en-us/powershell/module/exchange/active-directory/Get-ADPermission?view=exchange-ps
        * 获取邮箱用户权限，获取代理发送权限
            - identity 用户DN，如果有空格，需要用双引号括起来
            - **kwargs 表示函数接收可变长度的关键字参数字典作为函数的输入
        '''
        try:
            # 1. 反序列化 将其他格式（字典、JSON、XML等）转换为程序中的数据，例如将JSON字符串转换为Django中的模型类对象
            serializer = self.get_serializer(data=request.data)
            # 验证数据
            serializer.is_valid(raise_exception=True)
            headers = self.get_success_headers(serializer.data)
            data = serializer.data
            initial_data = serializer.initial_data
            kwargs = getkwargs(data, initial_data)
            result = getADPermission(data.get('identity'), **kwargs)
        except Exception as e:
            result = {"isSuccess": False, "message": '', 'count': 0, 'msg': str(e), 'code': 2}
        insert_drf_api_log(request, str(result['isSuccess']), str(result))
        return Response(result, status=status.HTTP_200_OK)

#获取邮箱联系人信息
class EXGetMailContact(mixins.CreateModelMixin, viewsets.GenericViewSet):
    '''
    '''
    # permission_classes = (ReadOnly,)
    serializer_class = IdentitySerializers

    def create(self, request, *args, **kwargs):
        '''
        * Get-MailContact
        * https://docs.microsoft.com/en-us/powershell/module/exchange/users-and-groups/Get-MailContact?view=exchange-ps
        * 获取邮箱联系人信息
            - identity 联系人唯一标识（必须）（Name，Alias，Distinguished name (DN)，Canonical DN，Email address，GUID）
            - **kwargs 表示函数接收可变长度的关键字参数字典作为函数的输入
        '''
        try:
            # 1. 反序列化 将其他格式（字典、JSON、XML等）转换为程序中的数据，例如将JSON字符串转换为Django中的模型类对象
            serializer = self.get_serializer(data=request.data)
            # 验证数据
            serializer.is_valid(raise_exception=True)
            headers = self.get_success_headers(serializer.data)
            data = serializer.data
            initial_data = serializer.initial_data
            kwargs = getkwargs(data, initial_data)
            result = GetMailContacthight(data.get('identity'), **kwargs)
        except Exception as e:
            result = {"isSuccess": False, "message": '', 'count': 0, 'msg': str(e), 'code': 2}
        insert_drf_api_log(request, str(result['isSuccess']), str(result))
        return Response(result, status=status.HTTP_200_OK)

#获取邮箱用户权限
class EXgetMailboxPermission(mixins.CreateModelMixin, viewsets.GenericViewSet):
    '''
    '''
    # permission_classes = (ReadOnly,)
    serializer_class = IdentitySerializers

    def create(self, request, *args, **kwargs):
        '''
        * get-MailboxPermission
        * https://docs.microsoft.com/en-us/powershell/module/exchange/mailboxes/Get-MailboxPermission?view=exchange-ps
        * 获取邮箱用户权限
            - identity 联系人唯一标识（必须）（Name，Alias，Distinguished name (DN)，Canonical DN，domain name\\account name，Email address，GUID，LegacyExchangeDN，SamAccountName，User ID or user principal name (UPN)）
            - **kwargs 表示函数接收可变长度的关键字参数字典作为函数的输入
        '''
        try:
            # 1. 反序列化 将其他格式（字典、JSON、XML等）转换为程序中的数据，例如将JSON字符串转换为Django中的模型类对象
            serializer = self.get_serializer(data=request.data)
            # 验证数据
            serializer.is_valid(raise_exception=True)
            headers = self.get_success_headers(serializer.data)
            data = serializer.data
            initial_data = serializer.initial_data
            kwargs = getkwargs(data, initial_data)
            result = getMailboxPermission(data.get('identity'), **kwargs)
        except Exception as e:
            result = {"isSuccess": False, "message": '', 'count': 0, 'msg': str(e), 'code': 2}
        insert_drf_api_log(request, str(result['isSuccess']), str(result))
        return Response(result, status=status.HTTP_200_OK)

#删除邮箱用户权限，一般用作删除用户完全访问权限
class EXRemoveMailboxPermission(mixins.CreateModelMixin, viewsets.GenericViewSet):
    '''
    '''
    # permission_classes = (ReadOnly,)
    serializer_class = RemoveMailboxPermissionSerializers

    def create(self, request, *args, **kwargs):
        '''
        * Remove-MailboxPermission
        * https://docs.microsoft.com/en-us/powershell/module/exchange/mailboxes/Remove-MailboxPermission?view=exchange-ps·
        * 删除邮箱用户权限，一般用作删除用户完全访问权限
            - identity 联系人唯一标识（必须）（Name，Alias，Distinguished name (DN)，Canonical DN，domain name\\account name，Email address，GUID，LegacyExchangeDN，SamAccountName，User ID or user principal name (UPN)）
            - User 删除哪个用户的权限（必须）
            - **kwargs 表示函数接收可变长度的关键字参数字典作为函数的输入
        '''
        try:
            # 1. 反序列化 将其他格式（字典、JSON、XML等）转换为程序中的数据，例如将JSON字符串转换为Django中的模型类对象
            serializer = self.get_serializer(data=request.data)
            # 验证数据
            serializer.is_valid(raise_exception=True)
            headers = self.get_success_headers(serializer.data)
            data = serializer.data
            initial_data = serializer.initial_data
            kwargs = getkwargs(data, initial_data)
            result = RemoveMailboxPermissionhight(data.get('identity'),data.get('User'),InheritanceType='All',AccessRights='FullAccess', **kwargs)
        except Exception as e:
            result = {"isSuccess": False, "message": '', 'count': 0, 'msg': str(e), 'code': 2}
        insert_drf_api_log(request, str(result['isSuccess']), str(result))
        return Response(result, status=status.HTTP_200_OK)

#添加邮箱用户权限，添加完全访问权限
class EXAddMailboxPermission(mixins.CreateModelMixin, viewsets.GenericViewSet):
    '''
    '''
    # permission_classes = (ReadOnly,)
    serializer_class = AddMailboxPermissionSerializers

    def create(self, request, *args, **kwargs):
        '''
        * Add-MailboxPermission
        * https://docs.microsoft.com/en-us/powershell/module/exchange/mailboxes/Add-MailboxPermission?view=exchange-ps
        * 添加邮箱用户权限，添加完全访问权限
            - identity 联系人唯一标识（必须）（Name，Alias，Distinguished name (DN)，Canonical DN，domain name\\account name，Email address，GUID，LegacyExchangeDN，SamAccountName，User ID or user principal name (UPN)）
            - User 添加哪个用户的权限（必须）
            - **kwargs 表示函数接收可变长度的关键字参数字典作为函数的输入
        '''
        try:
            # 1. 反序列化 将其他格式（字典、JSON、XML等）转换为程序中的数据，例如将JSON字符串转换为Django中的模型类对象
            serializer = self.get_serializer(data=request.data)
            # 验证数据
            serializer.is_valid(raise_exception=True)
            headers = self.get_success_headers(serializer.data)
            data = serializer.data
            initial_data = serializer.initial_data
            kwargs = getkwargs(data, initial_data)
            result = AddMailboxPermissionhight(data.get('identity'), data.get('User'), parametername='AccessRights',parametervalue='FullAccess', **kwargs)
        except Exception as e:
            result = {"isSuccess": False, "message": '', 'count': 0, 'msg': str(e), 'code': 2}
        insert_drf_api_log(request, str(result['isSuccess']), str(result))
        return Response(result, status=status.HTTP_200_OK)

#添加邮箱用户权限，添加代理发送权限
class EXAddADPermission(mixins.CreateModelMixin, viewsets.GenericViewSet):
    '''
    '''
    # permission_classes = (ReadOnly,)
    serializer_class = AddADPermissionSerializers

    def create(self, request, *args, **kwargs):
        '''
        * Add-ADPermission
        * https://docs.microsoft.com/en-us/powershell/module/exchange/active-directory/Add-ADPermission?view=exchange-ps
        * 添加邮箱用户权限，添加代理发送权限
            - identity 用户DN（必须）
            - User 添加哪个用户的权限（必须）
            - **kwargs 表示函数接收可变长度的关键字参数字典作为函数的输入
        '''
        try:
            # 1. 反序列化 将其他格式（字典、JSON、XML等）转换为程序中的数据，例如将JSON字符串转换为Django中的模型类对象
            serializer = self.get_serializer(data=request.data)
            # 验证数据
            serializer.is_valid(raise_exception=True)
            headers = self.get_success_headers(serializer.data)
            data = serializer.data
            initial_data = serializer.initial_data
            kwargs = getkwargs(data, initial_data)
            result = AddADPermission(data.get('identity'), data.get('User'), parametername='ExtendedRights',parametervalue='Send-as', **kwargs)
        except Exception as e:
            result = {"isSuccess": False, "message": '', 'count': 0, 'msg': str(e), 'code': 2}
        insert_drf_api_log(request, str(result['isSuccess']), str(result))
        return Response(result, status=status.HTTP_200_OK)

#删除邮箱用户权限 代理发送权限
class EXRemoveADPermission(mixins.CreateModelMixin, viewsets.GenericViewSet):
    '''
    '''
    # permission_classes = (ReadOnly,)
    serializer_class = RemoveADPermissionSerializers

    def create(self, request, *args, **kwargs):
        '''
        * Remove-ADPermission
        * https://docs.microsoft.com/zh-cn/powershell/module/exchange/active-directory/remove-adpermission?view=exchange-ps
        * 删除邮箱用户权限 代理发送权限
            - identity 用户DN（必须）
            - User 删除哪个用户的权限（必须）
            - **kwargs 表示函数接收可变长度的关键字参数字典作为函数的输入
        '''
        try:
            # 1. 反序列化 将其他格式（字典、JSON、XML等）转换为程序中的数据，例如将JSON字符串转换为Django中的模型类对象
            serializer = self.get_serializer(data=request.data)
            # 验证数据
            serializer.is_valid(raise_exception=True)
            headers = self.get_success_headers(serializer.data)
            data = serializer.data
            initial_data = serializer.initial_data
            kwargs = getkwargs(data, initial_data)
            result = RemoveADPermissionhight(data.get('identity'), data.get('User'), parametername='InheritanceType',parametervalue='All',parametername0='ExtendedRights',parametervalue0='send-as', **kwargs)
        except Exception as e:
            result = {"isSuccess": False, "message": '', 'count': 0, 'msg': str(e), 'code': 2}
        insert_drf_api_log(request, str(result['isSuccess']), str(result))
        return Response(result, status=status.HTTP_200_OK)


#开启联系人邮箱
class EXEnableMailContact(mixins.CreateModelMixin, viewsets.GenericViewSet):
    '''
    '''
    # permission_classes = (ReadOnly,)
    serializer_class = EnableMailContactSerializers

    def create(self, request, *args, **kwargs):
        '''
        * Enable-MailContact
        * https://docs.microsoft.com/en-us/powershell/module/exchange/users-and-groups/Enable-MailContact?view=exchange-ps
        * 开启联系人邮箱
            - identity 联系人唯一标识 （Name，Distinguished name (DN)，Canonical DN，GUID）
            - ExternalEmailAddress 邮箱地址
            - **kwargs 表示函数接收可变长度的关键字参数字典作为函数的输入
        '''
        try:
            # 1. 反序列化 将其他格式（字典、JSON、XML等）转换为程序中的数据，例如将JSON字符串转换为Django中的模型类对象
            serializer = self.get_serializer(data=request.data)
            # 验证数据
            serializer.is_valid(raise_exception=True)
            headers = self.get_success_headers(serializer.data)
            data = serializer.data
            initial_data = serializer.initial_data
            kwargs = getkwargs(data, initial_data)
            result = EnableMailContacthight(data.get('identity'), data.get('ExternalEmailAddress'), **kwargs)
        except Exception as e:
            result = {"isSuccess": False, "message": '', 'count': 0, 'msg': str(e), 'code': 2}
        insert_drf_api_log(request, str(result['isSuccess']), str(result))
        return Response(result, status=status.HTTP_200_OK)

#删除用户邮箱迁移请求
class EXRemoveMoveRequest(mixins.CreateModelMixin, viewsets.GenericViewSet):
    '''
    '''
    # permission_classes = (ReadOnly,)
    serializer_class = IdentitySerializers

    def create(self, request, *args, **kwargs):
        '''
        * Remove-MoveRequest
        * https://docs.microsoft.com/en-us/powershell/module/exchange/move-and-migration/Remove-MoveRequest?view=exchange-ps
        * 删除用户邮箱迁移请求
            - identity 移动请求用户的唯一标识（GUID，Distinguished name (DN)，Domain\Account，User principal name (UPN)，Legacy Exchange DN，SMTP address，Alias）
            - **kwargs 表示函数接收可变长度的关键字参数字典作为函数的输入
        '''
        try:
            # 1. 反序列化 将其他格式（字典、JSON、XML等）转换为程序中的数据，例如将JSON字符串转换为Django中的模型类对象
            serializer = self.get_serializer(data=request.data)
            # 验证数据
            serializer.is_valid(raise_exception=True)
            headers = self.get_success_headers(serializer.data)
            data = serializer.data
            initial_data = serializer.initial_data
            kwargs = getkwargs(data, initial_data)
            result = RemoveMoveRequesthight(data.get('identity'), **kwargs)
        except Exception as e:
            result = {"isSuccess": False, "message": '', 'count': 0, 'msg': str(e), 'code': 2}
        insert_drf_api_log(request, str(result['isSuccess']), str(result))
        return Response(result, status=status.HTTP_200_OK)

#新建联系人
class EXNewMailContact(mixins.CreateModelMixin, viewsets.GenericViewSet):
    '''
    '''
    # permission_classes = (ReadOnly,)
    serializer_class = NewMailContactSerializers

    def create(self, request, *args, **kwargs):
        '''
        * RNew-MailContact
        * https://docs.microsoft.com/en-us/powershell/module/exchange/users-and-groups/New-MailContact?view=exchange-ps
        * 新建联系人
            - Name =》CN，（displayname如果不写也会赋此值）  必须
            - ExternalEmailAddress  邮件地址  （必须）
            - **kwargs 表示函数接收可变长度的关键字参数字典作为函数的输入
        '''
        try:
            # 1. 反序列化 将其他格式（字典、JSON、XML等）转换为程序中的数据，例如将JSON字符串转换为Django中的模型类对象
            serializer = self.get_serializer(data=request.data)
            # 验证数据
            serializer.is_valid(raise_exception=True)
            headers = self.get_success_headers(serializer.data)
            data = serializer.data
            initial_data = serializer.initial_data
            kwargs = getkwargs(data, initial_data)
            result = NewMailContacthight(data.get('Name'), data.get('ExternalEmailAddress'), **kwargs)
        except Exception as e:
            result = {"isSuccess": False, "message": '', 'count': 0, 'msg': str(e), 'code': 2}
        insert_drf_api_log(request, str(result['isSuccess']), str(result))
        return Response(result, status=status.HTTP_200_OK)

#设置联系人邮箱
class EXSetMailContactvalue(mixins.CreateModelMixin, viewsets.GenericViewSet):
    '''
    '''
    # permission_classes = (ReadOnly,)
    serializer_class = IdentitySerializers

    def create(self, request, *args, **kwargs):
        '''
        * Set-MailContact
        * https://docs.microsoft.com/en-us/powershell/module/exchange/users-and-groups/Set-MailContact?view=exchange-ps
        * 设置联系人邮箱
            - identity  联系人唯一标识 （Name，Alias，Distinguished name (DN)，Canonical DN，Email address，GUID）
            - **kwargs 表示函数接收可变长度的关键字参数字典作为函数的输入
        '''
        try:
            # 1. 反序列化 将其他格式（字典、JSON、XML等）转换为程序中的数据，例如将JSON字符串转换为Django中的模型类对象
            serializer = self.get_serializer(data=request.data)
            # 验证数据
            serializer.is_valid(raise_exception=True)
            headers = self.get_success_headers(serializer.data)
            data = serializer.data
            initial_data = serializer.initial_data
            kwargs = getkwargs(data, initial_data)
            result = SetMailContactvalue(data.get('identity'), **kwargs)
        except Exception as e:
            result = {"isSuccess": False, "message": '', 'count': 0, 'msg': str(e), 'code': 2}
        insert_drf_api_log(request, str(result['isSuccess']), str(result))
        return Response(result, status=status.HTTP_200_OK)

#设置pop mapi信息
class EXSetCasMailbox(mixins.CreateModelMixin, viewsets.GenericViewSet):
    '''
    '''
    # permission_classes = (ReadOnly,)
    serializer_class = IdentitySerializers

    def create(self, request, *args, **kwargs):
        '''
        * Set-CasMailbox
        * https://docs.microsoft.com/en-us/powershell/module/exchange/client-access/Set-CASMailbox?view=exchange-ps
        * 设置pop mapi信息
            - identity  联系人唯一标识 （Name，Alias，Distinguished name (DN)，Canonical DN，domain name\\account name，Email address，GUID，LegacyExchangeDN，SamAccountName，User ID or user principal name (UPN)）
            - **kwargs 表示函数接收可变长度的关键字参数字典作为函数的输入
        '''
        try:
            # 1. 反序列化 将其他格式（字典、JSON、XML等）转换为程序中的数据，例如将JSON字符串转换为Django中的模型类对象
            serializer = self.get_serializer(data=request.data)
            # 验证数据
            serializer.is_valid(raise_exception=True)
            headers = self.get_success_headers(serializer.data)
            data = serializer.data
            initial_data = serializer.initial_data
            kwargs = getkwargs(data, initial_data)
            result = SetCasMailboxhight(data.get('identity'), **kwargs)
        except Exception as e:
            result = {"isSuccess": False, "message": '', 'count': 0, 'msg': str(e), 'code': 2}
        insert_drf_api_log(request, str(result['isSuccess']), str(result))
        return Response(result, status=status.HTTP_200_OK)

#新增/删除 用户smtp地址
class EXSetMailboxEmailAddresses(mixins.CreateModelMixin, viewsets.GenericViewSet):
    '''
    '''
    # permission_classes = (ReadOnly,)
    serializer_class = SetMailboxEmailAddressesSerializers

    def create(self, request, *args, **kwargs):
        '''
        * Set-Mailbox
        * https://docs.microsoft.com/en-us/powershell/module/exchange/mailboxes/Set-Mailbox?view=exchange-ps
        * 新增/删除 用户smtp地址
        * Set-Mailbox -Identity wzx -EmailAddresses @{add='hhhh@test.com'}
        * Set-Mailbox -Identity wzx -EmailAddresses @{remove='hhhh@test.com'}
            - identity  联系人唯一标识 （Name，Alias，Distinguished name (DN)，Canonical DN，domain name\\account name，Email address，GUID，LegacyExchangeDN，SamAccountName，User ID or user principal name (UPN)）
            - EmailAddresses 邮箱地址
            - **kwargs 表示函数接收可变长度的关键字参数字典作为函数的输入
        '''
        try:
            # 1. 反序列化 将其他格式（字典、JSON、XML等）转换为程序中的数据，例如将JSON字符串转换为Django中的模型类对象
            serializer = self.get_serializer(data=request.data)
            # 验证数据
            serializer.is_valid(raise_exception=True)
            headers = self.get_success_headers(serializer.data)
            data = serializer.data
            initial_data = serializer.initial_data
            kwargs = getkwargs(data, initial_data)
            result = SetMailboxEmailAddresses(data.get('identity'), **kwargs)
        except Exception as e:
            result = {"isSuccess": False, "message": '', 'count': 0, 'msg': str(e), 'code': 2}
        insert_drf_api_log(request, str(result['isSuccess']), str(result))
        return Response(result, status=status.HTTP_200_OK)


#设置用户邮箱
class EXSetMailbox(mixins.CreateModelMixin, viewsets.GenericViewSet):
    '''
    '''
    # permission_classes = (ReadOnly,)
    serializer_class = IdentitySerializers

    def create(self, request, *args, **kwargs):
        '''
        * Set-Mailbox
        * https://docs.microsoft.com/en-us/powershell/module/exchange/mailboxes/Set-Mailbox?view=exchange-ps
        * 设置用户邮箱
            - identity  联系人唯一标识（Name，Alias，Distinguished name (DN)，Canonical DN，domain name\\account name，Email address，GUID，LegacyExchangeDN，SamAccountName，User ID or user principal name (UPN)）
            - **kwargs 表示函数接收可变长度的关键字参数字典作为函数的输入
        '''
        try:
            # 1. 反序列化 将其他格式（字典、JSON、XML等）转换为程序中的数据，例如将JSON字符串转换为Django中的模型类对象
            serializer = self.get_serializer(data=request.data)
            # 验证数据
            serializer.is_valid(raise_exception=True)
            headers = self.get_success_headers(serializer.data)
            data = serializer.data
            initial_data = serializer.initial_data
            kwargs = getkwargs(data, initial_data)
            result = SetMailbox(data.get('identity'), **kwargs)
        except Exception as e:
            result = {"isSuccess": False, "message": '', 'count': 0, 'msg': str(e), 'code': 2}
        insert_drf_api_log(request, str(result['isSuccess']), str(result))
        return Response(result, status=status.HTTP_200_OK)

#设置用户邮箱level1
class EXSetMailbox1(mixins.CreateModelMixin, viewsets.GenericViewSet):
    '''
    '''
    # permission_classes = (ReadOnly,)
    serializer_class = IdentitySerializers

    def create(self, request, *args, **kwargs):
        '''
        * Set-Mailbox
        * https://docs.microsoft.com/en-us/powershell/module/exchange/mailboxes/Set-Mailbox?view=exchange-ps
        * 设置用户邮箱level1
            - identity  联系人唯一标识（Name，Alias，Distinguished name (DN)，Canonical DN，domain name\\account name，Email address，GUID，LegacyExchangeDN，SamAccountName，User ID or user principal name (UPN)）
            - **kwargs 表示函数接收可变长度的关键字参数字典作为函数的输入
        '''
        try:
            # 1. 反序列化 将其他格式（字典、JSON、XML等）转换为程序中的数据，例如将JSON字符串转换为Django中的模型类对象
            serializer = self.get_serializer(data=request.data)
            # 验证数据
            serializer.is_valid(raise_exception=True)
            headers = self.get_success_headers(serializer.data)
            data = serializer.data
            initial_data = serializer.initial_data
            kwargs = getkwargs(data, initial_data)
            result = SetMailbox(data.get('identity'), **kwargs)
        except Exception as e:
            result = {"isSuccess": False, "message": '', 'count': 0, 'msg': str(e), 'code': 2}
        insert_drf_api_log(request, str(result['isSuccess']), str(result))
        return Response(result, status=status.HTTP_200_OK)

#设置用户邮箱level2
class EXSetMailbox2(mixins.CreateModelMixin, viewsets.GenericViewSet):
    '''
    '''
    # permission_classes = (ReadOnly,)
    serializer_class = IdentitySerializers

    def create(self, request, *args, **kwargs):
        '''
        * Set-Mailbox
        * https://docs.microsoft.com/en-us/powershell/module/exchange/mailboxes/Set-Mailbox?view=exchange-ps
        * 设置用户邮箱level2
            - identity  联系人唯一标识（Name，Alias，Distinguished name (DN)，Canonical DN，domain name\\account name，Email address，GUID，LegacyExchangeDN，SamAccountName，User ID or user principal name (UPN)）
            - **kwargs 表示函数接收可变长度的关键字参数字典作为函数的输入
        '''
        try:
            # 1. 反序列化 将其他格式（字典、JSON、XML等）转换为程序中的数据，例如将JSON字符串转换为Django中的模型类对象
            serializer = self.get_serializer(data=request.data)
            # 验证数据
            serializer.is_valid(raise_exception=True)
            headers = self.get_success_headers(serializer.data)
            data = serializer.data
            initial_data = serializer.initial_data
            kwargs = getkwargs(data, initial_data)
            result = SetMailbox(data.get('identity'), **kwargs)
        except Exception as e:
            result = {"isSuccess": False, "message": '', 'count': 0, 'msg': str(e), 'code': 2}
        insert_drf_api_log(request, str(result['isSuccess']), str(result))
        return Response(result, status=status.HTTP_200_OK)

#设置群组邮箱
class EXSetDistributionGroup(mixins.CreateModelMixin, viewsets.GenericViewSet):
    '''
    '''
    # permission_classes = (ReadOnly,)
    serializer_class = IdentitySerializers

    def create(self, request, *args, **kwargs):
        '''
        * Set-DistributionGroup
        * https://docs.microsoft.com/en-us/powershell/module/exchange/users-and-groups/Set-DistributionGroup?view=exchange-ps
        * 设置群组邮箱
            - identity  联系人唯一标识 （Name，Alias，Distinguished name (DN)，Canonical DN，Email address，GUID）
            - **kwargs 表示函数接收可变长度的关键字参数字典作为函数的输入
        '''
        try:
            # 1. 反序列化 将其他格式（字典、JSON、XML等）转换为程序中的数据，例如将JSON字符串转换为Django中的模型类对象
            serializer = self.get_serializer(data=request.data)
            # 验证数据
            serializer.is_valid(raise_exception=True)
            headers = self.get_success_headers(serializer.data)
            data = serializer.data
            initial_data = serializer.initial_data
            kwargs = getkwargs(data, initial_data)
            result = SetDistributionGroup(data.get('identity'), **kwargs)
        except Exception as e:
            result = {"isSuccess": False, "message": '', 'count': 0, 'msg': str(e), 'code': 2}
        insert_drf_api_log(request, str(result['isSuccess']), str(result))
        return Response(result, status=status.HTTP_200_OK)

#获取pop mapi信息
class EXGetCasMailboxhight(mixins.CreateModelMixin, viewsets.GenericViewSet):
    '''
    '''
    # permission_classes = (ReadOnly,)
    serializer_class = IdentitySerializers

    def create(self, request, *args, **kwargs):
        '''
        * Get-CasMailbox
        * https://docs.microsoft.com/en-us/powershell/module/exchange/client-access/Get-CASMailbox?view=exchange-ps
        * 获取pop mapi信息
            - identity  联系人唯一标识 （Name，Alias，Distinguished name (DN)，Canonical DN，domain name\\account name，Email address，GUID，LegacyExchangeDN，SamAccountName，User ID or user principal name (UPN)）
            - **kwargs 表示函数接收可变长度的关键字参数字典作为函数的输入
        '''
        try:
            # 1. 反序列化 将其他格式（字典、JSON、XML等）转换为程序中的数据，例如将JSON字符串转换为Django中的模型类对象
            serializer = self.get_serializer(data=request.data)
            # 验证数据
            serializer.is_valid(raise_exception=True)
            headers = self.get_success_headers(serializer.data)
            data = serializer.data
            initial_data = serializer.initial_data
            kwargs = getkwargs(data, initial_data)
            result = GetCasMailboxhight(data.get('identity'), **kwargs)
        except Exception as e:
            result = {"isSuccess": False, "message": '', 'count': 0, 'msg': str(e), 'code': 2}
        insert_drf_api_log(request, str(result['isSuccess']), str(result))
        return Response(result, status=status.HTTP_200_OK)

#用户邮箱信息，获取用户邮箱容量数据库等信息
class EXGetMailbox(mixins.CreateModelMixin, viewsets.GenericViewSet):
    '''
    '''
    # permission_classes = (ReadOnly,)
    serializer_class = IdentitySerializers

    def create(self, request, *args, **kwargs):
        '''
        * Get-Mailbox
        * https://docs.microsoft.com/en-us/powershell/module/exchange/mailboxes/get-mailbox?view=exchange-ps
        * 用户邮箱信息，获取用户邮箱容量数据库等信息
            - identity  联系人唯一标识 （Name，Alias，Distinguished name (DN)，Canonical DN，domain name\\account name，Email address，GUID，LegacyExchangeDN，SamAccountName，User ID or user principal name (UPN)）
            - **kwargs 表示函数接收可变长度的关键字参数字典作为函数的输入
        '''
        try:
            # 1. 反序列化 将其他格式（字典、JSON、XML等）转换为程序中的数据，例如将JSON字符串转换为Django中的模型类对象
            serializer = self.get_serializer(data=request.data)
            # 验证数据
            serializer.is_valid(raise_exception=True)
            headers = self.get_success_headers(serializer.data)
            data = serializer.data
            initial_data = serializer.initial_data
            kwargs = getkwargs(data, initial_data)
            result = GetMailbox(data.get('identity'), **kwargs)
        except Exception as e:
            result = {"isSuccess": False, "message": '', 'count': 0, 'msg': str(e), 'code': 2}
        insert_drf_api_log(request, str(result['isSuccess']), str(result))
        return Response(result, status=status.HTTP_200_OK)