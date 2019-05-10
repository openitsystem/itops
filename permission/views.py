#判断获取权限

from ldap3 import Server, Connection, ALL, NONE
from django.utils.deprecation import MiddlewareMixin  # Django 1.10.x
from django.shortcuts import render, HttpResponseRedirect,HttpResponse
from apps.ldaptime.views import utc2local
from datetime import datetime
#

# from ADapi.views import link
# class permission(object):
#     ##获取用户的隶属于组###
#     def GetUserGroup(self,username):
#         try:
#             with link() as conn:
#                     conn.search(search_base='DC=,DC=com',
#                                 search_filter="(&(objectClass=user)(objectCategory=person)(sAMAccountName = "+username+"))",
#                                 search_scope='SUBTREE',
#                                 attributes=['sAMAccountName', 'memberOf'],
#                                 )
#                     if conn.result.get('result') == 0:
#                         if conn.response[0].get('attributes').get('memberOf'):
#                             result={'isSuccess': True, "message": conn.response[0].get('attributes')}
#                         else:
#                             result = {'isSuccess': False, "message": conn.response[0].get('attributes')}
#                     else:
#                         result = {'isSuccess': False, "message": conn.result}
#         except Exception as e:
#             result = {'isSuccess': False, "message": str(e)}
#         return result
#
#     ###############获取组的DN################
#     def groupdn(self,groupname):
#          try:
#              with link() as conn:
#                  conn.search(search_base='DC=,DC=com',
#                              search_filter="(&(objectClass=group)(sAMAccountName = " + groupname + "))",
#                              search_scope='SUBTREE',
#                              attributes=['sAMAccountName','distinguishedName'],
#                              )
#                  if conn.result.get('result') == 0:
#                      if conn.response[0].get('attributes'):
#                          result={'isSuccess': True, "message": conn.response[0].get('attributes')}
#                      else:
#                          result = {'isSuccess': False, "message": conn.response[0].get('attributes')}
#                  else:
#                      result={'isSuccess': False, "message": conn.result}
#          except Exception as e:
#              result = {'isSuccess': False, "message": str(e)}
#          return result
#
#         ###判断用户的权限
#         ###account 账号
#         ### project (setpwd,organization,other,)
#         ###setpwd 修改密码，projectadmin 管理员
#     def authorization(self,account,project):
#         setpwdgroup='CCCCC'
#         organization = 'ceshi11111'
#         othergroup='IT'
#         try:
#             setpwd_groupDN=permission().groupdn(setpwdgroup).get('message').get('distinguishedName')
#             organization_groupDN=permission().groupdn(organization).get('message').get('distinguishedName')
#             other_groupDN = permission().groupdn(othergroup).get('message').get('distinguishedName')
#             if permission().GetUserGroup(account).get('isSuccess'):
#                 user_group=permission().GetUserGroup(account).get('message').get('memberOf')
#                 result = {'isSuccess': False, "message": '无权限'}
#                 if project == 'other':
#                     for i in user_group:
#                         if  i == other_groupDN:
#                             result = {'isSuccess': True, "message": '有权限'}
#                 elif project == 'setpwd':
#                     for i in user_group:
#                         if  i == other_groupDN or i == setpwd_groupDN:
#                             result = {'isSuccess': True, "message": '有权限'}
#                 elif project == 'organization':
#                     for i in user_group:
#                         if  i == other_groupDN or i == organization_groupDN:
#                             result = {'isSuccess': True, "message": '有权限'}
#             else:
#                 result = {'isSuccess': False, "message": '没有权限'}
#         except Exception as e:
#             result = {'isSuccess': False, "message": str(e)}
#         return result
from dbinfo.views import getpermsessage
from itops.settings import Identity_Exception, ldap3RESTARTABLE, ladp3search_base, ladp3search_server, \
    ladp3search_domain


# class LoginMiddleware(MiddlewareMixin):
#     def process_request(self, request):
#         sessionusername = request.session.get("username")
#         try:
#             response = self.get_response(request)
#             return response
#         except Exception as e:
#             return HttpResponseRedirect('/login/', request)


class LoginMiddleware(MiddlewareMixin):
    def process_request(self, request):
        sessionusername = request.session.get("username")
        try:
            if sessionusername:
                response = self.get_response(request)
                return response
            else:
                for i in Identity_Exception:
                    if i in request.path:
                        response = self.get_response(request)
                        return response
                request.session['returnbackurl'] = request.path
                return HttpResponseRedirect('/login/', request)
        except Exception as e:
            print(e)
            return HttpResponseRedirect('/login/', request)

# def verify_user_login(sAMAccountName, password):
#     try:
#         with Connection(server, user, password, auto_bind=True) as conn:
#             conn.search(
#                 search_base=ladp3search_base,
#                 search_filter="(&(objectCategory=person)(objectClass=user)(sAMAccountName=" +
#                               sAMAccountName +
#                               "))",
#                 attributes=[
#                     'cn',
#                     'name',
#                     'sn',
#                     'givenName',
#                     'sAMAccountName',
#                     'userPrincipalName',
#                     'displayName',
#                     'wWWHomePage',
#                     'description',
#                     'physicalDeliveryOfficeName',
#                     'mail',
#                     'distinguishedName',
#                     'memberof',
#                     'userAccountControl'])
#             attributes_user = conn.response[0].get('attributes', '')
#             if attributes_user:
#                 result = {'isSuccess': True, "message": attributes_user}
#             else:
#                 result = {'isSuccess': False, "message": '没有查询到用户属性'}
#     except Exception as e:
#         result = {'isSuccess': False, "message": 'AD账户不存在,或密码错误'}
#     return result

def verifyuser_login(sAMAccountName, password):
    try:
        with ldap3RESTARTABLE as conn:
            conn.search(
                search_base=ladp3search_base,
                search_filter="(&(objectCategory=person)(objectClass=user)(sAMAccountName=" +sAMAccountName +"))",
                search_scope='SUBTREE',
                attributes=['distinguishedName'],
            )
            result_id = conn.result
            response_id = conn.response
            if result_id['result'] == 0:
                message = response_id[0].get('attributes', '')
                if message:
                    conn.search(
                        search_base=ladp3search_base,
                        search_filter="(&(sAMAccountName=" +sAMAccountName +")(&(objectCategory=person)(objectClass=user)(!(userAccountControl:1.2.840.113556.1.4.803:=2))))",
                        search_scope='SUBTREE',
                        attributes=['distinguishedName'],
                    )
                    result_id = conn.result
                    response_id = conn.response
                    if result_id['result'] == 0:
                        message = response_id[0].get('attributes', '')
                        if message:
                            conn.search(
                                search_base=ladp3search_base,
                                search_filter="(&(sAMAccountName=" + sAMAccountName + ")(&(objectCategory=person)(objectClass=user)(lockoutTime>=1)))",
                                search_scope='SUBTREE',
                                attributes=['distinguishedName'],
                            )
                            result_id = conn.result
                            response_id = conn.response
                            if result_id['result'] == 0:
                                message = response_id[0].get('attributes', '')
                                if message:
                                    result = {'isSuccess': False, "message": '账号锁定'}
                                else:
                                    try:
                                        server = Server(ladp3search_server, get_info=ALL)
                                        user = ladp3search_domain+'\\' + sAMAccountName
                                        with Connection(server, user, password, auto_bind=True) as conn:
                                            conn.search(
                                                search_base=ladp3search_base,
                                                search_filter="(&(objectCategory=person)(objectClass=user)(sAMAccountName=" +
                                                              sAMAccountName +
                                                              "))",
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
                                                    'mail',
                                                    'distinguishedName',
                                                    # 'memberof',
                                                    'userAccountControl'])
                                            attributes_user = conn.response[0].get('attributes', '')
                                            if attributes_user:
                                                result = {'isSuccess': True, "message": attributes_user}
                                            else:
                                                result = {'isSuccess': False, "message": '没有查询到用户属性'}
                                    except Exception as e:
                                        result = {'isSuccess': False, "message": '密码错误'}
                            else:
                                result = {'isSuccess': False, "message": '账号锁定'}
                        else:
                            result = {'isSuccess': False, "message": '账号已禁用'}
                    else:
                        result = {'isSuccess': False, "message": '未查询到账号'}
                else:
                    result = {'isSuccess': False, "message": '账户不存在'}
            else:
                result = {'isSuccess': False, "message": '账户不存在'}
    except Exception as e:
        result = {'isSuccess': False, "message": '出现异常'}
    return result


def repeace(message):
    promessage=message.replace('(',r'\28').replace(')',r'\29').replace('*',r'2a')
    return promessage

# def Userperm(username,types):
#     result = {'isSuccess': True, 'message': '正常用户'}
#     return result

# def Userperm(username,types):
#     permessa = getpermsessage()
#     if permessa:
#         if types=='operate':#操作
#             GroupName=permessa.get('operagroup', "None")
#             try:
#                 CountName = repeace(username)
#                 ldap3RESTARTABLE.search(
#                     search_base=ladp3search_base,
#                     # search_filter="(&(objectCategory=group)(sAMAccountName="+GroupName+"))",
#                     search_filter="(&(objectClass=user)(memberof:1.2.840.113556.1.4.1941:=%s))" % GroupName,
#                     search_scope='SUBTREE',
#                     attributes=['member','sAMAccountName'],
#                 )
#                 result_id = ldap3RESTARTABLE.result
#                 response_id = ldap3RESTARTABLE.response
#                 if result_id['result'] == 0:
#                     message = response_id[0].get('attributes', '')
#                     if message:
#                         ldap3RESTARTABLE.search(search_base=ladp3search_base,
#                                                 search_filter="(&(objectClass=user)(objectCategory=person) (sAMAccountName=" + CountName + "))",
#                                                 attributes=['distinguishedName'])
#                         resultdn_id = ldap3RESTARTABLE.result
#                         responsedn_id = ldap3RESTARTABLE.response
#                         if resultdn_id['result'] == 0:
#                             messagedn = responsedn_id[0].get('attributes', '')
#                             if messagedn:
#                                 if messagedn['distinguishedName'] in message['member']:
#                                     result = {'isSuccess': True, 'message': '正常用户'}
#                                 else:
#                                     result = {'isSuccess': False, 'message': '权限不足'}
#                             else:
#                                 result = {'isSuccess': False, 'message': '未查询到用户信息'}
#                         else:
#                             result = {'isSuccess': False, 'message': '未查询到信息'}
#                     else:
#                         result = {'isSuccess': False, 'message': '未查询到组信息'}
#                 else:
#                     result = {'isSuccess': False, "message": result_id}
#             except Exception as e:
#                 result = {'isSuccess': False, "message": str(e)}
#             return result
#         elif types=='changepwd':#改密码
#             GroupName = permessa.get('changepwdgroup', "None")
#             try:
#                 CountName = repeace(username)
#                 ldap3RESTARTABLE.search(
#                     search_base=ladp3search_base,
#                     search_filter="(&(objectCategory=group)(sAMAccountName=" + GroupName + "))",
#                     search_scope='SUBTREE',
#                     attributes=['member'],
#                 )
#                 result_id = ldap3RESTARTABLE.result
#                 response_id = ldap3RESTARTABLE.response
#                 if result_id['result'] == 0:
#                     messageon = response_id[0].get('attributes', '')
#                     if messageon:
#                         ldap3RESTARTABLE.search(search_base=ladp3search_base,
#                                                 search_filter="(&(objectClass=user)(objectCategory=person) (sAMAccountName=" + CountName + "))",
#                                                 attributes=['distinguishedName'])
#                         resultdn_id = ldap3RESTARTABLE.result
#                         responsedn_id = ldap3RESTARTABLE.response
#                         if resultdn_id['result'] == 0:
#                             messagedn = responsedn_id[0].get('attributes', '')
#                             if messagedn:
#                                 if messagedn['distinguishedName'] in messageon['member']:
#                                     result = {'isSuccess': True, 'message': '正常用户'}
#                                 else:
#                                     ldap3RESTARTABLE.search(
#                                         search_base=ladp3search_base,
#                                         search_filter="(&(objectCategory=group)(sAMAccountName=CAOZ))",
#                                         attributes=['member']
#                                     )
#                                     result_ido = ldap3RESTARTABLE.result
#                                     response_ido = ldap3RESTARTABLE.response
#                                     if result_ido['result'] == 0:
#                                         messageto = response_ido[0].get('attributes', '')
#                                         if messageto:
#                                             if messagedn['distinguishedName'] in messageto['member']:
#                                                 result = {'isSuccess': True, 'message': '正常用户'}
#                                             else:
#                                                 result = {'isSuccess': False, 'message': '权限不足'}
#                                         else:
#                                             result = {'isSuccess': False, 'message': '未查询到信息'}
#                                     else:
#                                         result = {'isSuccess': False, 'message': '未查询到信息'}
#                             else:
#                                 result = {'isSuccess': False, 'message': '未查询到用户信息'}
#                         else:
#                             result = {'isSuccess': False, 'message': '未查询到信息'}
#                     else:
#                         result = {'isSuccess': False, 'message': '未查询到组信息'}
#                 else:
#                     result = {'isSuccess': False, "message": result_id}
#             except Exception as e:
#                 result = {'isSuccess': False, "message": str(e)}
#             return result
#         elif types=='changelw':#改栏位
#             GroupName = permessa.get('fieldgroup', "None")
#             try:
#                 CountName = repeace(username)
#                 ldap3RESTARTABLE.search(
#                     search_base=ladp3search_base,
#                     search_filter="(&(objectCategory=group)(sAMAccountName=" + GroupName + "))",
#                     search_scope='SUBTREE',
#                     attributes=['member'],
#                 )
#                 result_id = ldap3RESTARTABLE.result
#                 response_id = ldap3RESTARTABLE.response
#                 if result_id['result'] == 0:
#                     messageon = response_id[0].get('attributes', '')
#                     if messageon:
#                         ldap3RESTARTABLE.search(search_base=ladp3search_base,
#                                                 search_filter="(&(objectClass=user)(objectCategory=person) (sAMAccountName=" + CountName + "))",
#                                                 attributes=['distinguishedName'])
#                         resultdn_id = ldap3RESTARTABLE.result
#                         responsedn_id = ldap3RESTARTABLE.response
#                         if resultdn_id['result'] == 0:
#                             messagedn = responsedn_id[0].get('attributes', '')
#                             if messagedn:
#                                 if messagedn['distinguishedName'] in messageon['member']:
#                                     result = {'isSuccess': True, 'message': '正常用户'}
#                                 else:
#                                     ldap3RESTARTABLE.search(
#                                         search_base=ladp3search_base,
#                                         search_filter="(&(objectCategory=group)(sAMAccountName=CAOZ))",
#                                         attributes=['member']
#                                     )
#                                     result_ido = ldap3RESTARTABLE.result
#                                     response_ido = ldap3RESTARTABLE.response
#                                     if result_ido['result'] == 0:
#                                         messageto = response_ido[0].get('attributes', '')
#                                         if messageto:
#                                             if messagedn['distinguishedName'] in messageto['member']:
#                                                 result = {'isSuccess': True, 'message': '正常用户'}
#                                             else:
#                                                 result = {'isSuccess': False, 'message': '权限不足'}
#                                         else:
#                                             result = {'isSuccess': False, 'message': '未查询到信息'}
#                                     else:
#                                         result = {'isSuccess': False, 'message': '未查询到信息'}
#                             else:
#                                 result = {'isSuccess': False, 'message': '未查询到用户信息'}
#                         else:
#                             result = {'isSuccess': False, 'message': '未查询到信息'}
#                     else:
#                         result = {'isSuccess': False, 'message': '未查询到组信息'}
#                 else:
#                     result = {'isSuccess': False, "message": result_id}
#             except Exception as e:
#                 result = {'isSuccess': False, "message": str(e)}
#             return result
#     else:
#         result = {'isSuccess': False, "message": '权限组未配置'}
#         return result
def Userperm(username,types):
    permessa = getpermsessage()
    if permessa:
        if types=='operate':#操作
            GroupName=permessa.get('operagroup', "None")
            try:
                with ldap3RESTARTABLE as conn:
                    conn.search(
                        search_base=ladp3search_base,
                        search_filter="(&(objectCategory=group)(sAMAccountName=" + GroupName + "))",
                        search_scope='SUBTREE',
                    )
                    result_logongroup = conn.result
                    response_logongroup = conn.response
                    logongroup_dn = response_logongroup[0].get('dn', '')
                    if logongroup_dn:
                        conn.search(search_base=ladp3search_base,
                                                search_filter="(&(objectCategory=person)(objectClass=user)(memberof:1.2.840.113556.1.4.1941:=%s)(sAMAccountName=%s))" % (logongroup_dn, username),)
                        result_user = conn.result
                        response_user = conn.response
                        logonuser_dn = response_user[0].get('dn', '')
                        if logonuser_dn:
                            result = {'isSuccess': True, 'message': '正常用户'}
                        else:
                            result = {'isSuccess': False, 'message': '权限不足'}
                    else:
                        result = {'isSuccess': False, 'message': '未查询到组信息'}
            except Exception as e:
                result = {'isSuccess': False, "message": str(e)}
            return result
        elif types=='changepwd':#改密码
            GroupName = permessa.get('changepwdgroup', "None")
            try:
                with ldap3RESTARTABLE as conn:
                    CountName = repeace(username)
                    conn.search(
                        search_base=ladp3search_base,
                        # search_filter="(&(objectCategory=group)(sAMAccountName="+GroupName+"))",
                        search_filter="(&(objectCategory=group)(sAMAccountName=" + GroupName + "))",
                        search_scope='SUBTREE',
                        attributes=['distinguishedName', 'sAMAccountName'],
                    )
                    result_id = conn.result
                    response_id = conn.response
                    if result_id['result'] == 0:
                        message = response_id[0].get('attributes', '')
                        distinguishedName = message['distinguishedName']
                        if message:
                            conn.search(search_base=ladp3search_base,
                                                    search_filter="(&(objectClass=user)(memberof:1.2.840.113556.1.4.1941:=%s))" % distinguishedName,
                                                    attributes=['sAMAccountName'])
                            resultdn_id = conn.result
                            responsedn_id = conn.response
                            uservalue = []
                            if resultdn_id['result'] == 0:

                                for i in responsedn_id:
                                    if i.get('attributes', ''):
                                        uservalue.append(i.get('attributes').get('sAMAccountName'))
                                if username in uservalue:
                                    result = {'isSuccess': True, 'message': '正常用户'}
                                else:
                                    GroupName = permessa.get('operagroup', "None")
                                    conn.search(
                                        search_base=ladp3search_base,
                                        # search_filter="(&(objectCategory=group)(sAMAccountName="+GroupName+"))",
                                        search_filter="(&(objectCategory=group)(sAMAccountName=" + GroupName + "))",
                                        search_scope='SUBTREE',
                                        attributes=['distinguishedName', 'sAMAccountName'],
                                    )
                                    result_id = conn.result
                                    response_id = conn.response
                                    if result_id['result'] == 0:
                                        message = response_id[0].get('attributes', '')
                                        distinguishedName = message['distinguishedName']
                                        if message:
                                            conn.search(search_base=ladp3search_base,
                                                                    search_filter="(&(objectClass=user)(memberof:1.2.840.113556.1.4.1941:=%s))" % distinguishedName,
                                                                    attributes=['sAMAccountName'])
                                            resultdn_id = conn.result
                                            responsedn_id = conn.response
                                            uservalue = []
                                            if resultdn_id['result'] == 0:
                                                for i in responsedn_id:
                                                    if i.get('attributes', ''):
                                                        uservalue.append(i.get('attributes').get('sAMAccountName'))
                                                if username in uservalue:
                                                    result = {'isSuccess': True, 'message': '正常用户'}
                                                else:
                                                    result = {'isSuccess': False, 'message': '权限不足'}
                                            else:
                                                result = {'isSuccess': False, 'message': '未查询到信息'}
                                        else:
                                            result = {'isSuccess': False, 'message': '未查询到组信息'}
                                    else:
                                        result = {'isSuccess': False, "message": result_id}
                            else:
                                result = {'isSuccess': False, 'message': '未查询到信息'}
                        else:
                            result = {'isSuccess': False, 'message': '未查询到组信息'}
                    else:
                        result = {'isSuccess': False, "message": result_id}
            except Exception as e:
                result = {'isSuccess': False, "message": str(e)}
            return result
        elif types=='changelw':#改栏位
            GroupName = permessa.get('fieldgroup', "None")
            try:
                with ldap3RESTARTABLE as conn:
                    conn.search(
                        search_base=ladp3search_base,
                        # search_filter="(&(objectCategory=group)(sAMAccountName="+GroupName+"))",
                        search_filter="(&(objectCategory=group)(sAMAccountName=" + GroupName + "))",
                        search_scope='SUBTREE',
                        attributes=['distinguishedName', 'sAMAccountName'],
                    )
                    result_id = conn.result
                    response_id = conn.response
                    if result_id['result'] == 0:
                        message = response_id[0].get('attributes', '')
                        distinguishedName = message['distinguishedName']
                        if message:
                            conn.search(search_base=ladp3search_base,
                                                    search_filter="(&(objectClass=user)(memberof:1.2.840.113556.1.4.1941:=%s))" % distinguishedName,
                                                    attributes=['sAMAccountName'])
                            resultdn_id = conn.result
                            responsedn_id = conn.response
                            uservalue = []
                            if resultdn_id['result'] == 0:

                                for i in responsedn_id:
                                    if i.get('attributes', ''):
                                        uservalue.append(i.get('attributes').get('sAMAccountName'))
                                if username in uservalue:
                                    result = {'isSuccess': True, 'message': '正常用户'}
                                else:
                                    GroupName = permessa.get('operagroup', "None")
                                    conn.search(
                                        search_base=ladp3search_base,
                                        # search_filter="(&(objectCategory=group)(sAMAccountName="+GroupName+"))",
                                        search_filter="(&(objectCategory=group)(sAMAccountName=" + GroupName + "))",
                                        search_scope='SUBTREE',
                                        attributes=['distinguishedName', 'sAMAccountName'],
                                    )
                                    result_id = conn.result
                                    response_id = conn.response
                                    if result_id['result'] == 0:
                                        message = response_id[0].get('attributes', '')
                                        distinguishedName = message['distinguishedName']
                                        if message:
                                            conn.search(search_base=ladp3search_base,
                                                                    search_filter="(&(objectClass=user)(memberof:1.2.840.113556.1.4.1941:=%s))" % distinguishedName,
                                                                    attributes=['sAMAccountName'])
                                            resultdn_id = conn.result
                                            responsedn_id = conn.response
                                            uservalue = []
                                            if resultdn_id['result'] == 0:
                                                for i in responsedn_id:
                                                    if i.get('attributes', ''):
                                                        uservalue.append(i.get('attributes').get('sAMAccountName'))
                                                if username in uservalue:
                                                    result = {'isSuccess': True, 'message': '正常用户'}
                                                else:
                                                    result = {'isSuccess': False, 'message': '权限不足'}
                                            else:
                                                result = {'isSuccess': False, 'message': '未查询到信息'}
                                        else:
                                            result = {'isSuccess': False, 'message': '未查询到组信息'}
                                    else:
                                        result = {'isSuccess': False, "message": result_id}
                            else:
                                result = {'isSuccess': False, 'message': '未查询到信息'}
                        else:
                            result = {'isSuccess': False, 'message': '未查询到组信息'}
                    else:
                        result = {'isSuccess': False, "message": result_id}
            except Exception as e:
                result = {'isSuccess': False, "message": str(e)}
            return result
    else:
        result = {'isSuccess': False, "message": '权限组未配置'}
        return result
#登录权限判断
# def Getgroupuser(username):
#     try:
#         permessa = getpermsessage()
#         if permessa:
#             CountName = repeace(username)
#             ldap3RESTARTABLE.search(
#                 search_base=ladp3search_base,
#                 search_filter="(&(objectCategory=group)(sAMAccountName="+permessa.get('logongroup', "None")+"))",
#                 search_scope='SUBTREE',
#                 attributes=['member'],
#             )
#             result_id = ldap3RESTARTABLE.result
#             response_id = ldap3RESTARTABLE.response
#             if result_id['result'] == 0:
#                 message = response_id[0].get('attributes', '')
#                 if message:
#                     ldap3RESTARTABLE.search(search_base=ladp3search_base,
#                                             search_filter="(&(objectClass=user)(objectCategory=person) (sAMAccountName=" + CountName + "))",
#                                             attributes=['distinguishedName'])
#                     resultdn_id = ldap3RESTARTABLE.result
#                     responsedn_id = ldap3RESTARTABLE.response
#                     if resultdn_id['result'] == 0:
#                         messagedn = responsedn_id[0].get('attributes', '')
#                         if messagedn:
#                             if messagedn['distinguishedName'] in message['member']:
#                                 result = {'isSuccess': True, 'message': '正常用户'}
#                             else:
#                                 result = {'isSuccess': False, 'message': '权限不足'}
#                         else:
#                             result = {'isSuccess': False, 'message': '未查询到用户信息'}
#                     else:
#                         result = {'isSuccess': False, 'message': '未查询到信息'}
#                 else:
#                     result = {'isSuccess': False, 'message': '未查询到组信息'}
#             else:
#                 result = {'isSuccess': False, "message": result_id}
#         else:
#             result = {'isSuccess': False, "message": '权限组未配置'}
#     except Exception as e:
#         result = {'isSuccess': False, "message": str(e)}
#     return result
# def Getgroupuser(username):
#     try:
#         permessa = getpermsessage()
#         if permessa:
#             dnvalue=[]
#             pervalue=[]
#             for i in permessa:
#                 ldap3RESTARTABLE.search(
#                     search_base=ladp3search_base,
#                     # search_filter="(&(objectCategory=group)(sAMAccountName="+GroupName+"))",
#                     search_filter="(&(objectCategory=group)(sAMAccountName=" + permessa[i] + "))",
#                     search_scope='SUBTREE',
#                     attributes=['distinguishedName', 'sAMAccountName'],
#                 )
#                 result_id = ldap3RESTARTABLE.result
#                 response_id = ldap3RESTARTABLE.response
#                 if result_id['result'] == 0:
#                     message = response_id[0].get('attributes', '')
#                     dnvalue.append(message['distinguishedName'])
#             for x in dnvalue:
#                 ldap3RESTARTABLE.search(search_base=ladp3search_base,
#                                         search_filter="(&(objectClass=user)(memberof:1.2.840.113556.1.4.1941:=%s))" % x,
#                                         attributes=['sAMAccountName'])
#                 resultdn_id = ldap3RESTARTABLE.result
#                 responsedn_id = ldap3RESTARTABLE.response
#                 if resultdn_id['result'] == 0:
#                     for i in responsedn_id:
#                         if i.get('attributes', ''):
#                             pervalue.append(i.get('attributes').get('sAMAccountName'))
#             if username in list(set(pervalue)):
#                 result = {'isSuccess': True, 'message': '正常用户'}
#             else:
#                 result = {'isSuccess': False, 'message': '权限不足'}
#         else:
#             result = {'isSuccess': False, "message": '权限组未配置'}
#     except Exception as e:
#         result = {'isSuccess': False, "message": str(e)}
#     return result


def verifyuser_login_new(sAMAccountName, password):
    try:
        permessa = getpermsessage()
        logongroup = permessa.get('logongroup','')
        with ldap3RESTARTABLE as conn:
            if logongroup:
                conn.search(
                    search_base=ladp3search_base,
                    search_filter="(&(objectCategory=group)(sAMAccountName=" + logongroup + "))",
                    search_scope='SUBTREE',
                )
                result_logongroup = conn.result
                response_logongroup = conn.response
                logongroup_dn = response_logongroup[0].get('dn','')
                if logongroup_dn:
                    conn.search(search_base=ladp3search_base,
                                            search_filter="(&(objectCategory=person)(objectClass=user)(memberof:1.2.840.113556.1.4.1941:=%s)(sAMAccountName=%s))" % (logongroup_dn, sAMAccountName),
                                            attributes=['sAMAccountName', 'userAccountControl', 'lockoutTime', 'distinguishedName','cn','name',
                                                        'sn','givenName','userPrincipalName','displayName','wWWHomePage','description','physicalDeliveryOfficeName','mail', 'accountExpires'])
                    result_user = conn.result
                    response_user = conn.response
                    user_attributes = response_user[0].get('attributes','')
                    if user_attributes:
                        userAccountControl = user_attributes.get('userAccountControl')
                        distinguishedName = user_attributes.get('distinguishedName')
                        lockoutTime = user_attributes.get('lockoutTime', '')
                        accountExpires = user_attributes.get('accountExpires', datetime.now())
                        if lockoutTime:
                            lockoutTime_str = (utc2local(lockoutTime)).strftime('%Y-%m-%d %H:%M:%S')
                        else:
                            lockoutTime_str = '1601-01-01 08:00:00'
                        # accountExpires  9999-12-31 23:59:59.999999 未设置账户过期
                        # accountExpires 1601-01-01 00:00:00+00:00 从不过期
                        # accountExpires 2019-05-17 16:00:00+00:00 账户过期时间
                        accountExpires_str = accountExpires.strftime('%Y-%m-%d %H:%M:%S')
                        if accountExpires_str in ['1601-01-01 00:00:00', '9999-12-31 23:59:59']:
                            Expires = True
                        else:
                            accountExpires = (utc2local(accountExpires)).replace(tzinfo=None)
                            now = (datetime.now()).replace(tzinfo=None)
                            if accountExpires > now:
                                Expires = True
                            else:
                                accountExpires_str = accountExpires.strftime('%Y-%m-%d %H:%M:%S')
                                Expires = False
                        if bin(userAccountControl)[-2] == '0':
                            if lockoutTime_str == '1601-01-01 08:00:00':
                                if Expires:
                                    try:
                                        server = Server(ladp3search_server, get_info=NONE)
                                        connect = Connection(server=server, user=distinguishedName, password=password)
                                        bind = connect.bind(read_server_info=False)
                                        if bind:
                                            result = {'isSuccess': True, "message": user_attributes}
                                        else:
                                            result = {'isSuccess': False, "message": '密码错误'}
                                    except Exception as e:
                                        result = {'isSuccess': False, "message": '服务器连接ldap错误'+str(e)}
                                else:
                                    result = {'isSuccess': False, "message": sAMAccountName + '账号已过期,过期时间' + accountExpires_str}
                            else:
                                result = {'isSuccess': False, "message": sAMAccountName + '账号已锁定,锁定时间'+lockoutTime_str}
                        else:
                            result = {'isSuccess': False, "message": sAMAccountName+'账号已禁用'}
                    else:
                        result = {'isSuccess': False, "message": sAMAccountName+'账号错误或没有权限'}
                else:
                    result = {'isSuccess': False, "message": '登陆权限组配置错误：'+str(result_logongroup.get('description',''))}
            else:
                result = {'isSuccess': False, "message": '登陆权限组未配置'}
    except Exception as e:
        result = {'isSuccess': False, "message": '服务器错误：'+str(e)}
    return result


