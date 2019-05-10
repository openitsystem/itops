# -*- coding: utf-8 -*-
# @Time    : 2019/1/16 18:33
# @Author  :
import queue
import threading

from apps.activeapi.th_creat_mail import UserCreatMail
from itops.settings import ldap3RESTARTABLE


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
                if 'disableuser' in getDatato:
                    getDatato.update({'userAccountControl': 546})
                    getDatato.pop('disableuser')
                else:
                    getDatato.update({'userAccountControl': 544})
                if 'password' in getDatato:
                    usermessage.update({'password': getDatato['password']})
                    getDatato.pop('password')
                if 'maildb' in getDatato:
                    usermessage.update({'maildb': getDatato['maildb']})
                    getDatato.pop('maildb')
                if getDatato['cn'] and getDatato['sAMAccountName']:
                    newdistinguishedName = "CN=" + getDatato['cn'] + "," + distinguishedName
                    usermessage.update({'cn': getDatato['cn']})
                    getDatato.pop('cn')
                    with ldap3RESTARTABLE as conn:
                        newuser = conn.add(
                            dn=newdistinguishedName,
                            object_class=[
                                "top",
                                "person",
                                "organizationalPerson",
                                "user"],
                            attributes=getDatato)
                        if newuser:
                            if 'password' in usermessage:
                                print('设置密码')
                            else:
                                print('自动密码')
                                result.update({'password': '自动密码'})
                            if 'maildb' in usermessage:
                                UserCreatMail(getDatato['sAMAccountName'], usermessage['maildb'])
                                status = {'status':'用户创建成功'}
                        else:
                            status = {'status': '用户创建失败：'+str(conn.result)}
                else:
                    status = {'status': '用户创建失败：cn,sAMAccountName不能为空'}
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