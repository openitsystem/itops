import hashlib
import uuid

from itapi.exapi import GetExchangeServer, exapi
import json
import requests
import datetime
from django.http import HttpResponseRedirect, HttpResponse
from dbinfo.views import selectexchangedbmessage, crear_exchangedbmessage, getskey, getexchangedbmessage, \
    getexchangedblastdaymessage, insert_exchangedbmessage, selectexchangedbisStartMailboxMessageHas, \
    create_isStartMailboxMessageHas, getexchangedbisStartMailboxMessageHas, insert_isStartMailboxMessageHas, \
    selectexmailboxsizeHas, create_exmailboxsize, insert_exmailboxsizedb, getexchangedbisStartMailboxMessageHas_Nodate, \
    selectMailboxConfigMessageHas, create_mailboxMessageConfigHas, getMailboxMessageConfigHas, \
    updateMailboxMessageConfigDB, updateMailboxMessageConfigDBMailboxNum, getexchangedbexmailboxsize
from itapi.exapi import GetMailboxdatabase
import random,time
from apscheduler.scheduler import Scheduler  #定时任务

sched = Scheduler()
sched.daemonic = False


def aaa():
    exchange = exapi()
    exchange.connectionscriptall('Get-Mailbox -database SZDB01| Measure-Object')
    # exchange.connectionscriptall('Get-MailboxDatabase -Status')
    exchange.Serializationmessage()
    # return exchange.returnfuction()
    a = exchange.returnfuction()
    # response = HttpResponse()
    # response['Content-Type'] = "application/json"
    # response.write(json.dumps(a, default=str).encode("UTF-8"))
    return a

# print(aaa())

def GetMailboxallaccount(mailboxname):
    try:
        exchange = exapi()
        exchange.connectionscriptall('get-mailboxstatistics -database ' + mailboxname + ' | Measure-Object')
        exchange.Serializationmessage()
        return  exchange.returnfuction()
    except Exception as e:
        return  {'isSuccess': False, 'count': 0, 'msg': str(e), 'code': 201, 'message': ''}


def GetMailboxStatisticsnoidentity(**kwargs):
    try:
        exchange = exapi()
        exchange.connection('Get-MailboxStatistics', **kwargs)
        exchange.Serializationmessage()
        return  exchange.returnfuction()
    except Exception as e:
        return  {'isSuccess': False, 'count': 0, 'msg': str(e), 'code': 201, 'message': ''}


def selectmysql():
    if not selectexchangedbmessage():
        crear_exchangedbmessage()
        return False
    getexchangedbmessagevalue = getexchangedbmessage(datetime.datetime.now().strftime("%Y-%m-%d"))
    return (getexchangedbmessagevalue)


def indexdef():
    hasexchange = getskey()
    if hasexchange:
        if hasexchange['status'] == '1':
            return True
    return False

def startmailboxvalue():
    if indexdef():
        if not selectmysql():
            MailboxDatabasevaluelist = GetMailboxdatabase(Status=True)
            if MailboxDatabasevaluelist['isSuccess']:
                for i in MailboxDatabasevaluelist['message']:
                    memberaccountvalue = GetMailboxStatisticsnoidentity(database = i['Identity'])
                    if memberaccountvalue['isSuccess']:
                        memberaccount = memberaccountvalue['count']
                    else:
                        memberaccount = 0
                    mailboxsitevalue = int((i['DatabaseSize']).split(' (')[1].split(' bytes)')[0].replace(',',''))
                    getexchangedblastdaymessagevalue = getexchangedblastdaymessage(i['Identity'],(datetime.datetime.now()+datetime.timedelta(days=-1)).strftime("%Y-%m-%d"))
                    if getexchangedblastdaymessagevalue:
                        increaseday = (int(mailboxsitevalue) - int(getexchangedblastdaymessagevalue['mailboxsite']))
                        estimateday = mailboxsitevalue + increaseday
                    else:
                        increaseday = 0
                        estimateday = 0
                    getexchangedblastweekmessagevalue = getexchangedblastdaymessage(i['Identity'], (
                                datetime.datetime.now() + datetime.timedelta(days=-7)).strftime("%Y-%m-%d"))
                    if getexchangedblastweekmessagevalue:
                        increaseweek = round((int(mailboxsitevalue) - int(getexchangedblastweekmessagevalue['mailboxsite']))/7)
                        estimateweek = (increaseweek * 7) + mailboxsitevalue
                    else:
                        increaseweek = 0
                        estimateweek = 0
                    getexchangedbthisdaymessagevalue = getexchangedblastdaymessage(i['Identity'],(datetime.datetime.now()).strftime("%Y-%m-%d"))
                    if not getexchangedbthisdaymessagevalue:
                        insert_exchangedbmessage(i['Identity'],int((i['DatabaseSize']).split(' (')[1].split(' bytes)')[0].replace(',','')),increaseday,increaseweek,estimateday,estimateweek,memberaccount)

#判断是否执行表是否存在，不存在则创建
def selectisStartMailboxMessageHasmysql():
    if not selectexchangedbisStartMailboxMessageHas():
        create_isStartMailboxMessageHas()
        return False
    selectisStartMailboxMessageHasmysqlValueSelect = selectisStartMailboxMessageHasmysqlValue()
    getexchangedbmessagevalue = getexchangedbisStartMailboxMessageHas(selectisStartMailboxMessageHasmysqlValueSelect['datetimeValue'].strftime("%Y-%m-%d"))
    return getexchangedbmessagevalue

#判断是否执行表是否存在，不存在则创建
def selectisStartMailboxMessageHasmysqlStart():
    if not selectexchangedbisStartMailboxMessageHas():
        create_isStartMailboxMessageHas()
        return False
    getexchangedbmessagevalue = getexchangedbisStartMailboxMessageHas(datetime.datetime.now().strftime("%Y-%m-%d"))
    return getexchangedbmessagevalue

#判断mailbox配置是否存在，不存在则创建
def selectMailboxConfigDBHas():
    if not selectMailboxConfigMessageHas():
        create_mailboxMessageConfigHas()
    getexchangedbmessagevalue = getMailboxMessageConfigHas()
    return getexchangedbmessagevalue


#更新db
def updateMailboxConfigDB(mailboxSizeThresholdIntValue,mailboxSizeThresholdCompanyValue,mailboxSizeThresholdInt):
    getexchangedbmessagevalue = getMailboxMessageConfigHas()['id']
    updateexchangedbmessagevalue = updateMailboxMessageConfigDB(getexchangedbmessagevalue,mailboxSizeThresholdIntValue,mailboxSizeThresholdCompanyValue,mailboxSizeThresholdInt)
    return updateexchangedbmessagevalue

#更新db
def updateMailboxConfigDBMailboxNum(mailboxSizeThresholdIntValue):
    getexchangedbmessagevalue = getMailboxMessageConfigHas()['id']
    updateexchangedbmessagevalue = updateMailboxMessageConfigDBMailboxNum(getexchangedbmessagevalue,mailboxSizeThresholdIntValue)
    return updateexchangedbmessagevalue


#判断是否执行表是否存在，不存在则创建
def selectisStartMailboxMessageHasmysqlValue():
    if not selectexchangedbisStartMailboxMessageHas():
        create_isStartMailboxMessageHas()
        return False
    getexchangedbmessagevalue = getexchangedbisStartMailboxMessageHas_Nodate()
    return getexchangedbmessagevalue


#判断exmailboxsize表是否存在，不存在则创建
def selectexmailboxsizeHasmysql():
    if not selectexmailboxsizeHas():
        create_exmailboxsize()


def sizeStrToInt(sizeStr):
    try:
        sizeInt = sizeStr.split(' (')[1].split(' bytes)')[0].replace(',','')
        return sizeInt
    except Exception as e:
        return 0

def startHasMailboxMessage(datetimeValueToday):
    try:
        datetimeValue = datetimeValueToday.strftime("%Y-%m-%d")
        allMailboxdatabaseList = GetMailboxdatabase(Status=True)
        if allMailboxdatabaseList['isSuccess']:
            selectexmailboxsizeHasmysql()
            for i in allMailboxdatabaseList['message']:
                DatabaseSizeInt = sizeStrToInt(i['DatabaseSize'])
                AvailableNewMailboxSpaceInt = sizeStrToInt(i['AvailableNewMailboxSpace'])
                mailboxAccountResponce = GetMailboxallaccount(i['Identity'])
                mailboxAccount = 0
                mailboxGuidValue = i['Guid']
                if mailboxAccountResponce['isSuccess']:
                    mailboxAccount_noarchive = mailboxAccountResponce['message'][0]['Count']
                else:
                    mailboxAccount_noarchive = 0
                    mailboxGuidValue = str(mailboxAccountResponce['message']) + str(mailboxAccountResponce['msg'])
                databaseSpaceProportion = int(float("%.4f" % (int(AvailableNewMailboxSpaceInt)/int(DatabaseSizeInt))) * 1000)
                insert_exmailboxsizedb(i['Identity'],mailboxGuidValue,i['DatabaseSize'],DatabaseSizeInt,i['AvailableNewMailboxSpace'],AvailableNewMailboxSpaceInt,mailboxAccount_noarchive,databaseSpaceProportion,datetimeValue)
    except Exception as e:
        print('邮箱数据插入失败！',e)

def hasMailboxMessage():
    sleepTimeValue = random.randint(1,100)
    time.sleep(sleepTimeValue)
    if indexdef():
        if not selectisStartMailboxMessageHasmysqlStart():
            datetimeValueToday = datetime.datetime.now()
            insert_isStartMailboxMessageHas(datetimeValueToday.strftime("%Y-%m-%d"))
            startHasMailboxMessage(datetimeValueToday)

# hasMailboxMessage()
# mailboxMessageMonitor(datetime.datetime.now().strftime("%Y-%m-%d"))
def startmailboxvaluescheduler():
    pass

# sched.add_cron_job(startmailboxvalue,max_instances=100,day='*/1', hour='*/8')
sched.add_cron_job(hasMailboxMessage,max_instances=100,day='*/1', hour='6',minute='25')

sched.start()
