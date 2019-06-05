import ast
import json
import time
from urllib import request, parse
from  itapi.exapi import *

import pytz
import tzlocal
from django.http import HttpResponse, JsonResponse
import datetime
# Create your views here.
from django.views import View
from ldap3 import Server, Connection, ALL, MODIFY_DELETE, MODIFY_REPLACE, MODIFY_ADD, MODIFY_INCREMENT, ObjectDef, \
    AttrDef, Reader, Writer, SEQUENCE_TYPES, SUBTREE

from dbinfo.views import insert_log, selectindexmessagedb, getskey
from itops.settings import  ldap3RESTARTABLE, ladp3search_base
from permission.views import Userperm
#替换（）*
from sendmailapi.sendmail import send_email_by_template


def repeace(message):
    promessage=message.replace('(',r'\28').replace(')',r'\29').replace('*',r'2a')
    return promessage

def repeacelist(message):
    a = list()
    for i in message:
        a.append(i.replace('(',r'\28').replace(')',r'\29').replace('*',r'2a'))
    return a

def iisurl():
    cusr='http://'+getskey()['iisserver']+':'+getskey()['iisport']
    return cusr

def date_handler(obj):
    if hasattr(obj, 'isoformat'):
        return obj.isoformat()
    else:
        raise TypeError

#AD账号条件模糊查找/ 传入 usernane
class GetConMessage(View):
    def get(self, request):
        usernammse = request.session.get('username')
        username = request.GET.get('username')
        try:
            username = repeace(username)
            with ldap3RESTARTABLE as conn:
                conn.search(
                search_base=ladp3search_base,
                search_filter= '(&(anr='+username+')(|(&(objectCategory=person)(objectClass=user))(objectCategory=group)))',
                attributes=['sAMAccountName', "distinguishedName", 'proxyAddresses','description', 'displayName', 'name', 'objectClass',
                            'userAccountControl'],
            )
                result_id = conn.result
                response_id = conn.response
                if result_id['result'] == 0:
                    message = []
                    for i in response_id:
                        if i.get('attributes'):
                            usemessage = i['attributes']
                            message.append(dict(usemessage))
                    result = {'isSuccess': True, 'message': message}
                else:
                    result = {'isSuccess': False, "message": result_id}
        except Exception as e:
            result = {'isSuccess': False, "message": str(e)}
        insert_log(usernammse, request, str(result['isSuccess']), str(result), 'AD账号条件模糊查找')
        response = HttpResponse()
        response['Content-Type'] = "application/json"
        response.write(json.dumps(result).encode("UTF-8"))
        return response

    def post(self, request):
        usernammse = request.session.get('username')
        username = request.POST.get('username')
        mode = request.POST.get('mode')
        try:
            username=repeace(username)
            if mode =='computer':
                search='(&(anr='+username+')(&(objectClass=computer)))'
            elif mode=='user':
                search = '(|(anr=' + username + ')(&(|(&(objectCategory=person)(objectClass=user))(objectCategory=group)(objectCategory=contact))(|(wWWHomePage=' + username + ')(physicalDeliveryOfficeName=' + username + '))))'
            else:
                search='(&(anr='+username+')(|(objectCategory=group)(&(objectCategory=person)(objectClass=user))(objectCategory=contact)))'
            with ldap3RESTARTABLE as conn:
                conn.search(
                search_base=ladp3search_base,
                search_filter=search,
                search_scope='SUBTREE',
                attributes=['sAMAccountName',"distinguishedName" ,'description','displayName', 'name','objectClass','userAccountControl','lockoutTime'], )
                result_id = conn.result
                response_id = conn.response
                if result_id['result']==0:
                    message=[]
                    for i in  response_id:
                        if i.get('attributes'):
                            usemessage=i['attributes']
                            if 'computer' in usemessage['objectClass']:
                                usemessage['objectClass']='计算机'
                                userAccountCon = bin(usemessage['userAccountControl'])[-2]
                                if userAccountCon=='0':
                                    usemessage['userAccountConte']='启用'
                                    usemessage['icon'] = '<img src="/static/zTreeStyle/img/Computer.png"> '
                                else:
                                    usemessage['userAccountConte'] = '禁用'
                                    usemessage['icon'] = '<img src="/static/zTreeStyle/img/computer2.png"> '
                            elif 'organizationalUnit' in usemessage['objectClass']:
                                usemessage['objectClass'] = '组织单位'
                                usemessage['icon'] = '<img src="/static/zTreeStyle/img/ou.png"> '
                            elif 'container' in usemessage['objectClass']:
                                usemessage['objectClass'] = '容器'
                                usemessage['icon'] = '<img src="/static/zTreeStyle/img/ou01.png"> '
                            elif 'group' in usemessage['objectClass']:
                                usemessage['objectClass'] = '组'
                                usemessage['icon'] = '<img src="/static/zTreeStyle/img/group.png"> '
                            elif 'user' in usemessage['objectClass'] and 'person' in usemessage['objectClass']:
                                usemessage['objectClass'] = '用户'
                                userAccountCon = bin(usemessage['userAccountControl'])[-2]
                                if userAccountCon=='0':
                                    usemessage['userAccountConte']='启用'
                                    usemessage['icon'] = '<img src="/static/zTreeStyle/img/user.png"> '
                                else:
                                    usemessage['userAccountConte'] = '禁用'
                                    usemessage['icon'] = '<img src="/static/zTreeStyle/img/user2.png"> '
                            elif 'contact' in usemessage['objectClass']:
                                usemessage['objectClass'] = '联系人'
                                usemessage['icon'] = '<img src="/static/zTreeStyle/img/user.png"> '
                            else:
                                usemessage['objectClass'] = '其他'
                                usemessage['icon'] = '<img src="/static/zTreeStyle/img/weizi.png"> '
                            message.append(dict(usemessage))
                    result = {'isSuccess': True,'count':len(response_id)-3,'message': message}
                else:
                    result = {'isSuccess': False, "message": result_id}
        except Exception as e:
            result = {'isSuccess': False, "message": str(e)}
        insert_log(usernammse, request, str(result['isSuccess']), str(result), 'AD账号条件模糊查找')
        response = HttpResponse()
        response['Content-Type'] = "application/json"
        response.write(json.dumps(result,default=date_handler).encode("UTF-8"))
        return response

#AD账号条件模糊查找/ 传入 usernane 仅仅查询用户
class GetOnlyConMessage(View):
    def get(self, request):
        usernammse = request.session.get('username')
        username = request.GET.get('username')
        try:
            username = repeace(username)
            with ldap3RESTARTABLE as conn:
                conn.search(
                search_base=ladp3search_base,
                search_filter= '(&(anr='+username+')(&(objectCategory=person)(objectClass=user)))',
                attributes=['sAMAccountName', "distinguishedName", 'description', 'displayName', 'name', 'objectClass',
                            'userAccountControl','cn'],
            )
                result_id = conn.result
                response_id = conn.response
                if result_id['result'] == 0:
                    message = []
                    for i in response_id:
                        if i.get('attributes'):
                            usemessage = i['attributes']
                            message.append(dict(usemessage))
                    result = {'isSuccess': True, 'message': message}
                else:
                    result = {'isSuccess': False, "message": result_id}
        except Exception as e:
            result = {'isSuccess': False, "message": str(e)}
        insert_log(usernammse, request, str(result['isSuccess']), str(result), 'AD账号条件模糊查找')
        response = HttpResponse()
        response['Content-Type'] = "application/json"
        response.write(json.dumps(result).encode("UTF-8"))
        return response

#AD账号条件模糊查找组信息/ 传入 usernane
class GetGroupAnrMessage(View):
    def get(self, request):
        usernammse = request.session.get('username')
        username = request.GET.get('username')
        CountName = request.GET.get('CountName')
        try:
            CountName=repeace(CountName)
            with ldap3RESTARTABLE as conn:
                conn.search(
                    search_base=ladp3search_base,
                    search_filter='(&(anr=' + CountName + ')(objectCategory=group))',
                    search_scope='SUBTREE',
                    attributes=['sAMAccountName', "distinguishedName", 'cn', 'name', 'displayName', 'canonicalName'],
                )
                result_id = conn.result
                response_id = conn.response
                if result_id['result'] == 0:
                    message = []
                    for i in response_id:
                        if i.get('attributes'):
                            usemessage = i['attributes']
                            message.append(dict(usemessage))
                    result = {'isSuccess': True, 'message': message,'count':len(message)}
                else:
                    result = {'isSuccess': False, "message": result_id}
        except Exception as e:
            result = {'isSuccess': False, "message": str(e)}
        insert_log(usernammse, request, str(result['isSuccess']), str(result), '组条件模糊查找')
        response = HttpResponse()
        response['Content-Type'] = "application/json"
        response.write(json.dumps(result).encode("UTF-8"))
        return response

    def post(self, request):
        CountName = request.GET.get('CountName')
        try:
            CountName=repeace(CountName)
            with ldap3RESTARTABLE as conn:
                conn.search(
                    search_base=ladp3search_base,
                    search_filter='(&(anr='+CountName+')(objectCategory=group))',
                    search_scope='SUBTREE',
                    attributes=['sAMAccountName',"distinguishedName" ,'cn','name', 'displayName','canonicalName','userAccountControl'],
                )
                result_id = conn.result
                response_id = conn.response
                if result_id['result']==0:
                    message=[]
                    for i in  response_id:
                        if i.get('attributes'):
                            usemessage=i['attributes']
                            message.append(dict(usemessage))
                    result = {'isSuccess': True,'message': message}
                else:
                    result = {'isSuccess': False, "message": result_id}
        except Exception as e:
            result = {'isSuccess': False, "message": str(e)}
        response = HttpResponse()
        response['Content-Type'] = "application/json"
        response.write(json.dumps(result).encode("UTF-8"))
        return response

# AD账号精准查找/ 传入dn 属性or sancount
class GetUserMessage(View):
    def get(self, request):
        CountName = request.GET.get('CountName')
        objectClass = request.GET.get('objectClass', None)
        try:
            CountName=repeace(CountName)
            with ldap3RESTARTABLE as conn:
                if objectClass:
                    conn.search(search_base=CountName,
                                            search_filter="(objectClass=*)",
                                            search_scope='BASE',
                                            attributes=['givenName', 'initials', 'sn', 'cn', 'sAMAccountName',
                                                        'accountExpires',
                                                        'msDS-UserPasswordExpiryTimeComputed', 'userAccountControl',
                                                        'displayName', 'physicalDeliveryOfficeName', 'mail',
                                                        'wWWHomePage',
                                                        'telephoneNumber', 'homePhone', 'mobile',
                                                        'facsimileTelephoneNumber', 'pager','lockoutTime',
                                                        'ipPhone', 'description',
                                                        'memberof', 'proxyAddresses', 'whenChanged', 'whenCreated','objectClass','distinguishedName','managedBy','street','l','st','postalCode','name'])
                else:
                    conn.search(search_base=ladp3search_base,
                                            search_filter="(&(objectClass=user)(objectCategory=person) (sAMAccountName=" + CountName +"))",
                                            attributes=['givenName', 'initials', 'sn', 'cn', 'sAMAccountName', 'accountExpires',
                                                        'msDS-UserPasswordExpiryTimeComputed', 'userAccountControl',
                                                        'displayName', 'physicalDeliveryOfficeName', 'mail', 'wWWHomePage',
                                                        'telephoneNumber', 'homePhone', 'mobile', 'facsimileTelephoneNumber', 'pager','lockoutTime',
                                                        'ipPhone', 'description',
                                                        'memberof','proxyAddresses','whenChanged','whenCreated','objectClass','distinguishedName','street','l','st','postalCode','name','managedBy'])
                result_id = conn.result
                response_id = conn.response
                if result_id['result'] == 0:
                    message = response_id[0].get('attributes', '')
                    if message:
                        if message['userAccountControl']:
                            userAccountCon = bin(message['userAccountControl'])[-2]
                            if userAccountCon == '0':
                                message['userAccountConte'] = True
                            else:
                                message['userAccountConte'] = False
                        if  message['msDS-UserPasswordExpiryTimeComputed']:
                            if message['msDS-UserPasswordExpiryTimeComputed']==9223372036854775807 or message['msDS-UserPasswordExpiryTimeComputed']==0:
                                message['msDSUserPasswordExpiryTimeComputed']='密码永不过期'
                            else:
                                date=message['msDS-UserPasswordExpiryTimeComputed']-116444736000000000
                                date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(date / 10000000))
                                message['msDSUserPasswordExpiryTimeComputed'] = date
                        result = {'isSuccess': True, 'message': dict(message)}
                    else:
                        result = {'isSuccess': False, 'message': '未查询到信息'}
                else:
                    result = {'isSuccess': False, "message": str(result_id)}
        except Exception as e:
            result = {'isSuccess': False, "message": str(e)}
        response = HttpResponse()
        response['Content-Type'] = "application/json"
        response.write(json.dumps(result, default=str).encode("UTF-8"))
        return response

    def post(self, request):
        print(1)

# AD账号精准查找/ 传入dn 属性or sancount
class GetUserMessageexchange(View):
    def get(self, request):
        CountName = request.GET.get('CountName')
        objectClass = request.GET.get('objectClass', None)
        try:
            CountName=repeace(CountName)
            with ldap3RESTARTABLE as conn:
                if objectClass:
                    conn.search(search_base=CountName,
                                            search_filter="(objectClass=*)",
                                            search_scope='BASE',
                                            attributes=['givenName', 'initials', 'sn', 'cn', 'sAMAccountName',
                                                        'accountExpires',
                                                        'msDS-UserPasswordExpiryTimeComputed', 'userAccountControl',
                                                        'displayName', 'physicalDeliveryOfficeName', 'mail',
                                                        'wWWHomePage',
                                                        'telephoneNumber', 'homePhone', 'mobile',
                                                        'facsimileTelephoneNumber', 'pager','lockoutTime',
                                                        'ipPhone', 'description',
                                                        'memberof','publicDelegates',  'proxyAddresses', 'whenChanged', 'whenCreated','objectClass','distinguishedName','managedBy','street','l','st','postalCode','name'])
                else:
                    conn.search(search_base=ladp3search_base,
                                            search_filter="(&(objectClass=user)(objectCategory=person) (sAMAccountName=" + CountName +"))",
                                            attributes=['givenName', 'initials', 'sn', 'cn', 'sAMAccountName', 'accountExpires',
                                                        'msDS-UserPasswordExpiryTimeComputed', 'userAccountControl',
                                                        'displayName', 'physicalDeliveryOfficeName', 'mail', 'wWWHomePage',
                                                        'telephoneNumber', 'homePhone', 'mobile', 'facsimileTelephoneNumber', 'pager','lockoutTime',
                                                        'ipPhone','description',
                                                        'memberof','publicDelegates',  'proxyAddresses','whenChanged','whenCreated','objectClass','distinguishedName','street','l','st','postalCode','name','managedBy'])
                result_id = conn.result
                response_id = conn.response
                if result_id['result'] == 0:
                    message = response_id[0].get('attributes', '')
                    if message:
                        if message['userAccountControl']:
                            userAccountCon = bin(message['userAccountControl'])[-2]
                            if userAccountCon == '0':
                                message['userAccountConte'] = True
                            else:
                                message['userAccountConte'] = False
                        if  message['msDS-UserPasswordExpiryTimeComputed']:
                            if message['msDS-UserPasswordExpiryTimeComputed']==9223372036854775807 or message['msDS-UserPasswordExpiryTimeComputed']==0:
                                message['msDSUserPasswordExpiryTimeComputed']='密码永不过期'
                            else:
                                date=message['msDS-UserPasswordExpiryTimeComputed']-116444736000000000
                                date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(date / 10000000))
                                message['msDSUserPasswordExpiryTimeComputed'] = date
                        result = {'isSuccess': True, 'message': dict(message)}
                    else:
                        result = {'isSuccess': False, 'message': '未查询到信息'}
                else:
                    result = {'isSuccess': False, "message": str(result_id)}
        except Exception as e:
            result = {'isSuccess': False, "message": str(e)}
        response = HttpResponse()
        response['Content-Type'] = "application/json"
        response.write(json.dumps(result, default=str).encode("UTF-8"))
        return response

    def post(self, request):
        print(1)

# 计算机账号精准查找/ sancount
class GetCompMessage(View):
    def get(self, request):
        CountName = request.GET.get('CountName')
        try:
            CountName = repeace(CountName)
            with ldap3RESTARTABLE as conn:
                conn.search(
                    search_base=ladp3search_base,
                    search_filter="(&(objectCategory=computer)(sAMAccountName=" + CountName +"))",
                    search_scope='SUBTREE',
                    attributes=['givenName', 'sn', 'cn', 'sAMAccountName','operatingSystemServicePack','operatingSystemVersion','distinguishedName',
                                'accountExpires',
                                'dNSHostName',
                                'displayName', 'physicalDeliveryOfficeName',
                                'managedBy', 'description',
                                'memberof', 'operatingSystem', 'whenChanged', 'whenCreated','objectClass','managedBy'],
                )
                result_id = conn.result
                response_id = conn.response
                if result_id['result'] == 0:
                    message = response_id[0].get('attributes', '')
                    if message:
                        result = {'isSuccess': True, 'message': dict(message)}
                    else:
                        result = {'isSuccess': False, 'message': '未查询到信息'}
                else:
                    result = {'isSuccess': False, "message": result_id}
        except Exception as e:
            result = {'isSuccess': False, "message": str(e)}
        response = HttpResponse()
        response['Content-Type'] = "application/json"
        response.write(json.dumps(result, default=str).encode("UTF-8"))
        return response



# 获取组信息精准查找/ 传入sAMAccountName 属性
class GetGroupPreMessage(View):
    def get(self, request):
        CountName = request.GET.get('CountName')
        try:
            CountName = repeace(CountName)
            with ldap3RESTARTABLE as conn:
                conn.search(
                    search_base=ladp3search_base,
                    search_filter="(&(objectCategory=group)(sAMAccountName=" + CountName +"))",
                    search_scope='SUBTREE',
                    # attributes=['member','memberof','groupType','msExchRequireAuthToSendTo','authOrig','managedBy','proxyAddresses','sAMAccountName', "distinguishedName", 'cn', 'name', 'displayName', 'canonicalName','mail','description','info','whenChanged','whenCreated'],
                    attributes=['member', 'memberof', 'groupType', 'managedBy', 'proxyAddresses', 'sAMAccountName',
                                "distinguishedName", 'cn', 'name', 'displayName', 'canonicalName', 'mail',
                                'description', 'info', 'whenChanged', 'whenCreated'],
                )
                result_id = conn.result
                response_id = conn.response
                if result_id['result'] == 0:
                    message = response_id[0].get('attributes', '')
                    if message:
                        result = {'isSuccess': True, 'message': dict(message)}
                    else:
                        result = {'isSuccess': False, 'message': '未查询到信息'}
                else:
                    result = {'isSuccess': False, "message": result_id}

        except Exception as e:
            result = {'isSuccess': False, "message": str(e)}

        response = HttpResponse()
        response['Content-Type'] = "application/json"
        response.write(json.dumps(result, default=str).encode("UTF-8"))
        return response

    def post(self, request):
        print(1)


# 获取组信息精准查找/ 传入sAMAccountName 属性
class GetGroupPreMessageexchangevalue(View):
    def get(self, request):
        CountName = request.GET.get('CountName')
        try:
            CountName = repeace(CountName)
            with ldap3RESTARTABLE as conn:
                conn.search(
                    search_base=ladp3search_base,
                    search_filter="(&(objectCategory=group)(sAMAccountName=" + CountName +"))",
                    search_scope='SUBTREE',
                    attributes=['member','memberof','groupType','msExchRequireAuthToSendTo','authOrig','managedBy','proxyAddresses','sAMAccountName', "distinguishedName", 'cn', 'name', 'displayName', 'canonicalName','mail','description','info','whenChanged','whenCreated'],
                )
                result_id = conn.result
                response_id = conn.response
                if result_id['result'] == 0:
                    message = response_id[0].get('attributes', '')
                    byteslist=message['authOrig']
                    Nbytes=list()
                    for i in byteslist:
                        Nbytes.append(i.decode())
                    if message:
                        message['authOrig']=Nbytes
                        result = {'isSuccess': True, 'message': dict(message)}
                    else:
                        result = {'isSuccess': False, 'message': '未查询到信息'}
                else:
                    result = {'isSuccess': False, "message": result_id}

        except Exception as e:
            result = {'isSuccess': False, "message": str(e)}

        response = HttpResponse()
        response['Content-Type'] = "application/json"
        response.write(json.dumps(result, default=str).encode("UTF-8"))
        return response

    def post(self, request):
        print(1)

#获取邮箱账号属性-get-mailboxstatic
def GetobjectProperty(mailname):
    try:
        exapivalue = GetMailbox(mailname)
        if (exapivalue['isSuccess']):
            return {'isSuccess':exapivalue['isSuccess'],'message':exapivalue['message'][0]}
        else:
            return {'isSuccess':exapivalue['isSuccess'],'message':exapivalue['msg']}
    except Exception as e :
        return {'isSuccess': False, 'message': str(e)}
    # url=iisurl()+'/api/ad/GetMailboxuser'
    # value = {
    #     "mailname":mailname,
    #     "skey": 'A8C4D656BBBB2C42436B4B9B45FC63AD'
    # }
    # querystring = parse.urlencode(value)
    # u = request.urlopen(url + '?' + querystring).read().decode('utf-8')
    # respjson = json.loads(u)
    # return respjson

#删除移动请求
def RemoveMoveRequest(username):
    try:
        exapivalue = RemoveMoveRequesthight(username)
        if (exapivalue['isSuccess']):
            return {'isSuccess':exapivalue['isSuccess'],'message':exapivalue['message']}
        else:
            return {'isSuccess':exapivalue['isSuccess'],'message':exapivalue['msg']}
    except Exception as e :
        return {'isSuccess': False, 'message': str(e)}
    # url=iisurl()+'/api/ad/RemoveMoveRequest'
    # value = {
    #     "username":username,
    #     "skey": 'A8C4D656BBBB2C42436B4B9B45FC63AD'
    # }
    # querystring = parse.urlencode(value)
    # u = request.urlopen(url + '?' + querystring).read().decode('utf-8')
    # respjson = json.loads(u)
    # return respjson


#获取邮箱账号属性-get-mailbox
def Getusermail(mailname):
    try:
        exapivalue = GetMailboxStatistics(mailname)
        if (exapivalue['isSuccess']):
            # return {'isSuccess':exapivalue['isSuccess'],'message':exapivalue['message'][0]}
            if exapivalue['message']:
                return {'isSuccess':exapivalue['isSuccess'],'message':exapivalue['message'][0]}
            else:
                return {'isSuccess':exapivalue['isSuccess'],'message':{}}
        else:
            return {'isSuccess':exapivalue['isSuccess'],'message':exapivalue['msg']}
    except Exception as e :
        return {'isSuccess': False, 'message': str(e)}
    # url=iisurl()+'/api/ad/GetMailboxStatisticsuser'
    # value = {
    #     "mailname":mailname,
    #     "skey": 'A8C4D656BBBB2C42436B4B9B45FC63AD'
    # }
    # querystring = parse.urlencode(value)
    # u = request.urlopen(url + '?' + querystring).read().decode('utf-8')
    # respjson = json.loads(u)
    # return respjson

#获取归档容量
def Getmailarchive(mailname):
    try:
        exapivalue = GetMailboxStatistics(mailname,archive=True)
        if (exapivalue['isSuccess']):
            return {'isSuccess':exapivalue['isSuccess'],'message':exapivalue['message'][0]['TotalItemSize']}
        else:
            return {'isSuccess':exapivalue['isSuccess'],'message':exapivalue['msg']}
    except Exception as e :
        return {'isSuccess': False, 'message': str(e)}
    # url=iisurl()+'/api/ad/GetMailboxStatisticsByArchive'
    # value = {
    #     "mailname":mailname,
    #     'parametername':'TotalItemSize',
    #     "skey": 'A8C4D656BBBB2C42436B4B9B45FC63AD'
    # }
    # querystring = parse.urlencode(value)
    # u = request.urlopen(url + '?' + querystring).read().decode('utf-8')
    # respjson = json.loads(u)
    # return respjson

##获取数据库容量大小
def getmailboxdatabaseapi(maildbname):
    try:
        exapivalue = GetMailboxdatabase(identity=maildbname)
        if (exapivalue['isSuccess']):
            return {'isSuccess':exapivalue['isSuccess'],'message':exapivalue['message'][0]}
        else:
            return {'isSuccess':exapivalue['isSuccess'],'message':exapivalue['msg']}
    except Exception as e :
        return {'isSuccess': False, 'message': str(e)}
    # url = iisurl()+'/api/ad/getmailboxdatabasecap'
    # value = {
    #     "maildbname":maildbname,
    #     "skey":'A8C4D656BBBB2C42436B4B9B45FC63AD'
    # }
    # querystring = parse.urlencode(value)
    # u = request.urlopen(url + '?' + querystring).read().decode('utf-8')
    # respjson = json.loads(u)
    # return respjson

##删除用户smtp地址
def deluseremailadressapi(username,smtpValue):
    try:
        parameter = "@{remove='" + smtpValue + "'}"
        exapivalue = SetMailboxEmailAddresses(username,parameter)
        if (exapivalue['isSuccess']):
            return {'isSuccess':exapivalue['isSuccess'],'message':exapivalue['message']}
        else:
            return {'isSuccess':exapivalue['isSuccess'],'message':exapivalue['msg']}
    except Exception as e :
        return {'isSuccess': False, 'message': str(e)}
    # url=iisurl()+'/api/ad/deluseremailadress'
    # # url='http://localhost:26816/api/ad/deluseremailadress'
    # value = {
    #     "username":username,
    #     "smtpValue":smtpValue,
    #     "skey":'A8C4D656BBBB2C42436B4B9B45FC63AD'
    # }
    # querystring = parse.urlencode(value)
    # u = request.urlopen(url + '?' + querystring).read().decode('utf-8')
    # respjson = json.loads(u)
    # return respjson



##获取邮箱DB
def getmailboxdatabasenovalue():
    try:
        dbapivalue = GetMailboxdatabase()
        message = list()
        if dbapivalue['isSuccess']:
            for i in dbapivalue['message']:
                message.append("{'daname':'"+i['Identity']+"'}")
        else:
            message.append(dbapivalue['msg'])
        return {'isSuccess':dbapivalue['isSuccess'],'message':message}
    except Exception as e:
        return {'isSuccess': False, 'message': [str(e)]}
    # url=iisurl()+'/api/ad/getmailboxdatabasenovalue'
    # value = {
    #     "skey":'A8C4D656BBBB2C42436B4B9B45FC63AD'
    # }
    # querystring = parse.urlencode(value)
    # u = request.urlopen(url + '?' + querystring).read().decode('utf-8')
    # respjson = json.loads(u)
    # return respjson

##联系人新建邮箱
def EnableMailContactapi(mailname,ExternalEmailAddress):
    try:
        exapivalue = EnableMailContacthight(mailname,ExternalEmailAddress)
        if (exapivalue['isSuccess']):
            return {"Data":{'isSuccess':exapivalue['isSuccess'],'message':exapivalue['message']}}
        else:
            return {"Data":{'isSuccess':exapivalue['isSuccess'],'message':exapivalue['msg']}}
    except Exception as e :
        return {"Data":{'isSuccess': False, 'message': str(e)}}
    # url=iisurl()+'/api/ad/EnableMailContact'
    # value = {
    #     "mailname":mailname,
    #     "ExternalEmailAddress":ExternalEmailAddress,
    #     "skey":'A8C4D656BBBB2C42436B4B9B45FC63AD'
    # }
    # querystring = parse.urlencode(value)
    # u = request.urlopen(url + '?' + querystring).read().decode('utf-8')
    # respjson = json.loads(u)
    # return respjson

##创建用户邮箱
def UserToExc(username,dbname):
    try:
        exapivalue = EnableMailboxhigh(username,username,dbname)
        if (exapivalue['isSuccess']):
            return {'isSuccess':exapivalue['isSuccess'],'message':exapivalue['message']}
        else:
            return {'isSuccess':exapivalue['isSuccess'],'message':exapivalue['msg']}
    except Exception as e :
        return {'isSuccess': False, 'message': str(e)}
    # url=iisurl()+'/api/ad/UserToExc'
    # value = {
    #     "username":username,
    #     "dbname":dbname,
    #     "skey":'A8C4D656BBBB2C42436B4B9B45FC63AD'
    # }
    # querystring = parse.urlencode(value)
    # u = request.urlopen(url + '?' + querystring).read().decode('utf-8')
    # respjson = json.loads(u)
    # return respjson

##获取邮箱群组信息
def NGetDistributionGroup(mailname):
    try:
        exapivalue = GetDistributionGroup(mailname)
        if (exapivalue['isSuccess']):
            return {'isSuccess':exapivalue['isSuccess'],'message':exapivalue['message'][0]}
        else:
            return {'isSuccess':exapivalue['isSuccess'],'message':exapivalue['msg']}
    except Exception as e :
        return {'isSuccess': False, 'message': str(e)}
    # url=iisurl()+'/api/ad/NGetDistributionGroup'
    # value = {
    #     "mailname":mailname,
    #     "skey":'A8C4D656BBBB2C42436B4B9B45FC63AD'
    # }
    # querystring = parse.urlencode(value)
    # u = request.urlopen(url + '?' + querystring).read().decode('utf-8')
    # respjson = json.loads(u)
    # return respjson

##获取联系人邮箱信息
def GetMailContactapi(mailname):
    try:
        exapivalue = GetMailContacthight(mailname)
        if (exapivalue['isSuccess']):
            return {'isSuccess':exapivalue['isSuccess'],'message':exapivalue['message'][0]}
        else:
            return {'isSuccess':exapivalue['isSuccess'],'message':exapivalue['msg']}
    except Exception as e :
        return {'isSuccess': False, 'message': str(e)}
    # url=iisurl()+'/api/ad/GetMailContact'
    # value = {
    #     "mailname":mailname,
    #     "skey":'A8C4D656BBBB2C42436B4B9B45FC63AD'
    # }
    # querystring = parse.urlencode(value)
    # u = request.urlopen(url + '?' + querystring).read().decode('utf-8')
    # respjson = json.loads(u)
    # return respjson

# 获取邮箱群组信息
class GetMailGroup(View):
    def get(self, request):
        CountName = request.GET.get('CountName')
        try:
            deluseremai = NGetDistributionGroup(CountName)
            if deluseremai['isSuccess']:
                result = {'isSuccess': True, "message": deluseremai['message']}
            else:
                result = {'isSuccess': False, "message": str(deluseremai['message'])}
        except Exception as e:
            result = {'isSuccess': False, "message": str(e)}
        response = HttpResponse()
        response['Content-Type'] = "application/json"
        response.write(json.dumps(result, default=str).encode("UTF-8"))
        return response

# 获取联系人邮箱信息
class GetMailContact(View):
    def get(self, request):
        CountName = request.GET.get('CountName')
        try:
            deluseremai = GetMailContactapi(CountName)
            print(deluseremai)
            if deluseremai['isSuccess']:
                result = {'isSuccess': True, "message": deluseremai['message']}
            else:
                result = {'isSuccess': False, "message": str(deluseremai['message'])}
        except Exception as e:
            result = {'isSuccess': False, "message": str(e)}
        response = HttpResponse()
        response['Content-Type'] = "application/json"
        response.write(json.dumps(result, default=str).encode("UTF-8"))
        return response

##开启归档
def  EnableMailbox(username,ArchiveDatabase):
    try:
        exapivalue = EnableMailboxarchive(username,ArchiveDatabase)
        if (exapivalue['isSuccess']):
            return {'isSuccess':exapivalue['isSuccess'],'message':exapivalue['message']}
        else:
            return {'isSuccess':exapivalue['isSuccess'],'message':exapivalue['msg']}
    except Exception as e :
        return {'isSuccess': False, 'message': str(e)}
    # url=iisurl()+'/api/ad/EnableMailbox'
    # value = {
    #     "username":username,
    #     "ArchiveDatabase":ArchiveDatabase,
    #     "skey":'A8C4D656BBBB2C42436B4B9B45FC63AD'
    # }
    # querystring = parse.urlencode(value)
    # u = request.urlopen(url + '?' + querystring).read().decode('utf-8')
    # respjson = json.loads(u)
    # return respjson


# 开启存档
class EnUserMailArchive(View):
    def get(self, request):
        username = request.session.get('username')
        permess = Userperm(username, 'operate')
        if permess['isSuccess']:
            CountName = request.GET.get('CountName')
            DBName = request.GET.get('DBName')
            try:
                deluseremai = EnableMailbox(CountName, DBName)
                if deluseremai['isSuccess']:
                    result = {'isSuccess': True, "message": '创建成功'}
                else:
                    result = {'isSuccess': False, "message": str(deluseremai['message'])}
            except Exception as e:
                result = {'isSuccess': False, "message": str(e)}
        else:
            result = {'isSuccess': False, "message": '权限不足'}
        insert_log(username, request, str(result['isSuccess']), str(result), '开启存档')
        response = HttpResponse()
        response['Content-Type'] = "application/json"
        response.write(json.dumps(result, default=str).encode("UTF-8"))
        return response

##迁移用户存档数据库
def NewMoveArchive(username,ArchiveTargetDatabase):
    try:
        exapivalue = NewMoveRequest(username,ArchiveTargetDatabase=ArchiveTargetDatabase,ArchiveOnly=True)
        if (exapivalue['isSuccess']):
            return {'isSuccess':exapivalue['isSuccess'],'message':exapivalue['message']}
        else:
            return {'isSuccess':exapivalue['isSuccess'],'message':exapivalue['msg']}
    except Exception as e :
        return {'isSuccess': False, 'message': str(e)}
    # url=iisurl()+'/api/ad/NewMoveArchive'
    # value = {
    #     "username":username,
    #     "ArchiveTargetDatabase":ArchiveTargetDatabase,
    #     "skey":'A8C4D656BBBB2C42436B4B9B45FC63AD'
    # }
    # querystring = parse.urlencode(value)
    # u = request.urlopen(url + '?' + querystring).read().decode('utf-8')
    # respjson = json.loads(u)
    # return respjson



##获取邮箱用户mapi pop 功能
def PGetCasMailbox(username):
    try:
        exapivalue = GetCasMailboxhight(username)
        if (exapivalue['isSuccess']):
            return {'isSuccess':exapivalue['isSuccess'],'message':exapivalue['message'][0]}
        else:
            return {'isSuccess':exapivalue['isSuccess'],'message':exapivalue['msg']}
    except Exception as e :
        return {'isSuccess': False, 'message': str(e)}
    # url=iisurl()+'/api/ad/GetCasMailbox'
    # value = {
    #     "mailname":username,
    #     "skey":'A8C4D656BBBB2C42436B4B9B45FC63AD'
    # }
    # querystring = parse.urlencode(value)
    # u = request.urlopen(url + '?' + querystring).read().decode('utf-8')
    # respjson = json.loads(u)
    # return respjson


# 获取pop 手机邮箱状态
class GetCasMailbox(View):
    def get(self, request):
        CountName = request.GET.get('CountName')
        try:
            deluseremai = PGetCasMailbox(CountName)
            if deluseremai['isSuccess']:
                result = {'isSuccess': True, "message": deluseremai['message']}
            else:
                result = {'isSuccess': False, "message": str(deluseremai['message'])}
        except Exception as e:
            result = {'isSuccess': False, "message": str(e)}
        response = HttpResponse()
        response['Content-Type'] = "application/json"
        response.write(json.dumps(result, default=str).encode("UTF-8"))
        return response


##设置邮箱用户mapi pop 功能
def PSetCasMailbox(username,parametername,parametervalue):
    try:
        parametervalue = True if parametervalue == 'true' else (False if parametervalue == 'false' else parametervalue)
        kwargs={}
        kwargs[parametername] = parametervalue
        exapivalue = SetCasMailboxhight(username,**kwargs)
        if (exapivalue['isSuccess']):
            return {'isSuccess':exapivalue['isSuccess'],'message':exapivalue['message']}
        else:
            return {'isSuccess':exapivalue['isSuccess'],'message':exapivalue['msg']}
    except Exception as e :
        return {'isSuccess': False, 'message': str(e)}


    # url=iisurl()+'/api/ad/SetCasMailbox'
    # value = {
    #     "username":username,
    #     "parametername":parametername,
    #     "parametervalue":parametervalue,
    #     "skey":'A8C4D656BBBB2C42436B4B9B45FC63AD'
    # }
    # querystring = parse.urlencode(value)
    # u = request.urlopen(url + '?' + querystring).read().decode('utf-8')
    # respjson = json.loads(u)
    # return respjson

# 设置pop 手机邮箱状态
class SetCasMailbox(View):
    def get(self, request):
        username = request.session.get('username')
        permess = Userperm(username, 'operate')
        if permess['isSuccess']:
            CountName = request.GET.get('CountName')
            parametername = request.GET.get('parametername')
            parametervalue = request.GET.get('parametervalue')
            try:
                deluseremai = PSetCasMailbox(CountName,parametername,parametervalue)
                if deluseremai['isSuccess']:
                    result = {'isSuccess': True, "message": deluseremai['message']}
                else:
                    result = {'isSuccess': False, "message": str(deluseremai['message'])}
            except Exception as e:
                result = {'isSuccess': False, "message": str(e)}
        else:
            result = {'isSuccess': False, "message": '权限不足'}
        insert_log(username, request, str(result['isSuccess']), str(result), '设置pop 手机邮箱状态')
        response = HttpResponse()
        response['Content-Type'] = "application/json"
        response.write(json.dumps(result, default=str).encode("UTF-8"))
        return response


##移除完全访问权限
def RemoveMailboxPermission(username,User,InheritanceType,AccessRights):
    try:
        exapivalue = RemoveMailboxPermissionhight(username,User,InheritanceType=InheritanceType,AccessRights=AccessRights)
        if (exapivalue['isSuccess']):
            return {'isSuccess':exapivalue['isSuccess'],'message':exapivalue['message']}
        else:
            return {'isSuccess':exapivalue['isSuccess'],'message':exapivalue['msg']}
    except Exception as e :
        return {'isSuccess': False, 'message': str(e)}
    # url=iisurl()+'/api/ad/RemoveMailboxPermission'
    # value = {
    #     "mailname":username,
    #     "User":User,
    #     "InheritanceType":InheritanceType,
    #     "AccessRights":AccessRights,
    #     "skey":'A8C4D656BBBB2C42436B4B9B45FC63AD'
    # }
    # querystring = parse.urlencode(value)
    # u = request.urlopen(url + '?' + querystring).read().decode('utf-8')
    # respjson = json.loads(u)
    # return respjson


# 移除完全访问权限
class ReMailboxPermission(View):
    def get(self, request):
        username = request.session.get('username')
        permess = Userperm(username, 'operate')
        if permess['isSuccess']:
            CountName = request.GET.get('CountName')
            User = request.GET.get('User')
            InheritanceType = request.GET.get('InheritanceType')
            AccessRights = request.GET.get('AccessRights')
            try:
                deluseremai = RemoveMailboxPermission(CountName,User,InheritanceType,AccessRights)
                if deluseremai['isSuccess']:
                    result = {'isSuccess': True, "message": deluseremai['message']}
                else:
                    result = {'isSuccess': False, "message": str(deluseremai['message'])}
            except Exception as e:
                result = {'isSuccess': False, "message": str(e)}
        else:
            result = {'isSuccess': False, "message": '权限不足'}
        insert_log(username, request, str(result['isSuccess']), str(result), '除完全访问权限')
        response = HttpResponse()
        response['Content-Type'] = "application/json"
        response.write(json.dumps(result, default=str).encode("UTF-8"))
        return response



#获取完全访问权限信息
def GMailboxPermission(username):
    try:
        exapivalue = getMailboxPermission(username)
        if (exapivalue['isSuccess']):
            return {'Data':{'isSuccess':exapivalue['isSuccess'],'data':exapivalue['message']}}
        else:
            return {'Data':{'isSuccess':exapivalue['isSuccess'],'message':exapivalue['msg']}}
    except Exception as e :
        return {'Data':{'isSuccess': False, 'message': str(e)}}
    # url=iisurl()+'/api/ad/GMailboxPermission'
    # value = {
    #     "mailname":username,
    #     "skey":'A8C4D656BBBB2C42436B4B9B45FC63AD'
    # }
    # querystring = parse.urlencode(value)
    # u = request.urlopen(url + '?' + querystring).read().decode('utf-8')
    # respjson = json.loads(u)
    # return respjson


# 获取完全访问权限信息
class GetPermission(View):
    def get(self, request):
        CountName = request.GET.get('CountName')
        try:
            deluseremai = GMailboxPermission(CountName)
            if deluseremai['Data']['isSuccess']:
                result = {'isSuccess': True, "message": deluseremai['Data']['data']}
            else:
                result = {'isSuccess': False, "message": str(deluseremai['Data']['message'])}
        except Exception as e:
            result = {'isSuccess': False, "message": str(e)}
        response = HttpResponse()
        response['Content-Type'] = "application/json"
        response.write(json.dumps(result, default=str).encode("UTF-8"))
        return response

# 首页表格用户信息获取一些信息的数量
class getallmessagenummber(View):
    def get(self, request):
        idtyes = request.GET.get('idtyes')
        datevalue = request.GET.get('datevalue')
        checkval = request.GET.get('checkval')
        try:
            deluseremai = selectindexmessagedb()
            result = {'isSuccess': True, "message": deluseremai}
        except Exception as e:
            result = {'isSuccess': False, "message": str(e)}
        response = HttpResponse()
        response['Content-Type'] = "application/json"
        response.write(json.dumps(result, default=str).encode("UTF-8"))
        return response

# 首页表格组信息获取一些信息的数量
class getallgroupmessagenummber(View):
    def get(self, request):
        idtyes = request.GET.get('idtyes')
        checkval = request.GET.get('checkval')
        try:
            deluseremai = getgroupdownload(idtyes=idtyes, checkval=checkval)
            if deluseremai['isSuccess']:
                result = {'isSuccess': True, "message": len(deluseremai['message'])}
            else:
                result = {'isSuccess': False, "message": str(deluseremai['message'])}
        except Exception as e:
            result = {'isSuccess': False, "message": str(e)}
        response = HttpResponse()
        response['Content-Type'] = "application/json"
        response.write(json.dumps(result, default=str).encode("UTF-8"))
        return response

# 首页表格邮箱信息获取一些信息的数量
class getallmailmessagenummber(View):
    def get(self, request):
        idtyes = request.GET.get('idtyes')
        checkval = request.GET.get('checkval')
        try:
            deluseremai = getmaildownload(idtyes=idtyes, checkval=checkval)
            if deluseremai['isSuccess']:
                result = {'isSuccess': True, "message": len(deluseremai['message'])}
            else:
                result = {'isSuccess': False, "message": str(deluseremai['message'])}
        except Exception as e:
            result = {'isSuccess': False, "message": str(e)}
        response = HttpResponse()
        response['Content-Type'] = "application/json"
        response.write(json.dumps(result, default=str).encode("UTF-8"))
        return response

# 首页表格计算机信息获取一些信息的数量
class getallcomputermessagenummber(View):
    def get(self, request):
        idtyes = request.GET.get('idtyes')
        datevalue = request.GET.get('datevalue')
        checkval = request.GET.get('checkval')
        try:
            if idtyes == 'N':
                datevalue = datetime.datetime.strptime(
                    (datetime.datetime.now() + datetime.timedelta(days=-int(datevalue))).strftime('%Y-%m-%d'),
                    '%Y-%m-%d')
                mintime = time.mktime(datevalue.timetuple())
                namintime = int(mintime + 11644473600)
                nowTime = lambda: int(round(namintime * 10000000))
                deluseremai = getdownload(idtyes, nowTime(), checkval)
            else:
                deluseremai = getdownload(idtyes, datevalue, checkval)
            # deluseremai = getdownload(idtyes=idtyes, datevalue=datevalue, checkval=checkval)
            if deluseremai['isSuccess']:
                result = {'isSuccess': True, "message": len(deluseremai['message'])}
            else:
                result = {'isSuccess': False, "message": str(deluseremai['message'])}
        except Exception as e:
            result = {'isSuccess': False, "message": str(e)}
        response = HttpResponse()
        response['Content-Type'] = "application/json"
        response.write(json.dumps(result, default=str).encode("UTF-8"))
        return response


#添加完全访问权限信息
def AddMailboxPermission(username,user,parametervalue,parametername):
    try:
        exapivalue = AddMailboxPermissionhight(username,user,parametername=parametername,parametervalue=parametervalue)
        if (exapivalue['isSuccess']):
            return {'isSuccess':exapivalue['isSuccess'],'message':exapivalue['message']}
        else:
            return {'isSuccess':exapivalue['isSuccess'],'message':exapivalue['msg']}
    except Exception as e :
        return {'isSuccess': False, 'message': str(e)}
    # url=iisurl()+'/api/ad/AddMailboxPermission'
    # value = {
    #     "username":username,
    #     "user":user,
    #     "parametervalue":parametervalue,
    #     "parametername":parametername,
    #     "skey":'A8C4D656BBBB2C42436B4B9B45FC63AD'
    # }
    # querystring = parse.urlencode(value)
    # u = request.urlopen(url + '?' + querystring).read().decode('utf-8')
    # respjson = json.loads(u)
    # return respjson

# 添加完全访问权限
class AddPermission(View):
    def get(self, request):
        username = request.session.get('username')
        permess = Userperm(username, 'operate')
        if permess['isSuccess']:
            CountName = request.GET.get('CountName')
            user = request.GET.get('User')
            parametervalue = request.GET.get('parametervalue')
            parametername = request.GET.get('parametername')
            try:
                deluseremai = AddMailboxPermission(CountName,user,parametervalue,parametername)
                if deluseremai['isSuccess']:
                    result = {'isSuccess': True, "message": deluseremai['message']}
                else:
                    result = {'isSuccess': False, "message": str(deluseremai['message'])}
            except Exception as e:
                result = {'isSuccess': False, "message": str(e)}
        else:
            result = {'isSuccess': False, "message": '权限不足'}
        insert_log(username, request, str(result['isSuccess']), str(result), '添加完全访问权限')
        response = HttpResponse()
        response['Content-Type'] = "application/json"
        response.write(json.dumps(result, default=str).encode("UTF-8"))
        return response



#设置群组属性
def SetDistributionGroupold(username,parametervalue,parametername):
    try:
        parametervalue = True if parametervalue == 'true' else (False if parametervalue == 'false' else parametervalue)
        kwargs={}
        kwargs[parametername] = parametervalue
        exapivalue = SetDistributionGroup(username,**kwargs)
        if (exapivalue['isSuccess']):
            return {'isSuccess':exapivalue['isSuccess'],'message':exapivalue['message']}
        else:
            return {'isSuccess':exapivalue['isSuccess'],'message':exapivalue['msg']}
    except Exception as e :
        return {'isSuccess': False, 'message': str(e)}
    # url=iisurl()+'/api/ad/SetDistributionGroup'
    # value = {
    #     "username":username,
    #     "parametervalue":parametervalue,
    #     "parametername":parametername,
    #     "skey":'A8C4D656BBBB2C42436B4B9B45FC63AD'
    # }
    # querystring = parse.urlencode(value)
    # u = request.urlopen(url + '?' + querystring).read().decode('utf-8')
    # respjson = json.loads(u)
    # return respjson

#设置联系人邮箱属性
def SetMailContactapi(username,parametervalue,parametername):
    try:
        parametervalue = '$true' if parametervalue == 'true' else ('$false' if parametervalue == 'false' else parametervalue)
        kwargs = {}
        kwargs[parametername] = parametervalue
        exapivalue = SetMailContactvalue('"' + username + '"',**kwargs)
        if (exapivalue['isSuccess']):
            return {'isSuccess':exapivalue['isSuccess'],'message':exapivalue['message']}
        else:
            return {'isSuccess':exapivalue['isSuccess'],'message':exapivalue['msg']}
    except Exception as e :
        return {'isSuccess': False, 'message': str(e)}
    # url=iisurl()+'/api/ad/SetMailContact'
    # value = {
    #     "username":username,
    #     "parametervalue":parametervalue,
    #     "parametername":parametername,
    #     "skey":'A8C4D656BBBB2C42436B4B9B45FC63AD'
    # }
    # querystring = parse.urlencode(value)
    # u = request.urlopen(url + '?' + querystring).read().decode('utf-8')
    # respjson = json.loads(u)
    # return respjson

#设置群组属性
class SetDistrGroup(View):
    def get(self, request):
        username = request.session.get('username')
        permess = Userperm(username, 'operate')
        if permess['isSuccess']:
            CountName = request.GET.get('CountName')
            parametervalue = request.GET.get('parametervalue')
            parametername = request.GET.get('parametername')
            try:
                deluseremai = SetDistributionGroupold(CountName,parametervalue,parametername)
                if deluseremai['isSuccess']:
                    result = {'isSuccess': True, "message": deluseremai['message']}
                else:
                    result = {'isSuccess': False, "message": str(deluseremai['message'])}
            except Exception as e:
                result = {'isSuccess': False, "message": str(e)}
        else:
            result = {'isSuccess': False, "message": '权限不足'}
        insert_log(username, request, str(result['isSuccess']), str(result), '设置群组属性')
        response = HttpResponse()
        response['Content-Type'] = "application/json"
        response.write(json.dumps(result, default=str).encode("UTF-8"))
        return response

#设置联系人属性
class SetMailContact(View):
    def get(self, request):
        username = request.session.get('username')
        permess = Userperm(username, 'operate')
        if permess['isSuccess']:
            CountName = request.GET.get('CountName')
            parametervalue = request.GET.get('parametervalue')
            parametername = request.GET.get('parametername')
            try:
                deluseremai = SetMailContactapi(CountName,parametervalue,parametername)
                if deluseremai['isSuccess']:
                    result = {'isSuccess': True, "message": deluseremai['message']}
                else:
                    result = {'isSuccess': False, "message": str(deluseremai['message'])}
            except Exception as e:
                result = {'isSuccess': False, "message": str(e)}
        else:
            result = {'isSuccess': False, "message": '权限不足'}
        insert_log(username, request, str(result['isSuccess']), str(result), '设置群组属性')
        response = HttpResponse()
        response['Content-Type'] = "application/json"
        response.write(json.dumps(result, default=str).encode("UTF-8"))
        return response



#添加代理发送权限
def ADMailPermission(username,user,parametervalue,parametername):
    try:
        parametervalue = True if parametervalue == 'true' else (False if parametervalue == 'false' else parametervalue)
        kwargs = {}
        kwargs[parametername] = parametervalue
        exapivalue = AddADPermission(username,user,**kwargs)
        if (exapivalue['isSuccess']):
            return {'isSuccess':exapivalue['isSuccess'],'message':exapivalue['message']}
        else:
            return {'isSuccess':exapivalue['isSuccess'],'message':exapivalue['msg']}
    except Exception as e :
        return {'isSuccess': False, 'message': str(e)}
    # url=iisurl()+'/api/ad/ADPermission'
    # value = {
    #     "username":username,
    #     "user":user,
    #     "parametervalue":parametervalue,
    #     "parametername":parametername,
    #     "skey":'A8C4D656BBBB2C42436B4B9B45FC63AD'
    # }
    # querystring = parse.urlencode(value)
    # u = request.urlopen(url + '?' + querystring).read().decode('utf-8')
    # respjson = json.loads(u)
    # return respjson


#添加代理发送权限
class AddMailPermission(View):
    def get(self, request):
        username = request.session.get('username')
        permess = Userperm(username, 'operate')
        if permess['isSuccess']:
            CountName = request.GET.get('CountName')
            user = request.GET.get('user')
            parametervalue = request.GET.get('parametervalue')
            parametername = request.GET.get('parametername')
            try:
                deluseremai = ADMailPermission(CountName,user,parametervalue,parametername)
                if deluseremai['isSuccess']:
                    result = {'isSuccess': True, "message": deluseremai['message']}
                else:
                    result = {'isSuccess': False, "message": str(deluseremai['message'])}
            except Exception as e:
                result = {'isSuccess': False, "message": str(e)}
        else:
            result = {'isSuccess': False, "message": '权限不足'}
        insert_log(username, request, str(result['isSuccess']), str(result), '添加代理发送权限')
        response = HttpResponse()
        response['Content-Type'] = "application/json"
        response.write(json.dumps(result, default=str).encode("UTF-8"))
        return response


#获取代理发送权限
def GADPermission(username):
    try:
        exapivalue = getADPermission(username)
        if (exapivalue['isSuccess']):
            return {'Data':{'isSuccess':exapivalue['isSuccess'],'data':exapivalue['message']}}
        else:
            return {'Data':{'isSuccess':exapivalue['isSuccess'],'message':exapivalue['msg']}}
    except Exception as e :
        return {'Data':{'isSuccess': False, 'message': str(e)}}
    # url=iisurl()+'/api/ad/GADPermission'
    # value = {
    #     "mailname":username,
    #     "skey":'A8C4D656BBBB2C42436B4B9B45FC63AD'
    # }
    # querystring = parse.urlencode(value)
    # u = request.urlopen(url + '?' + querystring).read().decode('utf-8')
    # respjson = json.loads(u)
    # return respjson


#获取代理发送权限
class GetADPermission(View):
    def get(self, request):
        CountName = request.GET.get('CountName')
        try:
            deluseremai = GADPermission(CountName)
            if deluseremai['Data']['isSuccess']:
                result = {'isSuccess': True, "message": deluseremai['Data']['data']}
            else:
                result = {'isSuccess': False, "message": str(deluseremai['Data']['message'])}
        except Exception as e:
            result = {'isSuccess': False, "message": str(e)}
        response = HttpResponse()
        response['Content-Type'] = "application/json"
        response.write(json.dumps(result, default=str).encode("UTF-8"))
        return response


#移除代理发送权限
def RemoveADPermission(username,user,parametername,parametervalue,parameternameo,parametervalueo):
    try:
        parametervalue = True if parametervalue == 'true' else (False if parametervalue == 'false' else parametervalue)
        parametervalueo = True if parametervalueo == 'true' else (False if parametervalueo == 'false' else parametervalueo)
        kwargs = {}
        kwargs[parametername] = parametervalue
        kwargs[parameternameo] = parametervalueo
        exapivalue = RemoveADPermissionhight(username,user,**kwargs)
        if (exapivalue['isSuccess']):
            return {'isSuccess':exapivalue['isSuccess'],'message':exapivalue['message']}
        else:
            return {'isSuccess':exapivalue['isSuccess'],'message':exapivalue['msg']}
    except Exception as e :
        return {'isSuccess': False, 'message': str(e)}
    # url=iisurl()+'/api/ad/RemoveADPermission'
    # value = {
    #     "username":username,
    #     "user":user,
    #     "parametername":parametername,
    #     "parametervalue":parametervalue,
    #     "parameternameo":parameternameo,
    #     "parametervalueo":parametervalueo,
    #     "skey":'A8C4D656BBBB2C42436B4B9B45FC63AD'
    # }
    # querystring = parse.urlencode(value)
    # u = request.urlopen(url + '?' + querystring).read().decode('utf-8')
    # respjson = json.loads(u)
    # return respjson


#移除代理发送权限
class RemovePermission(View):
    def get(self, request):
        username = request.session.get('username')
        permess = Userperm(username, 'operate')
        if permess['isSuccess']:
            CountName = request.GET.get('CountName')
            user = request.GET.get('user')
            parametername = request.GET.get('parametername')
            parametervalue = request.GET.get('parametervalue')
            parameternameo = request.GET.get('parameternameo')
            parametervalueo = request.GET.get('parametervalueo')
            try:
                deluseremai = RemoveADPermission(CountName,user,parametername,parametervalue,parameternameo,parametervalueo)
                if deluseremai['isSuccess']:
                    result = {'isSuccess': True, "message": deluseremai['message']}
                else:
                    result = {'isSuccess': False, "message": str(deluseremai['message'])}
            except Exception as e:
                result = {'isSuccess': False, "message": str(e)}
        else:
            result = {'isSuccess': False, "message": '权限不足'}
        insert_log(username, request, str(result['isSuccess']), str(result), '添加代理发送权限')
        response = HttpResponse()
        response['Content-Type'] = "application/json"
        response.write(json.dumps(result, default=str).encode("UTF-8"))
        return response



#开通邮箱群组
def PEnDistributionGroup(username):
    try:
        exapivalue = EnableDistributionGroup(username,username)
        if (exapivalue['isSuccess']):
            return {'isSuccess':exapivalue['isSuccess'],'message':'开通成功'}
        else:
            return {'isSuccess':exapivalue['isSuccess'],'message':exapivalue['msg']}
    except Exception as e :
        return {'isSuccess': False, 'message': str(e)}
    # url=iisurl()+'/api/ad/EnDistributionGroup'
    # value = {
    #     "mailname":username,
    #     "skey":'A8C4D656BBBB2C42436B4B9B45FC63AD'
    # }
    # querystring = parse.urlencode(value)
    # u = request.urlopen(url + '?' + querystring).read().decode('utf-8')
    # respjson = json.loads(u)
    # return respjson


# 开通邮箱群组
class EnDistributionGroup(View):
    def get(self, request):
        username = request.session.get('username')
        permess = Userperm(username, 'operate')
        if permess['isSuccess']:
            CountName = request.GET.get('CountName')
            try:
                deluseremai = PEnDistributionGroup(CountName)
                if deluseremai['isSuccess']:
                    result = {'isSuccess': True, "message": deluseremai['message']}
                else:
                    result = {'isSuccess': False, "message": str(deluseremai['message'])}
            except Exception as e:
                result = {'isSuccess': False, "message": str(e)}
        else:
            result = {'isSuccess': False, "message":'权限不足'}
        insert_log(username, request, str(result['isSuccess']), str(result), '开通邮箱群组')
        response = HttpResponse()
        response['Content-Type'] = "application/json"
        response.write(json.dumps(result, default=str).encode("UTF-8"))
        return response

# 移动存档
class MOUserMailArchive(View):
    def get(self, request):
        username = request.session.get('username')
        permess = Userperm(username, 'operate')
        if permess['isSuccess']:
            CountName = request.GET.get('CountName')
            DBName = request.GET.get('DBName')
            try:
                deluseremai = NewMoveArchive(CountName, DBName)
                if deluseremai['isSuccess']:
                    result = {'isSuccess': True, "message": '创建成功'}
                else:
                    result = {'isSuccess': False, "message": str(deluseremai['message'])}
            except Exception as e:
                result = {'isSuccess': False, "message": str(e)}
        else:
            result = {'isSuccess': False, "message": '权限不足'}
        insert_log(username, request, str(result['isSuccess']), str(result), '移动存档')
        response = HttpResponse()
        response['Content-Type'] = "application/json"
        response.write(json.dumps(result, default=str).encode("UTF-8"))
        return response

# 创建用户邮箱接口
class SetUserMail(View):
    def get(self, request):
        username = request.session.get('username')
        permess = Userperm(username, 'operate')
        if permess['isSuccess']:
            CountName = request.GET.get('CountName')
            DBName = request.GET.get('DBName')
            try:
                deluseremai = UserToExc(CountName, DBName)
                if deluseremai['isSuccess']:
                    result = {'isSuccess': True, "message": '创建成功'}
                else:
                    result = {'isSuccess': False, "message": str(deluseremai['message'])}
            except Exception as e:
                result = {'isSuccess': False, "message": str(e)}
        else:
            result = {'isSuccess': False, "message": '权限不足'}
        insert_log(username, request, str(result['isSuccess']), str(result), '创建用户邮箱接口')
        response = HttpResponse()
        response['Content-Type'] = "application/json"
        response.write(json.dumps(result, default=str).encode("UTF-8"))
        return response


##新建联系人加邮箱
def NewMailContact(name,dName,smtpvalue,ou):
    try:
        exapivalue = NewMailContacthight(dName,'SMTP:'+smtpvalue,OrganizationalUnit=ou,Alias=name)
        if (exapivalue['isSuccess']):
            return {'isSuccess':exapivalue['isSuccess'],'message':exapivalue['message']}
        else:
            return {'isSuccess':exapivalue['isSuccess'],'message':exapivalue['msg']}
    except Exception as e :
        return {'isSuccess': False, 'message': str(e)}
    # url=iisurl()+'/api/ad/NewMailContact'
    # value = {
    #     "name":name,
    #     "dName":dName,
    #     "smtpvalue":smtpvalue,
    #     "ou":ou,
    #     "skey":'A8C4D656BBBB2C42436B4B9B45FC63AD'
    # }
    # querystring = parse.urlencode(value)
    # u = request.urlopen(url + '?' + querystring).read().decode('utf-8')
    # respjson = json.loads(u)
    # return respjson

# 新建用户联系人
class SetContactMail(View):
    def get(self, request):
        username = request.session.get('username')
        permess = Userperm(username, 'operate')
        if permess['isSuccess']:
            Name = request.GET.get('Name')
            dName = request.GET.get('disName')
            smtpvalue = request.GET.get('SmtpValue')
            ou = request.GET.get('OU')
            try:
                deluseremai = NewMailContact(Name,dName,smtpvalue, ou)
                if deluseremai['isSuccess']:
                    result = {'isSuccess': True, "message": '创建成功'}
                else:
                    result = {'isSuccess': False, "message": str(deluseremai['message'])}
            except Exception as e:
                result = {'isSuccess': False, "message": str(e)}
        else:
            result = {'isSuccess': False, "message": '权限不足'}
        insert_log(username, request, str(result['isSuccess']), str(result), '新建用户联系人')
        response = HttpResponse()
        response['Content-Type'] = "application/json"
        response.write(json.dumps(result, default=str).encode("UTF-8"))
        return response

# 新建用户联系人
class EnableMailContact(View):
    def get(self, request):
        username = request.session.get('username')
        permess = Userperm(username, 'operate')
        if permess['isSuccess']:
            mailname = request.GET.get('mailname')
            ExternalEmailAddress = request.GET.get('ExternalEmailAddress')
            try:
                deluseremai = EnableMailContactapi(mailname,ExternalEmailAddress)
                if deluseremai['Data']['isSuccess']:
                    result = {'isSuccess': True, "message": '创建成功'}
                else:
                    result = {'isSuccess': False, "message": str(deluseremai['Data']['message'])}
            except Exception as e:
                result = {'isSuccess': False, "message": str(e)}
        else:
            result = {'isSuccess': False, "message": '权限不足'}
        insert_log(username, request, str(result['isSuccess']), str(result), '新建用户联系人')
        response = HttpResponse()
        response['Content-Type'] = "application/json"
        response.write(json.dumps(result, default=str).encode("UTF-8"))
        return response


##开启联系人加邮箱
def EnMailContact(name,dn,smtpvalue):
    try:
        exapivalue = EnableMailContacthight(dn,smtpvalue,Alias=name)
        if (exapivalue['isSuccess']):
            return {'isSuccess':exapivalue['isSuccess'],'message':exapivalue['message']}
        else:
            return {'isSuccess':exapivalue['isSuccess'],'message':exapivalue['msg']}
    except Exception as e :
        return {'isSuccess': False, 'message': str(e)}
    # url=iisurl()+'/api/ad/EnMailContact'
    # value = {
    #     "name":name,
    #     "dn":dn,
    #     "smtpvalue":smtpvalue,
    #     "skey":'A8C4D656BBBB2C42436B4B9B45FC63AD'
    # }
    # querystring = parse.urlencode(value)
    # u = request.urlopen(url + '?' + querystring).read().decode('utf-8')
    # respjson = json.loads(u)
    # return respjson


#开启联系人邮箱
class EnContactMail(View):
    def get(self, request):
        username = request.session.get('username')
        permess = Userperm(username, 'operate')
        if permess['isSuccess']:
            Name = request.GET.get('Name')
            dnName = request.GET.get('dnName')
            smtpvalue = request.GET.get('SmtpValue')
            try:
                deluseremai = EnMailContact(Name,dnName,smtpvalue)
                if deluseremai['isSuccess']:
                    result = {'isSuccess': True, "message": '开通成功'}
                else:
                    result = {'isSuccess': False, "message": str(deluseremai['message'])}
            except Exception as e:
                result = {'isSuccess': False, "message": str(e)}
        else:
            result = {'isSuccess': False, "message": '权限不足'}
        insert_log(username, request, str(result['isSuccess']), str(result), '开启联系人邮箱')
        response = HttpResponse()
        response['Content-Type'] = "application/json"
        response.write(json.dumps(result, default=str).encode("UTF-8"))
        return response

# s删除smtp
class EmUserSmtp(View):
    def get(self, request):
        username = request.session.get('username')
        permess = Userperm(username, 'operate')
        if permess['isSuccess']:
            CountName = request.GET.get('CountName')
            SmtpValue = request.GET.get('SmtpValue')
            try:
                deluseremai=deluseremailadressapi(CountName,SmtpValue)
                if deluseremai['isSuccess']:
                    result = {'isSuccess': True, "message": '删除成功'}
                else:
                    result = {'isSuccess': False, "message": str(deluseremai['message'])}
            except Exception as e:
                result = {'isSuccess': False, "message": str(e)}
        else:
            result = {'isSuccess': False, "message": '权限不足'}
        insert_log(username, request, str(result['isSuccess']), str(result), '删除smtp')
        response = HttpResponse()
        response['Content-Type'] = "application/json"
        response.write(json.dumps(result, default=str).encode("UTF-8"))
        return response


# 获取邮箱账号信息
class GetMailMessage(View):
    def get(self, request):
        username = request.GET.get('username')
        try:
            retumessage = GetobjectProperty(username)
            retumail = Getusermail(username)
            if retumessage['isSuccess'] == True:
                if retumail['isSuccess'] == True:
                    mailbox = retumessage['message']
                    mailuser = retumail['message']
                    archivemail=Getmailarchive(username)
                    DBcap=getmailboxdatabaseapi(mailbox['Database'])
                    if DBcap['isSuccess']==True:
                        DBmessa=DBcap['message']
                        mailbox['DBProhibitSendQuota']=DBmessa['ProhibitSendQuota']
                        mailbox['DBProhibitSendReceiveQuota']=DBmessa['ProhibitSendReceiveQuota']
                        mailbox['DBIssueWarningQuota']=DBmessa['IssueWarningQuota']
                    if archivemail['isSuccess']:
                        mailuser['ArTotalItemSize']=archivemail['message']
                        result = {'isSuccess': True, "message": dict(mailbox, **mailuser)}
                    else:
                        result = {'isSuccess': True, "message": dict(mailbox, **mailuser)}
                else:
                    mailbox = retumessage['message']
                    result = {'isSuccess': True, "message": mailbox}
            else:
                result = {'isSuccess': False, "message": retumail['message']}
        except Exception as e:
            result = {'isSuccess': False, "message": str(e)}
        response = HttpResponse()
        response['Content-Type'] = "application/json"
        response.write(json.dumps(result, default=str).encode("UTF-8"))
        return response

    def post(self, request):
        username = request.POST.get('username')
        try:
            retumessage=GetobjectProperty(username)
            retumail=Getusermail(username)
            if retumessage['isSuccess']==True :
                if retumail['isSuccess']==True:
                    mailbox = ast.literal_eval(retumessage['message'])
                    mailuser = ast.literal_eval(retumail['message'])
                    result = {'isSuccess': True, "message": dict(mailbox,**mailuser)}
                else:
                    mailbox = ast.literal_eval(retumessage['message'])
                    result = {'isSuccess': True, "message": mailbox}
            else:
                result = {'isSuccess': False, "message": retumail['message']}
        except Exception as e:
            result = {'isSuccess': False, "message": str(e)}
        response = HttpResponse()
        response['Content-Type'] = "application/json"
        response.write(json.dumps(result, default=str).encode("UTF-8"))
        return response

# 获取邮箱DB信息
class GetDBMessage(View):
    def get(self,request):
        try:
            retmessage=getmailboxdatabasenovalue()
            if retmessage['isSuccess']:
                result = {'isSuccess': True, 'message': retmessage['message']}
            else:
                result = {'isSuccess': True, 'message': str(retmessage['message'])}
        except Exception as e:
            result = {'isSuccess': False, "message": str(e)}
        response = HttpResponse()
        response['Content-Type'] = "application/json"
        response.write(json.dumps(result, default=str).encode("UTF-8"))
        return response

# 删除邮箱移动请求
class RemoveUserRequest(View):
    def get(self,request):
        username = request.session.get('username')
        permess = Userperm(username, 'operate')
        if permess['isSuccess']:
            CountName = request.GET.get('CountName')
            try:
                retmessage=RemoveMoveRequest(CountName)
                if retmessage['isSuccess']:
                    result = {'isSuccess': True, 'message': retmessage['message']}
                else:
                    result = {'isSuccess': True, 'message': str(retmessage['message'])}
            except Exception as e:
                result = {'isSuccess': False, "message": str(e)}
        else:
            result = {'isSuccess': False, "message": '权限不足'}
        insert_log(username, request, str(result['isSuccess']), str(result), '删除邮箱移动请求')
        response = HttpResponse()
        response['Content-Type'] = "application/json"
        response.write(json.dumps(result, default=str).encode("UTF-8"))
        return response

# 修改用户账号信息
class ChangeUserMessage(View):
    def get(self, request):
        username = request.session.get('username')
        Attributes = request.GET.get('Attributes')
        if Attributes=='telephoneNumber' or Attributes=='homePhone' or  Attributes=='mobile' or Attributes=='facsimileTelephoneNumber' or Attributes=='pager' or  Attributes=='ipPhone':
            permess = Userperm(username, 'changelw')
        else:
            permess = Userperm(username, 'operate')
        if permess['isSuccess']:
            CountName = request.GET.get('CountName')
            ChangeMessage = request.GET.get('ChangeMessage')
            types=request.GET.get('types')
            try:
                with ldap3RESTARTABLE as conn:
                    CountName = repeace(CountName)
                    if types:
                        ChangeMessagelist = []
                        if ChangeMessage != '':
                            ChangeMessagelist = [ChangeMessage]
                        ChangeAttr = conn.modify(
                            dn=CountName,
                            changes={Attributes: [(MODIFY_REPLACE, [ChangeMessagelist])]})
                        if ChangeAttr:
                            result = {'isSuccess': True, 'message': '重命名or修改属性成功'}
                        else:
                            result = {'isSuccess': False, 'message': '重命名or修改属性失败'}
                    else:
                        conn.search(search_base=ladp3search_base,
                                                search_filter="(&(sAMAccountName="+CountName+")(|(objectCategory=computer)(&(objectCategory=person)(objectClass=user))(objectCategory=group)))",
                                                attributes=['distinguishedName'])
                        result_id = conn.result
                        response_id = conn.response
                        if result_id['result'] == 0:
                            message = response_id[0].get('attributes', '')
                            if message:
                                dnName = message['distinguishedName']
                                ChangeMessagelist = []
                                if ChangeMessage != '':
                                    ChangeMessagelist = [ChangeMessage]
                                ChangeAttr = conn.modify(
                                    dn=dnName,
                                    changes={ Attributes: [(MODIFY_REPLACE, ChangeMessagelist)]})
                                if ChangeAttr:
                                    result = {'isSuccess': True, 'message': '重命名or修改属性成功'}
                                else:
                                    result = {'isSuccess': False, 'message': '重命名or修改属性失败：' + str(result_id)}
                            else:
                                result = {'isSuccess': False, "message": '未查询到信息'}
                        else:
                            result = {'isSuccess': False, "message": '未查询到信息'}
            except Exception as e:
                result = {'isSuccess': False, "message": str(e)}
        else:
            result = {'isSuccess': False, "message": '权限不足'}
        insert_log(username, request, str(result['isSuccess']), str(result), '修改用户账号信息')
        response = HttpResponse()
        response['Content-Type'] = "application/json"
        response.write(json.dumps(result, default=str).encode("UTF-8"))
        return response

    def post(self, request):
        username = request.session.get('username')
        permess = Userperm(username, 'operate')
        if permess['isSuccess']:
            disName = request.POST.get('disName')
            Attributes = request.POST.get('Attributes')
            ChangeMessage = request.POST.get('ChangeMessage')
            try:
                with ldap3RESTARTABLE as conn:
                    ChangeAttr = conn.modify(
                        dn=disName,
                        changes={Attributes: [(MODIFY_REPLACE, [ChangeMessage])]})
                    if ChangeAttr:
                        result = {'isSuccess': True, 'message': '重命名or修改属性成功'}
                    else:
                        result = {'isSuccess': False, 'message': '重命名or修改属性失败：'}
            except Exception as e:
                result = {'isSuccess': False, "message": str(e)}
        else:
            result = {'isSuccess': False, "message": '权限不足'}
        insert_log(username, request, str(result['isSuccess']), str(result), '修改用户账号信息')
        response = HttpResponse()
        response['Content-Type'] = "application/json"
        response.write(json.dumps(result, default=str).encode("UTF-8"))
        return response




#setmailbox权限查询
def setmailboxapi(username,Attributes,parametervalue):
    try:
        parametervalue = True if parametervalue == 'true' else (False if parametervalue == 'false' else parametervalue)
        kwargs = {}
        kwargs[Attributes] = parametervalue
        exapivalue = SetMailbox(username,**kwargs)
        if (exapivalue['isSuccess']):
            return {'isSuccess':exapivalue['isSuccess'],'message':exapivalue['message']}
        else:
            return {'isSuccess':exapivalue['isSuccess'],'message':exapivalue['msg']}
    except Exception as e :
        return {'isSuccess': False, 'message': str(e)}

# setmailbox权限查询
def setmailboxscriptapi(username, script = False, **kwargs):
    try:
        exapivalue = SetMailbox(username, script, **kwargs)
        if (exapivalue['isSuccess']):
            return {'isSuccess': exapivalue['isSuccess'], 'message': exapivalue['message']}
        else:
            return {'isSuccess': exapivalue['isSuccess'], 'message': exapivalue['msg']}
    except Exception as e:
        return {'isSuccess': False, 'message': str(e)}
    # url=iisurl()+'/api/ad/SetMailbox'
    # value = {
    #     "mailname":username,
    #     "parametername":Attributes,
    #     "parametervalue":ChangeMessage,
    #     "skey": 'A8C4D656BBBB2C42436B4B9B45FC63AD'
    # }
    # querystring = parse.urlencode(value)
    # u = request.urlopen(url + '?' + querystring).read().decode('utf-8')
    # respjson = json.loads(u)
    # return respjson



##新增用户smtp地址
def setuseremailadressapi(mailname,smtpValue):
    try:
        parameter = "@{add='" + smtpValue + "'}"
        exapivalue = SetMailboxEmailAddresses(mailname,parameter)
        if (exapivalue['isSuccess']):
            return {'isSuccess':exapivalue['isSuccess'],'message':exapivalue['message']}
        else:
            return {'isSuccess':exapivalue['isSuccess'],'message':exapivalue['msg']}
    except Exception as e :
        return {'isSuccess': False, 'message': str(e)}
    # url=iisurl()+'/api/ad/NSetMailboxsmtp'
    # value = {
    #     "mailname":mailname,
    #     "smtpValue":smtpValue,
    #     "skey": 'A8C4D656BBBB2C42436B4B9B45FC63AD'
    # }
    # querystring = parse.urlencode(value)
    # u = request.urlopen(url + '?' + querystring).read().decode('utf-8')
    # respjson = json.loads(u)
    # return respjson

##新增联系人邮箱smtp地址
def setMailContactaddsmtpapi(mailname,smtpValue):
    try:
        parameter = "@{add='" + smtpValue + "'}"
        exapivalue = SetMailContactvalue("'"+mailname+"'",EmailAddresses=parameter)
        if (exapivalue['isSuccess']):
            return {'isSuccess':exapivalue['isSuccess'],'message':exapivalue['message']}
        else:
            return {'isSuccess':exapivalue['isSuccess'],'message':exapivalue['msg']}
    except Exception as e :
        return {'isSuccess': False, 'message': str(e)}
    # url=iisurl()+'/api/ad/NSetMailContactsmtp'
    # value = {
    #     "mailname":mailname,
    #     "smtpValue":smtpValue,
    #     "skey": 'A8C4D656BBBB2C42436B4B9B45FC63AD'
    # }
    # querystring = parse.urlencode(value)
    # u = request.urlopen(url + '?' + querystring).read().decode('utf-8')
    # respjson = json.loads(u)
    # return respjson

##新增群组smtp地址
def setDistributionGroupsmtpapi(mailname,smtpValue):
    try:
        parameter = "@{add='" + smtpValue + "'}"
        exapivalue = SetDistributionGroup(mailname,True,EmailAddresses=parameter)
        if (exapivalue['isSuccess']):
            return {'isSuccess':exapivalue['isSuccess'],'message':exapivalue['message']}
        else:
            return {'isSuccess':exapivalue['isSuccess'],'message':exapivalue['msg']}
    except Exception as e :
        return {'isSuccess': False, 'message': str(e)}

    # url=iisurl()+'/api/ad/NSetDistributionGroupsmtp'
    # value = {
    #     "mailname":mailname,
    #     "smtpValue":smtpValue,
    #     "skey": 'A8C4D656BBBB2C42436B4B9B45FC63AD'
    # }
    # querystring = parse.urlencode(value)
    # u = request.urlopen(url + '?' + querystring).read().decode('utf-8')
    # respjson = json.loads(u)
    # return respjson


# 修改邮箱信息
class ChangeMailcapacity(View):
    def get(self, request):
        username = request.session.get('username')
        permess = Userperm(username, 'operate')
        if permess['isSuccess']:
            CountName = request.GET.get('CountName')
            UseDatabaseQuotaDefaults = request.GET.get('UseDatabaseQuotaDefaults')
            # 禁止接收发送
            ProhibitSendReceiveQuota = request.GET.get('ProhibitSendReceiveQuota')
            # 禁止发送
            ProhibitSendQuota = request.GET.get('ProhibitSendQuota')
            # 发出警告
            IssueWarningQuota = request.GET.get('IssueWarningQuota')
            # 禁止接收发送容量
            ProhibitSendReceiveQuotamessage = request.GET.get('ProhibitSendReceiveQuotamessage')
            # 禁止发送容量
            ProhibitSendQuotamessage = request.GET.get('ProhibitSendQuotamessage')
            # 发出警告容量
            IssueWarningQuotamessage = request.GET.get('IssueWarningQuotamessage')
            try:
                if UseDatabaseQuotaDefaults == True or UseDatabaseQuotaDefaults == 'true'or UseDatabaseQuotaDefaults == 'True':
                    retmessage=setmailboxapi(CountName,'UseDatabaseQuotaDefaults','$true')
                else:
                    kwargs = {'UseDatabaseQuotaDefaults': '$false'}

                    if ProhibitSendReceiveQuota == True or ProhibitSendReceiveQuota == 'true' or ProhibitSendReceiveQuota == 'True':
                        kwargs['ProhibitSendReceiveQuota'] = ProhibitSendReceiveQuotamessage
                    else:
                        kwargs['ProhibitSendReceiveQuota'] = 'unlimited'

                    if ProhibitSendQuota == True or ProhibitSendQuota == 'true' or ProhibitSendQuota == 'True':
                        kwargs['ProhibitSendQuota'] = ProhibitSendQuotamessage
                    else:
                        kwargs['ProhibitSendQuota'] = 'unlimited'

                    if IssueWarningQuota == True or IssueWarningQuota == 'true' or IssueWarningQuota == 'True':
                        kwargs['IssueWarningQuota'] = IssueWarningQuotamessage
                    else:
                        kwargs['IssueWarningQuota'] = 'unlimited'

                    retmessage = setmailboxscriptapi(CountName, True, **kwargs)
                if retmessage['isSuccess']:
                    result={'isSuccess': True, 'message': '修改属性成功'}
                else:
                    result = {'isSuccess': False, 'message': str(retmessage['message'])}
            except Exception as e:
                result = {'isSuccess': False, "message": str(e)}
        else:
            result = {'isSuccess': False, "message": '权限不足'}
        insert_log(username, request, str(result['isSuccess']), str(result), '修改邮箱信息')
        response = HttpResponse()
        response['Content-Type'] = "application/json"
        response.write(json.dumps(result, default=str).encode("UTF-8"))
        return response
    #
    # def post(self, request):
    #     disName = request.POST.get('disName')
    #     Attributes = request.POST.get('Attributes')
    #     ChangeMessage = request.POST.get('ChangeMessage')
    #     try:
    #         ChangeAttr = ldap3RESTARTABLE.modify(
    #             dn=disName,
    #             changes={Attributes: [(MODIFY_REPLACE, [ChangeMessage])]})
    #         if ChangeAttr:
    #             result = {'isSuccess': True, 'message': '重命名or修改属性成功'}
    #         else:
    #             result = {'isSuccess': False, 'message': '重命名or修改属性失败：'}
    #     except Exception as e:
    #         result = {'isSuccess': False, "message": str(e)}
    #     response = HttpResponse()
    #     response['Content-Type'] = "application/json"
    #     response.write(json.dumps(result, default=str).encode("UTF-8"))
    #     return response


# 修改邮箱信息
class ChangeMail(View):
    def get(self, request):
        username = request.session.get('username')
        permess = Userperm(username, 'operate')
        if permess['isSuccess']:
            CountName = request.GET.get('CountName')
            Attributes = request.GET.get('Attributes')
            ChangeMessage = request.GET.get('ChangeMessage')
            try:
                retmessage=setmailboxapi(CountName,Attributes,ChangeMessage)
                if retmessage['isSuccess']:
                    result={'isSuccess': True, 'message': '修改属性成功'}
                else:
                    result = {'isSuccess': True, 'message': str(retmessage['message'])}
            except Exception as e:
                result = {'isSuccess': False, "message": str(e)}
        else:
            result = {'isSuccess': False, "message": '权限不足'}
        insert_log(username, request, str(result['isSuccess']), str(result), '修改邮箱信息')
        response = HttpResponse()
        response['Content-Type'] = "application/json"
        response.write(json.dumps(result, default=str).encode("UTF-8"))
        return response
    #
    # def post(self, request):
    #     disName = request.POST.get('disName')
    #     Attributes = request.POST.get('Attributes')
    #     ChangeMessage = request.POST.get('ChangeMessage')
    #     try:
    #         ChangeAttr = ldap3RESTARTABLE.modify(
    #             dn=disName,
    #             changes={Attributes: [(MODIFY_REPLACE, [ChangeMessage])]})
    #         if ChangeAttr:
    #             result = {'isSuccess': True, 'message': '重命名or修改属性成功'}
    #         else:
    #             result = {'isSuccess': False, 'message': '重命名or修改属性失败：'}
    #     except Exception as e:
    #         result = {'isSuccess': False, "message": str(e)}
    #     response = HttpResponse()
    #     response['Content-Type'] = "application/json"
    #     response.write(json.dumps(result, default=str).encode("UTF-8"))
    #     return response


# 新增SMTP
class UserSmtpAdd(View):
    def get(self, request):
        username = request.session.get('username')
        permess = Userperm(username, 'operate')
        if permess['isSuccess']:
            CountName = request.GET.get('CountName')
            SmtpValue = request.GET.get('SmtpValue')
            try:
                retmessage=setuseremailadressapi(CountName,SmtpValue)
                if retmessage['isSuccess']:
                    result={'isSuccess': True, 'message': '新增成功'}
                else:
                    result = {'isSuccess': True, 'message': str(retmessage['message'])}
            except Exception as e:
                result = {'isSuccess': False, "message": str(e)}
        else:
            result = {'isSuccess': False, "message": '权限不足'}
        insert_log(username, request, str(result['isSuccess']), str(result), '新增SMTP')
        response = HttpResponse()
        response['Content-Type'] = "application/json"
        response.write(json.dumps(result, default=str).encode("UTF-8"))
        return response

# 新增联系人SMTP
class MailContactSmtpAdd(View):
    def get(self, request):
        username = request.session.get('username')
        permess = Userperm(username, 'operate')
        if permess['isSuccess']:
            CountName = request.GET.get('CountName')
            SmtpValue = request.GET.get('SmtpValue')
            try:
                retmessage=setMailContactaddsmtpapi(CountName,SmtpValue)
                if retmessage['isSuccess']:
                    result={'isSuccess': True, 'message': '新增成功'}
                else:
                    result = {'isSuccess': True, 'message': str(retmessage['message'])}
            except Exception as e:
                result = {'isSuccess': False, "message": str(e)}
        else:
            result = {'isSuccess': False, "message": '权限不足'}
        insert_log(username, request, str(result['isSuccess']), str(result), '新增SMTP')
        response = HttpResponse()
        response['Content-Type'] = "application/json"
        response.write(json.dumps(result, default=str).encode("UTF-8"))
        return response

# 新增邮箱群组SMTP
class setDistributionGroupsmtp(View):
    def get(self, request):
        username = request.session.get('username')
        permess = Userperm(username, 'operate')
        if permess['isSuccess']:
            CountName = request.GET.get('CountName')
            SmtpValue = request.GET.get('SmtpValue')
            try:
                retmessage=setDistributionGroupsmtpapi(CountName,SmtpValue)
                if retmessage['isSuccess']:
                    result={'isSuccess': True, 'message': '新增成功'}
                else:
                    result = {'isSuccess': True, 'message': str(retmessage['message'])}
            except Exception as e:
                result = {'isSuccess': False, "message": str(e)}
        else:
            result = {'isSuccess': False, "message": '权限不足'}
        insert_log(username, request, str(result['isSuccess']), str(result), '新增SMTP')
        response = HttpResponse()
        response['Content-Type'] = "application/json"
        response.write(json.dumps(result, default=str).encode("UTF-8"))
        return response


##NewMoveRequest用户数据库迁移
def NewMoveRequestapi(username,dbname):
    try:
        exapivalue = NewMoveRequest(username,TargetDatabase=dbname,PrimaryOnly=True)
        if (exapivalue['isSuccess']):
            return {'isSuccess':exapivalue['isSuccess'],'message':exapivalue['message']}
        else:
            return {'isSuccess':exapivalue['isSuccess'],'message':exapivalue['msg']}
    except Exception as e :
        return {'isSuccess': False, 'message': str(e)}
    # url=iisurl()+'/api/ad/NewMoveRequest'
    # value = {
    #     "username":username,
    #     "TargetDatabase":dbname,
    #     "skey": 'A8C4D656BBBB2C42436B4B9B45FC63AD'
    # }
    # querystring = parse.urlencode(value)
    # u = request.urlopen(url + '?' + querystring).read().decode('utf-8')
    # respjson = json.loads(u)
    # return respjson



# 用户数据库迁移
class UserDBMove(View):
    def get(self, request):
        username = request.session.get('username')
        permess = Userperm(username, 'operate')
        if permess['isSuccess']:
            CountName = request.GET.get('CountName')
            DBName = request.GET.get('DBName')
            try:
                retmessage=NewMoveRequestapi(CountName,DBName)
                if retmessage['isSuccess']:
                    result={'isSuccess': True, 'message': '已接收移动请求'}
                else:
                    result = {'isSuccess': True, 'message': str(retmessage['message'])}
            except Exception as e:
                result = {'isSuccess': False, "message": str(e)}
        else:
            result = {'isSuccess': False, "message": '权限不足'}
        insert_log(username, request, str(result['isSuccess']), str(result), '用户数据库迁移')
        response = HttpResponse()
        response['Content-Type'] = "application/json"
        response.write(json.dumps(result, default=str).encode("UTF-8"))
        return response
# def getmember(disName):
#     try:
#         ldap3RESTARTABLE.search(search_base=disName,
#                                 search_filter="(&(objectClass=group))",
#                                 search_scope='BASE',
#                                 attributes=['canonicalName','displayName'])
#         result_id = ldap3RESTARTABLE.result
#         response_id = ldap3RESTARTABLE.response
#         if result_id['result'] == 0:
#             message = response_id[0].get('attributes', '')
#             return {'isSuccess': True, 'message': dict(message)}
#         else:
#             return {'isSuccess': False, "message": str(result_id)}
#     except Exception as e:
#         return {'isSuccess': False, "message": str(e)}

# 删除组成员
class DelGroupUser(View):
    def get(self, request):
        username = request.session.get('username')
        permess = Userperm(username, 'operate')
        if permess['isSuccess']:
            GdisName = request.GET.get('GdisName')
            CountName = request.GET.get('CountName')
            objectClass = request.GET.get('objectClass',None)
            try:
                GdisName=repeace(GdisName)
                CountName=repeace(CountName)
                with ldap3RESTARTABLE as conn:
                    if objectClass:

                        remove_members_from_groups_ad = conn.extend.microsoft.remove_members_from_groups(
                            members=CountName, groups=GdisName)
                        if remove_members_from_groups_ad:
                            result = {
                                'isSuccess': True,
                                "message": CountName + "从组移除成功"}
                        else:
                            result = {'isSuccess': False, "message": '其他原因'}
                    else:
                        conn.search(
                            search_base=ladp3search_base,
                            # search_filter="(&(objectCategory=person)(objectClass=user)(sAMAccountName=" + CountName + "))",
                            search_filter='(&(sAMAccountName='+CountName+')(|(objectCategory=computer)(objectCategory=group)(&(objectCategory=person)(objectClass=user))))',
                            attributes=['distinguishedName'],
                        )
                        result_id = conn.result
                        response_id = conn.response
                        if result_id['result'] == 0:
                            message = response_id[0].get('attributes', '')
                            if message:
                                UserDisNanme=message['distinguishedName']
                                remove_members_from_groups_ad = conn.extend.microsoft.remove_members_from_groups(members=UserDisNanme, groups=GdisName)
                                if remove_members_from_groups_ad:
                                    result = {
                                        'isSuccess': True,
                                        "message":  CountName +"从组移除成功"}
                                else:
                                    result = {'isSuccess': False, "message": '其他原因'}
                            else:
                                result = {'isSuccess': False, 'message': '未查询到信息'}
                        else:
                            result = {'isSuccess': False, 'message': '未查询到信息'}
            except Exception as e:
                result = {'isSuccess': False, "message": str(e)}
        else:
            result = {'isSuccess': False, "message": '权限不足'}
        insert_log(username, request, str(result['isSuccess']), str(result), '删除组成员')
        response = HttpResponse()
        response['Content-Type'] = "application/json"
        response.write(json.dumps(result, default=str).encode("UTF-8"))
        return response

    # def post(self, request):
    #     disName = request.POST.get('disName')
    #     Attributes = request.POST.get('Attributes')
    #     ChangeMessage = request.POST.get('ChangeMessage')
    #     try:
    #         with link() as conn:
    #             ChangeAttr = conn.modify(
    #                 dn=disName,
    #                 changes={Attributes: [
    #                     (MODIFY_REPLACE, [ChangeMessage])
    #                 ]
    #                 }
    #             )
    #             if ChangeAttr:
    #                 result = {'isSuccess': True, 'message': '修改属性成功'}
    #             else:
    #                 result = {'isSuccess': False, 'message': '修改属性失败：' + str(conn.result)}
    #     except Exception as e:
    #         result = {'isSuccess': False, "message": str(e)}
    #     response = HttpResponse()
    #     response['Content-Type'] = "application/json"
    #     response.write(json.dumps(result, default=str).encode("UTF-8"))
    #     return response

# 删除组批量成员
class DelGroupUserMore(View):
    def get(self, request):
        username = request.session.get('username')
        permess = Userperm(username, 'operate')
        if permess['isSuccess']:
            GdisName = request.GET.get('CountName')
            CountName = request.GET.getlist('UserMembers')
            try:
                GdisName=repeace(GdisName)
                CountName=repeacelist(CountName)
                with ldap3RESTARTABLE as conn:
                        remove_members_from_groups_ad = conn.extend.microsoft.remove_members_from_groups(
                            members=CountName, groups=GdisName)
                        if remove_members_from_groups_ad:
                            result = {
                                'isSuccess': True,
                                "message": str(CountName) + "从组移除成功"}
                        else:
                            result = {'isSuccess': False, "message": '其他原因'}
            except Exception as e:
                result = {'isSuccess': False, "message": str(e)}
        else:
            result = {'isSuccess': False, "message": '权限不足'}
        insert_log(username, request, str(result['isSuccess']), str(result), '删除组成员')
        response = HttpResponse()
        response['Content-Type'] = "application/json"
        response.write(json.dumps(result, default=str).encode("UTF-8"))
        return response

    # def post(self, request):
    #     disName = request.POST.get('disName')
    #     Attributes = request.POST.get('Attributes')
    #     ChangeMessage = request.POST.get('ChangeMessage')
    #     try:
    #         with link() as conn:
    #             ChangeAttr = conn.modify(
    #                 dn=disName,
    #                 changes={Attributes: [
    #                     (MODIFY_REPLACE, [ChangeMessage])
    #                 ]
    #                 }
    #             )
    #             if ChangeAttr:
    #                 result = {'isSuccess': True, 'message': '修改属性成功'}
    #             else:
    #                 result = {'isSuccess': False, 'message': '修改属性失败：' + str(conn.result)}
    #     except Exception as e:
    #         result = {'isSuccess': False, "message": str(e)}
    #     response = HttpResponse()
    #     response['Content-Type'] = "application/json"
    #     response.write(json.dumps(result, default=str).encode("UTF-8"))
    #     return response

# 清空隶属于组
class EmUserGroup(View):
    def get(self, request):
        username = request.session.get('username')
        permess = Userperm(username, 'operate')
        if permess['isSuccess']:
            CountName = request.GET.get('CountName')
            UserMembers = request.GET.getlist('UserMembers')
            try:
                with ldap3RESTARTABLE as conn:
                    CountName=repeace(CountName)
                    conn.search(
                        search_base=ladp3search_base,
                        # search_filter="(&(objectCategory=person)(objectClass=user)(sAMAccountName=" + CountName + "))",
                        search_filter="(&(sAMAccountName="+CountName+")(|(&(objectCategory=person)(objectClass=user))(objectCategory=computer)(objectCategory=group)))",
                        attributes=['distinguishedName','memberof'],
                    )
                    result_id = conn.result
                    response_id = conn.response
                    if result_id['result'] == 0:
                        message = response_id[0].get('attributes', '')
                        if message:
                            UserDisNanme=message['distinguishedName']
                            if UserMembers:
                                UserMember = UserMembers
                            else:
                                UserMember=message['memberof']
                            remove_members_from_groups_ad = conn.extend.microsoft.remove_members_from_groups(members=UserDisNanme, groups=UserMember)
                            if remove_members_from_groups_ad:
                                result = {
                                    'isSuccess': True,
                                    "message":  CountName +"清空隶属于成功"}
                            else:
                                result = {'isSuccess': False, "message": '其他原因'}
                        else:
                            result = {'isSuccess': False, 'message': '未查询到信息'}
                    else:
                        result = {'isSuccess': False, 'message': '未查询到信息'}
            except Exception as e:
                result = {'isSuccess': False, "message": str(e)}
        else:
            result = {'isSuccess': False, "message": '权限不足'}
        insert_log(username, request, str(result['isSuccess']), str(result), '清空隶属于组')
        response = HttpResponse()
        response['Content-Type'] = "application/json"
        response.write(json.dumps(result, default=str).encode("UTF-8"))
        return response

# 一键清空组成员
class EmGroupAllUser(View):
    def get(self, request):
        username = request.session.get('username')
        permess = Userperm(username, 'operate')
        if permess['isSuccess']:
            CountName = request.GET.get('CountName')
            try:
                with ldap3RESTARTABLE as conn:
                    CountName=repeace(CountName)
                    conn.search(
                        search_base=ladp3search_base,
                        search_filter="(&(objectCategory=group)(sAMAccountName=" + CountName +"))",
                        attributes=['distinguishedName','member'],
                    )
                    result_id = conn.result
                    response_id = conn.response
                    if result_id['result'] == 0:
                        message = response_id[0].get('attributes', '')
                        if message:
                            remove_members_from_groups = conn.modify(message['distinguishedName'], {'member': [(MODIFY_REPLACE, [])]})
                            if remove_members_from_groups:
                                result = {
                                    'isSuccess': True,
                                    "message": '移除组成员成功'}
                            else:
                                result = {'isSuccess': False, "message": '移除组成员失败'}
                        else:
                            result = {'isSuccess': False, 'message': '未查询到信息'}
                    else:
                        result = {'isSuccess': False, 'message': '未查询到信息'}
            except Exception as e:
                result = {'isSuccess': False, "message": str(e)}
        else:
            result = {'isSuccess': False, "message": '权限不足'}
        insert_log(username, request, str(result['isSuccess']), str(result), '一键清空组成员')
        response = HttpResponse()
        response['Content-Type'] = "application/json"
        response.write(json.dumps(result, default=str).encode("UTF-8"))
        return response

# 根据账号添加到组
class AddUserToGroup(View):
    def get(self, request):
        username = request.session.get('username')
        permess=Userperm(username,'operate')
        if permess['isSuccess']:
            CountName = request.GET.get('CountName')
            GdisNameList = request.GET.getlist('GdisNameList')
            try:
                with ldap3RESTARTABLE as conn:
                    CountName = repeace(CountName)
                    group_list=[]
                    conn.search(
                        search_base=ladp3search_base,
                        search_filter="(&(sAMAccountName="+CountName+")(|(&(objectCategory=person)(objectClass=user))(objectCategory=computer)(objectCategory=group)))",
                        attributes=['distinguishedName'],
                    )
                    result_id = conn.result
                    response_id = conn.response
                    if result_id['result'] == 0:
                        message = response_id[0].get('attributes', '')
                        if message:
                            UserDisNanme = message['distinguishedName']
                            for Group in GdisNameList:
                                Group = repeace(Group)
                                conn.search(
                                    search_base=ladp3search_base,
                                    search_filter='(&(objectClass=group) (sAMAccountName=' + Group + '))',
                                    attributes=['distinguishedName'])
                                result_id = conn.result
                                response_id = conn.response
                                if result_id['result'] == 0:
                                    messagegroup = response_id[0].get('attributes', '')
                                    if messagegroup:
                                        group_list.append(messagegroup['distinguishedName'])
                            if group_list:
                                addmembers_from_groups_ad = conn.extend.microsoft.add_members_to_groups(members=UserDisNanme, groups=group_list)
                                if addmembers_from_groups_ad:
                                    result = {'isSuccess': True,"message": CountName + "添加到组成功"}
                                else:
                                    result = {'isSuccess': False, "message": '用户已在组里面或者其他原因'}
                            else:
                                result = {'isSuccess': False, "message": '未查询到组'}
                        else:
                            result = {'isSuccess': False, 'message': '未查询到信息'}
                    else:
                        result = {'isSuccess': False, 'message': '未查询到信息'}
            except Exception as e:
                result = {'isSuccess': False, "message": str(e)}
        else:
            result = {'isSuccess': False, "message": '权限不足'}
        insert_log(username, request, str(result['isSuccess']), str(result), '根据账号添加到组')
        response = HttpResponse()
        response['Content-Type'] = "application/json"
        response.write(json.dumps(result, default=str).encode("UTF-8"))
        return response



# 高级查找
class GetLeaveUser(View):
    def post(self, request):
        username = request.session.get('username')
        searchvalue = request.POST.get('searchvalue')
        NameList = request.POST.getlist('NameList')
        shellvalue=''
        searchvalue = repeace(searchvalue)
        try:
            if searchvalue:
                # shellvalue+='(anr='+searchvalue+')'
                shellvalue+='(|(anr='+searchvalue+')(|(wWWHomePage='+searchvalue+')(physicalDeliveryOfficeName='+searchvalue+')))'
            for i in NameList:
                if i == '禁用':
                    shellvalue+='(&(objectCategory=person)(objectClass=user)(userAccountControl:1.2.840.113556.1.4.803:=2))'
                elif i=='启用':
                    shellvalue+='(&(objectCategory=person)(objectClass=user)(!(userAccountControl:1.2.840.113556.1.4.803:=2)))'
                elif i=='用户':
                    shellvalue+='(&(objectCategory=person)(objectClass=user)(!(objectClass=inetOrgPerson)))'
                elif i=='计算机':
                    shellvalue+='(objectCategory=computer)'
                elif i=='组':
                    shellvalue+='(objectCategory=group)'
                elif i=='截止日期':
                    shellvalue+='(&(objectCategory=person)(objectClass=user)(!(userAccountControl:1.2.840.113556.1.4.803:=65536)))'
                elif i=='无截止日期':
                    shellvalue+='(&(objectCategory=person)(objectClass=user)(userAccountControl:1.2.840.113556.1.4.803:=65536))'
                elif i=='15':
                    shellvalue+='(&(objectCategory=person)(objectClass=user)(!(userAccountControl:1.2.840.113556.1.4.803:=2))(|(lastLogonTimestamp<=131891040000000000)(!(lastLogonTimestamp=*))))'
                elif i=='30':
                    shellvalue+='(&(objectCategory=person)(objectClass=user)(!(userAccountControl:1.2.840.113556.1.4.803:=2))(|(lastLogonTimestamp<=131878080000000000)(!(lastLogonTimestamp=*))))'
                elif i=='60':
                    shellvalue+='(&(objectCategory=person)(objectClass=user)(!(userAccountControl:1.2.840.113556.1.4.803:=2))(|(lastLogonTimestamp<=131852160000000000)(!(lastLogonTimestamp=*))))'
                elif i=='90':
                    shellvalue+='(&(objectCategory=person)(objectClass=user)(!(userAccountControl:1.2.840.113556.1.4.803:=2))(|(lastLogonTimestamp<=131826240000000000)(!(lastLogonTimestamp=*))))'
                elif i=='120':
                    shellvalue+='(&(objectCategory=person)(objectClass=user)(!(userAccountControl:1.2.840.113556.1.4.803:=2))(|(lastLogonTimestamp<=131800320000000000)(!(lastLogonTimestamp=*))))'
                elif i=='180':
                    shellvalue+='(&(objectCategory=person)(objectClass=user)(!(userAccountControl:1.2.840.113556.1.4.803:=2))(|(lastLogonTimestamp<=131748480000000000)(!(lastLogonTimestamp=*))))'
                elif i=='账号已启用但锁定的用户':
                    shellvalue+='(&(objectCategory=person)(objectClass=user)(!(userAccountControl:1.2.840.113556.1.4.803:=2))(lockoutTime>=131904519495100000))'
                elif i == '1' or i=='2' or i=='3'or i == '4'or i == '7' or i=='14' or i=='28':
                    ExpDate=i
                    shellvalue += '(&(&(objectCategory=person)(objectClass=user)(!(userAccountControl:1.2.840.113556.1.4.803:=2)))(&(objectCategory=person)(objectClass=user)(!(userAccountControl:1.2.840.113556.1.4.803:=8388608))(!(userAccountControl:1.2.840.113556.1.4.803:=65536))))'
            if searchvalue and NameList:
                shellvalue = '(&' + shellvalue + ')'
            with ldap3RESTARTABLE as conn:
                if  '1'  in NameList or '2' in NameList or '3'  in NameList or '7'  in NameList or '14' in NameList or '28' in NameList:
                    entry_generator = conn.extend.standard.paged_search(
                        search_base=ladp3search_base,
                        search_filter=shellvalue,
                        search_scope=SUBTREE,
                        attributes=['sAMAccountName',  "distinguishedName", 'description', 'displayName', 'name',
                                    'objectClass', 'userAccountControl', 'lockoutTime','msDS-UserPasswordExpiryTimeComputed', 'displayName', 'mail'],
                        paged_size=1000,
                        generator=True)
                    resultvalue = []
                    for entry in entry_generator:
                        message = entry.get('attributes', '')
                        if message:
                            if message['msDS-UserPasswordExpiryTimeComputed']:
                                try:
                                    date = message['msDS-UserPasswordExpiryTimeComputed'] - 116444736000000000
                                    dateo = time.strftime('%Y-%m-%d', time.localtime(date / 10000000))
                                    dutydatetime = datetime.datetime.strptime(dateo, '%Y-%m-%d')
                                    today = datetime.datetime.strptime(datetime.datetime.now().strftime('%Y-%m-%d'),'%Y-%m-%d')
                                    timeout = (dutydatetime - today).days
                                except Exception as e:
                                    pass
                                if timeout >=0 and timeout<=int(ExpDate):
                                    if 'computer' in message['objectClass']:
                                        message['objectClass'] = '计算机'
                                        userAccountCon = bin(message['userAccountControl'])[-2]
                                        if userAccountCon == '0':
                                            message['userAccountConte'] = '启用'
                                            message['icon'] = '<img src="/static/zTreeStyle/img/Computer.png"> '
                                        else:
                                            message['userAccountConte'] = '禁用'
                                            message['icon'] = '<img src="/static/zTreeStyle/img/computer2.png"> '
                                    elif 'organizationalUnit' in message['objectClass']:
                                        message['objectClass'] = '组织单位'
                                        message['icon'] = '<img src="/static/zTreeStyle/img/ou.png"> '
                                    elif 'container' in message['objectClass']:
                                        message['objectClass'] = '容器'
                                        message['icon'] = '<img src="/static/zTreeStyle/img/ou01.png"> '
                                    elif 'group' in message['objectClass']:
                                        message['objectClass'] = '组'
                                        message['icon'] = '<img src="/static/zTreeStyle/img/group.png"> '
                                    elif 'user' in message['objectClass'] and 'person' in message['objectClass']:
                                        message['objectClass'] = '用户'
                                        userAccountCon = bin(message['userAccountControl'])[-2]
                                        if userAccountCon == '0':
                                            message['userAccountConte'] = '启用'
                                            message['icon'] = '<img src="/static/zTreeStyle/img/user.png"> '
                                        else:
                                            message['userAccountConte'] = '禁用'
                                            message['icon'] = '<img src="/static/zTreeStyle/img/user2.png"> '
                                    elif 'contact' in message['objectClass']:
                                        message['objectClass'] = '联系人'
                                        message['icon'] = '<img src="/static/zTreeStyle/img/user.png"> '
                                    else:
                                        message['objectClass'] = '其他'
                                        message['icon'] = '<img src="/static/zTreeStyle/img/weizi.png"> '
                                    resultvalue.append(dict(message))
                    result = {'isSuccess': True,'count': len(resultvalue), "message": resultvalue}
                else:
                    conn.search(
                        search_base=ladp3search_base,
                        search_filter=shellvalue,
                        attributes=['sAMAccountName', "distinguishedName", 'description', 'displayName', 'name',
                                    'objectClass', 'userAccountControl', 'lockoutTime'],
                    )
                    result_id = conn.result
                    response_id = conn.response
                    if result_id['result'] == 0 or result_id['result'] == 4:
                        message = []
                        for i in response_id:
                            if i.get('attributes'):
                                usemessage = i['attributes']
                                if 'computer' in usemessage['objectClass']:
                                    usemessage['objectClass'] = '计算机'
                                    userAccountCon = bin(usemessage['userAccountControl'])[-2]
                                    if userAccountCon == '0':
                                        usemessage['userAccountConte'] = '启用'
                                        usemessage['icon'] = '<img src="/static/zTreeStyle/img/Computer.png"> '
                                    else:
                                        usemessage['userAccountConte'] = '禁用'
                                        usemessage['icon'] = '<img src="/static/zTreeStyle/img/computer2.png"> '
                                elif 'organizationalUnit' in usemessage['objectClass']:
                                    usemessage['objectClass'] = '组织单位'
                                    usemessage['icon'] = '<img src="/static/zTreeStyle/img/ou.png"> '
                                elif 'container' in usemessage['objectClass']:
                                    usemessage['objectClass'] = '容器'
                                    usemessage['icon'] = '<img src="/static/zTreeStyle/img/ou01.png"> '
                                elif 'group' in usemessage['objectClass']:
                                    usemessage['objectClass'] = '组'
                                    usemessage['icon'] = '<img src="/static/zTreeStyle/img/group.png"> '
                                elif 'user' in usemessage['objectClass'] and 'person' in usemessage['objectClass']:
                                    usemessage['objectClass'] = '用户'
                                    userAccountCon = bin(usemessage['userAccountControl'])[-2]
                                    if userAccountCon == '0':
                                        usemessage['userAccountConte'] = '启用'
                                        usemessage['icon'] = '<img src="/static/zTreeStyle/img/user.png"> '
                                    else:
                                        usemessage['userAccountConte'] = '禁用'
                                        usemessage['icon'] = '<img src="/static/zTreeStyle/img/user2.png"> '
                                elif 'contact' in usemessage['objectClass']:
                                    usemessage['objectClass'] = '联系人'
                                    usemessage['icon'] = '<img src="/static/zTreeStyle/img/user.png"> '
                                else:
                                    usemessage['objectClass'] = '其他'
                                    usemessage['icon'] = '<img src="/static/zTreeStyle/img/weizi.png"> '
                                message.append(dict(usemessage))
                        result = {'isSuccess': True, 'count': len(response_id) - 3, 'message': message}
                    else:
                        result = {'isSuccess': False, "message": result_id}
        except Exception as e:
            print(e)
            result = {'isSuccess': False, 'count': 0,"message": str(e)}

        response = HttpResponse()
        response['Content-Type'] = "application/json"
        response.write(json.dumps(result, default=date_handler).encode("UTF-8"))
        return response





# 根据组添加人员
class AddGroupsTo(View):
    def get(self, request):
        username = request.session.get('username')
        permess = Userperm(username, 'operate')
        if permess['isSuccess']:
            GroupName = request.GET.get('GroupName')
            GdisNameList = request.GET.getlist('GdisNameList')
            try:
                with ldap3RESTARTABLE as conn:
                    GroupName = repeace(GroupName)
                    group_list=[]
                    conn.search(
                        search_base=ladp3search_base,
                        # search_filter="(&(objectCategory=person)(objectClass=user)(sAMAccountName=" + CountName + "))",
                        search_filter="(&(sAMAccountName="+GroupName+")(|(&(objectCategory=person)(objectClass=user))(objectCategory=computer)(objectCategory=group)))",
                        attributes=['distinguishedName'],
                    )
                    result_id = conn.result
                    response_id = conn.response
                    if result_id['result'] == 0:
                        message = response_id[0].get('attributes', '')
                        if message:
                            UserDisNanme = message['distinguishedName']
                            for Group in GdisNameList:
                                Group = repeace(Group)
                                conn.search(
                                    search_base=ladp3search_base,
                                    search_filter="(&(sAMAccountName=" + Group + ")(|(&(objectCategory=person)(objectClass=user))(objectCategory=computer)(objectCategory=group)))",
                                    attributes=['distinguishedName'])
                                result_id = conn.result
                                response_id = conn.response
                                if result_id['result'] == 0:
                                    messagegroup = response_id[0].get('attributes', '')
                                    if messagegroup:
                                        group_list.append(messagegroup['distinguishedName'])
                            if group_list:
                                addmembers_from_groups_ad = conn.extend.microsoft.add_members_to_groups(members=group_list, groups=UserDisNanme)
                                if addmembers_from_groups_ad:
                                    result = {'isSuccess': True,"message": "添加到组成功"}
                                else:
                                    result = {'isSuccess': False, "message": '用户已在组里面或者其他原因'}
                            else:
                                result = {'isSuccess': False, "message": '未查询到组'}
                        else:
                            result = {'isSuccess': False, 'message': '未查询到信息'}
                    else:
                        result = {'isSuccess': False, 'message': '未查询到信息'}
            except Exception as e:
                result = {'isSuccess': False, "message": str(e)}
        else:
            result = {'isSuccess': False, "message": '权限不足'}
        insert_log(username, request, str(result['isSuccess']), str(result), '根据组添加人员')
        response = HttpResponse()
        response['Content-Type'] = "application/json"
        response.write(json.dumps(result, default=str).encode("UTF-8"))
        return response

# #重置密码方法
# class ChangePassword(View):
#     def get(self, request):
#         CountName = request.GET.get('CountName')
#         password = request.GET.get('password')
#         Npassword = request.GET.get('Npassword')
#         try:
#             CountName=repeace(CountName)
#             if password ==Npassword:
#                 ldap3RESTARTABLE.search(
#                     search_base='DC=,DC=com',
#                     search_filter="(&(objectCategory=person)(objectClass=user)(sAMAccountName=" +CountName +"))",
#                     attributes=['distinguishedName','memberof'],
#                 )
#                 result_id = ldap3RESTARTABLE.result
#                 response_id = ldap3RESTARTABLE.response
#                 if result_id['result'] == 0:
#                     message = response_id[0].get('attributes', '')
#                     if message:
#                         UserDisNanme = message['distinguishedName']
#                         if 'Domain Admins' in message['memberof'] or 'Enterprise Admins' in message['memberof'] :
#                             result = {'isSuccess': False, 'message': '无法重置此账号的密码'}
#                         else:
#                             modify_password = ldap3RESTARTABLE.extend.microsoft.modify_password(UserDisNanme['distinguishedName'], password)
#                             if modify_password:
#                                 result = {'isSuccess': True,"message": CountName +"：密码修改成功"}
#                             else:
#                                 result = {'isSuccess': False,
#                                           "message": "修改失败：" + str(result_id)}
#                     else:
#                         result = {'isSuccess': False, 'message': '未查询到信息'}
#                 else:
#                     result = {'isSuccess': False, 'message': '未查询到信息'}
#             else:
#                 result = {'isSuccess': False, 'message': '两次密码不一致'}
#         except Exception as e:
#             result = {'isSuccess': False, "message": str(e)}
#         response = HttpResponse()
#         response['Content-Type'] = "application/json"
#         response.write(json.dumps(result, default=str).encode("UTF-8"))
#         return response
#
#     def post(self, request):
#         CountName = request.POST.get('CountName')
#         password = request.POST.get('password')
#         Npassword = request.POST.get('Npassword')
#         try:
#             if password == Npassword:
#                 ldap3RESTARTABLE.search(
#                     search_base='DC=,DC=com',
#                     search_filter="(&(objectCategory=person)(objectClass=user)(sAMAccountName=" + CountName + "))",
#                     attributes=['distinguishedName', 'memberof'],
#                 )
#                 result_id = ldap3RESTARTABLE.result
#                 response_id = ldap3RESTARTABLE.response
#                 if result_id['result'] == 0:
#                     message = response_id[0].get('attributes', '')
#                     if message:
#                         UserDisNanme = message['distinguishedName']
#                         print(UserDisNanme)
#                         print(message['memberof'])
#                         if 'CN=Schema Admins,CN=Users,DC=,DC=com' in message['memberof'] or 'CN=Enterprise Admins,CN=Users,DC=,DC=com' in message['memberof']:
#                             result = {'isSuccess': False, 'message': '无法重置此账号的密码'}
#                         else:
#                             modify_password = ldap3RESTARTABLE.extend.microsoft.modify_password(UserDisNanme, password)
#                             if modify_password:
#                                 result = {'isSuccess': True, "message": CountName + "：密码修改成功"}
#                             else:
#                                 result = {'isSuccess': False,
#                                           "message": "修改失败：" + str(result_id)}
#                     else:
#                         result = {'isSuccess': False, 'message': '未查询到信息'}
#                 else:
#                     result = {'isSuccess': False, 'message': '未查询到信息'}
#             else:
#                 result = {'isSuccess': False, 'message': '两次密码不一致'}
#         except Exception as e:
#             result = {'isSuccess': False, "message": str(e)}
#         response = HttpResponse()
#         response['Content-Type'] = "application/json"
#         response.write(json.dumps(result, default=str).encode("UTF-8"))
#         return response

#修改DN
class ChangeDN(View):
    def get(self, request):
        username = request.session.get('username')
        permess = Userperm(username, 'operate')
        if permess['isSuccess']:
            CountName = request.GET.get('CountName')
            newName = request.GET.get('newName')
            objectClass = request.GET.get('objectClass',None)
            try:
                with ldap3RESTARTABLE as conn:
                    CountName=repeace(CountName)
                    conn.search(
                        search_base=ladp3search_base,
                        search_filter='(sAMAccountName=' + CountName + ")",
                    )
                    result_id = conn.result
                    response_id = conn.response
                    if result_id['result'] == 0:
                        message = response_id[0].get('dn', '')
                        if message:
                            if objectClass == ["top", "organizationalUnit"]:
                                cn = "OU=" + newName
                            else:
                                cn = "CN=" + newName
                            if conn.modify_dn(message,cn):
                                result = {"isSuccess": True, "message": CountName + ',重命名成功'}
                            else:
                                result = {"isSuccess": False, "message": CountName + ',重命名失败'}
                        else:
                            result = {"isSuccess": False, "message": CountName + ',重命名失败，没有获取到数据'}
                    else:
                        result = {'isSuccess': False, 'message': '未查询到信息'}

            except Exception as e:
                result = {'isSuccess': False, "message": str(e)}
        else:
            result = {'isSuccess': False, "message": '权限不足'}
        insert_log(username, request, str(result['isSuccess']), str(result), '修改DN')
        response = HttpResponse()
        response['Content-Type'] = "application/json"
        response.write(json.dumps(result, default=str).encode("UTF-8"))
        return response

#修改账号过期时间
class ChangeaccountExpires(View):
    def get(self, request):
        username = request.session.get('username')
        permess = Userperm(username, 'operate')
        if permess['isSuccess']:
            CountName = request.GET.get('CountName')
            accountExpires = request.GET.get('accountExpires')
            try:
                with ldap3RESTARTABLE as conn:
                    CountName=repeace(CountName)
                    conn.search(
                        search_base=ladp3search_base,
                        search_filter="(&(objectCategory=person)(objectClass=user)(sAMAccountName=" +CountName +"))",
                        attributes=['distinguishedName'],
                    )
                    result_id = conn.result
                    response_id = conn.response
                    if result_id['result'] == 0:
                        message = response_id[0].get('attributes', '')
                        if message:
                            olddate = datetime.datetime.strptime(accountExpires, "%Y-%m-%d %H:%M:%S")  # 将时间字符串转换成datetime.date形式
                            mintime = time.mktime(olddate.timetuple())
                            namintime = int(mintime + 11644473600)
                            nowTime = lambda: int(round(namintime * 10000000))
                            dnName = message['distinguishedName']
                            ChangeAttr = conn.modify(
                                dn=dnName,
                                changes={'accountExpires': [(MODIFY_REPLACE, [nowTime()])]})
                            if ChangeAttr:
                                result = {'isSuccess': True, 'message': '修改成功'}
                            else:
                                result = {'isSuccess': False, 'message': '修改失败'}
                        else:
                            result = {'isSuccess': False, 'message': '未查询到信息'}
                    else:
                        result = {'isSuccess': False, 'message': '未查询到信息'}

            except Exception as e:
                result = {'isSuccess': False, "message": str(e)}
        else:
            result = {'isSuccess': False, "message": '权限不足'}
        insert_log(username, request, str(result['isSuccess']), str(result), '修改账号过期时间')
        response = HttpResponse()
        response['Content-Type'] = "application/json"
        response.write(json.dumps(result, default=str).encode("UTF-8"))
        return response



#获取密码过期时间
class GetPasswordDate(View):
    def post(self, request):
        try:
            ExpDate = request.POST.get('ExpDate')
            Notice = request.POST.get('Notice')
            with ldap3RESTARTABLE as conn:
                if Notice:
                    username = request.session.get('username')
                    permess = Userperm(username, 'operate')
                    if permess['isSuccess']:
                        entry_generator = conn.extend.standard.paged_search(search_base = ladp3search_base,
                                                                                        search_filter = '(&(&(objectCategory=person)(objectClass=user)(!(userAccountControl:1.2.840.113556.1.4.803:=2)))(&(objectCategory=person)(objectClass=user)(!(userAccountControl:1.2.840.113556.1.4.803:=8388608))(!(userAccountControl:1.2.840.113556.1.4.803:=65536))))',
                                                                                        search_scope = SUBTREE,
                                                                                        attributes=['sAMAccountName', 'msDS-UserPasswordExpiryTimeComputed', 'displayName','mail'],
                                                                                        paged_size = 1000,
                                                                                        generator=True)
                        resultvalue = []
                        for entry in entry_generator:
                            message = entry.get('attributes', '')
                            if message:
                                if message['msDS-UserPasswordExpiryTimeComputed']:
                                    date = message['msDS-UserPasswordExpiryTimeComputed'] - 116444736000000000
                                    dateo = time.strftime('%Y-%m-%d', time.localtime(date / 10000000))
                                    dutydatetime = datetime.datetime.strptime(dateo, '%Y-%m-%d')
                                    today = datetime.datetime.strptime(datetime.datetime.now().strftime('%Y-%m-%d'), '%Y-%m-%d')
                                    timeout = (dutydatetime - today).days
                                    if timeout == int(ExpDate):
                                        dateva = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(date / 10000000))
                                        subject = u'AD邮箱密码过期提醒'
                                        message['passwordtime'] = dateva
                                        message['passwordday'] = ExpDate
                                        template = "sendmail/mail.html"
                                        # send_email_by_template(subject, template, message,[ ''])
                                        resultvalue.append(dict(message))

                        result = {'isSuccess': True, "message": resultvalue}
                    else:
                        result = {'isSuccess': False, "message": '权限不足'}
                else:
                    entry_generator = conn.extend.standard.paged_search(
                        search_base=ladp3search_base,
                        search_filter='(&(&(objectCategory=person)(objectClass=user)(!(userAccountControl:1.2.840.113556.1.4.803:=2)))(&(objectCategory=person)(objectClass=user)(!(userAccountControl:1.2.840.113556.1.4.803:=8388608))(!(userAccountControl:1.2.840.113556.1.4.803:=65536))))',
                        search_scope=SUBTREE,
                        attributes=['sAMAccountName', 'msDS-UserPasswordExpiryTimeComputed', 'displayName', 'mail'],
                        paged_size=1000,
                        generator=True)
                    resultvalue = []
                    for entry in entry_generator:
                        message = entry.get('attributes', '')
                        if message:
                            if message['msDS-UserPasswordExpiryTimeComputed']:
                                date = message['msDS-UserPasswordExpiryTimeComputed'] - 116444736000000000
                                dateo = time.strftime('%Y-%m-%d', time.localtime(date / 10000000))
                                dutydatetime = datetime.datetime.strptime(dateo, '%Y-%m-%d')
                                today = datetime.datetime.strptime(datetime.datetime.now().strftime('%Y-%m-%d'), '%Y-%m-%d')
                                timeout = (dutydatetime - today).days
                                if timeout == int(ExpDate):
                                    dateva = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(date / 10000000))
                                    message['passwordtime'] = dateva
                                    resultvalue.append(dict(message))
                    result = {'isSuccess': True, "message": resultvalue}
        except Exception as e:
            result = {'isSuccess': False, "message": str(e)}
        response = HttpResponse()
        response['Content-Type'] = "application/json"
        response.write(json.dumps(result, default=str).encode("UTF-8"))
        return response

# 修改用户账号信息
class ChangeUserMessagebylist(View):
    def get(self, request):
        username = request.session.get('username')
        permess = Userperm(username, 'changelw')
        if permess['isSuccess']:
            CountName = request.GET.get('CountName')
            Attributes = request.GET.get('Attributes')
            ChangeMessage = request.GET.getlist('ChangeMessage')
            types=request.GET.get('types')
            try:
                CountName = repeace(CountName)
                with ldap3RESTARTABLE as conn:
                    if types:

                        ChangeAttr = conn.modify(
                            dn=CountName,
                            changes={Attributes: [(MODIFY_ADD, [ChangeMessage])]})
                        if ChangeAttr:
                            result = {'isSuccess': True, 'message': '重命名or修改属性成功'}
                        else:
                            result = {'isSuccess': False, 'message': '重命名or修改属性失败'}
                    else:
                        conn.search(search_base=ladp3search_base,
                                                search_filter="(&(sAMAccountName="+CountName+")(|(objectCategory=computer)(&(objectCategory=person)(objectClass=user))(objectCategory=group)))",
                                                attributes=['distinguishedName'])
                        result_id = conn.result
                        response_id = conn.response
                        if result_id['result'] == 0:
                            message = response_id[0].get('attributes', '')
                            if message:
                                dnName = message['distinguishedName']
                                ChangeAttrlastvalue = True
                                ChangeAttrfirstvalue = conn.modify(
                                    dn=dnName,
                                    changes={Attributes: (MODIFY_REPLACE, [])}
                                )
                                if ChangeAttrfirstvalue:
                                    if ChangeMessage:
                                        for i in ChangeMessage:
                                            ChangeAttr = conn.modify(
                                                dn=dnName,
                                                changes={ Attributes: ('MODIFY_ADD', [i])}
                                            )
                                        if ChangeAttrlastvalue:
                                            result = {'isSuccess': True, 'message': '重命名or修改属性成功'}
                                        else:
                                            result = {'isSuccess': False, 'message': '重命名or修改属性失败：' + str(result_id)}
                                    else:
                                        result = {'isSuccess': True, 'message': '重命名or修改属性成功'}
                                else:
                                    result = {'isSuccess': False, 'message': '重命名or修改属性失败：' + str(result_id)}
                            else:
                                result = {'isSuccess': False, "message": '未查询到信息'}
                        else:
                            result = {'isSuccess': False, "message": '未查询到信息'}
            except Exception as e:
                result = {'isSuccess': False, "message": str(e)}
        else:
            result = {'isSuccess': False, "message": '权限不足'}
        insert_log(username, request, str(result['isSuccess']), str(result), '修改用户账号信息')
        response = HttpResponse()
        response['Content-Type'] = "application/json"
        response.write(json.dumps(result, default=str).encode("UTF-8"))
        return response

import io

import xlsxwriter

#邮箱导出
class GetMailDown(View):
    def get(self, request):
        username = request.session.get('username')
        idtyes = request.GET.get('idtyes')
        checkval = request.GET.get('checkval')
        try:
            messagerestual = getmaildownload(idtyes,checkval)
            if messagerestual['isSuccess']:
                output = io.BytesIO()  # 将xlsx数据写入数据流中
                workbook = xlsxwriter.Workbook(output)
                worksheet = workbook.add_worksheet()  # 创建一个工作表对象
                # 定义数据表头列
                datas = messagerestual
                format = workbook.add_format()  # 定义format格式对象
                format.set_border(1)  # 定义format对象单元格边框加粗(1像素)的格式
                format_title = workbook.add_format()  # 定义format_title格式对象
                format_title.set_border(1)  # 定义format_title对象单元格边框加粗(1像素)的格式
                format_title.set_bg_color('#cccccc')  # 定义format_title对象单元格背景颜色为
                # '#cccccc'的格式
                format_title.set_align('center')  # 定义format_title对象单元格居中对齐的格式
                format_title.set_bold()  # 定义format_title对象单元格内容加粗的格式
                format_ave = workbook.add_format()  # 定义format_ave格式对象
                format_ave.set_border(1)  # 定义format_ave对象单元格边框加粗(1像素)的格式
                format_ave.set_num_format('0.00')  # 定义format_ave对象单元格数字类别显示格式
                # 下面分别以行或列写入方式将标题、业务名称、流量数据写入起初单元格，同时引用不同格式对象
                worksheet.set_column('A:G', 19)
                worksheet.set_column('H:I', 10)
                worksheet.set_column('J:L', 35)
                if idtyes == '已启用邮箱的组':
                    title = [u'CN', u'账号', u'显示名称', u'描述', u'邮箱地址', u'类型', u'创建时间', u'修改时间', u'管理者', u'成员人数', u'成员']
                    worksheet.write_row('A1', title, format_title)
                else:
                    title1 = [u'userPrincipalName', u'sAMAccountName', u'cn', u'displayName', u'description',
                              u'mail', u'wWWHomePage', u'physicalDeliveryOfficeName', u'status', u'whenCreated',
                              u'lastLogonTimestamp', u'pwdLastSet']
                    title = [u'*登录名', u'*登录名(Windows 2000以前版本)', u'CN', u'显示名称', u'描述', u'邮箱地址', u'网页栏位', u'办公室栏位',
                             u'状态', u'创建时间', u'登录时间', u'密码设置时间']
                    worksheet.write_row('A1', title1, format_title)
                    worksheet.write_row('A2', title, format_title)
                nowdate = datetime.datetime.now().strftime('%Y-%m-%d')
                if datas['isSuccess']:
                    deatmessage = datas['message']
                    if idtyes=='已启用邮箱的组':
                        row = 1
                        col = 0
                        for data22 in deatmessage:
                            grouptype = (data22['groupType'])
                            if int(grouptype) == 2:
                                data22['groupType'] = '通讯组 - 全局'
                            elif int(grouptype) == 4:
                                data22['groupType'] = '通讯组 - 本地域'
                            elif int(grouptype) == 8:
                                data22['groupType'] = '通讯组 - 通用'
                            elif int(grouptype) == -2147483646:
                                data22['groupType'] = '安全组 - 全局'
                            elif int(grouptype) == -2147483644:
                                data22['groupType'] = '安全组 - 本地域'
                            elif int(grouptype) == -2147483640:
                                data22['groupType'] = '安全组 - 通用'
                            else:
                                data22['groupType'] = '组'
                            worksheet.write_string(row, col, str(data22['cn']))
                            worksheet.write_string(row, col + 1, str(data22['sAMAccountName']))
                            worksheet.write_string(row, col + 2, str(data22['displayName']))
                            worksheet.write_string(row, col + 3, str(data22['description']))
                            worksheet.write_string(row, col + 4, str(data22['mail']))
                            worksheet.write_string(row, col + 5, str(data22['groupType']))
                            worksheet.write_string(row, col + 6, str(data22['whenCreated']))
                            worksheet.write_string(row, col + 7, str(data22['whenChanged']))
                            worksheet.write_string(row, col + 8, str(data22['managedBy']))
                            worksheet.write_string(row, col + 9, str(len(data22['member'])))
                            worksheet.write_string(row, col + 10, str(data22['member']))
                            row += 1
                    else:
                        row = 2
                        col = 0
                        for data22 in deatmessage:
                            userAccountCon = bin(data22['userAccountControl'])[-2]
                            if userAccountCon == '0':
                                data22['userAccountConte'] = '启用'
                            else:
                                data22['userAccountConte'] = '禁用'
                            worksheet.write_string(row, col, str(data22['userPrincipalName']))
                            worksheet.write_string(row, col + 1, str(data22['sAMAccountName']))
                            worksheet.write_string(row, col + 2, str(data22['cn']))
                            worksheet.write_string(row, col + 3, str(data22['displayName']))
                            worksheet.write_string(row, col + 4, str(data22['description']))
                            worksheet.write_string(row, col + 5, str(data22['mail']))
                            worksheet.write_string(row, col + 6, str(data22['wWWHomePage']))
                            worksheet.write_string(row, col + 7, str(data22['physicalDeliveryOfficeName']))
                            worksheet.write_string(row, col + 8, str(data22['userAccountConte']))
                            worksheet.write_string(row, col + 9, str(data22['whenCreated']))
                            worksheet.write_string(row, col + 10, str(data22['lastLogonTimestamp']))
                            worksheet.write_string(row, col + 11, str(data22['pwdLastSet']))
                            row += 1
                    workbook.close()
                    # 将数据流的游标指向起始位置
                    output.seek(0)
                    response = HttpResponse(output.read(),
                                            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
                    response['Content-Disposition'] = 'attachment; filename="{0}{1}.xlsx"'.format(idtyes+'-', nowdate).encode(
                        'utf-8')
                    return response
                else:
                    result = {'isSuccess': False, "message": '暂未查询到数据'}
            else:
                result = {'isSuccess': False, "message":'暂未查询到数据'}
        except Exception as e:
            result = {'isSuccess': False, "message": str(e)}
        insert_log(username, request, str(result['isSuccess']), str(result), '邮箱信息导出')
        response = HttpResponse()
        response['Content-Type'] = "application/json"
        response.write(json.dumps(result, default=str).encode("UTF-8"))
        return response

#邮箱信息
def getmaildownload(idtyes,checkval):
    try:
        if checkval=='true':
            leave='SUBTREE'
        else:
            leave = 'BASE'
        if idtyes=='已启用邮箱的用户':
            searfil='(&(&(objectCategory=person)(objectClass=user))(msExchHomeServerName=*)(mailNickname=*))'
        elif idtyes=='未启用邮箱的用户':
            searfil ='(&(&(objectCategory=person)(objectClass=user))(!(msExchHomeServerName=*))(!(mailNickname=*)))'
        elif idtyes == '已启用邮箱的组':
            searfil = '(&(objectCategory=group)(mailNickname=*))'
        elif idtyes == '已启用IMAP的账户':
            searfil = '(&(&(objectCategory=person)(objectClass=user))(msExchHomeServerName=*)(mailNickname=*)(!(protocolSettings=MAPI§0§§§§§§§)))'
        elif idtyes == '已启用POP3的账户':
            searfil = '(&(&(objectCategory=person)(objectClass=user))(msExchHomeServerName=*)(mailNickname=*)(!(protocolSettings=POP3§0§§§§§§§§§§§)))'
        elif idtyes == '已启用OWA的账户':
            searfil = '(&(&(objectCategory=person)(objectClass=user))(msExchHomeServerName=*)(mailNickname=*)(!(protocolSettings=HTTP§0§1§§§§§§))(!(protocolSettings=OWA§0)))'
        elif idtyes == '已禁用IMAP的账户':
            searfil = '(&(&(objectCategory=person)(objectClass=user))(msExchHomeServerName=*)(mailNickname=*)(protocolSettings=MAPI§0§§§§§§§))'
        elif idtyes == '已禁用POP3的账户':
            searfil = '(&(&(objectCategory=person)(objectClass=user))(msExchHomeServerName=*)(mailNickname=*)(protocolSettings=POP3§0§§§§§§§§§§§))'
        elif idtyes == '已禁用OWA的账户':
            searfil = '(&(&(objectCategory=person)(objectClass=user))(msExchHomeServerName=*)(mailNickname=*)(protocolSettings=HTTP§0§1§§§§§§)(protocolSettings=OWA§0))'
        elif idtyes == '使用默认的数据库存储限制':
            searfil = '(&(&(objectCategory=person)(objectClass=user))(msExchHomeServerName=*)(mailNickname=*)(mDBUseDefaults=TRUE))'
        elif idtyes == '已启用归档账户':
            searfil = '(&(&(objectCategory=person)(objectClass=user))(msExchHomeServerName=*)(mailNickname=*)(msExchArchiveGUID=*))'
        elif idtyes == '已禁用归档账户':
            searfil = '(&(&(objectCategory=person)(objectClass=user))(msExchHomeServerName=*)(mailNickname=*)(!(msExchArchiveGUID=*)))'
        elif idtyes == '不显示在Exchange地址薄的用户':
            searfil = '(&(&(objectCategory=person)(objectClass=user))(msExchHideFromAddressLists=TRUE))'
        with ldap3RESTARTABLE as conn:
            if idtyes=='已启用邮箱的组':
                entry_generator = conn.extend.standard.paged_search(
                    search_base=ladp3search_base,
                    search_filter=searfil,
                    search_scope=leave,
                    attributes=['sn', 'cn', 'sAMAccountName', 'displayName', 'displayName',
                                'description', 'mail', 'whenChanged', 'groupType', 'whenCreated', 'managedBy',
                                'distinguishedName', 'member'],
                    paged_size=1000,
                    generator=True
                )
            else:
                entry_generator=conn.extend.standard.paged_search(
                    search_base=ladp3search_base,
                    search_filter=searfil,
                    search_scope=leave,
                    attributes=['givenName', 'sn', 'cn', 'userPrincipalName', 'sAMAccountName', 'displayName', 'pwdLastSet',
                                'accountExpires',
                                'pwdLastSet',
                                'physicalDeliveryOfficeName',
                                'description',
                                'mail', 'whenChanged', 'accountExpires', 'whenCreated', 'lastLogonTimestamp',
                                'userAccountControl', 'wWWHomePage', 'msDS-UserPasswordExpiryTimeComputed'],
                    paged_size=1000,
                    generator=True
                )
            resultvalue=[]
            for entry in entry_generator:
                message = entry.get('attributes', '')
                if message:
                    resultvalue.append(dict(message))
            result = {'isSuccess': True, 'message': resultvalue}
    except Exception as e:
        print(e)
        result = {'isSuccess': False, "message": str(e)}
    return result

#组导出
class GetGroupDown(View):
    def get(self, request):
        username = request.session.get('username')
        idtyes = request.GET.get('idtyes')
        checkval = request.GET.get('checkval')
        try:
            messagerestual = getgroupdownload(idtyes,checkval)
            if messagerestual['isSuccess']:
                output = io.BytesIO()  # 将xlsx数据写入数据流中
                workbook = xlsxwriter.Workbook(output)
                worksheet = workbook.add_worksheet()  # 创建一个工作表对象
                # 定义数据表头列
                title = [u'CN', u'账号',u'显示名称',u'描述', u'邮箱地址', u'类型', u'创建时间', u'修改时间',u'管理者',u'成员人数',u'成员']
                datas = messagerestual
                format = workbook.add_format()  # 定义format格式对象
                format.set_border(1)  # 定义format对象单元格边框加粗(1像素)的格式
                format_title = workbook.add_format()  # 定义format_title格式对象
                format_title.set_border(1)  # 定义format_title对象单元格边框加粗(1像素)的格式
                format_title.set_bg_color('#cccccc')  # 定义format_title对象单元格背景颜色为
                # '#cccccc'的格式
                format_title.set_align('center')  # 定义format_title对象单元格居中对齐的格式
                format_title.set_bold()  # 定义format_title对象单元格内容加粗的格式
                format_ave = workbook.add_format()  # 定义format_ave格式对象
                format_ave.set_border(1)  # 定义format_ave对象单元格边框加粗(1像素)的格式
                format_ave.set_num_format('0.00')  # 定义format_ave对象单元格数字类别显示格式
                # 下面分别以行或列写入方式将标题、业务名称、流量数据写入起初单元格，同时引用不同格式对象
                worksheet.set_column('A:G', 19)
                worksheet.set_column('H:I', 10)
                worksheet.set_column('J:K', 35)
                worksheet.write_row('A1', title, format_title)
                nowdate = datetime.datetime.now().strftime('%Y-%m-%d')
                if datas['isSuccess']:
                    deatmessage = datas['message']
                    row = 1
                    col = 0
                    for data22 in deatmessage:
                        grouptype = (data22['groupType'])
                        if int(grouptype) == 2:
                            data22['groupType'] = '通讯组 - 全局'
                        elif int(grouptype) == 4:
                            data22['groupType'] = '通讯组 - 本地域'
                        elif int(grouptype) == 8:
                            data22['groupType']='通讯组 - 通用'
                        elif int(grouptype) == -2147483646:
                            data22['groupType'] ='安全组 - 全局'
                        elif int(grouptype) == -2147483644:
                            data22['groupType'] ='安全组 - 本地域'
                        elif int(grouptype) == -2147483640:
                            data22['groupType'] ='安全组 - 通用'
                        else:
                            data22['groupType'] ='组'
                        worksheet.write_string(row, col, str(data22['cn']))
                        worksheet.write_string(row, col + 1, str(data22['sAMAccountName']))
                        worksheet.write_string(row, col + 2, str(data22['displayName']))
                        worksheet.write_string(row, col + 3, str(data22['description']))
                        worksheet.write_string(row, col + 4, str(data22['mail']))
                        worksheet.write_string(row, col + 5, str(data22['groupType']))
                        worksheet.write_string(row, col + 6, str(data22['whenCreated']))
                        worksheet.write_string(row, col + 7, str(data22['whenChanged']))
                        worksheet.write_string(row, col + 8, str(data22['managedBy']))
                        worksheet.write_string(row, col + 9, str(len(data22['member'])))
                        worksheet.write_string(row, col + 10, str(data22['member']))
                        row += 1
                    workbook.close()
                    # 将数据流的游标指向起始位置
                    output.seek(0)
                    response = HttpResponse(output.read(),
                                            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
                    response['Content-Disposition'] = 'attachment; filename="{0}{1}.xlsx"'.format(idtyes+'-', nowdate).encode(
                        'utf-8')
                    return response
                else:
                    result = {'isSuccess': False, "message": '暂未查询到数据'}
            else:
                result = {'isSuccess': False, "message":'暂未查询到数据'}
        except Exception as e:
            result = {'isSuccess': False, "message": str(e)}
        insert_log(username, request, str(result['isSuccess']), str(result), '组导出')
        response = HttpResponse()
        response['Content-Type'] = "application/json"
        response.write(json.dumps(result, default=str).encode("UTF-8"))
        return response

#组信息
def getgroupdownload(idtyes,checkval):
    try:
        if checkval=='true':
            leave='SUBTREE'
        else:
            leave = 'BASE'
        if idtyes=='所有组':
            searfil='(objectCategory=group)'
        elif idtyes=='安全组':
            searfil ='(&(objectCategory=group)(|(groupType=-2147483646)(groupType=-2147483644)(groupType=-2147483640)))'
        elif idtyes == '通讯组':
            searfil = '(&(objectCategory=group)(|(groupType=2)(groupType=4)(groupType=8)))'
        elif idtyes == '没有成员的组':
            searfil = '(&(objectCategory=group)(!(member=*)))'
        with ldap3RESTARTABLE as conn:
            entry_generator=conn.extend.standard.paged_search(
                search_base=ladp3search_base,
                search_filter=searfil,
                search_scope=leave,
                attributes=[ 'sn', 'cn', 'sAMAccountName','displayName','displayName',
                             'description', 'mail','whenChanged','groupType', 'whenCreated','managedBy','distinguishedName','member'],
                paged_size=1000,
                generator=True
            )
            resultvalue=[]
            # elif idtyes=='账号已过期的用户':
            #     for entry in entry_generator:
            #         message = entry.get('attributes', '')
            #         if message:
            #             if str(message['accountExpires']) != '9999-12-31 23:59:59.999999' and str(message['accountExpires']) != '1601-01-01 00:00:00+00:00':
            #                 local_timezone = tzlocal.get_localzone()  # get pytz tzinfo
            #                 utc_time = datetime.datetime.strptime(str(message['accountExpires']), "%Y-%m-%d %H:%M:%S+00:00")
            #                 local_time = utc_time.replace(tzinfo=pytz.utc).astimezone(local_timezone)
            #                 accounttime = local_time.strftime("%Y-%m-%d")
            #                 naccountday=datetime.datetime.strptime(accounttime,'%Y-%m-%d')
            #                 today = datetime.datetime.strptime(datetime.datetime.now().strftime('%Y-%m-%d'), '%Y-%m-%d')
            #                 timeout = (naccountday - today).days
            #                 if timeout <= 0:
            #                     message['accountExpires'] = accounttime
            #                     message['accountExpiresday'] = timeout
            #                     resultvalue.append(dict(message))
            #     result = {'isSuccess': True, 'message': resultvalue}

            for entry in entry_generator:
                message = entry.get('attributes', '')
                if message:
                    resultvalue.append(dict(message))
            result = {'isSuccess': True, 'message': resultvalue}
    except Exception as e:
        print(e)
        result = {'isSuccess': False, "message": str(e)}
    return result

#用户导出
class GetUserDown(View):
    def get(self, request):
        username = request.session.get('username')
        idtyes = request.GET.get('idtyes')
        datecount = request.GET.get('datecount')
        checkval = request.GET.get('checkval')
        try:
            if idtyes=='N':
                datevalue=datetime.datetime.strptime((datetime.datetime.now() + datetime.timedelta(days=-int(datecount))).strftime('%Y-%m-%d'),'%Y-%m-%d')
                mintime = time.mktime(datevalue.timetuple())
                namintime = int(mintime + 11644473600)
                nowTime = lambda: int(round(namintime * 10000000))
                messagerestual=getuserdownload(idtyes,nowTime(),checkval)
            else:
                messagerestual = getuserdownload(idtyes,datecount,checkval)
            if messagerestual['isSuccess']:
                output = io.BytesIO()  # 将xlsx数据写入数据流中
                workbook = xlsxwriter.Workbook(output)
                worksheet = workbook.add_worksheet()  # 创建一个工作表对象
                # 定义数据表头列表
                if idtyes=='密码已过期的用户'or idtyes=='密码某些天之内过期':
                    title1 = [u'userPrincipalName', u'sAMAccountName', u'cn', u'displayName', u'description', u'mail',u'wWWHomePage', u'physicalDeliveryOfficeName', u'status', u'Password expiration days',u'Password expiration time', u'whenCreated']
                    title = [u'*登录名', u'*登录名(Windows 2000以前版本)',u'CN', u'显示名称', u'描述', u'邮箱地址', u'网页栏位', u'办公室栏位', u'状态', u'密码过期天数',u'密码过期时间', u'创建时间']
                elif idtyes=='账号已过期的用户':
                    title1 = [u'userPrincipalName', u'sAMAccountName', u'cn', u'displayName', u'description',u'mail',u'wWWHomePage', u'physicalDeliveryOfficeName', u'status', u'accountExpires', u'whenCreated']
                    title = [u'*登录名', u'*登录名(Windows 2000以前版本)',u'CN',u'显示名称', u'描述', u'邮箱地址', u'网页栏位', u'办公室栏位', u'状态', u'账号过期时间',u'创建时间']
                else:
                    title1 = [u'userPrincipalName', u'sAMAccountName', u'cn', u'displayName', u'description',
                              u'mail', u'wWWHomePage', u'physicalDeliveryOfficeName', u'status', u'whenCreated',
                              u'lastLogonTimestamp',u'pwdLastSet']

                    title = [u'*登录名', u'*登录名(Windows 2000以前版本)',u'CN',u'显示名称',u'描述', u'邮箱地址', u'网页栏位',u'办公室栏位',u'状态', u'创建时间', u'登录时间',u'密码设置时间']
                datas = messagerestual
                format = workbook.add_format()  # 定义format格式对象
                format.set_border(1)  # 定义format对象单元格边框加粗(1像素)的格式
                format_title = workbook.add_format()  # 定义format_title格式对象
                format_title.set_border(1)  # 定义format_title对象单元格边框加粗(1像素)的格式
                format_title.set_bg_color('#cccccc')  # 定义format_title对象单元格背景颜色为
                # '#cccccc'的格式
                format_title.set_align('center')  # 定义format_title对象单元格居中对齐的格式
                format_title.set_bold()  # 定义format_title对象单元格内容加粗的格式
                format_ave = workbook.add_format()  # 定义format_ave格式对象
                format_ave.set_border(1)  # 定义format_ave对象单元格边框加粗(1像素)的格式
                format_ave.set_num_format('0.00')  # 定义format_ave对象单元格数字类别显示格式
                # 下面分别以行或列写入方式将标题、业务名称、流量数据写入起初单元格，同时引用不同格式对象
                worksheet.set_column('A:G', 19)
                worksheet.set_column('H:I', 10)
                worksheet.set_column('J:L', 35)
                worksheet.write_row('A1', title1, format_title)
                worksheet.write_row('A2', title, format_title)
                nowdate = datetime.datetime.now().strftime('%Y-%m-%d')
                if datas['isSuccess']:
                    deatmessage = datas['message']
                    row = 2
                    col = 0
                    if idtyes == '密码已过期的用户' or idtyes=='密码某些天之内过期':
                        for data22 in deatmessage:
                            userAccountCon = bin(data22['userAccountControl'])[-2]
                            if userAccountCon == '0':
                                data22['userAccountConte'] = '启用'
                            else:
                                data22['userAccountConte'] = '禁用'
                            worksheet.write_string(row, col, str(data22['userPrincipalName']))
                            worksheet.write_string(row, col + 1, str(data22['sAMAccountName']))
                            worksheet.write_string(row, col + 2, str(data22['cn']))
                            worksheet.write_string(row, col + 3, str(data22['displayName']))
                            worksheet.write_string(row, col + 4, str(data22['description']))
                            worksheet.write_string(row, col + 5, str(data22['mail']))
                            worksheet.write_string(row, col + 6, str(data22['wWWHomePage']))
                            worksheet.write_string(row, col + 7, str(data22['physicalDeliveryOfficeName']))
                            worksheet.write_string(row, col + 8, str(data22['userAccountConte']))
                            worksheet.write_string(row, col + 9, str(data22['passworday']))
                            worksheet.write_string(row, col + 10, str(data22['passwordtime']))
                            worksheet.write_string(row, col + 11, str(data22['whenCreated']))
                            row += 1
                    elif idtyes=='账号已过期的用户':
                        for data22 in deatmessage:
                            userAccountCon = bin(data22['userAccountControl'])[-2]
                            if userAccountCon == '0':
                                data22['userAccountConte'] = '启用'
                            else:
                                data22['userAccountConte'] = '禁用'
                            worksheet.write_string(row, col, str(data22['userPrincipalName']))
                            worksheet.write_string(row, col+1, str(data22['sAMAccountName']))
                            worksheet.write_string(row, col + 2, str(data22['cn']))
                            worksheet.write_string(row, col + 3, str(data22['displayName']))
                            worksheet.write_string(row, col + 4, str(data22['description']))
                            worksheet.write_string(row, col + 5, str(data22['mail']))
                            worksheet.write_string(row, col + 6, str(data22['wWWHomePage']))
                            worksheet.write_string(row, col + 7, str(data22['physicalDeliveryOfficeName']))
                            worksheet.write_string(row, col + 8, str(data22['userAccountConte']))
                            worksheet.write_string(row, col + 9, str(data22['accountExpires']))
                            worksheet.write_string(row, col + 10, str(data22['whenCreated']))
                            row += 1
                    else:
                        for data22 in deatmessage:
                            userAccountCon = bin(data22['userAccountControl'])[-2]
                            if userAccountCon == '0':
                                data22['userAccountConte'] = '启用'
                            else:
                                data22['userAccountConte'] = '禁用'
                            worksheet.write_string(row, col, str(data22['userPrincipalName']))
                            worksheet.write_string(row, col+1, str(data22['sAMAccountName']))
                            worksheet.write_string(row, col + 2, str(data22['cn']))
                            worksheet.write_string(row, col + 3, str(data22['displayName']))
                            worksheet.write_string(row, col + 4, str(data22['description']))
                            worksheet.write_string(row, col + 5, str(data22['mail']))
                            worksheet.write_string(row, col + 6, str(data22['wWWHomePage']))
                            worksheet.write_string(row, col + 7, str(data22['physicalDeliveryOfficeName']))
                            worksheet.write_string(row, col + 8, str(data22['userAccountConte']))
                            worksheet.write_string(row, col + 9, str(data22['whenCreated']))
                            worksheet.write_string(row, col + 10, str(data22['lastLogonTimestamp']))
                            worksheet.write_string(row, col + 11, str(data22['pwdLastSet']))
                            row += 1
                    workbook.close()
                    # 将数据流的游标指向起始位置
                    output.seek(0)
                    response = HttpResponse(output.read(),
                                            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
                    response['Content-Disposition'] = 'attachment; filename="{0}{1}.xlsx"'.format(idtyes+'-', nowdate).encode(
                        'utf-8')
                    return response
                else:
                    response = HttpResponse(output.read(),
                                            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
                    response['Content-Disposition'] = 'attachment; filename="{0}{1}.xlsx"'.format(idtyes+'-',
                                                                                                  nowdate).encode(
                        'utf-8')
                    return response
            else:
                result = {'isSuccess': False, "message":'暂未查询到数据'}
        except Exception as e:
            result = {'isSuccess': False, "message": str(e)}

        insert_log(username, request, str(result['isSuccess']), str(result), '用户信息导出')
        response = HttpResponse()
        response['Content-Type'] = "application/json"
        response.write(json.dumps(result, default=str).encode("UTF-8"))
        return response


#用户信息
def getuserdownload(idtyes,datevalue,checkval):
    try:
        if checkval=='true':
            leave='SUBTREE'
        else:
            leave = 'BASE'
        if idtyes=='所有用户':
            searfil='(&(objectCategory=person)(objectClass=user)(!(objectClass=inetOrgPerson)))'
        elif idtyes=='密码已过期的用户' or idtyes=='密码某些天之内过期':
            searfil = '(&(&(objectCategory=person)(objectClass=user)(!(userAccountControl:1.2.840.113556.1.4.803:=2)))(&(objectCategory=person)(objectClass=user)(!(userAccountControl:1.2.840.113556.1.4.803:=8388608))(!(userAccountControl:1.2.840.113556.1.4.803:=65536))))'
        elif idtyes == '下次登陆必须更改密码的用户':
            searfil = '(&(pwdLastSet=0)(&(objectCategory=person)(objectClass=user)(!(objectClass=inetOrgPerson))))'
        elif idtyes == '密码永不过期的用户':
            searfil = '(&(&(objectCategory=person)(objectClass=user)(!(objectClass=inetOrgPerson)))(&(objectCategory=person)(objectClass=user)(!(userAccountControl:1.2.840.113556.1.4.803:=8388608))(userAccountControl:1.2.840.113556.1.4.803:=65536)))'
        elif idtyes=='禁用的用户':
            searfil='(&(objectCategory=person)(objectClass=user)(userAccountControl:1.2.840.113556.1.4.803:=2))'
        elif idtyes=='账号已过期的用户':
            olddate = datetime.datetime.now()
            mintime = time.mktime(olddate.timetuple())
            namintime = int(mintime + 11644473600)
            nowTime = lambda: int(round(namintime * 10000000))
            searfil="(&(objectCategory=person)(objectClass=user)(!(accountExpires=0))(!(accountExpires=9223372036854775807))(accountExpires<="+str(nowTime())+"))"
        elif idtyes=='账号某些天之内未登录的账号':
            datevalue1 = datetime.datetime.strptime((datetime.datetime.now() + datetime.timedelta(days=-int(datevalue))).strftime('%Y-%m-%d'), '%Y-%m-%d')
            mintime = time.mktime(datevalue1.timetuple())
            namintime = int(mintime + 11644473600)
            nowTime = lambda: int(round(namintime * 10000000))
            searfil="(&(objectCategory=person)(objectClass=user)(|(lastLogonTimestamp<="+str(nowTime())+")(!(lastLogonTimestamp=*))))"
        elif idtyes=='锁定的用户':
            searfil='(&(objectCategory=person)(objectClass=user)(lockoutTime>=1))'
        with ldap3RESTARTABLE as conn:
            entry_generator = conn.extend.standard.paged_search(
                search_base=ladp3search_base,
                search_filter=searfil,
                search_scope=leave,
                attributes=['givenName', 'sn', 'cn', 'userPrincipalName','sAMAccountName','displayName','pwdLastSet',
                            'accountExpires',
                            'pwdLastSet',
                            'physicalDeliveryOfficeName','distinguishedName',
                            'description',
                            'mail','whenChanged','accountExpires', 'whenCreated','lastLogonTimestamp','userAccountControl','wWWHomePage','msDS-UserPasswordExpiryTimeComputed'],
                paged_size=2000,
                generator=True
            )
            resultvalue=[]
            if idtyes=='密码已过期的用户' or idtyes=='密码某些天之内过期':
                for entry in entry_generator:
                    message = entry.get('attributes', '')
                    if message:
                        if message['msDS-UserPasswordExpiryTimeComputed']:
                            if message['msDS-UserPasswordExpiryTimeComputed'] == 9223372036854775807 or message[
                                'msDS-UserPasswordExpiryTimeComputed'] == 0:
                                pass
                            else:
                                try:

                                    date = message['msDS-UserPasswordExpiryTimeComputed'] - 116444736000000000
                                    dateo = time.strftime('%Y-%m-%d', time.localtime(date / 10000000))
                                    dutydatetime = datetime.datetime.strptime(dateo, '%Y-%m-%d')
                                    today = datetime.datetime.strptime(datetime.datetime.now().strftime('%Y-%m-%d'), '%Y-%m-%d')
                                    timeout = (dutydatetime - today).days
                                except Exception as e:
                                    pass
                                if datevalue:
                                    if timeout >=0 and timeout<=int(datevalue):
                                        dateva = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(date / 10000000))
                                        message['passwordtime'] = dateva
                                        message['passworday'] = timeout
                                        resultvalue.append(dict(message))
                                else:
                                    if timeout <=0:
                                        dateva = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(date / 10000000))
                                        message['passwordtime'] = dateva
                                        message['passworday'] = timeout
                                        resultvalue.append(dict(message))
                result = {'isSuccess': True, 'message': resultvalue}
            elif idtyes=='密码永不过期的用户':
                for entry in entry_generator:
                    message = entry.get('attributes', '')
                    if message:
                        if message['msDS-UserPasswordExpiryTimeComputed'] == 9223372036854775807 or message['msDS-UserPasswordExpiryTimeComputed'] == 0:
                            message['msDSUserPasswordExpiryTimeComputed'] = '密码永不过期'
                            resultvalue.append(dict(message))
                result = {'isSuccess': True, 'message': resultvalue}
            # elif idtyes=='账号已过期的用户':
            #     for entry in entry_generator:
            #         message = entry.get('attributes', '')
            #         if message:
            #             if str(message['accountExpires']) != '9999-12-31 23:59:59.999999' and str(message['accountExpires']) != '1601-01-01 00:00:00+00:00':
            #                 local_timezone = tzlocal.get_localzone()  # get pytz tzinfo
            #                 utc_time = datetime.datetime.strptime(str(message['accountExpires']), "%Y-%m-%d %H:%M:%S+00:00")
            #                 local_time = utc_time.replace(tzinfo=pytz.utc).astimezone(local_timezone)
            #                 accounttime = local_time.strftime("%Y-%m-%d")
            #                 naccountday=datetime.datetime.strptime(accounttime,'%Y-%m-%d')
            #                 today = datetime.datetime.strptime(datetime.datetime.now().strftime('%Y-%m-%d'), '%Y-%m-%d')
            #                 timeout = (naccountday - today).days
            #                 if timeout <= 0:
            #                     message['accountExpires'] = accounttime
            #                     message['accountExpiresday'] = timeout
            #                     resultvalue.append(dict(message))
            #     result = {'isSuccess': True, 'message': resultvalue}
            else:
                for entry in entry_generator:
                    message = entry.get('attributes', '')
                    if message:
                        resultvalue.append(dict(message))
                result = {'isSuccess': True, 'message': resultvalue}
    except Exception as e:
        print(e)
        result = {'isSuccess': False, "message": str(e)}
    return result


#计算机导出
class GetDown(View):
    def get(self, request):
        username = request.session.get('username')
        idtyes = request.GET.get('idtyes')
        datecount = request.GET.get('datecount')
        checkval = request.GET.get('checkval')
        try:
            if idtyes=='N':
                datevalue=datetime.datetime.strptime((datetime.datetime.now() + datetime.timedelta(days=-int(datecount))).strftime('%Y-%m-%d'),'%Y-%m-%d')
                mintime = time.mktime(datevalue.timetuple())
                namintime = int(mintime + 11644473600)
                nowTime = lambda: int(round(namintime * 10000000))
                messagerestual=getdownload(idtyes,nowTime(),checkval)
            else:
                messagerestual = getdownload(idtyes,datecount,checkval)
            if messagerestual['isSuccess']:
                output = io.BytesIO()  # 将xlsx数据写入数据流中
                workbook = xlsxwriter.Workbook(output)
                worksheet = workbook.add_worksheet()  # 创建一个工作表对象
                # 定义数据表头列表
                title = [u'计算机名', u'DNS名称',u'操作系统',u'版本', u'状态', u'创建时间', u'登录时间']
                datas = messagerestual
                format = workbook.add_format()  # 定义format格式对象
                format.set_border(1)  # 定义format对象单元格边框加粗(1像素)的格式
                format_title = workbook.add_format()  # 定义format_title格式对象
                format_title.set_border(1)  # 定义format_title对象单元格边框加粗(1像素)的格式
                format_title.set_bg_color('#cccccc')  # 定义format_title对象单元格背景颜色为
                # '#cccccc'的格式
                format_title.set_align('center')  # 定义format_title对象单元格居中对齐的格式
                format_title.set_bold()  # 定义format_title对象单元格内容加粗的格式
                format_ave = workbook.add_format()  # 定义format_ave格式对象
                format_ave.set_border(1)  # 定义format_ave对象单元格边框加粗(1像素)的格式
                format_ave.set_num_format('0.00')  # 定义format_ave对象单元格数字类别显示格式
                # 下面分别以行或列写入方式将标题、业务名称、流量数据写入起初单元格，同时引用不同格式对象
                worksheet.set_column('A:J', 19)
                worksheet.set_column('B:C', 35)
                worksheet.set_column('F:G', 40)
                worksheet.write_row('A1', title, format_title)
                nowdate = datetime.datetime.now().strftime('%Y-%m-%d')
                if datas['isSuccess']:
                    deatmessage = datas['message']
                    row = 1
                    col = 0
                    for data22 in deatmessage:
                        userAccountCon = bin(data22['userAccountControl'])[-2]
                        if userAccountCon == '0':
                            data22['userAccountConte'] = '启用'
                        else:
                            data22['userAccountConte'] = '禁用'
                        worksheet.write_string(row,col, str(data22['cn']))
                        worksheet.write_string(row, col + 1,str(data22['dNSHostName']))
                        worksheet.write_string(row, col + 2,str(data22['operatingSystem']))
                        worksheet.write_string(row, col + 3,str(data22['operatingSystemVersion']))
                        worksheet.write_string(row, col + 4,str(data22['userAccountConte']))
                        worksheet.write_string(row, col + 5,str(data22['whenCreated']))
                        worksheet.write_string(row, col + 6,str(data22['lastLogonTimestamp']))
                        row += 1
                    workbook.close()
                    # 将数据流的游标指向起始位置
                    output.seek(0)
                    response = HttpResponse(output.read(),
                                            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
                    response['Content-Disposition'] = 'attachment; filename="{0}{1}.xlsx"'.format(idtyes+'-', nowdate).encode(
                        'utf-8')
                    return response
                else:
                    response = HttpResponse(output.read(),
                                            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
                    response['Content-Disposition'] = 'attachment; filename="{0}{1}.xlsx"'.format(idtyes+'-',
                                                                                                  nowdate).encode(
                        'utf-8')
                    return response
            else:
                result = {'isSuccess': False, "message":'暂未查询到数据'}
        except Exception as e:
            result = {'isSuccess': False, "message": str(e)}
        insert_log(username, request, str(result['isSuccess']), str(result), '计算机信息导出')
        response = HttpResponse()
        response['Content-Type'] = "application/json"
        response.write(json.dumps(result, default=str).encode("UTF-8"))
        return response

#计算机信息
def getdownload(idtyes,datevalue,checkval):
    try:
        if checkval=='true':
            leave='SUBTREE'
        else:
            leave = 'BASE'
        if idtyes=='N':
            searfil='(&(objectCategory=computer)(|(lastLogonTimestamp<='+str(datevalue)+')(!(lastLogonTimestamp=*))))'
        elif idtyes=='所有计算机':
            searfil = '(objectCategory=computer)'
        elif idtyes == '启用的计算机':
            searfil = '(&(objectCategory=computer)(!(userAccountControl:1.2.840.113556.1.4.803:=2)))'
        elif idtyes == '禁用的计算机':
            searfil = '(&(objectCategory=computer)(userAccountControl:1.2.840.113556.1.4.803:=2))'
        elif idtyes == '某操作系统的计算机':
            searfil = '(&(operatingSystem=*'+str(datevalue)+'*)(objectCategory=computer))'
        with ldap3RESTARTABLE as conn:
            entry_generator=conn.extend.standard.paged_search(
                search_base=ladp3search_base,
                search_filter=searfil,
                search_scope=leave,
                attributes=['givenName', 'sn', 'cn', 'sAMAccountName','operatingSystemServicePack','operatingSystemVersion',
                            'accountExpires',
                            'dNSHostName',
                            'displayName', 'physicalDeliveryOfficeName',
                            'managedBy', 'description',
                            'memberof', 'operatingSystem', 'lastLogonTimestamp','whenChanged', 'whenCreated','objectClass','userAccountControl'],
                paged_size=1000,
                generator=True
            )
            resultvalue=[]
            for entry in entry_generator:
                message = entry.get('attributes', '')
                if message:
                    resultvalue.append(dict(message))
            result = {'isSuccess': True, 'message': resultvalue}
    except Exception as e:
        result = {'isSuccess': False, "message": str(e)}
    return result