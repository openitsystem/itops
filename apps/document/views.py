# -*- coding: utf-8 -*-
# @Time    : 2019/2/1 11:24
# @Author  : 
import json
from django.shortcuts import render_to_response
from django.http import HttpResponse
from datetime import datetime


from dbinfo.views import findadmintable, onedeltable, onefindadmintablenoreplace, \
    savemessa, insert_log, searmessid, upsaves, saveearromessa, finderromintable, searmesserrid, upsaveerr, derroltable
from permission.views import Userperm


#datetime类型转换string
class DatetimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if obj:
            if isinstance(obj, (datetime, obj)):
                return obj.strftime('%Y-%m-%d %H:%M:%S')
            raise TypeError("Type %s not serializable" % type(obj))


# 故障回溯页面
def projects(request):
    username = request.session.get('username')
    if username:
        return render_to_response('document/projects.html', locals())
    else:
        return render_to_response('login.html', locals())


def creatproject(request):
    username = request.session.get('username')
    if username:
        return render_to_response('document/creatproject.html', locals())
    else:
        return render_to_response('login.html', locals())

def faultproject(request):
    username = request.session.get('username')
    if username:
        return render_to_response('document/faultproject.html', locals())
    else:
        return render_to_response('login.html', locals())
def findproject(request):
    username = request.session.get('username')
    if username:
        return render_to_response('document/findproject.html', locals())
    else:
        return render_to_response('login.html', locals())


# 查找数据库 所有故障回溯
def findallprojects(request):
    username = request.session.get('username')
    textvalue = findadmintable()
    respjson = { 'textvalues': textvalue}
    response = HttpResponse()
    response['Content-Type'] = "text/javascript"
    response.write(json.dumps(respjson, cls=DatetimeEncoder).encode("UTF-8"))
    return response

# 查找故障回溯
def finderroprojects(request):
    username = request.session.get('username')
    textvalue = finderromintable()
    respjson = { 'textvalues': textvalue}
    response = HttpResponse()
    response['Content-Type'] = "text/javascript"
    response.write(json.dumps(respjson, cls=DatetimeEncoder).encode("UTF-8"))
    return response

#删除 数据库 故障回溯
def delprojects(request):
    username = request.session.get('username')
    user = request.POST.get("user")
    id = request.POST.get("id")
    if username == user:
        try:
            delvalue = onedeltable(id)
            if delvalue == ():
                result = {'isSuccess': True, "message": '删除成功'}
            else:
                result = {'isSuccess': False, "message": '删除失败'}
        except Exception as e:
            result = {'isSuccess': False, "message": str(e)}
    else:
        permess = Userperm(username, 'operate')
        if permess['isSuccess']:
            try:

                delvalue = onedeltable(id)
                if delvalue == ():
                    result = {'isSuccess': True, "message": '删除成功'}
                else:
                    result = {'isSuccess': False, "message": '删除失败'}
            except Exception as e:
                result = {'isSuccess': False, "message": str(e)}
        else:
            result = {'isSuccess': False, "message": '权限不足'}
    insert_log(username, request, str(result['isSuccess']), str(result), '删除文档')
    response = HttpResponse()
    response['Content-Type'] = "application/json"
    response.write(json.dumps(result, default=str).encode("UTF-8"))
    return response


#删除 数据库 故障回溯
def delerrprojects(request):
    username = request.session.get('username')
    id = request.POST.get("id")
    creatuser = request.POST.get("creatuser")
    if creatuser ==username:
        try:
            delvalue = derroltable(id)
            if delvalue == ():
                result = {'isSuccess': True, "message": '删除成功'}
            else:
                result = {'isSuccess': False, "message": '删除失败'}
        except Exception as e:
            result = {'isSuccess': False, "message": str(e)}
    else:
        permess = Userperm(username, 'operate')
        if permess['isSuccess']:
            try:
                delvalue = derroltable(id)
                if delvalue == ():
                    result = {'isSuccess': True, "message": '删除成功'}
                else:
                    result = {'isSuccess': False, "message": '删除失败'}
            except Exception as e:
                result = {'isSuccess': False, "message": str(e)}
        else:
            result = {'isSuccess': False, "message": '权限不足'}
    insert_log(username, request, str(result['isSuccess']), str(result), '删除文档')
    response = HttpResponse()
    response['Content-Type'] = "application/json"
    response.write(json.dumps(result, default=str).encode("UTF-8"))
    return response

#保存内容
def savemess(request):
    username = request.session.get('username')
    try:
        post = request.POST
        title = post.get('titel')
        tab = post.get('tab1')
        name = post.get('markup')
        remessage=savemessa(title, tab, name, username)
        if remessage==():
            result = {'isSuccess': True, "message": '保存成功'}
        else:
            result = {'isSuccess': False, "message": '保存失败'}
    except Exception as e:
        result = {'isSuccess': False, "message": str(e)}
    insert_log(username, request, str(result['isSuccess']), str(result), '新建文档')
    response = HttpResponse()
    response['Content-Type'] = "application/json"
    response.write(json.dumps(result, default=str).encode("UTF-8"))
    return response


#新建故障
def savemesserro(request):
    username = request.session.get('username')
    try:
        post = request.POST
        title = post.get('titel')
        tab = post.get('tab1')
        name = post.get('markup')
        userper = post.get('userper')
        affect = post.get('affect')
        inpendtimeid = post.get('inpendtimeid')
        remessage=saveearromessa(title, userper,affect,inpendtimeid, tab,name, username)
        if remessage==():
            result = {'isSuccess': True, "message": '保存成功'}
        else:
            result = {'isSuccess': False, "message": '保存失败'}
    except Exception as e:
        result = {'isSuccess': False, "message": str(e)}
    insert_log(username, request, str(result['isSuccess']), str(result), '新建文档')
    response = HttpResponse()
    response['Content-Type'] = "application/json"
    response.write(json.dumps(result, default=str).encode("UTF-8"))
    return response
#更新内容
def upsave(request):
    username = request.session.get('username')
    permess = Userperm(username, 'operate')
    if permess['isSuccess']:
        try:
            post = request.POST
            texid = post.get('texid')
            title = post.get('titel')
            tab = post.get('tab1')
            name = post.get('markup')
            remessage=upsaves(texid, title, tab, name)
            if remessage==():
                result = {'isSuccess': True, "message": '保存成功'}
            else:
                result = {'isSuccess': False, "message": '保存失败'}
        except Exception as e:
            result = {'isSuccess': False, "message": str(e)}
    else:
        result = {'isSuccess': False, "message": '权限不足'}
    insert_log(username, request, str(result['isSuccess']), str(result), '新建文档')
    response = HttpResponse()
    response['Content-Type'] = "application/json"
    response.write(json.dumps(result, default=str).encode("UTF-8"))
    return response
#更新内容
def upmesserro(request):
    username = request.session.get('username')
    permess = Userperm(username, 'operate')
    if permess['isSuccess']:
        try:
            post = request.POST
            texid = post.get('texid')
            title = post.get('titel')
            tab = post.get('tab1')
            name = post.get('markup')
            userper = post.get('userper')
            affect = post.get('affect')
            inpendtimeid = post.get('inpendtimeid')
            remessage=upsaveerr(title, userper,affect,inpendtimeid, tab,name, username,texid)
            if remessage==():
                result = {'isSuccess': True, "message": '保存成功'}
            else:
                result = {'isSuccess': False, "message": '保存失败'}
        except Exception as e:
            result = {'isSuccess': False, "message": str(e)}
    else:
        result = {'isSuccess': False, "message": '权限不足'}
    insert_log(username, request, str(result['isSuccess']), str(result), '新建文档')
    response = HttpResponse()
    response['Content-Type'] = "application/json"
    response.write(json.dumps(result, default=str).encode("UTF-8"))
    return response
#验证权限
def userauto(request):
    username = request.session.get('username')
    try:
        post = request.POST
        texid = post.get('texid')
        if texid.lower()==username.lower():
            result = {'isSuccess': True, "message": '正常权限'}
        else:
            permess = Userperm(username, 'operate')
            if permess['isSuccess']:
                result = {'isSuccess': True, "message": '正常权限'}
            else:
                result = {'isSuccess': False, "message": '权限失败'}
    except Exception as e:
        result = {'isSuccess': False, "message": str(e)}
    response = HttpResponse()
    response['Content-Type'] = "application/json"
    response.write(json.dumps(result, default=str).encode("UTF-8"))
    return response


#查看事件跳转
def lookallmess(request):
    username = request.session.get('username')
    displayname = request.session.get('displayname')
    textid=request.GET.get("textid")
    if username:
        try:
            showmess = searmessid(textid)
            title = (showmess[0]["title"])
            messall = (showmess[0]["message"])
            inptabshow = (showmess[0]["tab"])
            tabshow = (showmess[0]["tab"]).split(',')
            userid =(showmess[0]["user"])
            return render_to_response('document/showprojectsall.html', locals())
        except Exception as e:
            print(e)
            return render_to_response('home.html', locals())
    else:
        return render_to_response('login.html')

#查看故障跳转
def lookerrmess(request):
    username = request.session.get('username')
    displayname = request.session.get('displayname')
    textid=request.GET.get("textid")
    if username:
        try:
            showmess = searmesserrid(textid)
            title = (showmess[0]["title"])
            messall = (showmess[0]["marke"])
            inptabshow = (showmess[0]["tips"])
            userper =(showmess[0]["userper"])
            accfet =(showmess[0]["accfet"])
            datetime =str(showmess[0]["datetime"])
            userid =str(showmess[0]["creatuser"])
            return render_to_response('document/showerrproject.html', locals())
        except Exception as e:
            print(e)
            return render_to_response('home.html', locals())
    else:
        return render_to_response('login.html')