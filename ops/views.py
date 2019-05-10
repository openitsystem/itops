import hashlib
import json
import uuid

import pyotp
import requests
from django.contrib.auth.hashers import check_password, make_password
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, render_to_response

import pypsrp
from pypsrp.powershell import PowerShell, RunspacePool
from pypsrp.wsman import WSMan

# Create your views here.
from ADapi.zapi import ZabbixApi
from dbinfo.Profile import writeprofile, readprofile
from dbinfo.encrypt_decode import encrypt_and_decode
from dbinfo.models import dbinfotest, ldaptest, selectldapdb, insert_ldapmessage, crearldapdb, mailtest, selectmaildb, \
    insert_sendmail, crearmaildb, searchsendmail, selectperdb, insert_userper, crearperdb, selectiisex, creariisdb, insert_expmessage,insert_userper_monitor, insert_userper_zabbix
from dbinfo.views import getldap3configtion, getpermsessage, getliisconfigtion, getskey, insert_log, seargooled, \
    insert_tokenb
from itops.settings import returnadminusernamevalue, ldap3RESTARTABLE, ladp3search_base
from ops.thrcreatmysqltable import creatmysqltable
from permission.therhasindexvalue import startapschedulerscheduler
from permission.views import  verifyuser_login_new


def home(request):
    try:
        return render_to_response('home.html', locals())
    except:
        return render_to_response('home.html', locals())


def login(request):
    startapschedulerscheduler()
    if request.session.get("username"):
        if request.session.get("username").lower() == 'adminportal':
            return HttpResponseRedirect('/basite/', request)
        return HttpResponseRedirect('/home/', request)
    return render_to_response('login.html',locals())



# def basite1(request):
#     username = request.session.get('username')
#     mysqlipvalue = readprofile('mysql','host')
#     mysqlusernamevalue = readprofile('mysql','username')
#     mysqlPortevalue = readprofile('mysql','Port')
#     mysqlPasswordvalue = readprofile('mysql','Password')
#     mysqldatabase = readprofile('mysql','database')
#
#     if mysqlipvalue != 'None'and mysqlipvalue != "" and mysqlipvalue != None:
#         mysqlallvalue = getldap3configtion()
#         myserver=mysqlallvalue.get('server', "None")
#         myuser=mysqlallvalue.get('user', "None")
#         mypassword=mysqlallvalue.get('password', "None")
#         mydomain=mysqlallvalue.get('domain', "None")
#         myusessl=mysqlallvalue.get('use_ssl', "None")
#         mysearch_base=mysqlallvalue.get('search_base', "None")
#         mailvalue=searchsendmail()
#         mascount = mailvalue.get('mailcount', "None")
#         mailpassr = mailvalue.get('password', "None")
#         masrever = mailvalue.get('mailserver', "None")
#         maddress = mailvalue.get('mailaddress', "None")
#         permessa=getpermsessage()
#         perlogn = permessa.get('logongroup', "None")
#         perchangepwd = permessa.get('changepwdgroup', "None")
#         perfile = permessa.get('fieldgroup', "None")
#         perset = permessa.get('operagroup', "None")
#     return render_to_response('basite1.html', locals())


def basite(request):
    username = request.session.get('username')
    mysqlipvalue = readprofile('mysql','host')
    mysqlusernamevalue = readprofile('mysql','username')
    mysqlPortevalue = readprofile('mysql','Port')
    mysqlPasswordvalue = readprofile('mysql','Password')
    mysqldatabase = readprofile('mysql','database')
    if username == returnadminusernamevalue:
        if mysqlipvalue != 'None'and mysqlipvalue != "" and mysqlipvalue != None and mysqlipvalue != False:
            mysqlallvalue = getldap3configtion()
            if mysqlallvalue:
                myserver=mysqlallvalue.get('server', "None")
                myuser=mysqlallvalue.get('user', "None")
                mypassword=mysqlallvalue.get('password', "None")
                mydomain=mysqlallvalue.get('domain', "None")
                myusessl=mysqlallvalue.get('use_ssl', "None")
                mysearch_base=mysqlallvalue.get('search_base', "None")
            else:
                myserver='None'
                myusessl='None'
            # mailvalue=searchsendmail()
            # if mailvalue:
            #     mascount = mailvalue.get('mailcount', "None")
            #     mailpassr = mailvalue.get('password', "None")
            #     masrever = mailvalue.get('mailserver', "None")
            #     maddress = mailvalue.get('mailaddress', "None")
            # else:
            #     masrever='None'
            permessa=getpermsessage()
            if permessa:
                perlogn = permessa.get('logongroup', "None")
                perchangepwd = permessa.get('changepwdgroup', "None")
                perfile = permessa.get('fieldgroup', "None")
                perset = permessa.get('operagroup', "None")
                monitorselect = permessa.get('monitor', "None")
                zabbixurl = permessa.get('zabbixurl', "None")
                zabbixuser = permessa.get('zabbixuser', "None")
                zabbixpassword = permessa.get('zabbixpassword', "None")
            else:
                perlogn='None'
                monitorselect = 'None'
                zabbixurl = 'None'
                zabbixuser = 'None'
                zabbixpassword = 'None'
            iisexx=getliisconfigtion()
            if iisexx:
                exuser = iisexx.get('exuser', "None")
                expassword = iisexx.get('expassword', "None")
                exdomain = iisexx.get('exdomain', "None")
                exip = iisexx.get('exserver', "None")
            else:
                iisserver='None'
                exserver='None'
        else:
            mysqldatabase='None'
        return render_to_response('basise.html',locals())
    else:
        return render_to_response('login.html', locals())

def logout(request):
    request.session.flush()
    return HttpResponseRedirect('/login/', request)



def changadminpwd(request):
    try:
        post = request.POST
        adminoldpwd = post.get("oldpassword")
        adminnewpwd = post.get("newpassword1")
        adminrealnewpwd = post.get("newpassword2")
        username = request.session.get('username')
        if username.lower() == returnadminusernamevalue:
            if adminoldpwd !='' and adminnewpwd != '' and adminrealnewpwd != '':
                if adminnewpwd == adminrealnewpwd:
                    adminoldassword = readprofile('password', 'administratorpassword')
                    if check_password(adminoldpwd, adminoldassword):
                        realpassword = make_password(adminnewpwd)
                        writeprofile("password", "administratorpassword", realpassword)
                        result = {'isSuccess': True, "message": '成功'}
                    else:
                        result = {'isSuccess': False, "message": '旧密码错误'}
                else:
                    result = {'isSuccess': False, "message": '两次密码不一致'}
            else:
                result = {'isSuccess': False, "message": '请填写完整信息'}
        else:
            result = {'isSuccess': False, "message": '权限不足'}
    except Exception as e:
        result = {'isSuccess': False, "message": '出现异常'+str(e)}
    response = HttpResponse()
    response['Content-Type'] = "text/javascript"
    response.write(json.dumps(result))
    return response

# def admd5_skey(skeyvalue):
#     m = hashlib.md5()
#     m.update(skeyvalue.encode() )
#     md5value = m.hexdigest()
#     skey = md5value.upper()
#     return skey

def iisservertest(ip,port):
    try:
        allurl = 'http://'+ip+':'+port+'/api/ad/iisonlinetest'
        u = requests.get(allurl)
        data = u.json()
        return  True
    except Exception as e:
        return  False
#
# def saveiisservertest(ip,port,**kwargs):
#     try:
#         allurl = 'http://'+ip+':'+port+'//api/ad/OnLineTest'
#         u = requests.get(allurl,params=kwargs)
#         data = u.json()
#         return  data
#     except Exception as e:
#         return  False


#exchange测试
def exservertest(**kwargs):
    try:
        wsman = WSMan(server=kwargs['exip'], port=80, path="/powershell/",ssl=False,username=kwargs['domain'] + "\\" + kwargs['exaccount'] , password=kwargs['expassword'],auth="basic",encryption='never')
        with RunspacePool(wsman, configuration_name="Microsoft.Exchange") as pool:
            ps = PowerShell(pool).add_cmdlet('Get-ExchangeServer')
            output = ps.invoke()
            if not ps.had_errors and not ps.streams.error:
                data = {'isSuccess':True}
            else:
                data = {'isSuccess':False}
        # allurl = 'http://'+getskey()['iisserver']+':'+getskey()['iisport']+'//api/ad/testexlink'
        # u = requests.get(allurl,params=kwargs)
        # data = u.json()
        return  data
    except Exception as e:
        return  False
# #xIIS信息配置
# def iislinktest(request):
#     post = request.POST
#     iisinputip = post.get("iisinputip")
#     iisinputport = post.get("iisinputport")
#     skeyvalue = admd5_skey(str(uuid.uuid4()))
#     insert_iisekey(skeyvalue)
#     if iisservertest(iisinputip,iisinputport):
#         if saveiisservertest(iisinputip,iisinputport,server=readprofile('mysql','host'),Database=readprofile('mysql','database'),PORT=readprofile('mysql','port'),Uid=readprofile('mysql','username'),password=readprofile('mysql','password'),skey=skeyvalue):
#             if selectiisex():
#                 if insert_iisexpmessage(iisinputip,iisinputport) == ():
#                     result = {'isSuccess': True, "message": '成功'}
#                 else:
#                     result = {'isSuccess': False, "message": '数据写入失败'}
#             else:
#                 if creariisdb() == ():
#                     if insert_iisexpmessage(iisinputip,iisinputport) == ():
#                         result = {'isSuccess': True, "message": '成功'}
#                     else:
#                         result = {'isSuccess': False, "message": '数据写入失败'}
#                 else:
#                     result = {'isSuccess': False, "message": '表格创建失败'}
#         else:
#             result = {'isSuccess': False, "message": '数据验证失败'}
#     else:
#         result = {'isSuccess': False, "message": 'iis连接失败'}
#     response = HttpResponse()
#     response['Content-Type'] = "text/javascript"
#     response.write(json.dumps(result))
#     return response


#ex测试
def exlinktest(request):
    post = request.POST
    exinputip = post.get("exinputip")
    exinputaccount = post.get("exinputaccount")
    exinputpassword = post.get("exinputpassword")
    exinputdomain = post.get("exinputdomain")
    password = encrypt_and_decode().encrypted_text(exinputpassword)
    exapitestvalue = exservertest(exip=exinputip,exaccount=exinputaccount,expassword=exinputpassword,domain=exinputdomain)
    if exapitestvalue and ('isSuccess' in exapitestvalue):
        if exapitestvalue['isSuccess']:
            if insert_expmessage(exinputip,exinputaccount,password,exinputdomain)==():
                result = {'isSuccess': True, "message": '成功'}
            else:
                result = {'isSuccess': False, "message": '写入失败'}
        else:
            result = {'isSuccess': False, "message": '测试失败'}
    else:
        result = {'isSuccess': False, "message": '测试失败'}
    response = HttpResponse()
    response['Content-Type'] = "text/javascript"
    response.write(json.dumps(result))
    return response

#数据库测试连接
def mysqltest(request):
    host = request.POST.get('host')
    database = request.POST.get('database')
    DBUser = request.POST.get('DBUser')
    password = request.POST.get('password')
    port = request.POST.get('port')
    try:
        username = request.session.get('username')
        if username == returnadminusernamevalue:
            if dbinfotest(host,DBUser, password, port,database):
                try:
                    # dir_now = os.path.dirname(os.path.abspath("settings.py"))
                    writeprofile("mysql", "host", host)
                    writeprofile("mysql", "username", DBUser)
                    writeprofile("mysql", "Password", encrypt_and_decode().encrypted_text(password))
                    writeprofile("mysql", "Port", port)
                    writeprofile("mysql", "database", database)
                    creatmysqltable()# 创建mysql数据库的一些表格
                    result = {'isSuccess': True, "message": '成功'}
                except:
                    result = {'isSuccess': False, "message": '出现异常'}
            else:
                result = {'isSuccess': False, "message": '连接失败'}
        else:
            result = {'isSuccess': False, "message": '连接失败'}
    except Exception as e:
        result = {'isSuccess': True, "message": str(e)}
    response = HttpResponse()
    response['Content-Type'] = "text/javascript"
    response.write(json.dumps(result))
    return response

#ldap测试连接
def adldaptest(request):
    adip = request.POST.get('adip')
    domian = request.POST.get('domian')
    aduser = request.POST.get('aduser')
    adpassword = request.POST.get('adpassword')
    adserchbase = request.POST.get('adserchbase')
    sele = request.POST.get('sele')
    try:
        username = request.session.get('username')
        if username == returnadminusernamevalue:
            if ldaptest(adip,aduser, adpassword,sele):
                try:
                    if selectldapdb():
                        if insert_ldapmessage(domian, adip, aduser, encrypt_and_decode().encrypted_text(adpassword), adserchbase, sele)==():
                            result = {'isSuccess': True, "message": '成功'}
                        else:
                            result = {'isSuccess': False, "message": '数据写入失败'}
                    else:
                        if crearldapdb()==():
                            if insert_ldapmessage(domian, adip, aduser, encrypt_and_decode().encrypted_text(adpassword), adserchbase, sele)==():
                                result = {'isSuccess': True, "message": '成功'}
                            else:
                                result = {'isSuccess': False, "message": '数据写入失败'}
                        else:
                            result = {'isSuccess': False, "message": '表格创建失败'}
                except:
                    result = {'isSuccess': False, "message": '出现异常'}
            else:
                result = {'isSuccess': False, "message": '连接失败'}
        else:
            result = {'isSuccess': False, "message": '权限不足'}
    except Exception as e:
        result = {'isSuccess': False, "message": str(e)}
    response = HttpResponse()
    response['Content-Type'] = "text/javascript"
    response.write(json.dumps(result))
    return response

# 判断zabbix URL;账户;密码相关
def testZabbix(zabbixurl,zabbixuser,zabbixpassword):
    try:
        zapi = ZabbixApi(zabbixurl=zabbixurl, zabbixuser=zabbixuser, zabbixpassword=zabbixpassword)
        token = zapi.authenticate()
        if token:
            return True
        else:
            return False
    except Exception as e:
        return False

# 重启uwsgi 服务
def restartuwsgi(request):
    try:
        username = request.session.get('username')
        if username == returnadminusernamevalue:
            try:
                import uwsgi
                uwsgi.reload()
                insert_log(username, request, 'True', str('restartuwsgi'), '重启 uwsgi服务 成功')
                result = {'isSuccess': True, "message": '重启 uwsgi服务 成功'}
            except Exception as e:
                insert_log(username, request, 'False', str('restartuwsgi'), '重启 uwsgi服务 失败'+str(e))
                result = {'isSuccess': False, "message": '重启 uwsgi服务 失败'+str(e)}
        else:
            result = {'isSuccess': False, "message": '权限不足'}
    except Exception as e:
        result = {'isSuccess': False, "message": str(e)}
    response = HttpResponse()
    response['Content-Type'] = "text/javascript"
    response.write(json.dumps(result))
    return response

#邮箱信息保存
def sendmailtest(request):
    mailladdress = request.POST.get('mailladdress')
    inputmail = request.POST.get('inputmail')
    mailpassword = request.POST.get('mailpassword')
    mailserver = request.POST.get('mailserver')
    try:
        username = request.session.get('username')
        if username == returnadminusernamevalue:
            if mailtest(mailladdress,inputmail,mailpassword,mailserver,mailladdress):
                try:
                    if selectmaildb():
                        if insert_sendmail(inputmail, encrypt_and_decode().encrypted_text(mailpassword), mailserver, mailladdress)==():
                            result = {'isSuccess': True, "message": '成功'}
                        else:
                            result = {'isSuccess': False, "message": '数据写入失败'}
                    else:
                        if crearmaildb()==():
                            if insert_sendmail(inputmail, encrypt_and_decode().encrypted_text(mailpassword), mailserver, mailladdress)==():
                                result = {'isSuccess': True, "message": '成功'}
                            else:
                                result = {'isSuccess': False, "message": '数据写入失败'}
                        else:
                            result = {'isSuccess': False, "message": '表格创建失败'}
                except:
                    result = {'isSuccess': False, "message": '出现异常'}
            else:
                result = {'isSuccess': False, "message": '连接失败'}
        else:
            result = {'isSuccess': False, "message": '权限不足'}
    except Exception as e:
        result = {'isSuccess': False, "message": str(e)}
    response = HttpResponse()
    response['Content-Type'] = "text/javascript"
    response.write(json.dumps(result))
    return response

#用户信息保存 权限组相关
def permsetest(request):
    logongroup = request.POST.get('logongroup')
    changpwdgr = request.POST.get('changpwdgr')
    changfiled = request.POST.get('changfiled')
    setopert = request.POST.get('setopert')
    permsetest_post = request.POST
    try:
        username = request.session.get('username')
        if username == returnadminusernamevalue:
            with ldap3RESTARTABLE as conn:
                try:
                    # 判断填写的栏位在AD中是否有对应的组
                    logingr_dn_list = []
                    per_dn_list = []
                    for per in permsetest_post:
                        conn.search(search_base=ladp3search_base, search_filter='(&(objectClass=group)(sAMAccountName=' + permsetest_post[per] + '))')
                        result_per = conn.result
                        response_per = conn.response
                        per_dn = response_per[0].get('dn', '')
                        if per_dn:
                            if per == 'logongroup':
                                logingr_dn_list.append(per_dn)
                            else:
                                per_dn_list.append(per_dn)
                        else:
                            result = {'isSuccess': False, "message": per+'栏位填写错误,找不到这个组 或 重启服务'}
                            insert_log(username, request, str(result['isSuccess']), str(result), '')
                            response = HttpResponse()
                            response['Content-Type'] = "text/javascript"
                            response.write(json.dumps(result))
                            return response
                        # 判断是否有相关数据表，没有则创建UserPer表
                    if not selectperdb():
                        if crearperdb() == ():
                            insert_log(username, request, str('true'), str('crearperdb'), '创建UserPer表')
                        else:
                            result = {'isSuccess': False, "message": '表格创建失败'}
                            insert_log(username, request, str(result['isSuccess']), str(result), '')
                            response = HttpResponse()
                            response['Content-Type'] = "text/javascript"
                            response.write(json.dumps(result))
                            return response
                    # 查询数据库，如果里面有权限组数据，则移除登陆组成员中的其他组
                    # 这一步 报错只记录数据库
                    try:
                        permessa = getpermsessage()
                        if permessa:
                            login_group_dn_list = []
                            per_group_dn_list = []
                            for i in permessa:
                                conn.search(
                                    search_base=ladp3search_base,
                                    search_filter="(&(objectCategory=group)(sAMAccountName=" + permessa[i] + "))",
                                    search_scope='SUBTREE',
                                )
                                result_id = conn.result
                                response_id = conn.response
                                group_dn = response_id[0].get('dn', '')
                                if group_dn:
                                    if i == 'logongroup':
                                        login_group_dn_list.append(group_dn)
                                    else:
                                        per_group_dn_list.append(group_dn)
                            if login_group_dn_list and per_group_dn_list:
                                remove_member = conn.extend.microsoft.remove_members_from_groups(members=per_group_dn_list, groups=login_group_dn_list)
                                insert_log(username, request, str(remove_member), str('remove_members_from_groups'), str({"members":per_group_dn_list, 'groups':login_group_dn_list}))
                    except Exception as e:
                        insert_log(username, request, 'false', str(e), '查询数据库，如果里面有权限组数据，则移除登陆组成员中的其他组')
                    # 在新登陆组成员中 ，加入新的组
                    add_members = conn.extend.microsoft.add_members_to_groups(members=per_dn_list, groups=logingr_dn_list)
                    insert_log(username, request, str(add_members), str('add_members_to_groups'), str({"members":per_dn_list, 'groups':logingr_dn_list}))
                    # 写数据库
                    if insert_userper(logongroup, changpwdgr, changfiled, setopert) == ():
                        result = {'isSuccess': True, "message": '成功'}
                    else:
                        result = {'isSuccess': False, "message": '数据写入失败'}
                except:
                    result = {'isSuccess': False, "message": '出现异常'}
        else:
            result = {'isSuccess': False, "message": '权限不足'}
    except Exception as e:
        result = {'isSuccess': False, "message": str(e)+"或 重启服务"}
    insert_log(username, request, str(result['isSuccess']), str(result), '')
    response = HttpResponse()
    response['Content-Type'] = "text/javascript"
    response.write(json.dumps(result))
    return response


#用户登录
def userlogin(request):
    post = request.POST
    username = post.get("Username")
    password = post.get("Password")
    try:
        if username:
            if password:
                if username.lower() == returnadminusernamevalue:
                    adminoldassword =readprofile('password','administratorpassword')
                    if check_password(password, adminoldassword):
                        request.session['username'] = returnadminusernamevalue
                        request.session['displayname'] = '超级管理员'
                        result = {'code': 3, "message": '/basite/'}
                    else:
                        result = {'code': 2, "message": '密码错误'}
                else:
                    loginvalue = verifyuser_login_new(username, password)
                    if loginvalue['isSuccess'] == True:
                        gotken=seargooled(username.lower())
                        if gotken:
                            result = {'code': 0, "message": {'username': loginvalue['message']['sAMAccountName'], 'displayname': loginvalue['message']['displayName']}}
                            response = HttpResponse()
                            response['Content-Type'] = "text/javascript"
                            response.write(json.dumps(result))
                            return response
                        else:
                            result = {'code': 1, "message": '未绑定'}
                            response = HttpResponse()
                            response['Content-Type'] = "text/javascript"
                            response.write(json.dumps(result))
                            return response
                        # return HttpResponseRedirect(returnbackurl, request)
                    else:
                        # return render_to_response("login.html", {'message': loginvalue['message']})
                        result = {'code': 2, "message": loginvalue['message']}
            else:
                result = {'code': 2, "message": '请填写密码'}
        else:
            result = {'code': 2, "message": '请填写用户名'}
    except Exception as e:
        print(e)
        result = {'code': 2, "message": '出现异常'}
    response = HttpResponse()
    response['Content-Type'] = "text/javascript"
    response.write(json.dumps(result))
    return response


def logingotok(request):
    post = request.POST
    username = post.get("Username")
    disname = post.get("disname")
    otpcode = post.get("otpcode")
    returnbackurl = request.session.get("returnbackurl")
    try:
        if not returnbackurl or returnbackurl==r'/' or returnbackurl==r'/login/':
            returnbackurl = r'/home/'
        gotken = seargooled(username.lower())
        if str(generate_otp(gotken[0]['token'])) == str(otpcode):
            request.session['username'] = username
            request.session['displayname'] = disname
            request.session['returnbackurl'] = ''
            result = {'isSuccess': True, "message": '验证成功','backurl': returnbackurl}
        else:
            result = {'isSuccess': False, "message": '验证失败'}
    except Exception as e:
        print(e)
        result = {'isSuccess': False, "message": '验证失败'}
    response = HttpResponse()
    response['Content-Type'] = "text/javascript"
    response.write(json.dumps(result))
    return response


#生成二维码
def gootokenpng(request):
    nameuser = request.POST.get('searchvalue')
    try:
        miyue=random_base32()
        goinamge=pyotp.totp.TOTP(miyue).provisioning_uri(nameuser)
        result = {'isSuccess': True, "message": goinamge,'miyue':miyue}
    except Exception as e:
        result = {'isSuccess': True, "message": str(e)}
    response = HttpResponse()
    response['Content-Type'] = "text/javascript"
    response.write(json.dumps(result))
    return response


#验证
def verificationtok(request):
    sixcount = request.POST.get('sixcount')
    mikey = request.POST.get('mikey')
    nameuser = request.POST.get('searchvalue')
    try:
        if str(generate_otp(mikey))==str(sixcount):
            insert_tokenb(nameuser,mikey)
            result = {'isSuccess': True, "message": '验证成功'}
        else:
            result = {'isSuccess': False, "message": '验证成功'}
    except Exception as e:
        result = {'isSuccess': True, "message": str(e)}
    response = HttpResponse()
    response['Content-Type'] = "text/javascript"
    response.write(json.dumps(result))
    return response

import base64
import hashlib
import hmac
import time
import datetime
import random as _random

def byte_secret(secret):
    missing_padding = len(secret) % 8
    if missing_padding != 0:
        secret += '=' * (8 - missing_padding)
    return base64.b32decode(secret, casefold=True)

def int_to_bytestring(i, padding=8):
    result = bytearray()
    while i != 0:
        result.append(i & 0xFF)
        i >>= 8
    return bytes(bytearray(reversed(result)).rjust(padding, b'\0'))

#根据约定的密钥计算当前动态密码
def generate_otp(secret):
    for_time = datetime.datetime.now()
    i = time.mktime(for_time.timetuple())
    input =  int(i / 30)
    digest = hashlib.sha1
    digits = 6
    if input < 0:
        raise ValueError('input must be positive integer')
    hasher = hmac.new(byte_secret(secret),int_to_bytestring(input),digest)
    hmac_hash = bytearray(hasher.digest())
    offset = hmac_hash[-1] & 0xf
    code = ((hmac_hash[offset] & 0x7f) << 24 |
            (hmac_hash[offset + 1] & 0xff) << 16 |
            (hmac_hash[offset + 2] & 0xff) << 8 |
            (hmac_hash[offset + 3] & 0xff))
    str_code = str(code % 10 ** digits)
    while len(str_code) < digits:
        str_code = '0' + str_code
    return str_code

#随机生成一个base32密钥
def random_base32(length=16, random=_random.SystemRandom(),
                  chars=list('ABCDEFGHIJKLMNOPQRSTUVWXYZ234567')):
    return ''.join(
        random.choice(chars)
        for _ in range(length)
    )