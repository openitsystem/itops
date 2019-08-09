# -*- coding: utf-8 -*-
# @Time    : 2019/1/16 18:33
# @Author  :
import queue
import threading

from ADapi.views import UserToExc
from apps.admanager.pwd import getpwd
from dbinfo.views import insert_log_table_name
from itops.settings import ldap3RESTARTABLE, ladp3search_domain


def repeace_dn(message):
    promessage=message.replace('(',r'\28').replace(')',r'\29').replace('*',r'2a')
    return promessage

creatusermessage = []

class CreatUserThread(threading.Thread):
    def __init__(self, que):
        threading.Thread.__init__(self)
        self.queue = que

    def run(self):
        while True: # 需要通过循环来不断的运行任务
            item = self.queue.get()
            getDatato = item[0]
            dn = item[1]
            try:
                distinguishedName = repeace_dn(dn)
                usermessage = {}
                result = {}
                status = {'status': '用户创建失败'}
                if '0' in getDatato:
                    getDatato.pop('0')
                if 'sAMAccountName' in getDatato:
                    sAMAccountName = getDatato['sAMAccountName']
                    if 'cn' in getDatato:
                        newdistinguishedName = "CN=" + getDatato['cn'] + "," + distinguishedName
                        usermessage.update({'cn': getDatato['cn']})
                        getDatato.pop('cn')
                    else:
                        newdistinguishedName = "CN=" + sAMAccountName + "," + distinguishedName
                    if 'userPrincipalName' in getDatato:
                        userPrincipalName = getDatato['userPrincipalName']
                        getDatato.pop('userPrincipalName')
                    else:
                        userPrincipalName = sAMAccountName + '@' + ladp3search_domain
                    if 'disableuser' in getDatato:
                        userAccountControl = 546
                        getDatato.pop('disableuser')
                    else:
                        userAccountControl = 544
                    with ldap3RESTARTABLE as conn:
                        newuser = conn.add(
                            dn=newdistinguishedName,
                            object_class=["top", "person", "organizationalPerson", "user"],
                            attributes={'sAMAccountName': sAMAccountName, 'userPrincipalName':userPrincipalName, 'userAccountControl':userAccountControl})
                        if newuser:
                            status = {'status': '用户创建成功'}
                            usermessage.update({'sAMAccountName': sAMAccountName})
                            usermessage.update({'userPrincipalName': userPrincipalName})
                            usermessage.update({'userAccountControl': userAccountControl})
                            getDatato.pop('sAMAccountName')
                            if 'password' in getDatato:
                                passwd = getDatato['password']
                                getDatato.pop('password')
                            else:
                                passwd = getpwd(10)
                            port = conn.server.port
                            if int(port) == 636:
                                modify_password = conn.extend.microsoft.modify_password(newdistinguishedName, passwd)
                                if modify_password:
                                    result.update({'password': passwd})
                                    modify_userAccountControl = conn.modify(dn=newdistinguishedName, changes={'userAccountControl': [('MODIFY_REPLACE', [512])]})
                                    if modify_userAccountControl:
                                        usermessage.update({'userAccountControl': 512})
                                else:
                                    result.update({'password': '设置密码失败'})
                            else:
                                result.update({'password': '设置密码LDAP必须采用加密连接,端口636'})
                            if 'maildb' in getDatato:
                                maildb = getDatato['maildb']
                                if maildb:
                                    #UserCreatMail(sAMAccountName, maildb)
                                    import time
                                    import random
                                    time.sleep(int(random.randint(60,130)))
                                    UserToExcs = UserToExc(sAMAccountName, maildb)
                                    if not UserToExcs['isSuccess']:
                                        insert_log_table_name('log', '', 'user_to_exc', '创建邮箱', str(UserToExcs['isSuccess']), str(sAMAccountName), str(UserToExcs['message']), str(maildb))
                                usermessage.update({'maildb': maildb})
                                getDatato.pop('maildb')
                            for dataName, dateVaule in getDatato.items():
                                try:
                                    modify_user = conn.modify(dn=newdistinguishedName, changes={dataName: [('MODIFY_REPLACE', [dateVaule])]})
                                    if not modify_user:
                                        getDatato.update({dataName: '修改属性失败'})
                                except:
                                    getDatato.pop(dataName)
                        else:
                            status = {'status': '用户创建失败：'+str(conn.result)}
                else:
                    status = {'status': '用户创建失败：sAMAccountName不能为空'}
            except Exception as e:
                status = {'status': '用户创建失败:'+str(e)}
            result.update(getDatato)
            result.update(usermessage)
            result.update(status)
            creatusermessage.append(result)
            self.queue.task_done()

q = queue.Queue(100)
def thrcreatalluser(getDatatojson,dn):
    del creatusermessage[:]
    # 开启线程
    for i in range(100):
        t = CreatUserThread(q)
        t.daemon = True
        t.start()

    for getDatato in getDatatojson:
        listvalue = [getDatato,dn]
        q.put(listvalue)
    q.join()
    return creatusermessage