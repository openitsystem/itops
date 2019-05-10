# -*- coding: utf-8 -*-
# @Time    : 2018/11/19 16:02
# @Author  : 
import ast
from datetime import datetime
import io

import xlsxwriter
from django.http import HttpResponse
import json
from django.shortcuts import render_to_response

from ADapi.views import getmailboxdatabasenovalue, date_handler
from apps.activeapi.views import moveToOu, \
    delete_object, inspect_object, getObjectToDn, objectClassFrom, setAccount, \
    resetPassword, dnMoveToOu, serchlock, unlockuser, can_accidentally_deleted, check_accidentally_deleted, uncheck_accidentally_deleted
from apps.activeapi.views import get_domainbase, get_ou_for_dn, get_object_for_dn, set_rename_object, newUser, newGroup, newOrganizationalUnit, newContact, newComputer
from apps.activedirectory.Ther import Usermessage
from dbinfo.views import insert_log, getpermsessage
from itops.settings import ldap3RESTARTABLE
from permission.views import Userperm



# AD树页面
def directorytree(request):

    return render_to_response('ad/directorytree.html', locals())


# AD搜索页面
def search(request):
    return render_to_response('ad/search.html', locals())

# 树搜索页面
def treesearch(request):
    return render_to_response('ad/treesearch.html', locals())
# 导出
def downloadcsv(request):
    return render_to_response('ad/downslx.html', locals())

#验证权限
def userautodow(request):
    username = request.session.get('username')
    try:
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

#账号过期时间查询页面
def passwordexp(request):
    return render_to_response('ad/passwordexp.html', locals())

#高级搜索
def leavesearch(request):
    return render_to_response('ad/leavesearch.html', locals())


#获取总节点
def show_domain(request):
    try:
        result = get_domainbase()
        response = HttpResponse()
        response['Content-Type'] = "text/javascript"
        response.write(json.dumps(result))
        return response
    except Exception as e:
        print(e)
        return render_to_response('ad/directorytree.html', locals())

#获取OU节点
def show_ou_for_dn(request):
    distinguishedName = request.POST.get('distinguishedName')
    treeid = request.POST.get('id')
    if distinguishedName:
        try:
            result = get_ou_for_dn(distinguishedName,treeid)['message']
            response = HttpResponse()
            response['Content-Type'] = "text/javascript"
            response.write(json.dumps(result))
            return response
        except Exception as e:
            print(e)
            return render_to_response('ad/directorytree.html', locals())
    else:
        return render_to_response('login.html')

#获取下层目录所有对象
def show_object_for_dn(request):
    distinguishedName = request.POST.get('distinguishedName')
    if distinguishedName:
        try:
            result = get_object_for_dn(distinguishedName)
            response = HttpResponse()
            response['Content-Type'] = "text/javascript"
            response.write(json.dumps(result,default=date_handler))
            return response
        except Exception as e:
            print(e)
            return render_to_response('ad/directorytree.html', locals())
    else:
        return render_to_response('login.html')

#调用重命名的方法
def setRenameObject(request):
    distinguishedName = request.POST.get('distinguishedName')
    cn = request.POST.get('cn')
    sn = request.POST.get('sn')
    givenName = request.POST.get('givenName')
    displayName = request.POST.get('displayName')
    userPrincipalName = request.POST.get('userPrincipalName')
    sAMAccountName = request.POST.get('sAMAccountName')
    objectClass = request.POST.get('objectClass')
    try:
        username = request.session.get('username')
        permess = Userperm(username, 'operate')
        if permess['isSuccess']:
                objectClass = objectClass.split(',')
                result = set_rename_object(distinguishedName,cn,sn,givenName,displayName,userPrincipalName,sAMAccountName,objectClass)
        else:
            result = {'isSuccess': False, "message": '权限不足'}
    except Exception as e:
        result = {'isSuccess': False, "message": str(e)}
    insert_log(username, request, str(result['isSuccess']), str(result), '')
    response = HttpResponse()
    response['Content-Type'] = "text/javascript"
    response.write(json.dumps(result))
    return response


#DN查组信息
def getgroup(count):
    try:
        with ldap3RESTARTABLE as conn:
            conn.search(
                # search_base='DC,DC=cn',
                search_base=count,
                search_filter="(&(objectCategory=group))",
                search_scope='BASE',
                attributes=['member']
            )
            result_id = conn.result
            response_id = conn.response
            if result_id['result'] == 0:
                message = response_id[0].get('attributes', '')
                if message:
                    message = Usermessage(message['member'])
                    result = {'isSuccess': True, 'message': message}
                else:
                    result = {'isSuccess': False, 'message': '未查询到信息'}
            else:
                result = {'isSuccess': False, "message": result_id}
    except Exception as e:
        result = {'isSuccess': False, "message": str(e)}
    return result

#导出组信息
def groupexport(request):
    username = request.session.get('username')
    filter = request.GET.get('filter')
    name = str(request.GET.get('samename'))
    """导出数据至excel"""
    # 如果是POST请求，则根据提交的表单数据，判断导出哪些数据
    try:
        username = request.session.get('username')
        permess = Userperm(username, 'operate')
        if permess['isSuccess']:
            if request.method == 'GET':
                output = io.BytesIO()  # 将xlsx数据写入数据流中
                workbook = xlsxwriter.Workbook(output)
                worksheet = workbook.add_worksheet()  # 创建一个工作表对象
                # 定义数据表头列表
                title = [u'账号', u'显示名称',u'工号', u'邮箱地址',u'GUID']
                datas = getgroup(filter)
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
                worksheet.write_row('A1', title, format_title)
                nowdate = datetime.now().strftime('%Y-%m-%d')
                if datas['isSuccess']:
                    deatmessage=datas['message']
                    i = 2
                    for data22 in deatmessage:
                        date=(str(data22['sAMAccountName']),str(data22['displayName']),str(data22['wWWHomePage']),str(data22['mail']),str(data22['physicalDeliveryOfficeName']))
                        row = 'A' + str(i)
                        worksheet.write_row(row, date, format)
                        i = i + 1
                    workbook.close()
                    # 将数据流的游标指向起始位置
                    output.seek(0)
                    result = {'isSuccess': True, "message": name+'组成员'}
                    insert_log(username, request, str(result['isSuccess']), str(result), '')
                    response = HttpResponse(output.read(),
                                            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
                    response['Content-Disposition'] = 'attachment; filename="{0}{1}.xlsx"'.format(name+'组成员', nowdate).encode('utf-8')
                    return response
                else:
                    result = {'isSuccess': False, "message": '导出出现异常'}
                    insert_log(username, request, str(result['isSuccess']), str(result), '')
                    response = HttpResponse(output.read(),
                                            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
                    response['Content-Disposition'] = 'attachment; filename="{0}{1}.xlsx"'.format('导出出现异常', nowdate).encode(
                        'utf-8')
                    return response
        else:
            result = {'isSuccess': False, "message": '权限不足'}
    except Exception as e:
        result = {'isSuccess': False, "message": str(e)}
    insert_log(username, request, str(result['isSuccess']), str(result), '')
    response = HttpResponse()
    response['Content-Type'] = "text/javascript"
    response.write(json.dumps(result))
    return response

# 导出OU 下成员 列表
def exportListToOU(request):
    distinguishedName = request.GET.get('distinguishedName')
    search_scope = request.GET.get('search_scope')
    try:
        username = request.session.get('username')
        permess = Userperm(username, 'operate')
        if permess['isSuccess']:
            if distinguishedName:
                if search_scope =='true':
                    search_scope = 'SUBTREE'
                else:
                    search_scope = 'LEVEL'
                """导出数据至excel"""
                # 如果是POST请求，则根据提交的表单数据，判断导出哪些数据
                output = io.BytesIO()  # 将xlsx数据写入数据流中
                workbook = xlsxwriter.Workbook(output)
                worksheet = workbook.add_worksheet()  # 创建一个工作表对象
                # 定义数据表头列表
                title = [u'名称',u'登录名', u'类型', u'描述', u'显示名称', u'路径']
                datas = getObjectToDn(distinguishedName,search_scope)
                name = distinguishedName.split(',')[0].split('=')[1]
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
                worksheet.set_column('F:F', 60)
                worksheet.write_row('A1', title, format_title)
                nowdate = datetime.now().strftime('%Y-%m-%d')
                if datas['isSuccess']:
                    deatmessageList = datas['message']
                    i = 2
                    for attributes in deatmessageList:
                        date = (str(attributes['name']), str(attributes['sAMAccountName']), str(objectClassFrom(attributes['objectClass'],attributes['groupType'])['types']), str(attributes['description']), str(attributes['displayName']), str(attributes['distinguishedName']))
                        row = 'A' + str(i)
                        worksheet.write_row(row, date, format)
                        i = i + 1
                    workbook.close()
                    # 将数据流的游标指向起始位置
                    output.seek(0)
                    result = {'isSuccess': True, "message": name + '导出列表'}
                    insert_log(username, request, str(result['isSuccess']), str(result), '')
                    response = HttpResponse(output.read(),
                                            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
                    response['Content-Disposition'] = 'attachment; filename="{0}{1}.xlsx"'.format(name + '导出列表', nowdate).encode('utf-8')
                    return response
                else:
                    result = {'isSuccess': False, "message": '导出出现异常'}
                    insert_log(username, request, str(result['isSuccess']), str(result), '')
                    response = HttpResponse(output.read(),
                                            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
                    response['Content-Disposition'] = 'attachment; filename="{0}{1}.xlsx"'.format('导出出现异常', nowdate).encode(
                        'utf-8')
                    return response
        else:
            result = {'isSuccess': False, "message": '权限不足'}
    except Exception as e:
        result = {'isSuccess': False, "message": str(e)}


#新建USer
def addUser(request):
    distinguishedName = request.POST.get('add_user_distinguishedName')
    cn = request.POST.get('add_user_cn')
    sn = request.POST.get('add_user_sn')
    givenName = request.POST.get('add_user_givenName')
    password = request.POST.get('add_user_password')
    userPrincipalName1 = request.POST.get('add_user_userPrincipalName1')
    userPrincipalName2 = request.POST.get('add_user_userPrincipalName2')
    sAMAccountName1 = request.POST.get('add_user_sAMAccountName1')
    sAMAccountName2 = request.POST.get('add_user_sAMAccountName2')
    displayName = request.POST.get('add_user_displayName')
    description = request.POST.get('add_user_description')
    userAccountControl = request.POST.get('add_user_userAccountControl')
    mail = request.POST.get('add_user_mail')
    maildb = request.POST.get('add_user_mail_db')
    try:
        userPrincipalName = userPrincipalName1+userPrincipalName2
        username = request.session.get('username')
        permess = Userperm(username, 'operate')
        if permess['isSuccess']:
            if userAccountControl=='yes':
                userAccountControl = 544
            else:
                userAccountControl = 546
            attributes ={}
            if displayName:
                attributes.update({'displayName': displayName})
            if description:
                attributes.update({'description': description})
            result = newUser(distinguishedName=distinguishedName,cn=cn,sn=sn,givenName=givenName,displayName=None,
                             userPrincipalName=userPrincipalName,sAMAccountName=sAMAccountName2,password=password,
                             userAccountControl=userAccountControl,mail=mail,maildb=maildb,attributes=attributes)
        else:
            result = {'isSuccess': False, "message": '权限不足'}
    except Exception as e:
        result = {'isSuccess': False, "message": str(e)}
    insert_log(username, request, str(result['isSuccess']), str(result), '')
    response = HttpResponse()
    response['Content-Type'] = "text/javascript"
    response.write(json.dumps(result))
    return response

#新建group
def addGroup(request):
    distinguishedName = request.POST.get('add_group_distinguishedName')
    cn = request.POST.get('add_group_cn')
    scope = request.POST.get('group_scope')
    type = request.POST.get('group_type')
    sAMAccountName = request.POST.get('add_group_sAMAccountName')
    displayName = request.POST.get('add_group_displayName')
    description = request.POST.get('add_group_description')
    try:
        username = request.session.get('username')
        permess = Userperm(username, 'operate')
        if permess['isSuccess']:
            groupType = int(scope)-int(type)
            attributes = {}
            if displayName:
                attributes.update({'displayName': displayName})
            if description:
                attributes.update({'description': description})
            result = newGroup(distinguishedName, cn,sAMAccountName, groupType,attributes=attributes)
        else:
            result = {'isSuccess': False, "message": '权限不足'}
    except Exception as e:
        result = {'isSuccess': False, "message": str(e)}
    insert_log(username, request, str(result['isSuccess']), str(result), '')
    response = HttpResponse()
    response['Content-Type'] = "text/javascript"
    response.write(json.dumps(result))
    return response


#新建organizationalUnit
def addorganizationalUnit(request):
    distinguishedName = request.POST.get('distinguishedName')
    cn = request.POST.get('cn')
    prevent = request.POST.get('checkbox')
    try:
        username = request.session.get('username')
        permess = Userperm(username, 'operate')
        if permess['isSuccess']:
            result = newOrganizationalUnit(distinguishedName, cn,prevent,attributes={})
        else:
            result = {'isSuccess': False, "message": '权限不足'}
    except Exception as e:
        result = {'isSuccess': False, "message": str(e)}
    insert_log(username, request, str(result['isSuccess']), str(result), '')
    response = HttpResponse()
    response['Content-Type'] = "text/javascript"
    response.write(json.dumps(result))
    return response


#新建联系人
def addContact(request):
    distinguishedName = request.POST.get('add_contact_distinguishedName')
    cn = request.POST.get('add_contact_cn')
    sn = request.POST.get('add_contact_sn')
    givenName = request.POST.get('add_contact_givenName')
    displayName = request.POST.get('add_contact_displayName')
    description = request.POST.get('add_contact_description')
    mail = request.POST.get('add_contact_mail')
    name = request.POST.get('add_contact_name')
    smtpvalue = request.POST.get('add_contact_smtpvalue')
    try:
        username = request.session.get('username')
        permess = Userperm(username, 'operate')
        if permess['isSuccess']:
            result = newContact(distinguishedName, cn, sn=sn, givenName=givenName, displayName=displayName,description=description,mail=mail,name=name,smtpvalue=smtpvalue,attributes = {})
        else:
            result = {'isSuccess': False, "message": '权限不足'}
    except Exception as e:
        result = {'isSuccess': False, "message": str(e)}
    insert_log(username, request, str(result['isSuccess']), str(result), '')
    response = HttpResponse()
    response['Content-Type'] = "text/javascript"
    response.write(json.dumps(result))
    return response

#新建Computer
def addComputer(request):
    distinguishedName = request.POST.get('add_computer_distinguishedName')
    cn = request.POST.get('add_computer_cn')
    displayName = request.POST.get('add_computer_displayName')
    description = request.POST.get('add_computer_description')
    try:
        username = request.session.get('username')
        permess = Userperm(username, 'operate')
        if permess['isSuccess']:
            attributes = {}
            if displayName:
                attributes.update({'displayName': displayName})
            if description:
                attributes.update({'description': description})
            result = newComputer(distinguishedName, cn, userAccountControl=4128,attributes=attributes)
        else:
            result = {'isSuccess': False, "message": '权限不足'}
    except Exception as e:
        result = {'isSuccess': False, "message": str(e)}
    insert_log(username, request, str(result['isSuccess']), str(result), '')
    response = HttpResponse()
    response['Content-Type'] = "text/javascript"
    response.write(json.dumps(result))
    return response

#右键单击移动到新OU
def setObjectMoveToOu(request):
    username = request.session.get('username')
    permess = Userperm(username, 'operate')
    if permess['isSuccess']:
        dn = request.POST.get('dn')
        new_superior = request.POST.get('new_superior')
        try:
            result = moveToOu(dn,new_superior)
        except Exception as e:
            result={'isSuccess': False, "message": str(e)}
    else:
        result = {'isSuccess': False, "message": '权限不足'}
    insert_log(username, request, str(result['isSuccess']), str(result), '')
    response = HttpResponse()
    response['Content-Type'] = "text/javascript"
    response.write(json.dumps(result))
    return response

# 删除对象
def delObject(request):
    dn = request.POST.get('dn')
    controls = request.POST.get('controls')
    checkboxtext = request.POST.get('checkboxtext')
    try:
        username = request.session.get('username')
        permess = Userperm(username, 'operate')
        if permess['isSuccess']:
            if controls == 'true':
                if checkboxtext == '删除下面所有账户或对象':
                    controls = [('1.2.840.113556.1.4.805', False, None)]
                    result = delete_object(dn, controls)
                else:
                    result = {'isSuccess': False, "message": '请输入"删除下面所有账户或对象"'}
            else:
                controls=None
                result = delete_object(dn,controls)
        else:
            result = {'isSuccess': False, "message": '权限不足'}
    except Exception as e:
        result = {'isSuccess': False, "message": str(e)}
    insert_log(username, request, str(result['isSuccess']), str(result), '')
    response = HttpResponse()
    response['Content-Type'] = "text/javascript"
    response.write(json.dumps(result))
    return response

#判断容器 OU 内是否有对象
def inspectObject(request):
    dn = request.POST.get('dn')
    search_scope = request.POST.get('search_scope')
    try:
        result = inspect_object(dn,search_scope)
        response = HttpResponse()
        response['Content-Type'] = "text/javascript"
        response.write(json.dumps(result))
        return response
    except Exception as e:
        print(e)
        return render_to_response('ad/directorytree.html', locals())

#修改对象属性
def setObjectAttributes(request):
    distinguishedName = request.POST.get('distinguishedName')
    attributesName = request.POST.get('attributesName')
    attributesVaule = request.POST.get('attributesVaule')
    try:
        username = request.session.get('username')
        permess = Userperm(username, 'changelw')
        if permess['isSuccess']:
            result = setAccount(distinguishedName,attributesName,attributesVaule)
        else:
            result = {'isSuccess': False, "message": '权限不足'}
    except Exception as e:
        result = {'isSuccess': False, "message": str(e)}
    insert_log(username, request, str(result['isSuccess']), str(result), '')
    response = HttpResponse()
    response['Content-Type'] = "text/javascript"
    response.write(json.dumps(result))
    return response

## 修改用户密码 设置 用户下次登陆时须更改密码 解锁用户的账户
def resetUserPassword(request):
    sAMAccountName = request.POST.get('sAMAccountName', None)
    distinguishedName = request.POST.get('distinguishedName', None)
    newpassword = request.POST.get('newpassword')
    pwdLastSet = request.POST.get('pwdLastSet')
    unlock = request.POST.get('unlock')
    ip = request.POST.get('ip',None)
    try:
        username = request.session.get('username')
        permess = Userperm(username, 'operate')
        if permess['isSuccess']:
            if pwdLastSet == 'true':
                pwdLastSet = True
            else:
                pwdLastSet = None
            if unlock == 'true':
                unlock = True
            else:
                unlock = None
            result = resetPassword(newpassword, distinguishedName=distinguishedName, sAMAccountName=sAMAccountName, pwdLastSet=pwdLastSet, unlock=unlock, ip=ip)
        else:
            result = {'isSuccess': False, "message": '权限不足'}
    except Exception as e:
        result = {'isSuccess': False, "message": str(e)}
    insert_log(username, request, str(result['isSuccess']), str(result), '')
    response = HttpResponse()
    response['Content-Type'] = "text/javascript"
    response.write(json.dumps(result))
    return response

## # 多dn 移动到新OU
def moveDnsToOu(request):
    dns = request.POST.getlist('dns[]')
    new_superior = request.POST.get('new_superior')
    try:
        username = request.session.get('username')
        permess = Userperm(username, 'operate')
        if permess['isSuccess']:
            result = dnMoveToOu(dns,new_superior)
        else:
            result = {'isSuccess': False, "message": '权限不足'}
    except Exception as e:
        result = {'isSuccess': False, "message": str(e)}
    insert_log(username, request, str(result['isSuccess']), str(result), '')
    response = HttpResponse()
    response['Content-Type'] = "text/javascript"
    response.write(json.dumps(result))
    return response

## psot 获取邮箱数据库
def getMailboxDatebase(request):
    try:
        result = getmailboxdatabasenovalue()
        new_result ={'isSuccess': result['isSuccess'], 'message': []}
        if result['isSuccess']:
            for i in result['message']:
                new_result['message'].append(ast.literal_eval(i))
        response = HttpResponse()
        response['Content-Type'] = "text/javascript"
        response.write(json.dumps(new_result))
        return response
    except Exception as e:
        print(e)
        return render_to_response('ad/directorytree.html', locals())

## 查找用户是否被锁定  传入 sAMAccountName or distinguishedName
def serchLock(request):
    distinguishedName = request.POST.get('distinguishedName',None)
    sAMAccountName = request.POST.get('sAMAccountName',None)
    try:
        result = serchlock(sAMAccountName=sAMAccountName,distinguishedName=distinguishedName)
    except Exception as e:
        result = {'isSuccess': False, "message": str(e)}
    response = HttpResponse()
    response['Content-Type'] = "text/javascript"
    response.write(json.dumps(result))
    return response

## 查找监控是否开启
def hasmonitorvalueurl(request):
    try:
        permessa = getpermsessage()
        if permessa:
            result = {'isSuccess': True, "message": permessa}
        else:
            result = {'isSuccess': False, "message": permessa}
    except Exception as e:
        result = {'isSuccess': False, "message": str(e)}
    response = HttpResponse()
    response['Content-Type'] = "text/javascript"
    response.write(json.dumps(result))
    return response

## 解锁用户  传入 sAMAccountName or distinguishedName
def unLockuser(request):
    distinguishedName = request.POST.get('distinguishedName',None)
    sAMAccountName = request.POST.get('sAMAccountName',None)
    ip = request.POST.get('ip',None)
    try:
        result = unlockuser(sAMAccountName=sAMAccountName,distinguishedName=distinguishedName,ip=ip)
    except Exception as e:
        result = {'isSuccess': False, "message": str(e)}
    response = HttpResponse()
    response['Content-Type'] = "text/javascript"
    response.write(json.dumps(result))
    return response

## 勾选 防止对象被意外删除(P)
def setAccidentallyDeleted(request):
    distinguishedName = request.POST.get('distinguishedName',None)
    sAMAccountName = request.POST.get('sAMAccountName',None)
    prevent = request.POST.get('prevent','true')
    try:
        username = request.session.get('username')
        permess = Userperm(username, 'operate')
        if permess['isSuccess']:
            if prevent == 'true':
                result = check_accidentally_deleted(sAMAccountName=sAMAccountName, distinguishedName=distinguishedName)
            else:
                result = uncheck_accidentally_deleted(sAMAccountName=sAMAccountName, distinguishedName=distinguishedName)
        else:
            result = {'isSuccess': False, "message": '权限不足'}
    except Exception as e:
        result = {'isSuccess': False, "message": str(e)}
    insert_log(username, request, str(result['isSuccess']), str(result), '')
    response = HttpResponse()
    response['Content-Type'] = "text/javascript"
    response.write(json.dumps(result))
    return response

## 判断 勾选 防止对象被意外删除(P)
def canAccidentallyDeleted(request):
    distinguishedName = request.POST.get('distinguishedName',None)
    sAMAccountName = request.POST.get('sAMAccountName',None)
    try:
        result = can_accidentally_deleted(sAMAccountName=sAMAccountName,distinguishedName=distinguishedName)
    except Exception as e:
        result = {'isSuccess': False, "message": str(e)}
    response = HttpResponse()
    response['Content-Type'] = "text/javascript"
    response.write(json.dumps(result))
    return response