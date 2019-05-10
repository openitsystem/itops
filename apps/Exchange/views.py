#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2018/12/13 12:31
# @Author  : Center
import json
from urllib import request, parse

from django.http import HttpResponse
from django.shortcuts import render_to_response


# AD搜索页面

from itapi.exapi import GetExchangeServer, exapi


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