# -*- coding: utf-8 -*-
# @Time    : 2019/1/28 11:12
# @Author  : 
import json

from django.shortcuts import render_to_response
from django.http import HttpResponse
from datetime import datetime

# 登录serchlog页面
from dbinfo.views import insert_log, get_log, show_tables, show_sqllog
from permission.views import Userperm

# 日志页面
def serchlog(request):
    username = request.session.get('username')
    if username:
        time_m = datetime.now().strftime('%Y_%m')
        table_name = str('log') + "_" + str(time_m)
        tablelist = []
        show_tabless = show_tables()
        if show_tabless:
            for tabless in show_tabless:
                for key, vaule in tabless.items():
                    if 'log' in vaule:
                        tablelist.append(vaule)
        if tablelist:
            if table_name in tablelist:
                tablelist.remove(table_name)
                tablelist.insert(0,table_name)
        return render_to_response('log/serchlog.html', locals())
    else:
        return render_to_response('login.html', locals())
# 查询日志
def getsqllog(request):
    sqlname = request.POST.get('sqlname', None)
    try:
        username = request.session.get('username')
        row = get_log(sqlname=sqlname)
        if row:
            result = {'row': row, "total": len(row)}
        else:
            result = {'row': [], "total": 0}
    except Exception as e:
        result = {'isSuccess': False, "message": str(e)}
    response = HttpResponse()
    response['Content-Type'] = "text/javascript"
    response.write(json.dumps(result,default=str).encode("UTF-8"))
    return response

# 获取有哪些日志数据表
def gettableslog(request):
    try:
        logtable =[]
        show_tabless = show_tables()
        if show_tabless:
            for tabless in show_tabless:
                for key,vaule in tabless.items():
                    if 'log' in tabless:
                        logtable.append(vaule)
        result = {'isSuccess': True, "message": logtable}
    except Exception as e:
        result = {'isSuccess': False, "message": str(e)}
    response = HttpResponse()
    response['Content-Type'] = "text/javascript"
    response.write(json.dumps(result,default=str).encode("UTF-8"))
    return response

# 搜索日志
def serchsqllog(request):
    sqlname = request.POST.get('sqlname', None)
    vaules = request.POST.get('vaules', '')
    try:
        username = request.session.get('username')
        if sqlname:
            if vaules:
                row = show_sqllog(sqlname=sqlname,vaules=vaules)
            else:
                row = get_log(sqlname=sqlname)
            if row:
                result = {'row': row, "total": len(row)}
            else:
                result = {'row': [], "total": 0}
        else:
            result = {'isSuccess': False, "message": 'sqlname传入空值'}
    except Exception as e:
        result = {'isSuccess': False, "message": str(e)}
    response = HttpResponse()
    response['Content-Type'] = "text/javascript"
    response.write(json.dumps(result,default=str).encode("UTF-8"))
    return response