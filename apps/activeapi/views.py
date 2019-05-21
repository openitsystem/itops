# -*- coding: utf-8 -*-
# @Time    : 2018/11/27 11:57
# @Author  : 
from ldap3 import Server, Connection, ALL, MODIFY_DELETE, MODIFY_REPLACE, MODIFY_ADD, MODIFY_INCREMENT, ObjectDef, AttrDef, Reader, Writer, SEQUENCE_TYPES, REUSABLE, RESTARTABLE

import datetime

from ldap3.protocol.microsoft import security_descriptor_control

from ADapi.views import repeace, UserToExc, NewMailContact
from apps.activeapi.th_creat_mail import UserCreatMail
from apps.securitytab import ldaptypes
from dbinfo.encrypt_decode import encrypt_and_decode
from dbinfo.views import getldap3configtion
from itops.settings import ldap3RESTARTABLE, ladp3search_base

# ldap3 测试
class AdLdap(object):
    def __init__(self):
        self.ip = ''
        self.user = ''
        self.password = ''
        self.base = 'DC=,DC='
        self.domain = ''
        self.mail_suffix = '@'
        self.ad_prefix = self.base.split(',')[0].replace(
            'DC=', '').replace('dc=', '') + '\\'
        self.conn = ldap3RESTARTABLE

    def search(self,
               search_filter,
               search_base=None,
               search_scope='SUBTREE',
               attributes=None,
               size_limit=0,
               time_limit=0):
        '''
        执行ldap搜索
        :param search_filter: 必填项，ldap的搜索语句
        :param search_base:
        :param search_scope:
        :param attributes:
        :param size_limit:
        :param time_limit:
        :return:
        '''
        try:
            if search_base is None:
                search_base = self.base
            operation_id = self.conn.search(
                search_base=search_base,
                search_filter=search_filter,
                search_scope=search_scope,
                attributes=attributes,
                size_limit=size_limit,
                time_limit=time_limit)
            response_id, result_id = self.conn.get_response(operation_id)
            if result_id.get('result', '') == 0:
                result = {'isSuccess': True, "message": response_id}
            else:
                result = {'isSuccess': False, "message": result_id}
        except Exception as e:
            result = {'isSuccess': False, "message": str(e)}
        return result

    def add(self, dn,
            object_class=None,
            attributes=None, ):
        '''
        新建对象
        print(AdLdap().add(dn="CN=s636,OU=LYUsers,DC=,DC=com",object_class='user',attributes={'givenName': 'Beatrix', 'sn': 'Young', 'departmentNumber': 'DEV', 'telephoneNumber': 1111}))
        :param dn:
        :param object_class: None,类名,列表,class name
        :param attributes:
        :return:
        '''
        try:
            operation_id = self.conn.add(
                dn=dn,
                object_class=object_class,
                attributes=attributes, )
            response_id, result_id = self.conn.get_response(operation_id)
            if result_id.get('result', '') == 0:
                result = {'isSuccess': True, "message": result_id}
            else:
                result = {'isSuccess': False, "message": result_id}
        except Exception as e:
            result = {'isSuccess': False, "message": str(e)}
        return result

    def delete(self, dn):
        '''
        删除对象
        print(AdLdap().delete(dn="CN=s636,OU=LYUsers,DC=,DC=com"))
        :param dn:
        :return:
        '''
        try:
            operation_id = self.conn.delete(dn=dn)
            response_id, result_id = self.conn.get_response(operation_id)
            if result_id.get('result', '') == 0:
                result = {'isSuccess': True, "message": result_id}
            else:
                result = {'isSuccess': False, "message": result_id}
        except Exception as e:
            result = {'isSuccess': False, "message": str(e)}
        return result

    def modify(self, dn, changes):
        '''
        修改对象(条目)的属性
        print(AdLdap().modify(dn="CN=,OU=,DC=,DC=com",changes={'sn': [(MODIFY_REPLACE, ['Young1'])], 'givenname': [(MODIFY_REPLACE, ['Young1'])]}))
        MODIFY_REPLACE
        MODIFY_ADD
        MODIFY_DELETE
        MODIFY_INCREMENT
        :param dn:
        :param changes:
        :return:
        '''
        try:

            operation_id = self.conn.modify(dn=dn, changes=changes)
            response_id, result_id = self.conn.get_response(operation_id)
            if result_id.get('result', '') == 0:
                result = {'isSuccess': True, "message": result_id}
            else:
                result = {'isSuccess': False, "message": result_id}
        except Exception as e:
            result = {'isSuccess': False, "message": str(e)}
        return result

    def modify_attributes(
            self,
            dn,
            PropertyName,
            PropertyValue,
            modify_object='MODIFY_REPLACE'):
        '''
        替换对象的属性
        print(AdLdap().modify_attributes(dn="CN=s6363,OU=LYUsers,DC=,DC=com",PropertyName='sn',PropertyValue='姓名'))
        :param dn:
        :param PropertyName:
        :param PropertyValue:
        :param modify_object:
        :return:
        '''
        try:
            operation_id = self.conn.modify(dn, {
                PropertyName: [
                    (modify_object, [PropertyValue])]})
            response_id, result_id = self.conn.get_response(operation_id)
            if result_id.get('result', '') == 0:
                result = {'isSuccess': True, "message": result_id}
            else:
                result = {'isSuccess': False, "message": result_id}
        except Exception as e:
            result = {'isSuccess': False, "message": str(e)}
        return result

    def modify_dn(self, dn, relative_dn, new_superior=None):
        '''
        重命名 和 移动 都用这个方法 不能一起调用
        重命名  print(AdLdap().modify_dn(dn="CN=s6363,OU=LYUsers,DC=,DC=com",relative_dn='cn=63631')) 重命名方法可以异步
        移动方法必须同步
        :param dn:
        :param relative_dn: 格式 "cn=xxx" "ou=XXX"
        :param new_superior:  new_superior='ou=ldap3-tutorial,dc=demo1,dc=freeipa,dc=org'
        :return:
        '''
        try:
            operation_id = self.conn.modify_dn(
                dn=dn,
                relative_dn=relative_dn,
                delete_old_dn=True,
                new_superior=new_superior)
            response_id, result_id = self.conn.get_response(operation_id)
            if result_id.get('result', '') == 0:
                result = {'isSuccess': True, "message": result_id}
            else:
                result = {'isSuccess': False, "message": result_id}
        except Exception as e:
            result = {'isSuccess': False, "message": str(e)}
        return result

#获取域的根结点数据,用来生成AD树
def get_domainbase():
    '''
    获取域的根结点数据,用来生成tree
    :return:
    '''
    try:
        ldap3configtion = getldap3configtion()
        icon = "/static/zTreeStyle/img/ou02.png"
        if ldap3configtion:
            ladp3search_domain = ldap3configtion['domain'].split('.')[0]

            message = {
                'name': ldap3configtion['domain'],
                'objectClass': 'domain',
                'distinguishedName': ldap3configtion['search_base'],
                "icon": icon,
                'pid': 0,
                'isParent': True,
                'id': 1,
                'upn': '@'+ldap3configtion['domain'],
                'domain': ladp3search_domain+'\\',
            }
        else:
            message ={
                'name': '没有找到domain数据',
                'objectClass': 'domain',
                'distinguishedName': '',
                "icon": icon,
                'pid': 0,
                'isParent': True,
                'id': 1,
                'upn': '',
                'domain': '',
            }
        return {'isSuccess': True, 'message': message}
    except Exception as e:
        return {'isSuccess': False, 'message': str(e)}

#根据distinguishedName 来获取下面移除OU ,用来生成AD树
def get_ou_for_dn(distinguishedName, treeid):
    '''
    根据distinguishedName 来获取下面移除OU ,用来生成AD树
    :param distinguishedName:
    :param treeid:
    :return:
    '''
    try:
        with ldap3RESTARTABLE as conn:
            ou_list = []
            operation_id = conn.search(
                search_base=distinguishedName,
                search_filter="(|(objectClass=organizationalUnit)(objectClass=container)(objectClass=connectionPoint))",
                search_scope="LEVEL",
                attributes=[
                    'name',
                    'objectClass',
                    'ou',
                    'cn'])
            response_id = conn.response
            result_id = conn.result
            if result_id.get('result', '') == 0:
                s = 1
                for response in response_id:
                    ou_attributes = response.get('attributes', '')
                    if ou_attributes:
                        if 'organizationalUnit' in ou_attributes['objectClass']:
                            icon = "/static/zTreeStyle/img/ou.png"
                        else:
                            icon = "/static/zTreeStyle/img/ou01.png"
                        ids = str(treeid) + str(s)
                        ou = {
                            "id": int(ids),
                            "pid": int(treeid),
                            "ou": ou_attributes['ou'],
                            "cn": ou_attributes['cn'],
                            "name": ou_attributes['name'],
                            "objectClass": ou_attributes['objectClass'],
                            "distinguishedName": response['dn'],
                            "isParent": True,
                            "icon": icon,
                        }
                        s = s + 1
                        ou_list.append(ou)
                result = {"isSuccess": True, "message": ou_list}
            else:
                result = {"isSuccess": False, "message": str(result_id['description'])}
    except Exception as e:
        result = {"isSuccess": False, "message": str(e)}
    return result


def get_object_for_dn(distinguishedName):
    try:
        with ldap3RESTARTABLE as conn:
            conn.search(
                search_base=distinguishedName,
                search_filter="(objectClass=*)",
                search_scope='BASE',)
            object_list = []
            total_entries = 0
            entry_generator = conn.extend.standard.paged_search(
                search_base=distinguishedName,
                search_filter="(objectClass=*)",
                search_scope="LEVEL",
                attributes=[
                    'ou',
                    'cn',
                    'name',
                    'sn',
                    'givenName',
                    'sAMAccountName',
                    'userPrincipalName',
                    'displayName',
                    'wWWHomePage',
                    'description',
                    'physicalDeliveryOfficeName',
                    'mail',
                    'distinguishedName',
                    'memberof',
                    'proxyAddresses',
                    'userAccountControl',
                    'objectClass',
                    'groupType',
                    'lockoutTime'], paged_size=1000, generator=True)
            result_id = conn.result
            if result_id.get('result', '') == 0:
                for entry in entry_generator:
                    total_entries += 1
                    object_attributes = entry.get('attributes', '')
                    if object_attributes:
                        objectClassFroms = objectClassFrom(object_attributes['objectClass'], object_attributes['groupType'], object_attributes['userAccountControl'])
                        object_attributes.update(objectClassFroms)
                        object_list.append(dict(object_attributes))
                result = {"isSuccess": True, "message": object_list,'count':total_entries}
            else:
                result = {"isSuccess": False, "message": str(result_id['description'])}
    except Exception as e:
        print(e)
        result = {"isSuccess": False, "message": str(e)}
    return result

#需要添加分页
def getObjectToDn(distinguishedName, search_scope):
    try:
        total_entries = 0
        response_id =[]
        with ldap3RESTARTABLE as conn:
            entry_generator = conn.extend.standard.paged_search(
                search_base=distinguishedName,
                search_filter="(objectClass=*)",
                search_scope=search_scope,
                attributes=[
                    'ou',
                    'cn',
                    'name',
                    'sn',
                    'givenName',
                    'sAMAccountName',
                    'userPrincipalName',
                    'displayName',
                    'wWWHomePage',
                    'description',
                    'physicalDeliveryOfficeName',
                    'mail',
                    'distinguishedName',
                    'memberof',
                    'proxyAddresses',
                    'userAccountControl',
                    'objectClass',
                    'groupType'], paged_size=1000, generator=True)
            for entry in entry_generator:
                total_entries += 1
                response_id.append(entry.get('attributes',''))
            result_id = conn.result
            if result_id.get('result', '') in [0, 4]:
                result = {"isSuccess": True, "message": response_id,'count':total_entries}
            else:
                result = {"isSuccess": False, "message": str(result_id['description'])}
    except Exception as e:
        result = {"isSuccess": False, "message": str(e)}
    return result


def set_rename_object(
        distinguishedName,
        cn,
        sn,
        givenName,
        displayName,
        userPrincipalName,
        sAMAccountName,
        objectClass):
    try:
        if distinguishedName and objectClass:
            with ldap3RESTARTABLE as conn:
                if ["top", "organizationalUnit"] == objectClass:
                    operation_id_ou = conn.modify_dn(
                        dn=distinguishedName,
                        relative_dn='OU=' + cn, )
                    if operation_id_ou:
                        result = {"isSuccess": True, "message": "OU重命名为：" + cn}
                    else:
                        result = {"isSuccess": False, "message": "OU重命名失败"}
                elif ["top", "container"] == objectClass:
                    operation_id_container = conn.modify_dn(
                        dn=distinguishedName,
                        relative_dn='CN=' + cn, )
                    if operation_id_container:
                        result = {"isSuccess": True, "message": "容器重命名为：" + cn}
                    else:
                        result = {"isSuccess": False, "message": "容器重命名失败"}
                elif ["top", "group"] == objectClass:
                    operation_modify_group = conn.modify(
                        dn=distinguishedName, changes={
                            'sAMAccountName': [
                                (MODIFY_REPLACE, [sAMAccountName])]}, )
                    if operation_modify_group:
                        operation_id_group = conn.modify_dn(
                            dn=distinguishedName,
                            relative_dn='CN=' + cn, )
                        if operation_id_group:
                            result = {
                                "isSuccess": True,
                                "message": '组,sAMAccountName：修改成功,重命名成功'}
                        else:
                            result = {
                                "isSuccess": False,
                                "message": '组,sAMAccountName：修改成功,重命名失败'}
                    else:
                        result = {
                            "isSuccess": False,
                            "message": 'sAMAccountName：修改失败'}
                elif ["top", "person", "organizationalPerson", "user"] == objectClass:
                    changes = {
                        'sAMAccountName': [
                            (MODIFY_REPLACE, [sAMAccountName])]}
                    if userPrincipalName:
                        changes.update(
                            {'userPrincipalName': [(MODIFY_REPLACE, [userPrincipalName])]})
                    else:
                        changes.update(
                            {'userPrincipalName': [(MODIFY_REPLACE, [])]})
                    if sn:
                        changes.update({'sn': [(MODIFY_REPLACE, [sn])]})
                    else:
                        changes.update({'sn': [(MODIFY_REPLACE, [])]})
                    if givenName:
                        changes.update(
                            {'givenName': [(MODIFY_REPLACE, [givenName])]})
                    else:
                        changes.update({'givenName': [(MODIFY_REPLACE, [])]})
                    if displayName:
                        changes.update(
                            {'displayName': [(MODIFY_REPLACE, [displayName])]})
                    else:
                        changes.update({'displayName': [(MODIFY_REPLACE, [])]})
                    operation_modify_user = conn.modify(
                        dn=distinguishedName, changes=changes)
                    if operation_modify_user:
                        operation_id_user = conn.modify_dn(
                            dn=distinguishedName,
                            relative_dn='CN=' + cn, )
                        if operation_id_user:
                            result = {
                                "isSuccess": True,
                                "message": '用户,属性：修改成功,重命名成功'}
                        else:
                            result = {
                                "isSuccess": False,
                                "message": '用户,属性：修改成功,重命名失败'}
                    else:
                        result = {
                            "isSuccess": False,
                            "message": 'sAMAccountName：修改失败'}

                elif ["top", "person", "organizationalPerson", "contact"] == objectClass:
                    changes = {}
                    if sn:
                        changes.update({'sn': [(MODIFY_REPLACE, [sn])]})
                    else:
                        changes.update({'sn': [(MODIFY_REPLACE, [])]})
                    if givenName:
                        changes.update(
                            {'givenName': [(MODIFY_REPLACE, [givenName])]})
                    else:
                        changes.update({'givenName': [(MODIFY_REPLACE, [])]})
                    if displayName:
                        changes.update(
                            {'displayName': [(MODIFY_REPLACE, [displayName])]})
                    else:
                        changes.update({'displayName': [(MODIFY_REPLACE, [])]})
                    operation_modify_contact = conn.modify(
                        dn=distinguishedName, changes=changes)
                    if operation_modify_contact:
                        operation_id_contact = conn.modify_dn(
                            dn=distinguishedName,
                            relative_dn='CN=' + cn, )
                        if operation_id_contact:
                            result = {
                                "isSuccess": True,
                                "message": '联系人,属性：修改成功,重命名成功'}
                        else:
                            result = {
                                "isSuccess": False,
                                "message": '联系人,属性：修改成功,重命名失败'}
                    else:
                        result = {
                            "isSuccess": False,
                            "message": 'sAMAccountName：修改失败'}
    except Exception as e:
        result = {"isSuccess": False, "message": str(e)}
    return result


def rename_object(sAMAccountName, newName, objectClass=None):
    try:
        with ldap3RESTARTABLE as conn:
            sAMAccountName_repeace = repeace(sAMAccountName)
            conn.search(search_base=ladp3search_base,
                        search_filter='(sAMAccountName=' + sAMAccountName_repeace + ")")
            response = conn.response[0]
            dn = response.get('dn', '')
            if dn:
                if objectClass == ["top", "organizationalUnit"]:
                    cn = "OU=" + newName
                else:
                    cn = "CN=" + newName
                if conn.modify_dn(dn, cn):
                    result = {
                        "isSuccess": True,
                        "message": sAMAccountName +
                                   ',重命名成功'}
                else:
                    result = {
                        "isSuccess": False,
                        "message": sAMAccountName +
                                   ',重命名失败'}
            else:
                result = {
                    "isSuccess": False,
                    "message": sAMAccountName +
                               ',重命名失败，没有获取到数据'}
    except Exception as e:
        result = {"isSuccess": False, "message": str(e)}
    return result


# 新建用户 是否启用 是否新建邮箱 544 546
def newUser(
        distinguishedName,
        cn,
        sn=None,
        givenName=None,
        displayName=None,
        userPrincipalName=None,
        sAMAccountName=None,
        password=None,
        userAccountControl=None,
        mail=None, maildb=None, attributes={}):
    '''

    :param distinguishedName: 这个是父OU 的dn
    :param cn:
    :param sn:
    :param givenName:
    :param displayName:
    :param userPrincipalName:
    :param sAMAccountName:
    :param objectClass:
    :return:
    '''
    try:
        if distinguishedName and cn and sAMAccountName:
            newdistinguishedName = "CN=" + cn + "," + distinguishedName
            if sn:
                attributes.update({'sn': sn})
            if givenName:
                attributes.update({'givenName': givenName})
            if displayName:
                attributes.update({'displayName': displayName})
            if userPrincipalName:
                attributes.update({'userPrincipalName': userPrincipalName})
            if sAMAccountName:
                attributes.update({'sAMAccountName': sAMAccountName})
            if userAccountControl:
                attributes.update({'userAccountControl': userAccountControl})
            with ldap3RESTARTABLE as conn:
                newuser = conn.add(
                    dn=newdistinguishedName,
                    object_class=[
                        "top",
                        "person",
                        "organizationalPerson",
                        "user"],
                    attributes=attributes)
                description = conn.result.get('description', '')
                if newuser:
                    if mail == 'yes' and maildb:
                        UserCreatMail(sAMAccountName, maildb)
                    if password:
                        modify_password = conn.extend.microsoft.modify_password(newdistinguishedName, password)
                        result_description = conn.result.get('description', '')
                        if modify_password and mail == 'yes':
                            result = {
                                "isSuccess": True,
                                "message": cn + ",用户新建成功并开始创建邮箱"}
                        elif modify_password:
                            result = {
                                "isSuccess": True,
                                "message": cn + ",用户新建成功"}
                        else:
                            result = {
                                "isSuccess": True,
                                "message": cn + ",用户新建成功,但设置密码失败："+result_description}
                    else:
                        result = {
                            "isSuccess": True,
                            "message": cn + ",用户新建成功,但没有设置密码"}
                else:
                    result = {"isSuccess": False, "message": cn + ",用户新建失败:"+description}
        else:
            result = {"isSuccess": False, "message": 'distinguishedName,cn,sAMAccountName,不能传入空值'}
    except Exception as e:
        result = {"isSuccess": False, "message": str(e)}
    return result


# 新建计算机
def newComputer(distinguishedName, cn, userAccountControl=4128, attributes={}):
    try:
        if distinguishedName and cn:
            newdistinguishedName = "CN=" + cn + "," + distinguishedName
            attributes.update({
                'sAMAccountName': cn.upper() + "$",
                'userAccountControl': userAccountControl})
            with ldap3RESTARTABLE as conn:
                newuser = conn.add(
                    dn=newdistinguishedName,
                    object_class=[
                        "top", "person", "organizationalPerson", "user", "computer"],
                    attributes=attributes)
                description = conn.result.get('description', '')
                if newuser:
                    result = {"isSuccess": True, "message": cn + ",计算机新建成功"}
                else:
                    result = {"isSuccess": False, "message": cn + ",计算机新建失败:"+description}
        else:
            result = {"isSuccess": False, "message": 'distinguishedName,cn,不能传入空值'}
    except Exception as e:
        result = {"isSuccess": False, "message": str(e)}
    return result


# 新建联系人
def newContact(distinguishedName, cn, sn=None, givenName=None, displayName=None,description=None,mail=None,name=None,smtpvalue=None,attributes = {}):
    try:
        if distinguishedName and cn:
            if mail == 'yes':
                if name and smtpvalue:
                    NewMailContacts = NewMailContact(name=name, dName=cn, smtpvalue=smtpvalue, ou=distinguishedName)
                    if NewMailContacts['isSuccess']:
                        with ldap3RESTARTABLE as conn:
                            newdistinguishedName = "CN=" + cn + "," + distinguishedName
                            if sn:
                                modify_sn = conn.modify(dn=newdistinguishedName, changes={'sn': [(MODIFY_REPLACE, [sn])]})
                            if givenName:
                                modify_givenName = conn.modify(dn=newdistinguishedName, changes={'givenName': [(MODIFY_REPLACE, [givenName])]})
                            if displayName:
                                modify_displayName = conn.modify(dn=newdistinguishedName, changes={'displayName': [(MODIFY_REPLACE, [displayName])]})
                            if description:
                                modify_description = conn.modify(dn=newdistinguishedName, changes={'description': [(MODIFY_REPLACE, [description])]})
                            result_description = conn.result.get('description', '')
                            result = {"isSuccess": True, "message": cn + ",联系人新建成功,并创建邮箱，修改属性:"+result_description}
                    else:
                        result = {"isSuccess": False, "message": cn + ",联系人新建失败:"+str(NewMailContacts['message'])}
                else:
                    result = {"isSuccess": False, "message": 'name,smtpvalue传入值为空'}
            else:
                if sn:
                    attributes.update({'sn': sn})
                if givenName:
                    attributes.update({'givenName': givenName})
                if displayName:
                    attributes.update({'displayName': displayName})
                if description:
                    attributes.update({'description': description})
                newdistinguishedName = "CN=" + cn + "," + distinguishedName
                with ldap3RESTARTABLE as conn:
                    newuser = conn.add(
                        dn=newdistinguishedName,
                        object_class=[
                            "top", "person", "organizationalPerson", "contact"],
                        attributes=attributes)
                    result_description = conn.result.get('description', '')
                    if newuser:
                        result = {"isSuccess": True, "message": cn + ",联系人新建成功"}
                    else:
                        result = {"isSuccess": False, "message": cn + ",联系人新建失败:"+result_description}
        else:
            result = {"isSuccess": False, "message": 'distinguishedName,cn传入值为空'}
    except Exception as e:
        result = {"isSuccess": False, "message": str(e)}
    return result


# 新建组织单位 ou 未添加防止意外删除
def newOrganizationalUnit(distinguishedName, cn, prevent,attributes={}):
    try:
        if distinguishedName and cn:
            newdistinguishedName = "OU=" + cn + "," + distinguishedName
            attributes.update({'cn': cn})
            with ldap3RESTARTABLE as conn:
                newuser = conn.add(
                    dn=newdistinguishedName,
                    object_class=[
                        "top", "organizationalUnit"],
                    attributes=attributes)
                result_description = conn.result.get('description', '')
                if newuser:
                    if prevent == 'true' or prevent == 'yes':
                        set_accidentally_deleteds = check_accidentally_deleted(distinguishedName=newdistinguishedName)
                        if set_accidentally_deleteds['isSuccess']:
                            result = {"isSuccess": True, "message": cn + ",组织单位新建成功,并勾选 防止意外删除"}
                        else:
                            result = {"isSuccess": True, "message": cn + ",组织单位新建成功,勾选 防止意外删除失败"}
                    else:
                        result = {"isSuccess": True, "message": cn + ",组织单位新建成功"}
                else:
                    result = {"isSuccess": False, "message": cn + ",组织单位新建失败:"+result_description}
        else:
            result = {"isSuccess": False, "message": '传入值为空'}
    except Exception as e:
        result = {"isSuccess": False, "message": str(e)}
    return result


# 新建组 默认安全组 全局 groupType
def newGroup(distinguishedName, cn, sAMAccountName=None, groupType=None, attributes={}):
    '''
    此属性可以是零或以下一个或多个值的组合。
    值	描述
    1（0x00000001）	指定由系统创建的组。

    2（0x00000002）	指定具有全局范围的组。
    4（0x00000004）	指定具有域本地范围的组。
    8（0x00000008）	指定具有通用范围的组。

    16（0x00000010）	指定Windows Server授权管理器的APP_BASIC组。
    32（0x00000020）	指定Windows Server授权管理器的APP_QUERY组
    。
    2147483648（0x80000000）	指定安全组。如果未设置此标志，则该组是通讯组。

      -2147483646  全局 安全组
      -2147483644  本地域 安全组
      -2147483640  通用 安全组

      2            全局   通讯组
      4            本地域 通讯组
      8            通用  通讯组
    全局组不能直接修改成本地域组 ，需要经过通用组转换
    :param distinguishedName:
    :param cn:
    :param sAMAccountName:
    :param groupType:
    :param attributes:
    :return:
    '''
    try:
        if distinguishedName and cn:
            newdistinguishedName = "CN=" + cn + "," + distinguishedName
            if sAMAccountName:
                attributes.update({'sAMAccountName': sAMAccountName})
            if groupType in [-2147483646, -2147483644, -2147483640, 2, 4, 8]:
                attributes.update({'groupType': groupType})
            with ldap3RESTARTABLE as conn:
                newuser = conn.add(
                    dn=newdistinguishedName,
                    object_class=[
                        "top", "group"],
                    attributes=attributes)
                result_description = conn.result.get('description', '')
                if newuser:
                    result = {"isSuccess": True, "message": cn + ",组新建成功"}
                else:
                    result = {"isSuccess": False, "message": cn + ",组新建失败:"+result_description}
        else:
            result = {"isSuccess": False, "message": '传入值为空'}
    except Exception as e:
        result = {"isSuccess": False, "message": str(e)}
    return result


# 移动到新OU
def moveToOu(dn, new_superior):
    try:
        if dn and new_superior:
            new_superior = repeace(new_superior)
            dn = repeace(dn)
            relative_dn = dn.split(",")[0]
            with ldap3RESTARTABLE as conn:
                operation_id = conn.modify_dn(
                    dn=dn,
                    relative_dn=relative_dn,
                    delete_old_dn=True,
                    new_superior=new_superior)
                if operation_id:
                    result = {'isSuccess': True, "message": relative_dn + "移动到" + new_superior}
                else:
                    result = conn.result
                    result = {'isSuccess': False, "message": str(result['description'])}
        else:
            result = {'isSuccess': False, "message": '传入空值'}
    except Exception as e:
        result = {'isSuccess': False, "message": str(e)}
    return result


# 多dn移动到新OU
def dnMoveToOu(dns, new_superior):
    try:
        if dns and new_superior:
            if not isinstance(dns, SEQUENCE_TYPES):
                dns = [dns]
            new_superior = repeace(new_superior)
            if new_superior.split(",")[0].split("=")[0] == 'CN':
                new_superior_list = new_superior.split(",")
                new_superior_list.pop(0)
                new_superior = ','.join(new_superior_list)
            message = []
            for dn in dns:
                dn = repeace(dn)
                relative_dn = dn.split(",")[0]
                cn = relative_dn.split("=")[1]
                with ldap3RESTARTABLE as conn:
                    operation_id = conn.modify_dn(
                        dn=dn,
                        relative_dn=relative_dn,
                        delete_old_dn=True,
                        new_superior=new_superior)
                    if not operation_id:
                        message.append({'cn': cn, 'moveresult': '拒绝访问'})
            result = {'isSuccess': True, "message": message, "count": len(message)}
        else:
            result = {'isSuccess': False, "message": '传入空值'}
    except Exception as e:
        result = {'isSuccess': False, "message": str(e)}
    return result


# controls=[('1.2.840.113556.1.4.805', False, None)] # 删除对象
def delete_object(dn, controls=None):
    try:
        if dn:
            with ldap3RESTARTABLE as conn:
                delObject = conn.delete(dn=dn, controls=controls)
                relative_dn = dn.split(",")[0]
                cn = relative_dn.split("=")[1]
                delObject_result_description = conn.result.get('description', '')
                if delObject:
                    result = {'isSuccess': True, "message": cn + "删除成功"}
                else:
                    if delObject_result_description == "insufficientAccessRights":
                        result = {'isSuccess': False, "message": "您没有足够的权限删除 " + cn + "，或者该对象受保护，以防止意外删除。"}
                    elif delObject_result_description == "notAllowedOnNonLeaf":
                        result = {'isSuccess': False, "message": "OU下面有子对象,无法删除"}
                    else:
                        result = {'isSuccess': False, "message": str(delObject_result_description)}
        else:
            result = {'isSuccess': False, "message": '传入空值'}
    except Exception as e:
        result = {'isSuccess': False, "message": str(e)}
    return result

# 删除用户
def delete_user(dn, controls=None):
    try:
        if dn:
            with ldap3RESTARTABLE as conn:
                conn.search(
                    search_base=ladp3search_base,
                    search_filter="(&(objectCategory=person)(objectClass=user)(distinguishedName=" + dn + "))",
                    search_scope='SUBTREE',
                )
                dn_result = conn.result
                dn_response = conn.response
                distinguishedName = dn_response[0].get('dn', '')
                relative_dn = dn.split(",")[0]
                cn = relative_dn.split("=")[1]
                if distinguishedName:
                    delObject = conn.delete(dn=dn, controls=controls)
                    if delObject:
                        result = {'isSuccess': True, "message": cn + "删除成功"}
                    else:
                        result = {'isSuccess': False, "message": "您没有足够的权限删除 " + cn + "，或者该对象受保护，以防止意外删除。"}
                else:
                    result = {'isSuccess': False, "message":  cn + "，对象不是用户，无法通过这个方法删除。"}
        else:
            result = {'isSuccess': False, "message": '传入空值'}
    except Exception as e:
        result = {'isSuccess': False, "message": str(e)}
    return result

# 删除组
def delete_group(dn, controls=None):
    try:
        if dn:
            with ldap3RESTARTABLE as conn:
                conn.search(
                    search_base=ladp3search_base,
                    search_filter="(&(objectClass=group)(distinguishedName=" + dn + "))",
                    search_scope='SUBTREE',
                )
                dn_result = conn.result
                dn_response = conn.response
                distinguishedName = dn_response[0].get('dn', '')
                relative_dn = dn.split(",")[0]
                cn = relative_dn.split("=")[1]
                if distinguishedName:
                    delObject = conn.delete(dn=dn, controls=controls)
                    if delObject:
                        result = {'isSuccess': True, "message": cn + "删除成功"}
                    else:
                        result = {'isSuccess': False, "message": "您没有足够的权限删除 " + cn + "，或者该对象受保护，以防止意外删除。"}
                else:
                    result = {'isSuccess': False, "message":  cn + "，对象不是组，无法通过这个方法删除。"}
        else:
            result = {'isSuccess': False, "message": '传入空值'}
    except Exception as e:
        result = {'isSuccess': False, "message": str(e)}
    return result

# 删除联系人
def delete_contact(dn, controls=None):
    try:
        if dn:
            with ldap3RESTARTABLE as conn:
                conn.search(
                    search_base=ladp3search_base,
                    search_filter="(&(objectClass=contact)(objectClass=person)(distinguishedName=" + dn + "))",
                    search_scope='SUBTREE',
                )
                dn_result = conn.result
                dn_response = conn.response
                distinguishedName = dn_response[0].get('dn', '')
                relative_dn = dn.split(",")[0]
                cn = relative_dn.split("=")[1]
                if distinguishedName:
                    delObject = conn.delete(dn=dn, controls=controls)
                    if delObject:
                        result = {'isSuccess': True, "message": cn + "删除成功"}
                    else:
                        result = {'isSuccess': False, "message": "您没有足够的权限删除 " + cn + "，或者该对象受保护，以防止意外删除。"}
                else:
                    result = {'isSuccess': False, "message":  cn + "，对象不是联系人，无法通过这个方法删除。"}
        else:
            result = {'isSuccess': False, "message": '传入空值'}
    except Exception as e:
        result = {'isSuccess': False, "message": str(e)}
    return result

# 删除计算机
def delete_computer(dn, controls=None):
    try:
        if dn:
            with ldap3RESTARTABLE as conn:
                conn.search(
                    search_base=ladp3search_base,
                    search_filter="(&(objectClass=computer)(distinguishedName=" + dn + "))",
                    search_scope='SUBTREE',
                )
                dn_result = conn.result
                dn_response = conn.response
                distinguishedName = dn_response[0].get('dn', '')
                relative_dn = dn.split(",")[0]
                cn = relative_dn.split("=")[1]
                if distinguishedName:
                    delObject = conn.delete(dn=dn, controls=controls)
                    if delObject:
                        result = {'isSuccess': True, "message": cn + "删除成功"}
                    else:
                        result = {'isSuccess': False, "message": "您没有足够的权限删除 " + cn + "，或者该对象受保护，以防止意外删除。"}
                else:
                    result = {'isSuccess': False, "message":  cn + "，对象不是计算机，无法通过这个方法删除。"}
        else:
            result = {'isSuccess': False, "message": '传入空值'}
    except Exception as e:
        result = {'isSuccess': False, "message": str(e)}
    return result

# 删除组织单位
def delete_ou(dn, controls=None):
    try:
        if dn:
            with ldap3RESTARTABLE as conn:
                conn.search(
                    search_base=ladp3search_base,
                    search_filter="(&(objectClass=organizationalUnit)(distinguishedName=" + dn + "))",
                    search_scope='SUBTREE',
                )
                dn_result = conn.result
                dn_response = conn.response
                distinguishedName = dn_response[0].get('dn', '')
                relative_dn = dn.split(",")[0]
                cn = relative_dn.split("=")[1]
                if distinguishedName:
                    delObject = conn.delete(dn=dn, controls=controls)
                    delObject_result_description = conn.result.get('description','')
                    if delObject:
                        result = {'isSuccess': True, "message": cn + "删除成功"}
                    else:
                        if delObject_result_description == "insufficientAccessRights":
                            result = {'isSuccess': False, "message": "您没有足够的权限删除 " + cn + "，或者该对象受保护，以防止意外删除。"}
                        elif delObject_result_description == "notAllowedOnNonLeaf":
                            result = {'isSuccess': False, "message": "OU下面有子对象,无法删除"}
                        else:
                            result = {'isSuccess': False, "message": str(delObject_result_description)}
                else:
                    result = {'isSuccess': False, "message":  cn + "，对象不是组织单位，无法通过这个方法删除。"}
        else:
            result = {'isSuccess': False, "message": '传入空值'}
    except Exception as e:
        result = {'isSuccess': False, "message": str(e)}
    return result


# 判断容器或OU内是否有对象
def inspect_object(dn, search_scope='LEVEL'):
    try:
        if dn:
            with ldap3RESTARTABLE as conn:
                conn.search(
                    search_base=dn,
                    search_filter='(objectCategory=*)',
                    search_scope=search_scope, )
                result_id = conn.result
                if result_id.get('result', '') == 0:
                    if len(conn.response) < 1:
                        result = {'isSuccess': True, 'count': 0, 'message': '没有其他用户'}
                    else:
                        attributesList = []
                        for attributes in conn.response:
                            attributesList.append(attributes['dn'])
                        result = {
                            'isSuccess': True,
                            'count': len(attributesList),
                            "message": attributesList}
                else:
                    result = {'isSuccess': False, 'count': 0, 'message': str(result_id['description'])}
        else:
            result = {'isSuccess': False, 'count': 0, "message": '传入空值'}
    except Exception as e:
        result = {'isSuccess': False, 'count': 0, "message": str(e)}
    return result


# 根据 objectClass 返回 str(类型)
def objectClassFrom(objectClass, groupType=-2147483646, userAccountControl=512):
    '''
    -2147483646  全局 安全组
      -2147483644  本地域 安全组
      -2147483640  通用 安全组

      2            全局   通讯组
      4            本地域 通讯组
      8            通用  通讯组
    :param objectClass:
    :param groupType:
    :return:
    '''
    try:
        if objectClass == ["top", "person", "organizationalPerson", "user"]:
            if userAccountControl:
                if bin(userAccountControl)[-2] == '0':
                    result = {'types': '用户', 'icon': '/static/zTreeStyle/img/user.png', 'Conte': '启用'}
                else:
                    result = {'types': '用户', 'icon': '/static/zTreeStyle/img/user2.png', 'Conte': '禁用'}
            else:
                result = {'types': '用户', 'icon': '/static/zTreeStyle/img/user.png', 'Conte': '未知'}
        elif objectClass == ["top", "group"]:
            if int(groupType) == 2:
                result = {'types': '通讯组 - 全局', 'icon': '/static/zTreeStyle/img/group.png'}
            elif int(groupType) == 4:
                result = {'types': '通讯组 - 本地域', 'icon': '/static/zTreeStyle/img/group.png'}
            elif int(groupType) == 8:
                result = {'types': '通讯组 - 通用', 'icon': '/static/zTreeStyle/img/group.png'}
            elif int(groupType) == -2147483646:
                result = {'types': '安全组 - 全局', 'icon': '/static/zTreeStyle/img/group.png'}
            elif int(groupType) == -2147483644:
                result = {'types': '安全组 - 本地域', 'icon': '/static/zTreeStyle/img/group.png'}
            elif int(groupType) == -2147483640:
                result = {'types': '安全组 - 通用', 'icon': '/static/zTreeStyle/img/group.png'}
            else:
                result = {'types': '组', 'icon': '/static/zTreeStyle/img/group.png'}
        elif objectClass == ["top", "person", "organizationalPerson", "user", "computer"]:
            if userAccountControl:
                if bin(userAccountControl)[-2] == '0':
                    result = {'types': '计算机', 'icon': '/static/zTreeStyle/img/Computer.png', 'Conte': '启用'}
                else:
                    result = {'types': '计算机', 'icon': '/static/zTreeStyle/img/computer2.png', 'Conte': '禁用'}
            else:
                result = {'types': '计算机', 'icon': '/static/zTreeStyle/img/Computer.png', 'Conte': '未知'}
        elif objectClass == ["top", "person", "organizationalPerson", "contact"]:
            result = {'types': '联系人', 'icon': '/static/zTreeStyle/img/user.png'}
        elif objectClass == ["top", "organizationalUnit"]:
            result = {'types': '组织单位', 'icon': '/static/zTreeStyle/img/ou.png'}
        elif objectClass == ["top", "container"]:
            result = {'types': '容器', 'icon': '/static/zTreeStyle/img/ou01.png'}
        else:
            result = {'types': '未知', 'icon': '/static/zTreeStyle/img/weizi.png'}
    except Exception as e:
        print(e)
        result = {'types': '未知', 'icon': '/static/zTreeStyle/img/weizi.png'}
    return result


# 修改对象属性
def setAccount(distinguishedName, attributesName, attributesVaule):
    try:
        if distinguishedName and attributesName:
            with ldap3RESTARTABLE as conn:
                if attributesVaule:
                    attributesVaule = [attributesVaule]
                else:
                    attributesVaule = []
                modify_id = conn.modify(dn=distinguishedName, changes={attributesName: [(MODIFY_REPLACE, attributesVaule)]})
                if modify_id:
                    result = {'isSuccess': True, 'message': '属性修改成功'}
                else:
                    result = {'isSuccess': False, 'message': '属性修改失败'}
        else:
            result = {'isSuccess': False, 'message': '属性修改失败：传入空值'}
    except Exception as e:
        result = {'isSuccess': False, 'message': '属性修改失败：' + str(e)}
    return result



# 修改用户密码 设置 用户下次登陆时须更改密码 解锁用户的账户
def resetPassword(newpassword, distinguishedName=None, sAMAccountName=None, pwdLastSet=None, unlock=None, ip=None):
    try:
        if (distinguishedName or sAMAccountName) and newpassword:

            with ldap3RESTARTABLE as conn:
                if sAMAccountName:
                    search_dn = conn.search(
                        search_base=ladp3search_base,
                        search_filter="(&(objectCategory=person)(objectClass=user)(sAMAccountName=" + sAMAccountName + "))",)
                    response_dn = conn.response[0].get('dn', '')
                    if response_dn and search_dn:
                        distinguishedName = response_dn
                    else:
                        return {'isSuccess': False, "message": str(sAMAccountName)+':没有查找到这个用户'}
                port = conn.server.port
                if int(port) == 636:
                    dn_name = distinguishedName.split(',')[0].split('CN=')[1]
                    if dn_name.lower() == 'administrator':
                        return {'isSuccess': False, "message": 'administrator密码不能修改'}
                    if sAMAccountName:
                        if sAMAccountName.lower() == 'administrator':
                            return {'isSuccess': False, "message": 'administrator密码不能修改'}
                    modify_password = conn.extend.microsoft.modify_password(distinguishedName, newpassword)
                    result_description = conn.result.get('description', '')
                    if modify_password:
                        if pwdLastSet:
                            modify_pwdLastSet = conn.modify(dn=distinguishedName, changes={'pwdLastSet': [(MODIFY_REPLACE, [0])]})
                        if unlock:
                            unlock_account = unlockuser(sAMAccountName=None, distinguishedName=distinguishedName, ip=ip)
                        return {'isSuccess': True, "message": '密码修改成功'}
                    else:
                        return {'isSuccess': False, "message": '密码修改失败:'+result_description}
                else:
                    return {'isSuccess': False, "message": '修改密码LDAP必须采用加密连接，端口636，现在连接的端口：'+str(port)}
        else:
            return {'isSuccess': False, "message": 'distinguishedName,sAMAccountName,newpassword,传入值为空'}
    except Exception as e:
        return {'isSuccess': False, "message": '密码修改失败：' + str(e)}


# 查找用户是否被锁定  传入 sAMAccountName or distinguishedName
def serchlock(sAMAccountName=None, distinguishedName=None):
    try:
        ldap3configtion = getldap3configtion()
        if int(ldap3configtion['use_ssl']) == 1:
            use_ssl = True
        else:
            use_ssl = False
        ldap3Server = Server(ldap3configtion['server'], get_info=ALL, use_ssl=False)
        address_info = ldap3Server.address_info
        serverIpList = []
        serverIpListser = []
        if address_info:
            for serverIp in address_info:
                if serverIp[5] != False:
                    serverIpList.append(serverIp[4][0])
                    for serverIpLists in serverIpListser:
                        if serverIpLists == serverIp[4][0].split('.')[0:3]:
                            serverIpList.remove(serverIp[4][0])
                    if serverIp[4][0].split('.')[0:3] not in serverIpListser:
                        serverIpListser.append(serverIp[4][0].split('.')[0:3])
        for serverip in serverIpList:
            with Connection(server=Server(serverip, get_info=ALL, use_ssl=use_ssl), user=ldap3configtion['user'], password=encrypt_and_decode().decrypted_text(ldap3configtion['password']),
                            auto_bind=True) as conn:
                if sAMAccountName:
                    search_userlock = conn.search(
                        search_base=ldap3configtion['search_base'],
                        search_filter="(&(objectCategory=person)(objectClass=user)(sAMAccountName=" +
                                      sAMAccountName +
                                      ")(lockoutTime>=1))",
                        attributes=[
                            'distinguishedName',
                            'sAMAccountName'])
                else:
                    search_userlock = conn.search(
                        search_base=distinguishedName,
                        search_filter="(&(objectCategory=person)(objectClass=user)(lockoutTime>=1))",
                        search_scope="BASE",
                        attributes=[
                            'distinguishedName',
                            'sAMAccountName'])
                if conn.response and search_userlock:
                    attributes = conn.response[0].get('attributes', '')
                    if attributes:
                        return {
                            'isSuccess': True, "message": {
                                'sAMAccountName': attributes.get(
                                    'sAMAccountName', ''), 'distinguishedName': attributes.get(
                                    'distinguishedName', ''), 'ip': serverip}}
        return {'isSuccess': False, "message": '账户没有被锁定,或找不到账户'}
    except Exception as e:
        return {'isSuccess': False, "message": str(e)}


# 解锁用户锁定
def unlockuser(sAMAccountName=None, distinguishedName=None, ip=None):
    try:
        ldap3configtion = getldap3configtion()
        if ldap3configtion['use_ssl'] == 1:
            use_ssl = True
        else:
            use_ssl = False
        if ip:
            serverIpList = [ip]
        else:
            ldap3Server = Server(ldap3configtion['server'], get_info=ALL, use_ssl=False)
            address_info = ldap3Server.address_info
            serverIpList = []
            serverIpListser = []
            if address_info:
                for serverIp in address_info:
                    if serverIp[5] != False:
                        serverIpList.append(serverIp[4][0])
                        for serverIpLists in serverIpListser:
                            if serverIpLists == serverIp[4][0].split('.')[0:3]:
                                serverIpList.remove(serverIp[4][0])
                        if serverIp[4][0].split('.')[0:3] not in serverIpListser:
                            serverIpListser.append(serverIp[4][0].split('.')[0:3])
        for serverip in serverIpList:
            with Connection(server=Server(serverip, get_info=ALL, use_ssl=use_ssl), user=ldap3configtion['user'], password=encrypt_and_decode().decrypted_text(ldap3configtion['password']),
                            auto_bind=True) as conn:
                if sAMAccountName:
                    search_userlock = conn.search(
                        search_base=ldap3configtion['search_base'],
                        search_filter="(&(objectCategory=person)(objectClass=user)(sAMAccountName=" +
                                      sAMAccountName +
                                      "))",
                        attributes=['distinguishedName'])
                    if conn.response and search_userlock:
                        attributes = conn.response[0].get('attributes', '')
                        if attributes:
                            unlock_account = conn.extend.microsoft.unlock_account(attributes['distinguishedName'])
                else:
                    unlock_account = conn.extend.microsoft.unlock_account(distinguishedName)
        if unlock_account == True:
            return {'isSuccess': True, "message": '解锁成功'}
        return {'isSuccess': False, "message": '账户没有被锁定,或找不到账户'}
    except Exception as e:
        return {'isSuccess': False, "message": str(e)}

#创建 防止对象被意外删除 DACL
def create_every_ace(Sid,Mask):
    '''

    :param Sid: 'S-1-1-0'
    :param Mask: 65602  65600 2
    :return:
    '''
    nace = ldaptypes.ACE()
    nace['AceFlags'] = 0
    nace['AceLen'] = 16
    nace['AceSize'] = 20
    nace['AceType'] = 1
    nace['TypeName'] = 'ACCESS_DENIED_ACE'
    acedata = ldaptypes.ACCESS_DENIED_ACE()
    acedata['Mask'] = ldaptypes.ACCESS_MASK()
    # acedata['Mask']['Mask'] = ldaptypes.ACCESS_ALLOWED_OBJECT_ACE.ADS_RIGHT_DS_CONTROL_ACCESS
    acedata['Mask']['Mask'] = Mask
    # acedata['ObjectType'] = b''
    # acedata['InheritedObjectType'] = b''
    acedata['Sid'] = ldaptypes.LDAP_SID()
    acedata['Sid'].fromCanonical(Sid)
    assert Sid == acedata['Sid'].formatCanonical()
    # acedata['Flags'] = ldaptypes.ACCESS_ALLOWED_OBJECT_ACE.ACE_OBJECT_TYPE_PRESENT
    nace['Ace'] = acedata
    return nace

# 勾选 防止对象被意外删除(P) 弃用
def set_accidentally_deleted(sAMAccountName=None, distinguishedName=None,prevent=True):
    try:
        if distinguishedName or sAMAccountName:
            # Set SD flags to only query for DACL设置SD标志仅查询DACL
            controls = security_descriptor_control(sdflags=0x04)
            with ldap3RESTARTABLE as conn:
                if distinguishedName:
                    search_dacl = conn.search(search_base=distinguishedName, search_filter='(objectClass=*)',search_scope='BASE', attributes=['nTSecurityDescriptor','distinguishedName', 'objectClass'],
                                              controls=controls)
                else:
                    search_dacl = conn.search(
                        search_base=ladp3search_base,
                        search_filter="(sAMAccountName=" +sAMAccountName +")",
                        attributes=['nTSecurityDescriptor','distinguishedName', 'objectClass'],controls=controls)
                if conn.response and search_dacl:
                    attributes = conn.response[0].get('attributes', '')
                    if attributes:
                        secDescData = attributes['nTSecurityDescriptor']
                        distinguishedName = attributes['distinguishedName']
                        objectClass = attributes['objectClass']
                        secDesc = ldaptypes.SR_SECURITY_DESCRIPTOR(data=secDescData)
                        for ace in secDesc['Dacl'].aces:
                            Sid = ace['Ace']['Sid'].formatCanonical()
                            Mask = ace['Ace']['Mask']['Mask']
                            AceFlags = ace['AceFlags']
                            if Sid == 'S-1-1-0' and (Mask in [65600, 65602] and AceFlags == 0):
                                if prevent:
                                    objectace = 65600
                                else:
                                    secDesc['Dacl']['Data'].remove(ace)
                                break
                        if prevent and objectace != 65600:
                            if objectClass == ["top", "organizationalUnit"] or objectClass == ["top", "container"]:
                                objectClassMask = 65602
                            else:
                                objectClassMask = 65600
                            everyone = create_every_ace('S-1-1-0',objectClassMask)
                            secDesc['Dacl']['Data'].insert(0,everyone)
                        data = secDesc.getData()
                        modifynt = conn.modify(distinguishedName, {'nTSecurityDescriptor': (MODIFY_REPLACE, [data])}, controls=controls)
                        if modifynt:
                            return {'isSuccess': True, "message": '修改nTSecurityDescriptor成功'}
                        else:
                            return {'isSuccess': False, "message": '修改nTSecurityDescriptor失败'}
            return {'isSuccess': False, "message": 'ldap没有查询到数据'}
        else:
            return {'isSuccess': False, "message": 'sAMAccountName或distinguishedName，必须有一个有值'}
    except Exception as e:
        return {'isSuccess': False, "message": str(e)}
# 判断 勾选 防止对象被意外删除(P)
def can_accidentally_deleted(sAMAccountName=None, distinguishedName=None):
    try:
        if distinguishedName or sAMAccountName:
            # Set SD flags to only query for DACL设置SD标志仅查询DACL
            controls = security_descriptor_control(sdflags=0x04)
            with ldap3RESTARTABLE as conn:
                if distinguishedName:
                    search_dacl = conn.search(search_base=distinguishedName, search_filter='(objectClass=*)',search_scope='BASE', attributes=['nTSecurityDescriptor','distinguishedName'],
                                        controls=controls)
                else:
                    search_dacl = conn.search(
                        search_base=ladp3search_base,
                        search_filter="(sAMAccountName=" +sAMAccountName +")",
                        attributes=['nTSecurityDescriptor','distinguishedName'],controls=controls)
                if conn.response and search_dacl:
                    attributes = conn.response[0].get('attributes', '')
                    if attributes:
                        secDescData = attributes['nTSecurityDescriptor']
                        secDesc = ldaptypes.SR_SECURITY_DESCRIPTOR(data=secDescData)
                        for ace in secDesc['Dacl'].aces:
                            Sid = ace['Ace']['Sid'].formatCanonical()
                            Mask = ace['Ace']['Mask']['Mask']
                            AceFlags = ace['AceFlags']
                            if Sid == 'S-1-1-0' and (Mask in [65600, 65602]) and AceFlags == 0:
                                return {'isSuccess': True,"ResultCode":0, "message": '已勾选防止对象被意外删除(P)'}
                    else:
                        return {'isSuccess': False, "message": 'ldap没有查询到对象'}
                else:
                    result_id = conn.result
                    return {'isSuccess': False, "message": 'ldap没有查询失败'+str(result_id['description'])}
            return {'isSuccess': True, "ResultCode": -1, "message": '未勾选防止对象被意外删除(P)'}
        else:
            return {'isSuccess': False, "message": 'sAMAccountName或distinguishedName，必须有一个有值'}
    except Exception as e:
        return {'isSuccess': False, "message": str(e)}

#勾选 防止对象被意外删除(P)
def check_accidentally_deleted(sAMAccountName=None, distinguishedName=None):
    '''
    您可以使用此过程添加以下访问控制条目（ACE）：
    1.在要保护的组织单位（OU）上，为Everyone组的删除和删除子树高级权限添加显式拒绝ACE。
    2.在要保护的OU的父容器上，为Everyone组的“删除所有子对象”权限添加显式拒绝ACE。
    这可以保护OU不被意外删除。当用户尝试删除受保护对象时，该操作将返回一个错误，指示访问被拒绝。
    :param sAMAccountName:
    :param distinguishedName:
    :return:
    '''
    try:
        objectace = 0
        objectace_fdn = 0
        if distinguishedName or sAMAccountName:
            # Set SD flags to only query for DACL设置SD标志仅查询DACL
            controls = security_descriptor_control(sdflags=0x04)
            with ldap3RESTARTABLE as conn:
                if distinguishedName:
                    search_dacl = conn.search(search_base=distinguishedName, search_filter='(objectClass=*)',search_scope='BASE', attributes=['nTSecurityDescriptor','distinguishedName', 'objectClass'],
                                              controls=controls)
                else:
                    search_dacl = conn.search(
                        search_base=ladp3search_base,
                        search_filter="(sAMAccountName=" +sAMAccountName +")",
                        attributes=['nTSecurityDescriptor','distinguishedName', 'objectClass'],controls=controls)
                if conn.response and search_dacl:
                    attributes = conn.response[0].get('attributes', '')
                    if attributes:
                        secDescData = attributes['nTSecurityDescriptor']
                        distinguishedName = attributes['distinguishedName']
                        objectClass = attributes['objectClass']
                        secDesc = ldaptypes.SR_SECURITY_DESCRIPTOR(data=secDescData)
                        for ace in secDesc['Dacl'].aces:
                            Sid = ace['Ace']['Sid'].formatCanonical()
                            Mask = ace['Ace']['Mask']['Mask']
                            AceFlags = ace['AceFlags']
                            if Sid == 'S-1-1-0' and (Mask in [65600, 65602] and AceFlags == 0):
                                objectace = 1
                                break
                        if objectace == 0:
                            if objectClass == ["top", "organizationalUnit"] or objectClass == ["top", "container"]:
                                objectClassMask = 65602
                            else:
                                objectClassMask = 65600
                            everyone = create_every_ace('S-1-1-0',objectClassMask)
                            secDesc['Dacl']['Data'].insert(0,everyone)
                            data = secDesc.getData()
                            modifynt = conn.modify(distinguishedName, {'nTSecurityDescriptor': (MODIFY_REPLACE, [data])}, controls=controls)
                            if modifynt:
                                #判断父容器OU  要保护的OU的父容器上，为Everyone组的“删除所有子对象”权限添加显式拒绝ACE。
                                distinguishedNamelist = distinguishedName.split(',')
                                dntype = distinguishedNamelist[1].split('=')[0]
                                if dntype=='OU':
                                    distinguishedNamelist.remove(distinguishedNamelist[0])
                                    fdistinguishedNamelist =','.join(distinguishedNamelist)
                                    search_fdn = conn.search(search_base=fdistinguishedNamelist, search_filter='(objectClass=*)', search_scope='BASE',
                                                              attributes=['nTSecurityDescriptor', 'distinguishedName', 'objectClass'],
                                                              controls=controls)
                                    if conn.response and search_fdn:
                                        attributes_fdn = conn.response[0].get('attributes', '')
                                        if attributes_fdn:
                                            secDescData_fdn = attributes_fdn['nTSecurityDescriptor']
                                            distinguishedName_fdn = attributes_fdn['distinguishedName']
                                            objectClass_fdn = attributes_fdn['objectClass']
                                            secDesc_fdn = ldaptypes.SR_SECURITY_DESCRIPTOR(data=secDescData_fdn)
                                            for ace_fdn in secDesc_fdn['Dacl'].aces:
                                                Sid_fdn = ace_fdn['Ace']['Sid'].formatCanonical()
                                                Mask_fdn = ace_fdn['Ace']['Mask']['Mask']
                                                AceFlags_fdn = ace_fdn['AceFlags']
                                                if Sid_fdn == 'S-1-1-0' and (Mask_fdn in [65602,2] and AceFlags_fdn == 0):
                                                    objectace_fdn = 1
                                                    break
                                            if objectace_fdn == 0:
                                                everyone_fdn = create_every_ace('S-1-1-0', 2)
                                                secDesc_fdn['Dacl']['Data'].insert(0, everyone_fdn)
                                                data_fdn = secDesc_fdn.getData()
                                                modifynt_fdn = conn.modify(distinguishedName_fdn, {'nTSecurityDescriptor': (MODIFY_REPLACE, [data_fdn])}, controls=controls)
                                                if modifynt_fdn:
                                                    result = {'isSuccess': True, "message": '勾选防止对象被意外删除(P)成功'}
                                                else:
                                                    result = {'isSuccess': True, "message": '勾选防止对象被意外删除(P),要保护的OU的父容器上，为Everyone组的“删除所有子对象”权限添加显式拒绝ACE失败'}
                                            else:
                                                result = {'isSuccess': True, "message": '勾选防止对象被意外删除(P)成功'}
                                        else:
                                            result ={'isSuccess': False, "message": 'ldap没有查询到数据'}
                                    else:
                                        result = {'isSuccess': False, "message": 'ldap没有查询到数据'}
                                else:
                                    result = {'isSuccess': True, "message": '勾选防止对象被意外删除(P)成功'}
                            else:
                                result = {'isSuccess': False, "message": '勾选防止对象被意外删除(P)失败'}
                        else:
                            result = {'isSuccess': True, "message": '已勾选防止对象被意外删除(P)'}
                    else:
                        result = {'isSuccess': False, "message": 'ldap没有查询到数据'}
                else:
                    result = {'isSuccess': False, "message": 'ldap没有查询到数据'}
        else:
            result = {'isSuccess': False, "message": 'sAMAccountName或distinguishedName，必须有一个有值'}
    except Exception as e:
        result = {'isSuccess': False, "message": str(e)}
    return result

# 去除勾选防止对象被意外删除(P)
def uncheck_accidentally_deleted(sAMAccountName=None, distinguishedName=None):
    try:
        uncheck = 0
        if distinguishedName or sAMAccountName:
            # Set SD flags to only query for DACL设置SD标志仅查询DACL
            controls = security_descriptor_control(sdflags=0x04)
            with ldap3RESTARTABLE as conn:
                if distinguishedName:
                    search_dacl = conn.search(search_base=distinguishedName, search_filter='(objectClass=*)',search_scope='BASE', attributes=['nTSecurityDescriptor','distinguishedName', 'objectClass'],
                                              controls=controls)
                else:
                    search_dacl = conn.search(
                        search_base=ladp3search_base,
                        search_filter="(sAMAccountName=" +sAMAccountName +")",
                        attributes=['nTSecurityDescriptor','distinguishedName', 'objectClass'],controls=controls)
                if conn.response and search_dacl:
                    attributes = conn.response[0].get('attributes', '')
                    if attributes:
                        secDescData = attributes['nTSecurityDescriptor']
                        distinguishedName = attributes['distinguishedName']
                        objectClass = attributes['objectClass']
                        secDesc = ldaptypes.SR_SECURITY_DESCRIPTOR(data=secDescData)
                        for ace in secDesc['Dacl'].aces:
                            Sid = ace['Ace']['Sid'].formatCanonical()
                            Mask = ace['Ace']['Mask']['Mask']
                            AceFlags = ace['AceFlags']
                            if Sid == 'S-1-1-0' and (Mask in [65600, 65602] and AceFlags == 0):
                                secDesc['Dacl']['Data'].remove(ace)
                                uncheck = 1
                                break
                        if uncheck == 1:
                            data = secDesc.getData()
                            modifynt = conn.modify(distinguishedName, {'nTSecurityDescriptor': (MODIFY_REPLACE, [data])}, controls=controls)
                            if modifynt:
                                return {'isSuccess': True, "message": '去除勾选防止对象被意外删除(P)'}
                            else:
                                return {'isSuccess': False, "message": '去除勾选防止对象被意外删除(P)失败'}
                        else:
                            return {'isSuccess': True, "message": '没有勾选防止对象被意外删除(P)'}
            return {'isSuccess': False, "message": 'ldap没有查询到数据'}
        else:
            return {'isSuccess': False, "message": 'sAMAccountName或distinguishedName，必须有一个有值'}
    except Exception as e:
        return {'isSuccess': False, "message": str(e)}

# 获取用户信息
def get_users(sAMAccountName=None,jobnumber=None):
    try:
        if sAMAccountName:
            search_filter = "(&(objectCategory=person)(objectClass=user)(sAMAccountName=" + sAMAccountName + "))"
        else:
            search_filter = "(&(objectCategory=person)(objectClass=user)(wWWHomePage=" + jobnumber + "))"
        with ldap3RESTARTABLE as conn:
            conn.search(search_base=ladp3search_base,
                        search_filter=search_filter,
                        attributes=[
                            'cn',
                            'name',
                            'sn',
                            'givenName',
                            'sAMAccountName',
                            'userPrincipalName',
                            'displayName',
                            'wWWHomePage',
                            'description',
                            'physicalDeliveryOfficeName',
                            'wWWHomePage',
                            'mail',
                            'distinguishedName',
                            'memberof',
                            'userAccountControl',
                            'accountExpires',
                            'msDS-UserPasswordExpiryTimeComputed'
                        ], )
            result_id = conn.result
            response_id = conn.response
            attributes = response_id[0].get('attributes', '')
            if attributes:
                sAMAccountName = attributes.get('sAMAccountName', '')
                mail = attributes.get('mail', '')
                wWWHomePage = attributes.get('wWWHomePage', '')
                userAccountControl = attributes.get('userAccountControl')
                memberof = attributes.get('memberof', '')
                UserPasswordExpiryTimeComputed = attributes.get('msDS-UserPasswordExpiryTimeComputed', '')
                from datetime import datetime
                accountExpires = attributes.get('accountExpires', datetime.now())
                distinguishedName = attributes.get('distinguishedName', '')
                if bin(userAccountControl)[-2] == '0':
                    AccountControl = "启用"
                else:
                    AccountControl = "禁用"
                # accountExpires  9999-12-31 23:59:59.999999 未设置账户过期
                # accountExpires 1601-01-01 00:00:00+00:00 从不过期
                # accountExpires 2019-05-17 16:00:00+00:00 账户过期时间
                accountExpires_str = accountExpires.strftime('%Y-%m-%d %H:%M:%S')
                if accountExpires_str in ['1601-01-01 00:00:00', '9999-12-31 23:59:59']:
                    Expires = '账户永不过期'
                else:
                    accountExpires = (utc2local(accountExpires)).replace(tzinfo=None)
                    accountExpires_str = accountExpires.strftime('%Y-%m-%d %H:%M:%S')
                    now = (datetime.now()).replace(tzinfo=None)
                    if accountExpires > now:
                        Expires = "账户未过期"
                    else:
                        Expires = '账户已过期'
                # 密码过期时间
                if UserPasswordExpiryTimeComputed == 9223372036854775807 or UserPasswordExpiryTimeComputed == 0:
                    Password_expiration = '密码永不过期'
                else:
                    import time
                    Password_expiration = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime((UserPasswordExpiryTimeComputed - 116444736000000000) / 10000000))
                serchlocks = serchlock(sAMAccountName=None, distinguishedName=distinguishedName)
                if serchlocks['isSuccess']:
                    Lock = '已锁定'
                    ip = serchlocks['message']['ip']
                else:
                    Lock = '未锁定'
                    ip = ''
                Mail = []
                Vpn = ['没有VPN权限']
                Internet = []
                Dfs = []
                Wifi = []
                if memberof:
                    for member in memberof:
                        if "MailGroups" in member:
                            Mail.append((member.split(',')[0].split('=')[1]))
                        if "vpn用户组" in member:
                            if (member.split(',')[0].split('=')[1]) == "vpn用户组":
                                Vpn = ['有VPN权限']
                        if "WifiUsers" in member:
                            if (member.split(',')[0].split('=')[1]) == "WifiUsers":
                                Wifi.append('苏州无线权限')
                        if "hf-wifi" in member:
                            if (member.split(',')[0].split('=')[1]) == "hf-wifi":
                                Wifi.append('合肥无线权限')
                        if "PermissionGroups" in member:
                            Internet2 = (member.split(',')[0].split('=')[1])
                            if Internet2 == "(28)Net Level 28 (IM8-L4)":
                                Internet2 = "高级上网权限"
                            if Internet2 == "(11)Net Level 11 (QQ-L3)":
                                Internet2 = "一般上网权限"
                            if Internet2 == "(91)财务上网安全组 L1":
                                Internet2 = "仅能访问财务相关网站"
                            if Internet2 == "(51)MSSQL-研发":
                                Internet2 = "研发远程端口权限"
                            Internet.append(Internet2)
                        if "ITPermissionGroups" in member:
                            Internet2 = (member.split(',')[0].split('=')[1])
                            if Internet2 == "分公司白名单组":
                                Internet2 = "分公司白名单上网权"
                            if Internet2 == "(00)公司领导":
                                Internet2 = "特殊权限"
                            Internet.append(Internet2)
                        if "DFSGroups" in member:
                            Dfs.append((member.split(',')[0].split('=')[1]))
                message = [{'MailGroups': Mail, "Vpn": Vpn, "Internet": Internet, 'Dfs': Dfs, 'Wifi': Wifi, 'Password_expiration': Password_expiration,
                            'Lock': Lock, 'ip': ip,
                            'Expires': Expires, 'accountExpires_str': accountExpires_str, 'AccountControl': AccountControl, 'sAMAccountName': sAMAccountName,
                            'mail': mail, 'wWWHomePage': wWWHomePage, 'attributes': dict(attributes)}]
                result = {"isSuccess": True, "message": message, 'count': 1, 'msg': str(result_id['description']), 'code': 0}
            else:
                result = {"isSuccess": False, "message": '', 'count': 1, 'msg': "没有查询到用户" + str(result_id['description']), 'code': 1}
    except Exception as e:
        result = {"isSuccess": False, "message": '', 'count': 0, 'msg': str(e), 'code': 2}
    return result