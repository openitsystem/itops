import datetime
import threading
import time

from ADapi.views import getuserdownload,getgroupdownload,getdownload,getmaildownload
from dbinfo.views import selectindexmessagesrecord, selectindexmessagedb, insert_indexmessagedb
from dbinfo.models import crearindexmessagedb

from apscheduler.scheduler import Scheduler  #定时任务

sched = Scheduler()
sched.daemonic = False



class SendHtmlEmail(threading.Thread):
    """send html email"""
    def __init__(self,):
        threading.Thread.__init__(self)
    def gotwo(self):
        alluservalue = hasuservaluebyspi()
        allgroupvalue = hasgroupvaluebyspi()
        allcomputervalue = hascomputervaluebyspi()
        allexchangevalue = hasexchangevaluebyspi()
        insert_indexmessagedb(allusercountvalue=alluservalue['allusercountvalue'],
                              alldisableusercountvalue=alluservalue['alldisableusercountvalue'],
                              allexpiredpasswordusercountvalue=alluservalue['allexpiredpasswordusercountvalue'],
                              alllockusercountvalue=alluservalue['alllockusercountvalue'],
                              nologoinusercountvalue=alluservalue['nologoinusercountvalue'],
                              allgroupcountvalue = allgroupvalue['allgroupcountvalue'],
                              allgrouptalkgroupcountvalue = allgroupvalue['allgrouptalkgroupcountvalue'],
                              allgroupsavegroupcpuntvalue = allgroupvalue['allgroupsavegroupcpuntvalue'],
                              allgroupnomembercountvalue = allgroupvalue['allgroupnomembercountvalue'],
                              allgrouphasmailcountvalue = allgroupvalue['allgrouphasmailcountvalue'],
                              allcomputercountvalue = allcomputervalue['allcomputercountvalue'],
                              allcomputernologoincountvalue = allcomputervalue['allcomputernologoincountvalue'],
                              allcomputernodisablecpuntvalue = allcomputervalue['allcomputernodisablecpuntvalue'],
                              allcomputerdisablecountvalue = allcomputervalue['allcomputerdisablecountvalue'],
                              allexchangeusercountvalue = allexchangevalue['allexchangeusercountvalue'],
                              allnoexchangeusercountvalue = allexchangevalue['allnoexchangeusercountvalue'],
                              allexchangehasarchivecpuntvalue = allexchangevalue['allexchangehasarchivecpuntvalue'],
                              allexchangenodizhicountvalue = allexchangevalue['allexchangenodizhicountvalue'],
                              allexchangenoarchivecountvalue = allexchangevalue['allexchangenoarchivecountvalue']
                              )
        # if selectindexmessagedb():
        #     print(2)
        # else:
        #     print(1)
    # 新建数据库
    def creatdb(self):
        crearindexmessagedb()
    def run(self):
        if selectindexmessagesrecord():
            self.gotwo()
        else:
            self.creatdb()
            self.gotwo()


def hasuservaluebyspi():
    getuserdownloadallusercountvalue = getuserdownload(idtyes='所有用户', datevalue=False, checkval='true')
    if getuserdownloadallusercountvalue['isSuccess']:
        allusercountvalue = len(getuserdownloadallusercountvalue['message'])
    else:
        allusercountvalue = 0
    getuserdownloadalldisableusercountvalue = getuserdownload(idtyes='禁用的用户', datevalue=False, checkval='true')
    if getuserdownloadalldisableusercountvalue['isSuccess']:
        alldisableusercountvalue = len(getuserdownloadalldisableusercountvalue['message'])
    else:
        alldisableusercountvalue = 0
    getuserdownloadallexpiredpasswordusercountvalue = getuserdownload(idtyes='密码已过期的用户', datevalue=False, checkval='true')
    if getuserdownloadallexpiredpasswordusercountvalue['isSuccess']:
        allexpiredpasswordusercountvalue = len(getuserdownloadallexpiredpasswordusercountvalue['message'])
    else:
        allexpiredpasswordusercountvalue = 0
    getuserdownloadalllockusercountvalue = getuserdownload(idtyes='锁定的用户', datevalue=False, checkval='true')
    if getuserdownloadalllockusercountvalue['isSuccess']:
        alllockusercountvalue = len(getuserdownloadalllockusercountvalue['message'])
    else:
        alllockusercountvalue = 0
    getuserdownloadnologoinusercountvalue = getuserdownload(idtyes='账号某些天之内未登录的账号', datevalue=int(30), checkval='true')
    if getuserdownloadnologoinusercountvalue['isSuccess']:
        nologoinusercountvalue = len(getuserdownloadnologoinusercountvalue['message'])
    else:
        nologoinusercountvalue = 0
    return {'allusercountvalue':allusercountvalue,'alldisableusercountvalue':alldisableusercountvalue,'allexpiredpasswordusercountvalue':allexpiredpasswordusercountvalue,'alllockusercountvalue':alllockusercountvalue,'nologoinusercountvalue':nologoinusercountvalue}


def hasgroupvaluebyspi():
    getgroupdownloadallgroupcountvalue = getgroupdownload(idtyes='所有组', checkval='true')
    if getgroupdownloadallgroupcountvalue['isSuccess']:
        allgroupcountvalue = len(getgroupdownloadallgroupcountvalue['message'])
    else:
        allgroupcountvalue = 0
    getgroupdownloadallgroupsavegroupcpuntvalue = getgroupdownload(idtyes='安全组', checkval='true')
    if getgroupdownloadallgroupsavegroupcpuntvalue['isSuccess']:
        allgroupsavegroupcpuntvalue = len(getgroupdownloadallgroupsavegroupcpuntvalue['message'])
    else:
        allgroupsavegroupcpuntvalue = 0
    getgroupdownloadallgrouptalkgroupcountvalue = getgroupdownload(idtyes='通讯组', checkval='true')
    if getgroupdownloadallgrouptalkgroupcountvalue['isSuccess']:
        allgrouptalkgroupcountvalue = len(getgroupdownloadallgrouptalkgroupcountvalue['message'])
    else:
        allgrouptalkgroupcountvalue = 0
    getgroupdownloadallgroupnomembercountvalue = getgroupdownload(idtyes='没有成员的组', checkval='true')
    if getgroupdownloadallgroupnomembercountvalue['isSuccess']:
        allgroupnomembercountvalue = len(getgroupdownloadallgroupnomembercountvalue['message'])
    else:
        allgroupnomembercountvalue = 0
    getgroupdownloadallgrouphasmailcountvalue = getmaildownload(idtyes='已启用邮箱的组', checkval='true')
    if getgroupdownloadallgrouphasmailcountvalue['isSuccess']:
        allgrouphasmailcountvalue = len(getgroupdownloadallgrouphasmailcountvalue['message'])
    else:
        allgrouphasmailcountvalue = 0
    return {'allgroupcountvalue':allgroupcountvalue,'allgroupsavegroupcpuntvalue':allgroupsavegroupcpuntvalue,'allgrouptalkgroupcountvalue':allgrouptalkgroupcountvalue,'allgroupnomembercountvalue':allgroupnomembercountvalue,'allgrouphasmailcountvalue':allgrouphasmailcountvalue}


def hascomputervaluebyspi():
    getdownloadallcomputercountvalue = getdownload('所有计算机', int(1), 'true')
    if getdownloadallcomputercountvalue['isSuccess']:
        allcomputercountvalue = len(getdownloadallcomputercountvalue['message'])
    else:
        allcomputercountvalue = 0
    getdownloadallcomputernodisablecpuntvalue = getdownload('启用的计算机', int(1), 'true')
    if getdownloadallcomputernodisablecpuntvalue['isSuccess']:
        allcomputernodisablecpuntvalue = len(getdownloadallcomputernodisablecpuntvalue['message'])
    else:
        allcomputernodisablecpuntvalue = 0
    getdownloadallcomputerdisablecountvalue = getdownload('禁用的计算机', int(1), 'true')
    if getdownloadallcomputerdisablecountvalue['isSuccess']:
        allcomputerdisablecountvalue = len(getdownloadallcomputerdisablecountvalue['message'])
    else:
        allcomputerdisablecountvalue = 0
    datevalue = datetime.datetime.strptime(
        (datetime.datetime.now() + datetime.timedelta(days=-int(30))).strftime('%Y-%m-%d'),
        '%Y-%m-%d')
    mintime = time.mktime(datevalue.timetuple())
    namintime = int(mintime + 11644473600)
    nowTime = lambda: int(round(namintime * 10000000))
    getdownloadallcomputernologoincountvalue = getdownload('N', nowTime(), 'true')
    if getdownloadallcomputernologoincountvalue['isSuccess']:
        allcomputernologoincountvalue = len(getdownloadallcomputernologoincountvalue['message'])
    else:
        allcomputernologoincountvalue = 0
    return {'allcomputercountvalue':allcomputercountvalue,'allcomputernodisablecpuntvalue':allcomputernodisablecpuntvalue,'allcomputerdisablecountvalue':allcomputerdisablecountvalue,'allcomputernologoincountvalue':allcomputernologoincountvalue}


def hasexchangevaluebyspi():
    getmaildownloadallexchangeusercountvalue = getmaildownload(idtyes='已启用邮箱的用户',checkval='true')
    if getmaildownloadallexchangeusercountvalue['isSuccess']:
        allexchangeusercountvalue = len(getmaildownloadallexchangeusercountvalue['message'])
    else:
        allexchangeusercountvalue = 0
    getmaildownloadallnoexchangeusercountvalue = getmaildownload(idtyes='未启用邮箱的用户',checkval='true')
    if getmaildownloadallnoexchangeusercountvalue['isSuccess']:
        allnoexchangeusercountvalue = len(getmaildownloadallnoexchangeusercountvalue['message'])
    else:
        allnoexchangeusercountvalue = 0
    getmaildownloadallexchangehasarchivecpuntvalue = getmaildownload(idtyes='已启用归档账户',checkval='true')
    if getmaildownloadallexchangehasarchivecpuntvalue['isSuccess']:
        allexchangehasarchivecpuntvalue = len(getmaildownloadallexchangehasarchivecpuntvalue['message'])
    else:
        allexchangehasarchivecpuntvalue = 0
    getmaildownloadallexchangenodizhicountvalue = getmaildownload(idtyes='使用默认的数据库存储限制',checkval='true')
    if getmaildownloadallexchangenodizhicountvalue['isSuccess']:
        allexchangenodizhicountvalue = len(getmaildownloadallexchangenodizhicountvalue['message'])
    else:
        allexchangenodizhicountvalue = 0
    getmaildownloadallexchangenoarchivecountvalue = getmaildownload(idtyes='已禁用归档账户',checkval='true')
    if getmaildownloadallexchangenoarchivecountvalue['isSuccess']:
        allexchangenoarchivecountvalue = len(getmaildownloadallexchangenoarchivecountvalue['message'])
    else:
        allexchangenoarchivecountvalue = 0
    return {'allexchangeusercountvalue':allexchangeusercountvalue,'allnoexchangeusercountvalue':allnoexchangeusercountvalue,'allexchangehasarchivecpuntvalue':allexchangehasarchivecpuntvalue,'allexchangenodizhicountvalue':allexchangenodizhicountvalue,'allexchangenoarchivecountvalue':allexchangenoarchivecountvalue}

def hasindexvaluemessagetomysql():
    send_email = SendHtmlEmail()
    send_email.start()

# print(hasindexvaluemessagetomysql())

def startapschedulerscheduler():
    pass

sched.add_cron_job(hasindexvaluemessagetomysql,max_instances=100,day='*/1', hour='*/1',minute='30')

sched.start()
