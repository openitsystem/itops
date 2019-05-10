# -*- coding: utf-8 -*-
import six
from django.http import HttpResponse
import json
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication

from apps.activeapi.views import newUser, newGroup, newComputer, newContact, newOrganizationalUnit, set_rename_object, dnMoveToOu, delete_object, inspect_object, setAccount, resetPassword, \
    serchlock, unlockuser, can_accidentally_deleted, check_accidentally_deleted, uncheck_accidentally_deleted, delete_user, delete_group, delete_contact, delete_computer, delete_ou, \
    get_users
from apps.ldaptime.views import utc2local
from dbinfo.views import insert_drf_api_log
from itapi.serializers import *
from itops.settings import ldap3RESTARTABLE
from utils.permissions import AdapiPermissionsLevel, AdapiPermissions


def date_handler(obj):
    if hasattr(obj, 'isoformat'):
        try:
            obj_time_str = (utc2local(obj)).strftime('%Y-%m-%d %H:%M:%S')
        except:
            obj_time_str = obj.isoformat()
        return obj_time_str
    elif isinstance(obj, six.binary_type):
        # Best-effort for binary blobs. See #4187.
        try:
            objs = obj.decode('utf-8')
        except:
            objs = str(obj)
        return objs
    else:
        raise TypeError

# Api方法调用说明
class Api_docs(mixins.CreateModelMixin, viewsets.GenericViewSet):
    '''
    '''
    permission_classes = ()
    serializer_class = serializers.Serializer

    def create(self, request, *args, **kwargs):
        '''
        ## [Api方法调用说明(点击跳转到文档)](itapidocument)

        #### 1.找管理员新建API 用户，密码。并添加相应的权限
        #### 2.用账号，密码 json post调用 Api-token-auth

        ```
        {"username":"admin","password":"123456"}
        ```

        * 生成token
        ### ==注意token过期时间,默认2小时==
        #### 3.调用方法
        * 注意方法的类型，正常都是POST
        * 把上面获取的token 填写到Headers ,注意 JWT 后面有一个空格

        ```
        headers = {
                "Authorization": "JWT eyJ0eXAiOiJKV1QiLCJhbGciOiJIiJ9.eyJleHAiOjE1NTQ5OTExMTUsInVzZXJuYW1lIjoiYWRtaW4iLCJ1c2VyX2lkIjo1LCJlbWFpbCI6IiJ9.lfUCokn_V6wPCopE4tMMl",
                "Content-Type": "application/json"
            }
        ```

        * body 传入对应格式的json # python

        value = json.dumps({"dn":"CN=sss,OU=users,OU=SUZ,DC=contos,DC=cn",
        "attributesName":"ipphone",
        "attributesVaule":"sew12",
        "displayname":"displayname1",
        "Office":"Office1"})

        '''
        try:
            # 1. 反序列化 将其他格式（字典、JSON、XML等）转换为程序中的数据，例如将JSON字符串转换为Django中的模型类对象
            serializer = self.get_serializer(data=request.data)
            result = {"isSuccess": True, "message": '调用成功', 'count': 0, 'msg': '', 'code': 0}
        except Exception as e:
            result = {"isSuccess": False, "message": '', 'count': 0, 'msg': str(e), 'code': 2}
        insert_drf_api_log(request, str(result['isSuccess']), str(result))
        return Response(result, status=status.HTTP_200_OK)


#ldap3 搜索方法 获取数据数量受服务器限制
class Ldap3Search(mixins.CreateModelMixin, viewsets.GenericViewSet):
    '''

    '''
    # permission_classes = (ReadOnly,)
    serializer_class = Ldap3SearchSerializers

    def create(self, request, *args, **kwargs):
        '''
        ldap3搜索
        '''
        # 1. 反序列化 将其他格式（字典、JSON、XML等）转换为程序中的数据，例如将JSON字符串转换为Django中的模型类对象
        serializer = self.get_serializer(data=request.data)
        # 验证数据
        serializer.is_valid(raise_exception=True)
        headers = self.get_success_headers(serializer.data)
        data = serializer.data
        try:
            with ldap3RESTARTABLE as conn:
                object_list = []
                if data['attributes'] == ['']:
                    data['attributes'] = None
                if data['paged_cookie'] == ['']:
                    data['paged_cookie'] = None
                conn.search(search_base=data['search_base'], search_filter=data['search_filter'], search_scope=data['search_scope'],
                            attributes=data['attributes'], size_limit=data['size_limit'], time_limit=data['time_limit'],
                            paged_size=data['paged_size'], paged_criticality=data['paged_criticality'], paged_cookie=data['paged_cookie'],)
                result_id = conn.result
                response_id = conn.response
                if result_id.get('result', '') == 0:
                    for response in response_id:
                        object_dn = response.get('dn','')
                        object_attributes = response.get('attributes', '')
                        if object_dn:
                            object_list.append({'dn': object_dn, "attributes" : dict(object_attributes)})
                    result = {"isSuccess": True, "message": object_list, 'count': len(object_list), 'msg': '', 'code': 0}
                else:
                    result = {"isSuccess": False, "message": '', 'count': 0, 'msg': str(result_id['description']), 'code': 1}
        except Exception as e:
            result = {"isSuccess": False, "message": '', 'count': 0, 'msg': str(e), 'code': 2}
        #return Response(result, status=status.HTTP_200_OK)
        insert_drf_api_log(request, str(result['isSuccess']), str(result))
        response = HttpResponse()
        response['Content-Type'] = "text/javascript"
        response.write(json.dumps(result, default=date_handler).encode("UTF-8"))
        return response

# ldap3 搜索方法 根据sAMAccountName属性 搜索对象
class Ldap3SearchDN(mixins.CreateModelMixin, viewsets.GenericViewSet):
        '''

        '''
        # permission_classes = (ReadOnly,)
        serializer_class = Ldap3sAMAccountNameSerializers

        def create(self, request, *args, **kwargs):
            '''
            ldap3 根据sAMAccountName属性 搜索对象
            '''
            # 1. 反序列化 将其他格式（字典、JSON、XML等）转换为程序中的数据，例如将JSON字符串转换为Django中的模型类对象
            serializer = self.get_serializer(data=request.data)
            # 验证数据
            serializer.is_valid(raise_exception=True)
            headers = self.get_success_headers(serializer.data)
            data = serializer.data
            try:
                with ldap3RESTARTABLE as conn:
                    object_list = []
                    sAMAccountName = data.get('sAMAccountName','')
                    conn.search(search_base=data.get('search_base', ''),
                                search_filter="(sAMAccountName="+sAMAccountName+")",
                                attributes=data.get('attributes',{}),
                                )
                    result_id = conn.result
                    response_id = conn.response
                    if result_id.get('result', '') == 0:
                        for response in response_id:
                            object_dn = response.get('dn', '')
                            object_attributes = response.get('attributes', '')
                            if object_dn:
                                object_list.append({'dn': object_dn, "attributes": dict(object_attributes)})
                        result = {"isSuccess": True, "message": object_list, 'count': len(object_list), 'msg': '', 'code': 0}
                    else:
                        result = {"isSuccess": False, "message": '', 'count': 0, 'msg': str(result_id['description']), 'code': 1}
            except Exception as e:
                result = {"isSuccess": False, "message": '', 'count': 0, 'msg': str(e), 'code': 2}
            # return Response(result, status=status.HTTP_200_OK)
            insert_drf_api_log(request, str(result['isSuccess']), str(result))
            response = HttpResponse()
            response['Content-Type'] = "text/javascript"
            response.write(json.dumps(result, default=date_handler).encode("UTF-8"))
            return response

#ldap3 分页搜索方法 分页获取数据后一起返回
class Ldap3PagedSearch(mixins.CreateModelMixin, viewsets.GenericViewSet):
    '''
    视图中一般做三件事:
            1 .将请求的数据（如JSON格式）转换为模型类对象 -反序列化
            2 .操作数据库
            3 .将模型类对象转换为响应的数据（如JSON格式） -序列化
            我们在第一步和第三步的时候我们都会涉及到将json数据转化成模型类对象,以及将模型类对象转化成json的数据返回回去.
            这里就会涉及到一个来回重复转化的问题,所以我们使用序列化,以及反序列化.
    '''
    # permission_classes = (ReadOnly,)
    serializer_class = Ldap3SearchSerializers

    def create(self, request, *args, **kwargs):
        '''
        ldap3搜索
        '''
        # 1. 反序列化 将其他格式（字典、JSON、XML等）转换为程序中的数据，例如将JSON字符串转换为Django中的模型类对象
        serializer = self.get_serializer(data=request.data)
        # 验证数据
        serializer.is_valid(raise_exception=True)
        headers = self.get_success_headers(serializer.data)
        data = serializer.data
        try:
            with ldap3RESTARTABLE as conn:
                object_list = []
                if data['attributes'] == ['']:
                    data['attributes'] = None
                if data['paged_cookie'] == ['']:
                    data['paged_cookie'] = None
                conn.search(search_base=data['search_base'], search_filter=data['search_filter'], search_scope=data['search_scope'],
                            attributes=data['attributes'], size_limit=data['size_limit'], time_limit=data['time_limit'],
                            paged_size=data['paged_size'], paged_criticality=data['paged_criticality'], paged_cookie=data['paged_cookie'],)
                result_id = conn.result
                response_id = conn.response
                if result_id.get('result', '') == 0:
                    for response in response_id:
                        object_dn = response.get('dn','')
                        object_attributes = response.get('attributes', '')
                        if object_dn:
                            object_list.append({'dn': object_dn, "attributes" : dict(object_attributes)})
                    result = {"isSuccess": True, "message": object_list, 'count': len(object_list), 'msg': '', 'code': 0}
                else:
                    result = {"isSuccess": False, "message": '', 'count': 0, 'msg': str(result_id['description']), 'code': 1}
        except Exception as e:
            result = {"isSuccess": False, "message": '', 'count': 0, 'msg': str(e), 'code': 2}
        #return Response(result, status=status.HTTP_200_OK)
        response = HttpResponse()
        response['Content-Type'] = "text/javascript"
        response.write(json.dumps(result, default=date_handler).encode("UTF-8"))
        return response

# ldap3 新建用户
class Ldap3AddUser(mixins.CreateModelMixin, viewsets.GenericViewSet):
    '''
    '''
    # permission_classes = (ReadOnly,)
    serializer_class = Ldap3AddUserSerializers

    def create(self, request, *args, **kwargs):
        '''
        ldap3 新建用户
        '''
        try:
            # 1. 反序列化 将其他格式（字典、JSON、XML等）转换为程序中的数据，例如将JSON字符串转换为Django中的模型类对象
            serializer = self.get_serializer(data=request.data)
            # 验证数据
            serializer.is_valid(raise_exception=True)
            headers = self.get_success_headers(serializer.data)
            data = serializer.data
            newUsers = newUser(
                distinguishedName=data.get('dn'),
                cn=data.get('cn', None),
                sn=data.get('sn', None),
                givenName=data.get('givenName', None),
                displayName=data.get('displayName', None),
                userPrincipalName=data.get('userPrincipalName', None),
                sAMAccountName=data.get('sAMAccountName', None),
                password=data.get('password', None),
                userAccountControl=data.get('userAccountControl', None),
                mail=data.get('mail', None), maildb=data.get('maildb', None), attributes=data.get('attributes', {}))
            if newUsers['isSuccess']:
                result = {"isSuccess": True, "message": newUsers['message'], 'count': 1, 'msg': '', 'code': 0}
            else:
                result = {"isSuccess": False, "message": '', 'count': 1, 'msg': newUsers['message'], 'code': 1}
        except Exception as e:
            result = {"isSuccess": False, "message": '', 'count': 0, 'msg': str(e), 'code': 2}
        insert_drf_api_log(request, str(result['isSuccess']), str(result))
        return Response(result, status=status.HTTP_200_OK)

# ldap3 新建组
class Ldap3AddGroup(mixins.CreateModelMixin, viewsets.GenericViewSet):
    '''
    '''
    # permission_classes = (ReadOnly,)
    serializer_class = Ldap3AddGroupSerializers

    def create(self, request, *args, **kwargs):
        '''
        ldap3 新建组
        '''
        try:
            # 1. 反序列化 将其他格式（字典、JSON、XML等）转换为程序中的数据，例如将JSON字符串转换为Django中的模型类对象
            serializer = self.get_serializer(data=request.data)
            # 验证数据
            serializer.is_valid(raise_exception=True)
            headers = self.get_success_headers(serializer.data)
            data = serializer.data
            newGroups = newGroup(
                distinguishedName=data.get('dn'),
                cn=data.get('cn', None),
                sAMAccountName=data.get('sAMAccountName', None),
                groupType=data.get('groupType', ''),
                attributes=data.get('attributes', {}))
            if newGroups['isSuccess']:
                result = {"isSuccess": True, "message": newGroups['message'], 'count': 1, 'msg': '', 'code': 0}
            else:
                result = {"isSuccess": False, "message": '', 'count': 1, 'msg': newGroups['message'], 'code': 1}
        except Exception as e:
            result = {"isSuccess": False, "message": '', 'count': 0, 'msg': str(e), 'code': 2}
        insert_drf_api_log(request, str(result['isSuccess']), str(result))
        return Response(result, status=status.HTTP_200_OK)

# ldap3 新建计算机
class Ldap3AddComputer(mixins.CreateModelMixin, viewsets.GenericViewSet):
    '''
    '''
    # permission_classes = (ReadOnly,)
    serializer_class = Ldap3AddComputerSerializers

    def create(self, request, *args, **kwargs):
        '''
        ldap3 新建计算机
        '''
        try:
            # 1. 反序列化 将其他格式（字典、JSON、XML等）转换为程序中的数据，例如将JSON字符串转换为Django中的模型类对象
            serializer = self.get_serializer(data=request.data)
            # 验证数据
            serializer.is_valid(raise_exception=True)
            headers = self.get_success_headers(serializer.data)
            data = serializer.data
            newComputers = newComputer(
                distinguishedName=data.get('dn'),
                cn=data.get('cn', None),
                userAccountControl=4128,
                attributes=data.get('attributes', {}))
            if newComputers['isSuccess']:
                result = {"isSuccess": True, "message": newComputers['message'], 'count': 1, 'msg': '', 'code': 0}
            else:
                result = {"isSuccess": False, "message": '', 'count': 1, 'msg': newComputers['message'], 'code': 1}
        except Exception as e:
            result = {"isSuccess": False, "message": '', 'count': 0, 'msg': str(e), 'code': 2}
        insert_drf_api_log(request, str(result['isSuccess']), str(result))
        return Response(result, status=status.HTTP_200_OK)

# ldap3 新建联系人
class Ldap3AddContact(mixins.CreateModelMixin, viewsets.GenericViewSet):
    '''
    '''
    # permission_classes = (ReadOnly,)
    serializer_class = Ldap3AddContactSerializers

    def create(self, request, *args, **kwargs):
        '''
        ldap3 新建联系人
        '''
        try:
            # 1. 反序列化 将其他格式（字典、JSON、XML等）转换为程序中的数据，例如将JSON字符串转换为Django中的模型类对象
            serializer = self.get_serializer(data=request.data)
            # 验证数据
            serializer.is_valid(raise_exception=True)
            headers = self.get_success_headers(serializer.data)
            data = serializer.data
            newContacts = newContact(
                distinguishedName=data.get('dn'),
                cn=data.get('cn', None),
                sn=data.get('sn', None),
                givenName=data.get('givenName', None),
                displayName=data.get('displayName', None),
                description=data.get('description', None),
                mail=data.get('mail', None),
                name=data.get('name', None),
                smtpvalue=data.get('smtpvalue', None),
                attributes=data.get('attributes', {}))
            if newContacts['isSuccess']:
                result = {"isSuccess": True, "message": newContacts['message'], 'count': 1, 'msg': '', 'code': 0}
            else:
                result = {"isSuccess": False, "message": '', 'count': 1, 'msg': newContacts['message'], 'code': 1}
        except Exception as e:
            result = {"isSuccess": False, "message": '', 'count': 0, 'msg': str(e), 'code': 2}
        insert_drf_api_log(request, str(result['isSuccess']), str(result))
        return Response(result, status=status.HTTP_200_OK)

# ldap3 新建组织单位
class Ldap3AddOU(mixins.CreateModelMixin, viewsets.GenericViewSet):
    '''
    '''
    # permission_classes = (ReadOnly,)
    serializer_class = Ldap3AddOrganizationalUnitSerializers

    def create(self, request, *args, **kwargs):
        '''
        ldap3 新建组织单位
        '''
        try:
            # 1. 反序列化 将其他格式（字典、JSON、XML等）转换为程序中的数据，例如将JSON字符串转换为Django中的模型类对象
            serializer = self.get_serializer(data=request.data)
            # 验证数据
            serializer.is_valid(raise_exception=True)
            headers = self.get_success_headers(serializer.data)
            data = serializer.data
            newOrganizationalUnits = newOrganizationalUnit(
                distinguishedName=data.get('dn'),
                cn=data.get('cn', None),
                prevent=data.get('prevent', None),
                attributes=data.get('attributes', {}))
            if newOrganizationalUnits['isSuccess']:
                result = {"isSuccess": True, "message": newOrganizationalUnits['message'], 'count': 1, 'msg': '', 'code': 0}
            else:
                result = {"isSuccess": False, "message": '', 'count': 1, 'msg': newOrganizationalUnits['message'], 'code': 1}
        except Exception as e:
            result = {"isSuccess": False, "message": '', 'count': 0, 'msg': str(e), 'code': 2}
        insert_drf_api_log(request, str(result['isSuccess']), str(result))
        return Response(result, status=status.HTTP_200_OK)

# ldap3 重命名对象
class Ldap3RenameObject(mixins.CreateModelMixin, viewsets.GenericViewSet):
    '''
    '''
    # permission_classes = (ReadOnly,)
    serializer_class = Ldap3RenameObjectSerializers

    def create(self, request, *args, **kwargs):
        '''
        ldap3 重命名对象
        '''
        try:
            # 1. 反序列化 将其他格式（字典、JSON、XML等）转换为程序中的数据，例如将JSON字符串转换为Django中的模型类对象
            serializer = self.get_serializer(data=request.data)
            # 验证数据
            serializer.is_valid(raise_exception=True)
            headers = self.get_success_headers(serializer.data)
            data = serializer.data
            set_rename_objects = set_rename_object(
                distinguishedName=data.get('dn'),
                cn=data.get('cn', None),
                sn=data.get('sn', None),
                givenName=data.get('givenName', None),
                displayName=data.get('displayName', None),
                userPrincipalName=data.get('userPrincipalName', None),
                sAMAccountName=data.get('sAMAccountName', None),
                objectClass=data.get('objectClass', None))
            if set_rename_objects['isSuccess']:
                result = {"isSuccess": True, "message": set_rename_objects['message'], 'count': 1, 'msg': '', 'code': 0}
            else:
                result = {"isSuccess": False, "message": '', 'count': 1, 'msg': set_rename_objects['message'], 'code': 1}
        except Exception as e:
            result = {"isSuccess": False, "message": '', 'count': 0, 'msg': str(e), 'code': 2}
        insert_drf_api_log(request, str(result['isSuccess']), str(result))
        return Response(result, status=status.HTTP_200_OK)

# ldap3 多dn移动到新OU
class Ldap3DnMoveToOu(mixins.CreateModelMixin, viewsets.GenericViewSet):
    '''
    '''
    # permission_classes = (ReadOnly,)
    serializer_class = Ldap3DnMoveToOuSerializers

    def create(self, request, *args, **kwargs):
        '''
        ldap3 多dn移动到新OU
        '''
        try:
            # 1. 反序列化 将其他格式（字典、JSON、XML等）转换为程序中的数据，例如将JSON字符串转换为Django中的模型类对象
            serializer = self.get_serializer(data=request.data)
            # 验证数据
            serializer.is_valid(raise_exception=True)
            headers = self.get_success_headers(serializer.data)
            data = serializer.data
            dnMoveToOus = dnMoveToOu(
                dns=data.get('dns'),
                new_superior=data.get('new_superior', None),)
            if dnMoveToOus['isSuccess']:
                result = {"isSuccess": True, "message": dnMoveToOus['message'], 'count': 1, 'msg': '', 'code': 0}
            else:
                result = {"isSuccess": False, "message": '', 'count': 1, 'msg': dnMoveToOus['message'], 'code': 1}
        except Exception as e:
            result = {"isSuccess": False, "message": '', 'count': 0, 'msg': str(e), 'code': 2}
        insert_drf_api_log(request, str(result['isSuccess']), str(result))
        return Response(result, status=status.HTTP_200_OK)

#Ldap3DeleteObjectSerializers 删除对象
class Ldap3DeleteObject(mixins.CreateModelMixin, viewsets.GenericViewSet):
    '''
    '''
    # permission_classes = (ReadOnly,)
    serializer_class = Ldap3DeleteObjectSerializers

    def create(self, request, *args, **kwargs):
        '''
        ldap3 删除对象
        '''
        try:
            # 1. 反序列化 将其他格式（字典、JSON、XML等）转换为程序中的数据，例如将JSON字符串转换为Django中的模型类对象
            serializer = self.get_serializer(data=request.data)
            # 验证数据
            serializer.is_valid(raise_exception=True)
            headers = self.get_success_headers(serializer.data)
            data = serializer.data
            delete_objects = delete_object(
                dn=data.get('dn'),
                controls=data.get('controls', None),)
            if delete_objects['isSuccess']:
                result = {"isSuccess": True, "message": delete_objects['message'], 'count': 1, 'msg': '', 'code': 0}
            else:
                result = {"isSuccess": False, "message": '', 'count': 1, 'msg': delete_objects['message'], 'code': 1}
        except Exception as e:
            result = {"isSuccess": False, "message": '', 'count': 0, 'msg': str(e), 'code': 2}
        insert_drf_api_log(request, str(result['isSuccess']), str(result))
        return Response(result, status=status.HTTP_200_OK)

# 删除用户
class Ldap3DeleteUser(mixins.CreateModelMixin, viewsets.GenericViewSet):
    '''
    '''
    # permission_classes = (ReadOnly,)
    serializer_class = Ldap3DeleteObjectSerializers

    def create(self, request, *args, **kwargs):
        '''
        ldap3 删除用户
        '''
        try:
            # 1. 反序列化 将其他格式（字典、JSON、XML等）转换为程序中的数据，例如将JSON字符串转换为Django中的模型类对象
            serializer = self.get_serializer(data=request.data)
            # 验证数据
            serializer.is_valid(raise_exception=True)
            headers = self.get_success_headers(serializer.data)
            data = serializer.data
            delete_objects = delete_user(
                dn=data.get('dn'),
                controls=data.get('controls', None), )
            if delete_objects['isSuccess']:
                result = {"isSuccess": True, "message": delete_objects['message'], 'count': 1, 'msg': '', 'code': 0}
            else:
                result = {"isSuccess": False, "message": '', 'count': 1, 'msg': delete_objects['message'], 'code': 1}
        except Exception as e:
            result = {"isSuccess": False, "message": '', 'count': 0, 'msg': str(e), 'code': 2}
        insert_drf_api_log(request, str(result['isSuccess']), str(result))
        return Response(result, status=status.HTTP_200_OK)

# 删除组
class Ldap3DeleteGroup(mixins.CreateModelMixin, viewsets.GenericViewSet):
    '''
    '''
    # permission_classes = (ReadOnly,)
    serializer_class = Ldap3DeleteObjectSerializers

    def create(self, request, *args, **kwargs):
        '''
        ldap3 删除组
        '''
        try:
            # 1. 反序列化 将其他格式（字典、JSON、XML等）转换为程序中的数据，例如将JSON字符串转换为Django中的模型类对象
            serializer = self.get_serializer(data=request.data)
            # 验证数据
            serializer.is_valid(raise_exception=True)
            headers = self.get_success_headers(serializer.data)
            data = serializer.data
            delete_objects = delete_group(
                dn=data.get('dn'),
                controls=data.get('controls', None), )
            if delete_objects['isSuccess']:
                result = {"isSuccess": True, "message": delete_objects['message'], 'count': 1, 'msg': '', 'code': 0}
            else:
                result = {"isSuccess": False, "message": '', 'count': 1, 'msg': delete_objects['message'], 'code': 1}
        except Exception as e:
            result = {"isSuccess": False, "message": '', 'count': 0, 'msg': str(e), 'code': 2}
        insert_drf_api_log(request, str(result['isSuccess']), str(result))
        return Response(result, status=status.HTTP_200_OK)

# 删除联系人
class Ldap3DeleteContact(mixins.CreateModelMixin, viewsets.GenericViewSet):
    '''
    '''
    # permission_classes = (ReadOnly,)
    serializer_class = Ldap3DeleteObjectSerializers

    def create(self, request, *args, **kwargs):
        '''
        ldap3 删除联系人
        '''
        try:
            # 1. 反序列化 将其他格式（字典、JSON、XML等）转换为程序中的数据，例如将JSON字符串转换为Django中的模型类对象
            serializer = self.get_serializer(data=request.data)
            # 验证数据
            serializer.is_valid(raise_exception=True)
            headers = self.get_success_headers(serializer.data)
            data = serializer.data
            delete_objects = delete_contact(
                dn=data.get('dn'),
                controls=data.get('controls', None), )
            if delete_objects['isSuccess']:
                result = {"isSuccess": True, "message": delete_objects['message'], 'count': 1, 'msg': '', 'code': 0}
            else:
                result = {"isSuccess": False, "message": '', 'count': 1, 'msg': delete_objects['message'], 'code': 1}
        except Exception as e:
            result = {"isSuccess": False, "message": '', 'count': 0, 'msg': str(e), 'code': 2}
        insert_drf_api_log(request, str(result['isSuccess']), str(result))
        return Response(result, status=status.HTTP_200_OK)

# 删除计算机
class Ldap3DeleteComputer(mixins.CreateModelMixin, viewsets.GenericViewSet):
    '''
    '''
    # permission_classes = (ReadOnly,)
    serializer_class = Ldap3DeleteObjectSerializers

    def create(self, request, *args, **kwargs):
        '''
        ldap3 删除计算机
        '''
        try:
            # 1. 反序列化 将其他格式（字典、JSON、XML等）转换为程序中的数据，例如将JSON字符串转换为Django中的模型类对象
            serializer = self.get_serializer(data=request.data)
            # 验证数据
            serializer.is_valid(raise_exception=True)
            headers = self.get_success_headers(serializer.data)
            data = serializer.data
            delete_objects = delete_computer(
                dn=data.get('dn'),
                controls=data.get('controls', None), )
            if delete_objects['isSuccess']:
                result = {"isSuccess": True, "message": delete_objects['message'], 'count': 1, 'msg': '', 'code': 0}
            else:
                result = {"isSuccess": False, "message": '', 'count': 1, 'msg': delete_objects['message'], 'code': 1}
        except Exception as e:
            result = {"isSuccess": False, "message": '', 'count': 0, 'msg': str(e), 'code': 2}
        insert_drf_api_log(request, str(result['isSuccess']), str(result))
        return Response(result, status=status.HTTP_200_OK)

# 删除组织单位
class Ldap3DeleteOU(mixins.CreateModelMixin, viewsets.GenericViewSet):
    '''
    '''
    # permission_classes = (ReadOnly,)
    serializer_class = Ldap3DeleteObjectSerializers

    def create(self, request, *args, **kwargs):
        '''
        * ldap3 删除组织单位
             - controls  [("1.2.840.113556.1.4.805", False, None)],重要,特殊的附加值，用来删除OU下所有对象
        '''
        try:
            # 1. 反序列化 将其他格式（字典、JSON、XML等）转换为程序中的数据，例如将JSON字符串转换为Django中的模型类对象
            serializer = self.get_serializer(data=request.data)
            # 验证数据
            serializer.is_valid(raise_exception=True)
            headers = self.get_success_headers(serializer.data)
            data = serializer.data
            delete_objects = delete_ou(
                dn=data.get('dn'),
                controls=data.get('controls', None), )
            if delete_objects['isSuccess']:
                result = {"isSuccess": True, "message": delete_objects['message'], 'count': 1, 'msg': '', 'code': 0}
            else:
                result = {"isSuccess": False, "message": '', 'count': 1, 'msg': delete_objects['message'], 'code': 1}
        except Exception as e:
            result = {"isSuccess": False, "message": '', 'count': 0, 'msg': str(e), 'code': 2}
        insert_drf_api_log(request, str(result['isSuccess']), str(result))
        return Response(result, status=status.HTTP_200_OK)

#Ldap3inspectObjectSerializers 判断容器或OU内是否有对象
class Ldap3inspectObject(mixins.CreateModelMixin, viewsets.GenericViewSet):
    '''
    '''
    # permission_classes = (ReadOnly,)
    serializer_class = Ldap3inspectObjectSerializers

    def create(self, request, *args, **kwargs):
        '''
        ldap3 判断容器或OU内是否有对象
        '''
        try:
            # 1. 反序列化 将其他格式（字典、JSON、XML等）转换为程序中的数据，例如将JSON字符串转换为Django中的模型类对象
            serializer = self.get_serializer(data=request.data)
            # 验证数据
            serializer.is_valid(raise_exception=True)
            headers = self.get_success_headers(serializer.data)
            data = serializer.data
            inspect_objects = inspect_object(
                dn=data.get('dn'),
                search_scope='LEVEL',)
            if inspect_objects['isSuccess']:
                result = {"isSuccess": True, "message": inspect_objects['message'], 'count': len(inspect_objects['message']), 'msg': '', 'code': 0}
            else:
                result = {"isSuccess": False, "message": '', 'count': 1, 'msg': inspect_objects['message'], 'code': 1}
        except Exception as e:
            result = {"isSuccess": False, "message": '', 'count': 0, 'msg': str(e), 'code': 2}
        insert_drf_api_log(request, str(result['isSuccess']), str(result))
        return Response(result, status=status.HTTP_200_OK)

#Ldap3SetAccountSerializers 修改对象属性
class Ldap3SetAccount(mixins.CreateModelMixin, viewsets.GenericViewSet):
    '''
    '''
    # permission_classes = (ReadOnly,)
    serializer_class = Ldap3SetAccountSerializers

    def create(self, request, *args, **kwargs):
        '''
        * ldap3 修改对象属性
            attributesName:必须传入对应的属性值
        '''
        try:
            # 1. 反序列化 将其他格式（字典、JSON、XML等）转换为程序中的数据，例如将JSON字符串转换为Django中的模型类对象
            serializer = self.get_serializer(data=request.data)
            # 验证数据
            serializer.is_valid(raise_exception=True)
            headers = self.get_success_headers(serializer.data)
            data = serializer.data
            setAccounts = setAccount(
                distinguishedName=data.get('dn'),
                attributesName=data.get('attributesName'),
                attributesVaule=data.get('attributesVaule'))
            if setAccounts['isSuccess']:
                result = {"isSuccess": True, "message": setAccounts['message'], 'count': 1, 'msg': '', 'code': 0}
            else:
                result = {"isSuccess": False, "message": '', 'count': 1, 'msg': setAccounts['message'], 'code': 1}
        except Exception as e:
            result = {"isSuccess": False, "message": '', 'count': 0, 'msg': str(e), 'code': 2}
        insert_drf_api_log(request, str(result['isSuccess']), str(result))
        return Response(result, status=status.HTTP_200_OK)

# Ldap3SetAccountSerializers 修改对象属性Level1
class Ldap3SetAccountLevel1(mixins.CreateModelMixin, viewsets.GenericViewSet):
    '''
    '''
    permission_classes = (AdapiPermissions, AdapiPermissionsLevel,)
    serializer_class = Ldap3SetAccountSerializers

    def create(self, request, *args, **kwargs):
        '''
        * ldap3 修改对象属性
            attributesName:必须传入对应的属性值
        '''
        try:
            # 1. 反序列化 将其他格式（字典、JSON、XML等）转换为程序中的数据，例如将JSON字符串转换为Django中的模型类对象
            serializer = self.get_serializer(data=request.data)
            # 验证数据
            serializer.is_valid(raise_exception=True)
            headers = self.get_success_headers(serializer.data)
            data = serializer.data
            setAccounts = setAccount(
                distinguishedName=data.get('dn'),
                attributesName=data.get('attributesName'),
                attributesVaule=data.get('attributesVaule'))
            if setAccounts['isSuccess']:
                result = {"isSuccess": True, "message": setAccounts['message'], 'count': 1, 'msg': '', 'code': 0}
            else:
                result = {"isSuccess": False, "message": '', 'count': 1, 'msg': setAccounts['message'], 'code': 1}
        except Exception as e:
            result = {"isSuccess": False, "message": '', 'count': 0, 'msg': str(e), 'code': 2}
        insert_drf_api_log(request, str(result['isSuccess']), str(result))
        return Response(result, status=status.HTTP_200_OK)

# Ldap3SetAccountSerializers 修改对象属性Level2
class Ldap3SetAccountLevel2(mixins.CreateModelMixin, viewsets.GenericViewSet):
    '''
    '''
    permission_classes = (AdapiPermissions, AdapiPermissionsLevel,)
    serializer_class = Ldap3SetAccountSerializers

    def create(self, request, *args, **kwargs):
        '''
        * ldap3 修改对象属性
            attributesName:必须传入对应的属性值
        '''
        try:
            # 1. 反序列化 将其他格式（字典、JSON、XML等）转换为程序中的数据，例如将JSON字符串转换为Django中的模型类对象
            serializer = self.get_serializer(data=request.data)
            # 验证数据
            serializer.is_valid(raise_exception=True)
            headers = self.get_success_headers(serializer.data)
            data = serializer.data
            setAccounts = setAccount(
                distinguishedName=data.get('dn'),
                attributesName=data.get('attributesName'),
                attributesVaule=data.get('attributesVaule'))
            if setAccounts['isSuccess']:
                result = {"isSuccess": True, "message": setAccounts['message'], 'count': 1, 'msg': '', 'code': 0}
            else:
                result = {"isSuccess": False, "message": '', 'count': 1, 'msg': setAccounts['message'], 'code': 1}
        except Exception as e:
            result = {"isSuccess": False, "message": '', 'count': 0, 'msg': str(e), 'code': 2}
        insert_drf_api_log(request, str(result['isSuccess']), str(result))
        return Response(result, status=status.HTTP_200_OK)

# Ldap3ResetPasswordSerializers  修改用户密码 设置 用户下次登陆时须更改密码 解锁用户的账户
class Ldap3ResetPassword(mixins.CreateModelMixin, viewsets.GenericViewSet):
    '''
    '''
    # permission_classes = (ReadOnly,)
    serializer_class = Ldap3ResetPasswordSerializers

    def create(self, request, *args, **kwargs):
        '''
        * ldap3 修改用户密码
            * pwdLastSet:用户下次登陆时须更改密码
            * unlock ： 解锁用户的账户
            * ip ：解锁用户的账户的域控,不填写则在所有站点上解锁
        '''
        try:
            # 1. 反序列化 将其他格式（字典、JSON、XML等）转换为程序中的数据，例如将JSON字符串转换为Django中的模型类对象
            serializer = self.get_serializer(data=request.data)
            # 验证数据
            serializer.is_valid(raise_exception=True)
            headers = self.get_success_headers(serializer.data)
            data = serializer.data
            resetPasswords = resetPassword(
                newpassword=data.get('newpassword'),
                distinguishedName=data.get('dn', None),
                sAMAccountName=data.get('sAMAccountName', None),
                pwdLastSet=data.get('pwdLastSet', None),
                unlock=data.get('unlock', None),
                ip=data.get('ip', None))
            if resetPasswords['isSuccess']:
                result = {"isSuccess": True, "message": resetPasswords['message'], 'count': 1, 'msg': '', 'code': 0}
            else:
                result = {"isSuccess": False, "message": '', 'count': 1, 'msg': resetPasswords['message'], 'code': 1}
        except Exception as e:
            result = {"isSuccess": False, "message": '', 'count': 0, 'msg': str(e), 'code': 2}
        insert_drf_api_log(request, str(result['isSuccess']), str(result))
        return Response(result, status=status.HTTP_200_OK)

#   判断用户是否被锁定  传入 sAMAccountName or distinguishedName
class Ldap3SerchLock(mixins.CreateModelMixin, viewsets.GenericViewSet):
    '''
    '''
    # permission_classes = (ReadOnly,)
    serializer_class = Ldap3UserSerializers

    def create(self, request, *args, **kwargs):
        '''
        * 查找用户是否被锁定
        * 逻辑
            - 1.获取服务器所有可连接的域控
            - 2.根据IP,区分服务器
            - 3.去服务器上验证用户是否锁定
        '''
        try:
            # 1. 反序列化 将其他格式（字典、JSON、XML等）转换为程序中的数据，例如将JSON字符串转换为Django中的模型类对象
            serializer = self.get_serializer(data=request.data)
            # 验证数据
            serializer.is_valid(raise_exception=True)
            headers = self.get_success_headers(serializer.data)
            data = serializer.data
            serchlocks = serchlock(
                distinguishedName=data.get('dn', None),
                sAMAccountName=data.get('sAMAccountName', None),)
            if serchlocks['isSuccess']:
                result = {"isSuccess": True, "message": serchlocks['message'], 'count': 1, 'msg': '', 'code': 0}
            else:
                result = {"isSuccess": False, "message": '', 'count': 1, 'msg': serchlocks['message'], 'code': 1}
        except Exception as e:
            result = {"isSuccess": False, "message": '', 'count': 0, 'msg': str(e), 'code': 2}
        insert_drf_api_log(request, str(result['isSuccess']), str(result))
        return Response(result, status=status.HTTP_200_OK)

# 解锁用户锁定
class Ldap3UnlockUser(mixins.CreateModelMixin, viewsets.GenericViewSet):
    '''
    '''
    # permission_classes = (ReadOnly,)
    serializer_class = Ldap3UnlockUserSerializers

    def create(self, request, *args, **kwargs):
        '''
        * 解锁用户锁定
        * 逻辑 传入IP
            - 根据IP去服务器上解锁用户
        * 逻辑 不传入IP
            - 1.获取服务器所有可连接的域控
            - 2.根据IP,区分服务器
            - 3.去服务器上解锁用户锁定
        '''
        try:
            # 1. 反序列化 将其他格式（字典、JSON、XML等）转换为程序中的数据，例如将JSON字符串转换为Django中的模型类对象
            serializer = self.get_serializer(data=request.data)
            # 验证数据
            serializer.is_valid(raise_exception=True)
            headers = self.get_success_headers(serializer.data)
            data = serializer.data
            unlockusers = unlockuser(
                distinguishedName=data.get('dn', None),
                sAMAccountName=data.get('sAMAccountName', None),
                ip=data.get('ip', None))
            if unlockusers['isSuccess']:
                result = {"isSuccess": True, "message": unlockusers['message'], 'count': 1, 'msg': '', 'code': 0}
            else:
                result = {"isSuccess": False, "message": '', 'count': 1, 'msg': unlockusers['message'], 'code': 1}
        except Exception as e:
            result = {"isSuccess": False, "message": '', 'count': 0, 'msg': str(e), 'code': 2}
        insert_drf_api_log(request, str(result['isSuccess']), str(result))
        return Response(result, status=status.HTTP_200_OK)

# 判断对象是否勾选防止对象被意外删除(P)
class Ldap3CanObject(mixins.CreateModelMixin, viewsets.GenericViewSet):
    '''
    '''
    # permission_classes = (ReadOnly,)
    serializer_class = Ldap3UserSerializers

    def create(self, request, *args, **kwargs):
        '''
        * 判断对象是否 勾选 防止对象被意外删除(P)
        * 逻辑 isSuccess ==True
            - ResultCode == 0 :已勾选防止对象被意外删除(P)
            - ResultCode == -1 :未勾选防止对象被意外删除(P)
        '''
        try:
            # 1. 反序列化 将其他格式（字典、JSON、XML等）转换为程序中的数据，例如将JSON字符串转换为Django中的模型类对象
            serializer = self.get_serializer(data=request.data)
            # 验证数据
            serializer.is_valid(raise_exception=True)
            headers = self.get_success_headers(serializer.data)
            data = serializer.data
            can_accidentally_deleteds = can_accidentally_deleted(
                distinguishedName=data.get('dn', None),
                sAMAccountName=data.get('sAMAccountName', None),)
            if can_accidentally_deleteds['isSuccess']:
                result = {"isSuccess": True, "message": can_accidentally_deleteds['message'], 'count': 1, 'msg': '', 'code': 0, 'ResultCode':can_accidentally_deleteds['ResultCode']}
            else:
                result = {"isSuccess": False, "message": '', 'count': 1, 'msg': can_accidentally_deleteds['message'], 'code': 1}
        except Exception as e:
            result = {"isSuccess": False, "message": '', 'count': 0, 'msg': str(e), 'code': 2}
        insert_drf_api_log(request, str(result['isSuccess']), str(result))
        return Response(result, status=status.HTTP_200_OK)

# 勾选防止对象被意外删除(P)
class Ldap3CheckObject(mixins.CreateModelMixin, viewsets.GenericViewSet):
    '''
    '''
    # permission_classes = (ReadOnly,)
    serializer_class = Ldap3UserSerializers

    def create(self, request, *args, **kwargs):
        '''
        * 勾选 防止对象被意外删除(P)
        * 逻辑
            - 您可以使用此过程添加以下访问控制条目（ACE）：
            - 1.在要保护的组织单位（OU）上，为Everyone组的删除和删除子树高级权限添加显式拒绝ACE。
            - 2.在要保护的OU的父容器上，为Everyone组的“删除所有子对象”权限添加显式拒绝ACE。
            - 这可以保护OU不被意外删除。当用户尝试删除受保护对象时，该操作将返回一个错误，指示访问被拒绝。
        '''
        try:
            # 1. 反序列化 将其他格式（字典、JSON、XML等）转换为程序中的数据，例如将JSON字符串转换为Django中的模型类对象
            serializer = self.get_serializer(data=request.data)
            # 验证数据
            serializer.is_valid(raise_exception=True)
            headers = self.get_success_headers(serializer.data)
            data = serializer.data
            check_accidentally_deleteds = check_accidentally_deleted(
                distinguishedName=data.get('dn', None),
                sAMAccountName=data.get('sAMAccountName', None),)
            if check_accidentally_deleteds['isSuccess']:
                result = {"isSuccess": True, "message": check_accidentally_deleteds['message'], 'count': 1, 'msg': '', 'code': 0,}
            else:
                result = {"isSuccess": False, "message": '', 'count': 1, 'msg': check_accidentally_deleteds['message'], 'code': 1}
        except Exception as e:
            result = {"isSuccess": False, "message": '', 'count': 0, 'msg': str(e), 'code': 2}
        insert_drf_api_log(request, str(result['isSuccess']), str(result))
        return Response(result, status=status.HTTP_200_OK)

# 去除勾选防止对象被意外删除(P)
class Ldap3UncheckObject(mixins.CreateModelMixin, viewsets.GenericViewSet):
    '''
    '''
    # permission_classes = (ReadOnly,)
    serializer_class = Ldap3UserSerializers

    def create(self, request, *args, **kwargs):
        '''
        * 去除勾选防止对象被意外删除(P)
        '''
        try:
            # 1. 反序列化 将其他格式（字典、JSON、XML等）转换为程序中的数据，例如将JSON字符串转换为Django中的模型类对象
            serializer = self.get_serializer(data=request.data)
            # 验证数据
            serializer.is_valid(raise_exception=True)
            headers = self.get_success_headers(serializer.data)
            data = serializer.data
            uncheck_accidentally_deleteds = uncheck_accidentally_deleted(
                distinguishedName=data.get('dn', None),
                sAMAccountName=data.get('sAMAccountName', None),)
            if uncheck_accidentally_deleteds['isSuccess']:
                result = {"isSuccess": True, "message": uncheck_accidentally_deleteds['message'], 'count': 1, 'msg': '', 'code': 0,}
            else:
                result = {"isSuccess": False, "message": '', 'count': 1, 'msg': uncheck_accidentally_deleteds['message'], 'code': 1}
        except Exception as e:
            result = {"isSuccess": False, "message": '', 'count': 0, 'msg': str(e), 'code': 2}
        insert_drf_api_log(request, str(result['isSuccess']), str(result))
        return Response(result, status=status.HTTP_200_OK)

# 批量添加用户(组)到组
class Ldap3AddMembers(mixins.CreateModelMixin, viewsets.GenericViewSet):
    '''
    '''
    # permission_classes = (ReadOnly,)
    serializer_class = Ldap3Group

    def create(self, request, *args, **kwargs):
        '''
        * 批量添加用户(组)到组
        '''
        try:
            # 1. 反序列化 将其他格式（字典、JSON、XML等）转换为程序中的数据，例如将JSON字符串转换为Django中的模型类对象
            serializer = self.get_serializer(data=request.data)
            # 验证数据
            serializer.is_valid(raise_exception=True)
            headers = self.get_success_headers(serializer.data)
            data = serializer.data
            with ldap3RESTARTABLE as conn:
                add_members_to_groups = conn.extend.microsoft.add_members_to_groups(members=data.get('members',''), groups=data.get('groups',''))
                result_id = conn.result
                response_id = conn.response
                if add_members_to_groups:
                    result = {"isSuccess": True, "message": '添加成功', 'count': 1, 'msg': str(result_id['description']), 'code': 0}
                else:
                    result = {"isSuccess": False, "message": '', 'count': 1, 'msg': str(result_id['description']), 'code': 1}
        except Exception as e:
            result = {"isSuccess": False, "message": '', 'count': 0, 'msg': str(e), 'code': 2}
        insert_drf_api_log(request, str(result['isSuccess']), str(result))
        return Response(result, status=status.HTTP_200_OK)

# 批量删除用户(组)到组
class Ldap3ReMembers(mixins.CreateModelMixin, viewsets.GenericViewSet):
    '''
    '''
    # permission_classes = (ReadOnly,)
    serializer_class = Ldap3Group

    def create(self, request, *args, **kwargs):
        '''
        * 批量删除用户(组)到组
        '''
        try:
            # 1. 反序列化 将其他格式（字典、JSON、XML等）转换为程序中的数据，例如将JSON字符串转换为Django中的模型类对象
            serializer = self.get_serializer(data=request.data)
            # 验证数据
            serializer.is_valid(raise_exception=True)
            headers = self.get_success_headers(serializer.data)
            data = serializer.data
            with ldap3RESTARTABLE as conn:
                remove_members_to_groups = conn.extend.microsoft.remove_members_from_groups(members=data.get('members',''), groups=data.get('groups',''))
                result_id = conn.result
                response_id = conn.response
                if remove_members_to_groups:
                    result = {"isSuccess": True, "message": '删除成功', 'count': 1, 'msg': str(result_id['description']), 'code': 0}
                else:
                    result = {"isSuccess": False, "message": '', 'count': 1, 'msg': str(result_id['description']), 'code': 1}
        except Exception as e:
            result = {"isSuccess": False, "message": '', 'count': 0, 'msg': str(e), 'code': 2}
        insert_drf_api_log(request, str(result['isSuccess']), str(result))
        return Response(result, status=status.HTTP_200_OK)

# 获取用户信息
class Ldap3GetUser(mixins.CreateModelMixin, viewsets.GenericViewSet):
    '''
    '''
    serializer_class = Ldap3GetUserSerializers

    def create(self, request, *args, **kwargs):
        '''
        * 获取用户信息
        '''
        try:
            # 1. 反序列化 将其他格式（字典、JSON、XML等）转换为程序中的数据，例如将JSON字符串转换为Django中的模型类对象
            serializer = self.get_serializer(data=request.data)
            # 验证数据
            serializer.is_valid(raise_exception=True)
            headers = self.get_success_headers(serializer.data)
            data = serializer.data
            jobnumber = data.get('jobnumber', '')
            sAMAccountName = data.get('sAMAccountName', '')
            result = get_users(sAMAccountName=sAMAccountName, jobnumber=jobnumber)
        except Exception as e:
            result = {"isSuccess": False, "message": '', 'count': 0, 'msg': str(e), 'code': 2}
        insert_drf_api_log(request, str(result['isSuccess']), str(result))
        return Response(result, status=status.HTTP_200_OK)