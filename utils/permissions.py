# -*- coding: utf-8 -*-
# @Time    : 2019/3/21 18:47
# @Author  :
from rest_framework.permissions import BasePermission
from dbinfo.views import select_apipermissions, insert_log_table_name, get_attributeslevel_apiname
import ast


class AdapiPermissions(BasePermission):
    """
    判断对应的账号是否有对应的api权限
    """
    def has_permission(self, request, view):
        try:
            apiname = request.path.split(r"/")[1]
        except Exception as e:
            apiname = request._request.split(r'/')[-2]
        ip = request.META.get('HTTP_X_FORWARDED_FOR', request.META['REMOTE_ADDR'])
        apiusername = request.user
        select_apipermission = select_apipermissions(str(apiname), str(apiusername))
        if select_apipermission:
                return True
        else:
            insert_log_table_name('log_api', str(ip), str(apiname), str(apiusername), 'False', str(request.data), '没有对应的api权限', str(request.auth))
            return False

# 修改AD,邮箱属性需要根据数据库确定 传入的值
class AdapiPermissionsLevel(BasePermission):
    """
    修改AD,邮箱属性需要根据数据库确定 传入的值 的权限
    """
    def has_permission(self, request, view):
        try:
            try:
                apiname = request.path.split(r"/")[1]
            except Exception as e:
                apiname = request._request.split(r'/')[-2]
            ip = request.META.get('HTTP_X_FORWARDED_FOR', request.META['REMOTE_ADDR'])
            apiusername = request.user
            attributes_level = get_attributeslevel_apiname(apiname)
            data = request.data
            if attributes_level:
                attributes = attributes_level[0]['attributes']
                attributesList= ast.literal_eval(attributes)
                if "SetAccount" in apiname:
                    attributesName = data.get('attributesName','')
                    if attributesName.lower() in [attributesL.lower() for attributesL in attributesList]:
                        return True
                    else:
                        insert_log_table_name('log_api', str(ip), str(apiname), str(apiusername), 'False', str(request.data), 'SetAccount 数据库没有对应的权限数据', str(request.auth))
                        return False
                else:
                    data_copy = data.copy()
                    data_copy.pop('identity')
                    data_copy_keylist = data_copy.keys()
                    for data_key in data_copy_keylist:
                        if data_key.lower() not in [attributesL.lower() for attributesL in attributesList]:
                            insert_log_table_name('log_api', str(ip), str(apiname), str(apiusername), 'False', str(request.data), str(attributes_level)+'SetAccount 数据库没有对应的权限数据', str(request.auth))
                            return False
                    return True
            else:
                insert_log_table_name('log_api', str(ip), str(apiname), str(apiusername), 'False', str(request.data), 'apiusers_attributeslevel数据库没有对应的权限数据', str(request.auth))
                return False
        except Exception as e:
            insert_log_table_name('log_api', str(ip), str(apiname), str(apiusername), 'False', str(request.data), "AdapiPermissionsLevel:修改AD,邮箱属性需要根据数据库确定 传入的值 的权限"+str(e), str(request.auth))
            return False

