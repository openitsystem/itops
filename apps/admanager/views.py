import json

from django.shortcuts import render_to_response
import io
from django.http import HttpResponse
from datetime import datetime
import xlsxwriter
import xlrd
from ldap3 import MODIFY_REPLACE

from apps.admanager.thercrearmail import threxecutecreatmail
from apps.admanager.thercreatuser import thrcreatalluser
from apps.admanager.thermodifyuser import thrmodifyalluser
from apps.admanager.thermoveuser import threxecutemoveuser
from apps.admanager.theruserpaawd import thrmodifyalluserpasswd
from apps.ldaptime.views import utc2local
from dbinfo.views import insert_log, get_log, get_log_ldapattributes
from itops.settings import ldap3RESTARTABLE, ladp3search_base
from permission.views import Userperm

def repeace(message):
    promessage=message.replace('(',r'\28').replace(')',r'\29').replace('*',r'2a')
    return promessage
def ldapattributes(userPrincipalName=None,cn=None,givenName=None,initials=None,sn=None,displayName=None,description=None,physicalDeliveryOfficeName=None,telephoneNumber=None,mail=None,maildb=None,wWWHomePage=None,
                   password = None, userAccountControl = None,distinguishedName=None):
    try:
        titleldap = ['sAMAccountName']
        title = [u'*登录名(Windows 2000以前版本)']
        if userPrincipalName == 'true':
            titleldap.append('userPrincipalName')
            title.append(u'登录名')
        if cn == 'true':
            titleldap.append('cn')
            title.append(u'全名')
        if givenName == 'true':
            titleldap.append('givenName')
            title.append(u'名字')
        if initials == 'true':
            titleldap.append('initials')
            title.append(u'中间名首字母缩写')
        if sn == 'true':
            titleldap.append('sn')
            title.append(u'姓氏')
        if displayName == 'true':
            titleldap.append('displayName')
            title.append(u'显示名称')
        if description == 'true':
            titleldap.append('description')
            title.append(u'描述')
        if physicalDeliveryOfficeName == 'true':
            titleldap.append('physicalDeliveryOfficeName')
            title.append(u'办公室')
        if telephoneNumber == 'true':
            titleldap.append('telephoneNumber')
            title.append(u'电话号码')
        if mail == 'true':
            titleldap.append('mail')
            title.append(u'电子邮件')
        if maildb == 'true':
            titleldap.append('maildb')
            title.append(u'邮箱存储')
        if wWWHomePage == 'true':
            titleldap.append('wWWHomePage')
            title.append(u'网页')
        if password == 'true':
            titleldap.append('password')
            title.append(u'密码')
        if userAccountControl == 'true':
            titleldap.append('disableuser')
            title.append(u'禁用用户')
        if distinguishedName == 'true':
            titleldap.append('distinguishedName')
            title.append(u'目录路径')
        return {'titleldap': titleldap, 'title': title}
    except Exception as e:
        return {'titleldap':[],'title':[]}

# 登录admanager页面
def admanager(request):
    username = request.session.get('username')
    if username:
        return render_to_response('ad/admanager.html', locals())
    else:
        return render_to_response('login.html', locals())


# 登录creatusers页面
def creatusers(request):
    username = request.session.get('username')
    if username:
        return render_to_response('admanager/creatusers.html', locals())
    else:
        return render_to_response('login.html', locals())


# 导出文件模板
def exportfiletemplate(request):
    userPrincipalName = request.GET.get('userPrincipalName','')
    cn = request.GET.get('cn', '')
    givenName = request.GET.get('givenName')
    initials = request.GET.get('initials')
    sn = request.GET.get('sn')
    displayName = request.GET.get('displayName')
    description = request.GET.get('description')
    physicalDeliveryOfficeName = request.GET.get('physicalDeliveryOfficeName')
    telephoneNumber = request.GET.get('telephoneNumber')
    mail = request.GET.get('mail')
    maildb = request.GET.get('maildb')
    wWWHomePage = request.GET.get('wWWHomePage')
    password = request.GET.get('password')
    userAccountControl = request.GET.get('userAccountControl')
    template = request.GET.get('template','用户模板')
    try:
        username = request.session.get('username')
        permess = Userperm(username, 'operate')
        if permess['isSuccess']:
            """导出数据至excel"""
            # 如果是POST请求，则根据提交的表单数据，判断导出哪些数据
            output = io.BytesIO()  # 将xlsx数据写入数据流中
            workbook = xlsxwriter.Workbook(output)
            worksheet = workbook.add_worksheet()  # 创建一个工作表对象
            # 定义数据表头列表

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
            worksheet.set_column('A:O', 25)
            ldapattributess = ldapattributes(userPrincipalName=userPrincipalName,cn=cn,givenName=givenName, initials=initials, sn=sn, displayName=displayName, description=description, physicalDeliveryOfficeName=physicalDeliveryOfficeName,
                           telephoneNumber=telephoneNumber, mail=mail, maildb=maildb,wWWHomePage=wWWHomePage,password=password, userAccountControl=userAccountControl,)
            worksheet.write_row('A1', ldapattributess['titleldap'], format_title)
            nowdate = datetime.now().strftime('%Y-%m-%d')
            workbook.close()
            # 将数据流的游标指向起始位置
            output.seek(0)
            response = HttpResponse(output.read(),
                                    content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
            response['Content-Disposition'] = 'attachment; filename="{0}.xlsx"'.format(template).encode('utf-8')
            return response
        else:
            result = {'isSuccess': False, "message": '权限不足'}
    except Exception as e:
        result = {'isSuccess': False, "message": str(e)}

def handle_uploaded_file(f):
    file_name = ""
    try:
        path = "upload/"
        file_name = path + f.name
        destination = open(file_name, 'wb+')
        for chunk in f.chunks():
            destination.write(chunk)
        destination.close()
    except Exception as e:
        print(e)
    return file_name


# 导入文件模板
def uploadfiletemplate(request):
    files = request.FILES.get('file')
    try:
        username = request.session.get('username')
        permess = Userperm(username, 'operate')
        if permess['isSuccess']:
            filename = handle_uploaded_file(files)
            data = xlrd.open_workbook(filename)
            table = data.sheet_by_index(0)
            nrows = table.nrows  # 行数
            ncols = table.ncols  # 列数
            heard = []
            heardfield = table.row_values(0)
            #获取抬头
            for c in heardfield:
                if c:
                    heard.append({'field':c,'title':c})
            # 从第2行开始读取 EXCEL
            tabledata = []
            for i in range(1,nrows):
                data1 ={}
                row_data = table.row_values(i)
                for j in range(0,len(heardfield)):
                    if isinstance(row_data[j],str):
                        row_data1 = row_data[j].replace(" ", '')
                    else:
                        row_data1 = row_data[j]
                    data1.update({heardfield[j]:row_data1})
                tabledata.append(data1)
            result = {'isSuccess': True, "message": '','heard':heard,'tabledata':tabledata}
        else:
            result = {'isSuccess': False, "message": '权限不足'}
    except Exception as e:
        result = {'isSuccess': False, "message": str(e)}
    insert_log(username, request, str(result['isSuccess']), str(result), '')
    response = HttpResponse()
    response['Content-Type'] = "text/javascript"
    response.write(json.dumps(result))
    return response

## 批量创建用户 多进程
def creatalluser(request):
    get_user_distinguishedName = request.POST.get('get_user_distinguishedName',None)
    getData = request.POST.get('getData',{})
    try:
        username = request.session.get('username')
        permess = Userperm(username, 'operate')
        if permess['isSuccess']:
            getDatatojson = json.loads(getData)
            creatallusers = thrcreatalluser(getDatatojson,get_user_distinguishedName)
            if creatallusers:
                if '' in getDatatojson[0]:
                    getDatatojson[0].pop('')
                if '0' in getDatatojson[0]:
                    getDatatojson[0].pop('0')
                attributesldap = list(creatallusers[0].keys())
                columns=[]
                for c in range(0, len(attributesldap)):
                    if not attributesldap[c] == 'status':
                        columns.append({'field': attributesldap[c], 'title':attributesldap[c]})
                result = {'isSuccess': True, "message": creatallusers, "columns": columns}
            else:
                result = {'isSuccess': False, "message": '都未新建成功或者没有数据'}
        else:
            result = {'isSuccess': False, "message": '权限不足'}
    except Exception as e:
        result = {'isSuccess': False, "message": str(e)}
    insert_log(username, request, str(result['isSuccess']), str(result), '')
    response = HttpResponse()
    response['Content-Type'] = "text/javascript"
    response.write(json.dumps(result))
    return response


# 登录批量修改用户属性页面
def modifyuserattributes(request):
    username = request.session.get('username')
    if username:
        return render_to_response('admanager/modifyuserattributes.html', locals())
    else:
        return render_to_response('login.html', locals())

## 查找需要修改的用户属性
def searchuser_modify(request):
    dn = request.POST.get('dn',None)
    filteruser = request.POST.get('filteruser',None)
    userPrincipalName = request.POST.get('userPrincipalName', None)
    cn = request.POST.get('cn', None)
    givenName = request.POST.get('givenName', None)
    initials = request.POST.get('initials', None)
    sn = request.POST.get('sn', None)
    displayName = request.POST.get('displayName', None)
    description = request.POST.get('description', None)
    physicalDeliveryOfficeName = request.POST.get('physicalDeliveryOfficeName', None)
    telephoneNumber = request.POST.get('telephoneNumber', None)
    mail = request.POST.get('mail', None)
    wWWHomePage = request.POST.get('wWWHomePage', None)
    distinguishedName = request.POST.get('distinguishedName', None)
    serchtype = request.POST.get('serchtype', None)
    try:
        heard =[]
        ldapattributess = ldapattributes(userPrincipalName=userPrincipalName,cn=cn, givenName=givenName, initials=initials, sn=sn, displayName=displayName, description=description,
                                         physicalDeliveryOfficeName=physicalDeliveryOfficeName,
                                         telephoneNumber=telephoneNumber, mail=mail, wWWHomePage=wWWHomePage,distinguishedName=distinguishedName)
        for c in range(0, len(ldapattributess['titleldap'])):
            heard.append({'field': ldapattributess['titleldap'][c], 'title': ldapattributess['titleldap'][c]})
        if serchtype == 'creatusermail' and filteruser:
            search_filter = '(&(anr=' + filteruser + ')(&(objectCategory=person)(objectClass=user))(!(msExchHomeServerName=*))(!(mailNickname=*)))'
        elif serchtype == 'creatusermail':
            search_filter = '(&(objectCategory=person)(objectClass=user)(!(msExchHomeServerName=*))(!(mailNickname=*)))'
        elif serchtype == 'computer' and filteruser:
            search_filter = '(&(anr='+filteruser+')(objectClass=computer))'
        elif serchtype == 'computer':
            search_filter = '(objectClass=computer)'
        elif filteruser:
            search_filter = '(&(anr='+filteruser+')(&(objectCategory=person)(objectClass=user)))'
        else:
            search_filter = "(&(objectCategory=person)(objectClass=user))"
        total_entries = 0
        response_id = []
        with ldap3RESTARTABLE as conn:
            entry_generator = conn.extend.standard.paged_search(
                search_base=dn,
                search_filter=search_filter,
                attributes=ldapattributess['titleldap'], paged_size=1000, generator=True)
            for entry in entry_generator:
                attributes = (entry.get('attributes', ''))
                if attributes:
                    if attributes.get('description',''):
                        attributes['description'] = str(attributes['description'][0])
                    total_entries += 1
                    response_id.append(dict(attributes))
            result_id = conn.result
            if result_id.get('result', '') in [0, 4]:
                result = {"isSuccess": True, "tabledata": response_id,'heard':heard}
            else:
                result = {"isSuccess": False, "message": str(result_id['description'])}
    except Exception as e:
        result = {'isSuccess': False, "message": str(e)}
    response = HttpResponse()
    response['Content-Type'] = "text/javascript"
    response.write(json.dumps(result).encode("UTF-8"))
    return response

# 修改用户属性，可修改cn(重命名）
def modifyuser(request):
    field = request.POST.get('field',None)
    row = request.POST.get('row',None)
    oldValue = request.POST.get('oldValue', None)
    try:
        username = request.session.get('username')
        permess = Userperm(username, 'changelw')
        if permess['isSuccess']:
            rowjson = json.loads(row)
            if field == 'sAMAccountName':
                sAMAccountName = oldValue
            else:
                sAMAccountName = rowjson['sAMAccountName']
            sAMAccountName_repeace = repeace(sAMAccountName)
            with ldap3RESTARTABLE as conn:
                conn.search(
                    search_base=ladp3search_base,
                    search_filter='(&(sAMAccountName='+sAMAccountName_repeace+')(&(objectCategory=person)(objectClass=user)))',)
                response = conn.response[0]
                dn = response.get('dn', '')
                if dn:
                    if field =='cn':
                        cn = "CN=" + rowjson['cn']
                        modify_dn = conn.modify_dn(dn, cn)
                    else:
                        attributesVaule = rowjson.get(field,None)
                        if attributesVaule:
                            attributesVaule = [attributesVaule]
                        else:
                            attributesVaule = []
                        modify_dn = conn.modify(dn=dn, changes={field: [(MODIFY_REPLACE, attributesVaule)]})
                    if modify_dn:
                        result = {'isSuccess': True, "message": str(field)+'的属性值'+str(oldValue)+'修改为'+rowjson.get(field,'')}
                    else:
                        result = {'isSuccess': False, "message": str(field)+'的属性修改失败'}
        else:
            result = {'isSuccess': False, "message": '权限不足'}
    except Exception as e:
        result = {'isSuccess': False, "message": str(e)}
    insert_log(username, request, str(result['isSuccess']), str(result), '')
    response = HttpResponse()
    response['Content-Type'] = "text/javascript"
    response.write(json.dumps(result).encode("UTF-8"))
    return response

# 批量修改文件 多进程
def executemodifyuser(request):
    getData = request.POST.get('getData',{})
    username = request.session.get('username')
    try:
        username = request.session.get('username')
        permess = Userperm(username, 'operate')
        if permess['isSuccess']:
            getDatatojson = json.loads(getData)
            modifyalluser = thrmodifyalluser(getDatatojson,username)
            if modifyalluser:
                if '' in getDatatojson[0]:
                    getDatatojson[0].pop('')
                if '0' in getDatatojson[0]:
                    getDatatojson[0].pop('0')
                attributesldap = list(getDatatojson[0].keys())
                columns=[]
                for c in range(0, len(attributesldap)):
                    columns.append({'field': attributesldap[c], 'title':attributesldap[c]})
            result = {'isSuccess': True, "message": modifyalluser,'columns':columns}
        else:
            result = {'isSuccess': False, "message": '权限不足'}
    except Exception as e:
        result = {'isSuccess': False, "message": str(e)}
    insert_log(username, request, str(result['isSuccess']), str(result), '')
    response = HttpResponse()
    response['Content-Type'] = "text/javascript"
    response.write(json.dumps(result))
    return response

# 登录批量修改用户密码页面
def modifypasswd(request):
    username = request.session.get('username')
    if username:
        return render_to_response('admanager/modifypasswd.html', locals())
    else:
        return render_to_response('login.html', locals())

## 查找需要修改的用户密码属性
def searchuser_passwd(request):
    dn = request.POST.get('dn',None)
    filteruser = request.POST.get('filteruser',None)
    try:
        heard =[{'field': 'sAMAccountName', 'title': 'sAMAccountName'},{'field': 'pwdLastSet', 'title': 'pwdLastSet'}]
        if filteruser:
            search_filter = '(&(anr='+filteruser+')(&(objectCategory=person)(objectClass=user)))'
        else:
            search_filter = "(&(objectCategory=person)(objectClass=user))"
        total_entries = 0
        response_id = []
        with ldap3RESTARTABLE as conn:
            entry_generator = conn.extend.standard.paged_search(
                search_base=dn,
                search_filter=search_filter,
                attributes=['sAMAccountName','pwdLastSet'], paged_size=1000, generator=True)
            for entry in entry_generator:
                attributes = (entry.get('attributes', ''))
                if attributes:
                    total_entries += 1
                    attributes = dict(attributes)
                    attributes['pwdLastSet'] = (utc2local(attributes['pwdLastSet'])).strftime("%Y-%m-%d %H:%M:%S")
                    if attributes['pwdLastSet'] == '1601-01-01 08:00:00':
                        attributes['pwdLastSet'] = 0
                    response_id.append(attributes)
            result_id = conn.result
            if result_id.get('result', '') in [0, 4]:
                result = {"isSuccess": True, "tabledata": response_id,'heard':heard}
            else:
                result = {"isSuccess": False, "message": str(result_id['description'])}
    except Exception as e:
        result = {'isSuccess': False, "message": str(e)}
    response = HttpResponse()
    response['Content-Type'] = "text/javascript"
    response.write(json.dumps(result).encode("UTF-8"))
    return response

# 批量修改用户密码 多进程
def executemodifypasswd(request):
    getData = request.POST.get('getData',{})
    radiovaule = request.POST.get('radiovaule', None)
    pwdLastSet = request.POST.get('pwdLastSet', None)
    add_passwd_count = request.POST.get('add_passwd_count', None)
    add_passwd1 = request.POST.get('add_passwd1', None)
    add_passwd2 = request.POST.get('add_passwd2', None)
    username = request.session.get('username')
    try:
        username = request.session.get('username')
        permess = Userperm(username, 'operate')
        if permess['isSuccess']:
            getDatatojson = json.loads(getData)
            if getDatatojson and radiovaule and (add_passwd1 == add_passwd2):
                modifyalluser = thrmodifyalluserpasswd(getDatatojson,username,radiovaule,pwdLastSet,add_passwd_count,add_passwd1)
                columns=[{'field': 'sAMAccountName', 'title':'sAMAccountName'},{'field': 'password', 'title':'password'},{'field': 'pwdLastSet', 'title':'pwdLastSet'}]
                result = {'isSuccess': True, "message": modifyalluser,'columns':columns}
            else:
                result = {'isSuccess': False, "message": '传入空值或2次密码不一致', }
        else:
            result = {'isSuccess': False, "message": '权限不足'}
    except Exception as e:
        result = {'isSuccess': False, "message": str(e)}
    insert_log(username, request, str(result['isSuccess']), str(result), '')
    response = HttpResponse()
    response['Content-Type'] = "text/javascript"
    response.write(json.dumps(result))
    return response

# 登录移动用户页面
def moveuser(request):
    username = request.session.get('username')
    if username:
        return render_to_response('admanager/moveuser.html', locals())
    else:
        return render_to_response('login.html', locals())

# 批量移动用户 多进程
def executemoveuser(request):
    getData = request.POST.get('getData',{})
    movetoou = request.POST.get('movetoou', None)
    username = request.session.get('username')
    objectClass = request.POST.get('objectClass', 'user')
    try:
        permess = Userperm(username, 'operate')
        if permess['isSuccess']:
            getDatatojson = json.loads(getData)
            if getDatatojson and movetoou:
                modifyalluser = threxecutemoveuser(getDatatojson,username,movetoou,objectClass)
                if modifyalluser:
                    if '' in getDatatojson[0]:
                        getDatatojson[0].pop('')
                    if '0' in getDatatojson[0]:
                        getDatatojson[0].pop('0')
                    if 'status' in getDatatojson[0]:
                        getDatatojson[0].pop('status')
                    attributesldap = list(getDatatojson[0].keys())
                    columns = []
                    for c in range(0, len(attributesldap)):
                        columns.append({'field': attributesldap[c], 'title': attributesldap[c]})
                    for modifuser in modifyalluser:
                        if modifuser.get('description', ''):
                            modifuser['description'] = str(modifuser['description'][0])
                result = {'isSuccess': True, "message": modifyalluser,'columns':columns}
            else:
                result = {'isSuccess': False, "message": '传入空值', }
        else:
            result = {'isSuccess': False, "message": '权限不足'}
    except Exception as e:
        result = {'isSuccess': False, "message": str(e)}
    insert_log(username, request, str(result['isSuccess']), str(result), '')
    response = HttpResponse()
    response['Content-Type'] = "text/javascript"
    response.write(json.dumps(result))
    return response

# 登录批量创建邮箱 页面
def creatusermail(request):
    username = request.session.get('username')
    if username:
        return render_to_response('admanager/creatusermail.html', locals())
    else:
        return render_to_response('login.html', locals())

# 批量新建邮箱 多进程
def executecreatmail(request):
    getData = request.POST.get('getData',{})
    maildb = request.POST.get('maildb', '')
    mailarchive = request.POST.get('mailarchive', '')
    mailarchivedb = request.POST.get('mailarchivedb', '')
    username = request.session.get('username')
    try:
        permess = Userperm(username, 'operate')
        if permess['isSuccess']:
            getDatatojson = json.loads(getData)
            if getDatatojson and maildb:
                modifyalluser = threxecutecreatmail(getDatatojson,username,maildb,mailarchive,mailarchivedb)
                if modifyalluser:
                    if '' in getDatatojson[0]:
                        getDatatojson[0].pop('')
                    if '0' in getDatatojson[0]:
                        getDatatojson[0].pop('0')
                    if 'status' in getDatatojson[0]:
                        getDatatojson[0].pop('status')
                    attributesldap = list(getDatatojson[0].keys())
                    columns = []
                    for c in range(0, len(attributesldap)):
                        columns.append({'field': attributesldap[c], 'title': attributesldap[c]})
                    for modifuser in modifyalluser:
                        if modifuser.get('description', ''):
                            modifuser['description'] = str(modifuser['description'][0])
                result = {'isSuccess': True, "message": modifyalluser,'columns':columns}
            else:
                result = {'isSuccess': False, "message": '传入空值', }
        else:
            result = {'isSuccess': False, "message": '权限不足'}
    except Exception as e:
        result = {'isSuccess': False, "message": str(e)}
    insert_log(username, request, str(result['isSuccess']), str(result), '')
    response = HttpResponse()
    response['Content-Type'] = "text/javascript"
    response.write(json.dumps(result))
    return response

# 登录ldap属性 页面
def ladpattributes(request):
    username = request.session.get('username')
    if username:
        return render_to_response('admanager/ladpattributes.html', locals())
    else:
        return render_to_response('login.html', locals())

# 获取ldap属性 查找数据库
def getsqlldapattributes(request):
    try:
        username = request.session.get('username')
        row = get_log_ldapattributes()
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

# 登录移动计算机页面
def movecomputer(request):
    username = request.session.get('username')
    if username:
        return render_to_response('admanager/movecomputer.html', locals())
    else:
        return render_to_response('login.html', locals())