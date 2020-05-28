#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2018/12/13 12:31
# @Author  : Center
import datetime
import json
from urllib import request, parse

from django.http import HttpResponse
from django.shortcuts import render_to_response


# AD搜索页面
from apps.Exchange.exchangeserver import selectisStartMailboxMessageHasmysql, selectisStartMailboxMessageHasmysqlValue, \
    selectMailboxConfigDBHas, updateMailboxConfigDB, updateMailboxConfigDBMailboxNum
from dbinfo.views import getexchangedbexmailboxsize, getexchangedbexmailboxsizeValue, getMailboxMessagebyGuidAndDays
from itapi.exapi import GetExchangeServer, exapi, GetMailboxDatabaseCopyStatus, MoveActiveMailboxDatabase, \
    GetMailboxdatabase, SetMailboxdatabase


def findmail(request):
    return render_to_response('mail/findmail.html', locals())



##Get-ExchangeServer *cas*权限查询
# def GetcasexchangeServerapi():
#     url=iisurl()+'/api/ad/GetcasexchangeServer'
#     value = {
#         "skey": 'A8C4D656BBBB2C42436B4B9B45FC63AD'
#     }
#     querystring = parse.urlencode(value)
#     u = request.urlopen(url + '?' + querystring).read().decode('utf-8')
#     respjson = json.loads(u)
#     return respjson

##get-messagetrackinglog权限查询
def getmessagetrackinglogapi(powermessage):
    try:
        exchange = exapi()
        exchange.connectionscriptall(powermessage)
        exchange.Serializationmessage()
        return exchange.returnfuction()
    except Exception as e:
        return  {'isSuccess': False, 'count': 0, 'msg': str(e), 'code': 201, 'message': ''}
    # url=iisurl()+'/api/ad/newgetmessagetrackinglog'
    # value = {
    #     "powermessage":powermessage,
    #     "skey": 'A8C4D656BBBB2C42436B4B9B45FC63AD'
    # }
    # querystring = parse.urlencode(value)
    # u = request.urlopen(url + '?' + querystring).read().decode('utf-8')
    # respjson = json.loads(u)
    # return respjson


def mailvlafind(request):
    inpresive = request.POST.get('inpresive')#收件人
    inpsender = request.POST.get('inpsender')#发件人
    inptselevenid = request.POST.get('inptselevenid')#eventid
    inpmessagidmail = request.POST.get('inpmessagidmail')#messageid
    inpnternaMessage = request.POST.get('inpnternaMessage')#intermessageid
    inpsubjtcdid = request.POST.get('inpsubjtcdid')#主题
    inpendtimeid = request.POST.get('inpendtimeid')#时间段
    powermessage = 'get-messagetrackinglog'
    try:
        if inpresive :
            powermessage =  powermessage+' -Recipients: '+inpresive
        if inpsender:
            powermessage=powermessage+' -Sender '+inpsender
        if inptselevenid:
            powermessage=powermessage+' -EventID '+inptselevenid
        if inpmessagidmail:
            powermessage = powermessage + ' -MessageID ' + inpmessagidmail
        if inpnternaMessage:
            powermessage=powermessage+' -InternalMessageID '+inpnternaMessage
        if inpsubjtcdid:
            powermessage = powermessage + ' -MessageSubject "' + inpsubjtcdid + '"'
        if inpendtimeid:
            inpendtimeid=inpendtimeid.split(' 到 ')
            powermessage = powermessage + ' -Start ' +'"'+ inpendtimeid[0]+'"'+' -End '+'"'+inpendtimeid[1]+'"'
        # allcasservers = GetcasexchangeServerapi()['message'].split(";")
        allcasservers = list()
        allcasserversvalue = GetExchangeServer()['message']
        allcasserversvaluelastvalue = list()
        for i in allcasserversvalue:
            if 'ClientAccess' in i['ServerRole']:
                allcasserversvaluelastvalue.append(i)
        for i in allcasserversvalue:
            allcasservers.append(i['Identity'])
        values = list()
        for casserver in allcasservers:
            if casserver != '':
                powermessageo = powermessage+' -Server '+casserver
                allmailvalues=getmessagetrackinglogapi(powermessageo)
                mailvalues = allmailvalues['message']
                if allmailvalues['isSuccess']:
                    for mailvalue in mailvalues:
                        if mailvalue != []:
                            if values == []:
                                values.append(mailvalue)
                            else:
                                if mailvalue not in values:
                                    values.append(mailvalue)
        result = {'isSuccess': True, "result": values}

    except Exception as e:
        result = {'isSuccess': False, "result": str(e)}
    response = HttpResponse()
    response['Content-Type'] = "application/json"
    response.write(json.dumps(result, default=str).encode("UTF-8"))
    return response


def searchMailboxMessage(request):
    isSuccess,message = False,list()
    # 获取执行列表里上一次获取数据库数据的时间
    Hasmysql = selectisStartMailboxMessageHasmysqlValue()
    if Hasmysql:
        getexchangedbexmailboxsizeValue = getexchangedbexmailboxsize(Hasmysql['datetimeValue'])
        isSuccess,message = True,getexchangedbexmailboxsizeValue
    else:
        isSuccess,message = False,[]
    result = {'isSuccess':isSuccess,'message':message}
    response = HttpResponse()
    response['Content-Type'] = "text/javascript"
    response.write(json.dumps(result,default=str).encode("UTF-8"))
    return response

def searchmailboxvalue(request):
    mailboxName = request.POST.get('mailboxName')
    typeValue = request.POST.get('typeValue')
    isSuccess,message = False,list()
    # 获取执行列表里上一次获取数据库数据的时间
    Hasmysql = selectisStartMailboxMessageHasmysql()
    if Hasmysql:
        getexchangedbexmailboxsize = getexchangedbexmailboxsizeValue(Hasmysql['datetimeValue'],mailboxName,typeValue)
        isSuccess,message = True,getexchangedbexmailboxsize
    else:
        isSuccess,message = False,[]
    result = {'isSuccess':isSuccess,'message':message}
    response = HttpResponse()
    response['Content-Type'] = "text/javascript"
    response.write(json.dumps(result,default=str).encode("UTF-8"))
    return response


def searchmailboxconfig(request):
    # 获取执行列表里上一次获取数据库数据的时间
    try:
        Hasmysql = selectMailboxConfigDBHas()
        result = {'isSuccess': True, 'message': Hasmysql}
    except Exception as e:
        result = {'isSuccess': False, 'message': ''}
    response = HttpResponse()
    response['Content-Type'] = "text/javascript"
    response.write(json.dumps(result,default=str).encode("UTF-8"))
    return response


def savemailboxconfig(request):
    # 获取执行列表里上一次获取数据库数据的时间
    try:
        saveType = request.POST.get('saveType')
        if saveType == 'mailboxSizeValue':
            mailboxSizeValueStr = request.POST.get('mailboxSizeValueStr')
            mailboxSizeValueCompany = request.POST.get('mailboxSizeValueCompany')
            if 1 <= int(mailboxSizeValueStr) <= 1024 and mailboxSizeValueCompany in ['TB', 'MB', 'GB']:
                selectMailboxConfigDBHas()
                typeValueTB, typeValueMB, typeValueGB = 'TB', 'MB', 'GB'
                typeIntValue = 1099511627776 if mailboxSizeValueCompany == typeValueTB else (1048576 if mailboxSizeValueCompany == typeValueMB else 1073741824)
                updateMailboxConfigDB(int(mailboxSizeValueStr),mailboxSizeValueCompany,int(mailboxSizeValueStr)*int(typeIntValue))
                result = {'isSuccess': True, 'message': '保存成功'}
            else:
                result = {'isSuccess': False, 'message': '范围错误'}
        elif saveType == 'mailboxNumValue':
            mailboxNumValueStr = request.POST.get('mailboxNumValueStr')
            if 1 <= int(mailboxNumValueStr):
                selectMailboxConfigDBHas()
                updateMailboxConfigDBMailboxNum(int(mailboxNumValueStr))
                result = {'isSuccess': True, 'message': '保存成功'}
            else:
                result = {'isSuccess': False, 'message': '范围错误'}
        else:
            result = {'isSuccess': False, 'message': '类型错误'}
    except Exception as e:
        result = {'isSuccess': False, 'message': ''}
    response = HttpResponse()
    response['Content-Type'] = "text/javascript"
    response.write(json.dumps(result,default=str).encode("UTF-8"))
    return response


def getmailboxaccounttrend(request):
    mailboxGuid = request.POST.get('mailboxGuid')
    datetimeNow = datetime.datetime.now()
    datatimeValuetoday = datetimeNow.strftime("%Y-%m-%d") + ' 00:00:00'
    datatimeValuestartday = (datetimeNow + datetime.timedelta(days=-7)).strftime("%Y-%m-%d") + ' 00:00:00'
    # 获取执行列表里上一次获取数据库数据的时间
    try:
        Hasmysql = getMailboxMessagebyGuidAndDays(mailboxGuid,datatimeValuetoday,datatimeValuestartday)
        accountList = list()
        datetimeValueList = list()
        databaseSizeIntList = list()
        databaseSpaceProportion = list()
        for i in Hasmysql:
            datetimeValueList.append(i['messageDatetime'].strftime("%m/%d"))
            accountList.append(i['databaseMailboxNumber'])
            databaseSizeIntList.append(i['databaseSizeInt'])
            databaseSpaceProportion.append(i['databaseSpaceProportion'])
        result = {'isSuccess': True, 'message': {'Hasmysql':Hasmysql,'accountList':accountList,'datetimeValueList':datetimeValueList,'databaseSizeIntList':databaseSizeIntList,'databaseSpaceProportion':databaseSpaceProportion}}
    except Exception as e:
        result = {'isSuccess': False, 'message': ''}
    response = HttpResponse()
    response['Content-Type'] = "text/javascript"
    response.write(json.dumps(result,default=str).encode("UTF-8"))
    return response

def getmailboxStatusMessage(request):
    mailboxIdentity = request.POST.get('mailboxIdentity')
    # 获取执行列表里上一次获取数据库数据的时间
    try:
        GetMailboxDatabaseCopyStatusListreturnValue = list()
        GetMailboxDatabaseCopyStatusList = GetMailboxDatabaseCopyStatus(mailboxIdentity)
        # for i in GetMailboxDatabaseCopyStatusList['message']:
        #     GetMailboxDatabaseCopyStatusListreturnValue.append({'ActiveCopy':i['ActiveCopy'],
        #                                                         'DiskTotalSpace':i['DiskTotalSpace'],
        #                                                         'Identity':i['Identity'],
        #                                                         'DiskFreeSpace':i['DiskFreeSpace'],
        #                                                         'ActivationPreference':i['ActivationPreference'],
        #                                                         'Status':i['Status'],
        #                                                         'ContentIndexState':i['ContentIndexState'],
        #                                                         'CopyQueueLength':i['CopyQueueLength'],
        #                                                         'ReplayQueueLength':i['ReplayQueueLength'],
        #                                                         'DiskFreeSpacePercent':i['DiskFreeSpacePercent'],
        #                                                         'DatabaseVolumeMountPoint':i['DatabaseVolumeMountPoint'],
        #                                                         'MailboxServer':i['MailboxServer']})
        result = {'isSuccess': True, 'message': GetMailboxDatabaseCopyStatusList,'count':GetMailboxDatabaseCopyStatusList['count']}
    except Exception as e:
        result = {'isSuccess': False, 'message': ''}
    response = HttpResponse()
    response['Content-Type'] = "text/javascript"
    response.write(json.dumps(result,default=str).encode("UTF-8"))
    return response

#迁移激活数据库
def moveDatabaseActiveOperation(request):
    identity = request.POST.get('identity')
    ActivateOnServer = request.POST.get('ActivateOnServer')
    # 获取执行列表里上一次获取数据库数据的时间
    try:
        result = MoveActiveMailboxDatabase(identity,ActivateOnServer=ActivateOnServer,SkipMoveSuppressionChecks=True,Confirm=False)
    except Exception as e:
        result = {'isSuccess': False, 'message': ''}
    response = HttpResponse()
    response['Content-Type'] = "text/javascript"
    response.write(json.dumps(result,default=str).encode("UTF-8"))
    return response

#获取数据库限制信息
def getmailboxSizelimitMessage(request):
    identity = request.POST.get('mailboxIdentity')
    # 获取执行列表里上一次获取数据库数据的时间
    try:
        GetMailboxdatabaseValue = GetMailboxdatabase(identity=identity)
        if GetMailboxdatabaseValue['isSuccess']:
            result = {'isSuccess': True, 'message': {'ProhibitSendReceiveQuota':GetMailboxdatabaseValue['message'][0]['ProhibitSendReceiveQuota'],
                                                     'ProhibitSendQuota':GetMailboxdatabaseValue['message'][0]['ProhibitSendQuota'],
                                                     'IssueWarningQuota':GetMailboxdatabaseValue['message'][0]['IssueWarningQuota']}}
        else:
            result = GetMailboxdatabaseValue
    except Exception as e:
        result = {'isSuccess': False, 'message': ''}
    response = HttpResponse()
    response['Content-Type'] = "text/javascript"
    response.write(json.dumps(result,default=str).encode("UTF-8"))
    return response


#获取数据库限制信息
def savemailboxSizelimit(request):
    saveType = request.POST.get('saveType')
    valueCompany = request.POST.get('valueCompany')
    valueInt = request.POST.get('valueInt')
    dbname = request.POST.get('dbname')
    # 获取执行列表里上一次获取数据库数据的时间
    try:
        SetMailboxdatabaseValue = SetMailboxdatabase(Identity=dbname,**{saveType:valueInt + ' ' + valueCompany})
        result = {'isSuccess': SetMailboxdatabaseValue['isSuccess'], 'message': SetMailboxdatabaseValue['msg']}
    except Exception as e:
        result = {'isSuccess': False, 'message': str(e)}
    response = HttpResponse()
    response['Content-Type'] = "text/javascript"
    response.write(json.dumps(result,default=str).encode("UTF-8"))
    return response

