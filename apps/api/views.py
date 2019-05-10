# -*- coding: utf-8 -*-
# @Time    : 2019/3/26 12:09
# @Author  :
import json
import requests
from django.contrib.auth.hashers import make_password
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template.loader import get_template

from apiusers.views import ApiUserViewset
from dbinfo.views import get_apiusers_profile, insert_log, update_apiusers_profile, delect_apiusers_profile, insert_apiusers_profile, get_apinamepermissions, delect_apinamepermissions, \
    get_attributeslevel, insert_apinamepermissions, delect_attributeslevel, insert_attributeslevel, update_attributeslevel, get_apinamepermissions_is, delect_apinamepermissions_username_id

# 登录api权限接口页面
from permission.views import Userperm


def apipermissions(request):
    username = request.session.get('username')
    if username:
        return render_to_response('api/apipermissions.html', locals())
    else:
        return render_to_response('login.html', locals())


# 获取apiuser权限相关数据
def getapiuser(request):
    username = request.session.get('username')
    try:
        get_apiusers_profiles = get_apiusers_profile()
        if get_apiusers_profiles:
            result = {"rows": get_apiusers_profiles,
                      "total": len(get_apiusers_profiles)}
        else:
            result = {"rows": [], "total": 0}
    except Exception as e:
        result = {"rows": [], "total": 0}
    response = HttpResponse()
    response['Content-Type'] = "text/javascript"
    response.write(json.dumps(result, default=str))
    return response

# 修改api用户的属性
def modifyapiuser(request):
    field = request.POST.get('field', None)
    row = request.POST.get('row', None)
    oldValue = request.POST.get('oldValue', None)
    password = request.POST.get('password', None)
    new_active = request.POST.get('new_active', None)
    try:
        username = request.session.get('username')
        permess = Userperm(username, 'operate')
        if permess['isSuccess']:
            if field == 'password':
                password = make_password(password)
                update_apiusers_profiles = update_apiusers_profile(row, field, password)
            elif field == 'is_active':
                update_apiusers_profiles = update_apiusers_profile(row, field, new_active)
            else:
                rowjson = json.loads(row)
                id = rowjson.get('id')
                attributesVaule = rowjson.get(field, None)
                update_apiusers_profiles = update_apiusers_profile(id, field, attributesVaule)
            if update_apiusers_profiles:
                result = {'isSuccess': True, "message": field+'更新成功'}
            else:
                result = {'isSuccess': False, "message": '更新失败'}
        else:
            result = {'isSuccess': False, "message": '权限不足'}
    except Exception as e:
        result = {'isSuccess': False, "message": str(e)}
    insert_log(username, request, str(result['isSuccess']), str(result), '')
    response = HttpResponse()
    response['Content-Type'] = "text/javascript"
    response.write(json.dumps(result).encode("UTF-8"))
    return response

# 删除api用户的
def deletcapiuser(request):
    ids = request.POST.getlist('ids', None)
    try:
        username = request.session.get('username')
        permess = Userperm(username, 'operate')
        if permess['isSuccess']:
            for id in ids:
                delect_apinamepermissions_username_id(id)
                delect_apiusers_profiles = delect_apiusers_profile(id)
            if delect_apiusers_profiles:
                result = {'isSuccess': True, "message": str(ids)+'删除成功'}
            else:
                result = {'isSuccess': False, "message": str(ids) + '删除失败'}
        else:
            result = {'isSuccess': False, "message": '权限不足'}
    except Exception as e:
        result = {'isSuccess': False, "message": str(e)}
    insert_log(username, request, str(result['isSuccess']), str(result), '')
    response = HttpResponse()
    response['Content-Type'] = "text/javascript"
    response.write(json.dumps(result).encode("UTF-8"))
    return response

#新建api user
def addapiuser(request):
    apiusername = request.POST.get('add_api_username', None)
    password = request.POST.get('add_api_password', None)
    name = request.POST.get('add_api_name', None)
    department = request.POST.get('add_api_department', None)
    description = request.POST.get('add_api_description', None)
    try:
        username = request.session.get('username')
        permess = Userperm(username, 'operate')
        if permess['isSuccess']:
            if apiusername and password:
                insert_apiusers_profiles = insert_apiusers_profile(apiusername, password, name, department, description)
                if insert_apiusers_profiles:
                    result = {'isSuccess': True, "message": '新建成功'}
                else:
                    result = {'isSuccess': False, "message": '写入数据库失败'}
            else:
                result = {'isSuccess': False, "message": '用户名或密码未填写'}
        else:
            result = {'isSuccess': False, "message": '权限不足'}
    except Exception as e:
        result = {'isSuccess': False, "message": str(e)}
    insert_log(username, request, str(result['isSuccess']), str(result), '')
    response = HttpResponse()
    response['Content-Type'] = "text/javascript"
    response.write(json.dumps(result))
    return response

# 获取apiusers_apinamepermissions权限相关数据
def getapiuserpermissions(request):
    username = request.session.get('username')
    username_id = request.POST.get('username_id','')
    try:
        get_apiusers_profiles = get_apinamepermissions(username_id)
        if get_apiusers_profiles:
            result = {"rows": get_apiusers_profiles,
                      "total": len(get_apiusers_profiles)}
        else:
            result = {"rows": [], "total": 0}
    except Exception as e:
        result = {"rows": [], "total": 0}
    response = HttpResponse()
    response['Content-Type'] = "text/javascript"
    response.write(json.dumps(result, default=str))
    return response

# 删除api用户的权限
def deluserpermissions(request):
    ids = request.POST.getlist('ids', None)
    try:
        username = request.session.get('username')
        permess = Userperm(username, 'operate')
        if permess['isSuccess']:
            for id in ids:
                delect_apiusers_profiles = delect_apinamepermissions(id)
            if delect_apiusers_profiles:
                result = {'isSuccess': True, "message": str(ids)+'删除成功'}
            else:
                result = {'isSuccess': False, "message": str(ids) + '删除失败'}
        else:
            result = {'isSuccess': False, "message": '权限不足'}
    except Exception as e:
        result = {'isSuccess': False, "message": str(e)}
    insert_log(username, request, str(result['isSuccess']), str(result), '')
    response = HttpResponse()
    response['Content-Type'] = "text/javascript"
    response.write(json.dumps(result).encode("UTF-8"))
    return response

# 获取attributeslevel权限相关数据
def getattributeslevel(request):
    username = request.session.get('username')
    try:
        get_apiusers_profiles = get_attributeslevel()
        if get_apiusers_profiles:
            result = {"rows": get_apiusers_profiles,
                      "total": len(get_apiusers_profiles)}
        else:
            result = {"rows": [], "total": 0}
    except Exception as e:
        result = {"rows": [], "total": 0}
    response = HttpResponse()
    response['Content-Type'] = "text/javascript"
    response.write(json.dumps(result, default=str))
    return response

#添加 api 权限addapipermissions
def addapipermissions(request):
    username_id = request.POST.get('username_id', None)
    apinames = request.POST.get('apiname', None)
    try:
        username = request.session.get('username')
        permess = Userperm(username, 'operate')
        if permess['isSuccess']:
            if username_id and apinames:
                apinamelist = apinames.split(',')
                for apiname in apinamelist:
                    apiname_s = apiname.strip()
                    if apiname_s:
                        apinamepermissions =True
                        get_apinamepermissions_iss = get_apinamepermissions_is(username_id, apiname_s)
                        if not get_apinamepermissions_iss:
                            apinamepermissions = insert_apinamepermissions(username_id, apiname_s)
                if apinamepermissions:
                    result = {'isSuccess': True, "message": '添加成功'}
                else:
                    result = {'isSuccess': False, "message": '写入数据库失败'}
            else:
                result = {'isSuccess': False, "message": 'apiname栏位未填写，或其他'}
        else:
            result = {'isSuccess': False, "message": '权限不足'}
    except Exception as e:
        result = {'isSuccess': False, "message": str(e)}
    insert_log(username, request, str(result['isSuccess']), str(result), '')
    response = HttpResponse()
    response['Content-Type'] = "text/javascript"
    response.write(json.dumps(result))
    return response

# 修改attributeslevel权限相关数据
def modifyapiattributesleve(request):
    id = request.POST.get('add_api_apiname', None)
    attributes = request.POST.get('add_api_attributes', None)
    try:
        username = request.session.get('username')
        permess = Userperm(username, 'operate')
        if permess['isSuccess']:
            update_attributeslevels = update_attributeslevel(attributes,id)
            if update_attributeslevels:
                result = {'isSuccess': True, "message": '更新成功'}
            else:
                result = {'isSuccess': False, "message": '更新数据库失败'}
        else:
            result = {'isSuccess': False, "message": '权限不足'}
    except Exception as e:
        result = {'isSuccess': False, "message": str(e)}
    insert_log(username, request, str(result['isSuccess']), str(result), '')
    response = HttpResponse()
    response['Content-Type'] = "text/javascript"
    response.write(json.dumps(result).encode("UTF-8"))
    return response


import markdown

def itapidocument(request):
    template = get_template('api/itapidocument.html')
    docfile = get_template('api/itapidocument.md')
    content = docfile.render()
    html = template.render({
        'docname': 'itapidocument',
        'content':
            markdown.markdown(content,
                              extensions=[
                                  'markdown.extensions.extra',
                                  'markdown.extensions.codehilite',
                                  'markdown.extensions.toc',
                              ])
    })
    return HttpResponse(html)


def apinames(request):
    username = request.session.get('username')
    if username:
        return render_to_response('api/apinames.html', locals())
    else:
        return render_to_response('login.html', locals())