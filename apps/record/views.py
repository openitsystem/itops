from django.http import HttpResponse
import json
from django.shortcuts import render_to_response
import datetime
from dbinfo.views import *
#LDAP管理
def ldaprecord(request):
    mess=selectdb('record_ldap','1')
    return render_to_response('ad/ldap.html', locals())

#DNS管理
def dnsrecord(request):
    mess=selectdb('record_dns','1')
    return render_to_response('ad/dns.html', locals())

#LDAP录入，修改
def insert_ldap(request):
    ID=request.POST.get('id')
    account=request.POST.get('account')
    apps = request.POST.get('apps')
    applicant = request.POST.get('applicant')
    application_division = request.POST.get('application_division')
    manager = request.POST.get('manager')
    permission = request.POST.get('permission')
    Application_Date = request.POST.get('Application_Date')
    end = request.POST.get('end')
    link_server = request.POST.get('link_server')
    try:
        if ID:
            result=upadte_ldapdb(ID,account, apps, applicant, application_division, manager, permission, Application_Date,end,link_server)
            if  result == 0:
                result='无数据更改'
            elif result == 1:
                result='更新成功'
            else:
                result = '更新失败'
        else:
            if selectldaprecord():
                result=insert_ldapdb(account, apps, applicant, application_division, manager, permission, Application_Date,end,link_server,Status='1')
                if  result == 1:
                    result='录入成功'
                else:
                    result='录入失败'
            else:
                if crear_record_ldap()==():
                    result=insert_ldapdb(account, apps, applicant, application_division, manager, permission, Application_Date,end,link_server,Status='1')
                    if  result == 1:
                        result='录入成功'
                    else:
                        result='录入失败'
                else:
                    result = '数据库表创建失败'
    except Exception as e:
        print(e)
        result = '异常出错'
    response = HttpResponse()
    response['Content-Type'] = "application/json"
    response.write(json.dumps(result, default=str).encode("UTF-8"))
    return response

#删除LDAP数据,更改Status
def delete_ldap(request):
    ID = request.POST.get('ID')
    try:
        result=delete_ldapdb(ID,Status='2')
        if result == 1:
            result = '删除成功'
        else:
            result = '删除失败'
    except Exception as e:
        print(e)
        result = '异常出错'
    response = HttpResponse()
    response['Content-Type'] = "application/json"
    response.write(json.dumps(result, default=str).encode("UTF-8"))
    return response

#DNS录入，修改
def insert_dns(request):
    ID=request.POST.get('id')
    domain_name=request.POST.get('domain_name')
    apps = request.POST.get('apps')
    applicant = request.POST.get('applicant')
    application_division = request.POST.get('application_division')
    ops = request.POST.get('ops')
    type = request.POST.get('type')
    Applicant_time = request.POST.get('Applicant_time')
    try:
        if ID:
            result=upadte_dnsdb(ID,domain_name, apps, applicant, application_division, ops, type, Applicant_time)
            if  result == 0:
                result='无数据更改'
            elif result == 1:
                result='更新成功'
            else:
                result = '更新失败'
        else:
            if selectdnsrecord():
                result=insert_dnsdb(domain_name, apps, applicant, application_division, ops, type, Applicant_time,Status='1')
                if  result == 1:
                    result='录入成功'
                else:
                    result='录入失败'
            else:
                if crear_record_dns() == ():
                    result = insert_dnsdb(domain_name, apps, applicant, application_division, ops, type, Applicant_time,
                                          Status='1')
                    if result == 1:
                        result = '录入成功'
                    else:
                        result = '录入失败'
                else:
                    result = '数据库表创建失败'
    except Exception as e:
        print(e)
        result = '异常出错'
    response = HttpResponse()
    response['Content-Type'] = "application/json"
    response.write(json.dumps(result, default=str).encode("UTF-8"))
    return response

#删除LDAP数据,更改Status
def delete_dns(request):
    ID = request.POST.get('ID')
    try:
        result=delete_dnsdb(ID,Status='2')
        if result == 1:
            result = '删除成功'
        else:
            result = '删除失败'
    except Exception as e:
        print(e)
        result = '异常出错'
    response = HttpResponse()
    response['Content-Type'] = "application/json"
    response.write(json.dumps(result, default=str).encode("UTF-8"))
    return response

# 根据id 获取dns数据
def getdnsdbvaule(request):
    ID = request.POST.get('ID')
    try:
        get_dnsdbvaules = get_dnsdbvaule(ID)
        if get_dnsdbvaules:
            result = {'isSuccess': True, 'message': get_dnsdbvaules[0]}
        else:
            result = {'isSuccess': False, 'message': '根据id获取dns数据失败'}
    except Exception as e:
        result = {'isSuccess': False, 'message': '根据id获取dns数据失败：'+str(e)}
    response = HttpResponse()
    response['Content-Type'] = "application/json"
    response.write(json.dumps(result, default=str).encode("UTF-8"))
    return response

# 根据id 获取ldap数据
def getldapdbvaule(request):
    ID = request.POST.get('ID')
    try:
        get_ldapdbvaules = get_ldapdbvaule(ID)
        if get_ldapdbvaules:
            result = {'isSuccess': True, 'message': get_ldapdbvaules[0]}
        else:
            result = {'isSuccess': False, 'message': '根据id获取ldap数据失败'}
    except Exception as e:
        result = {'isSuccess': False, 'message': '根据id获取ldap数据失败：'+str(e)}
    response = HttpResponse()
    response['Content-Type'] = "application/json"
    response.write(json.dumps(result, default=str).encode("UTF-8"))
    return response