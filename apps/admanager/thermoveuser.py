# -*- coding: utf-8 -*-
# @Time    : 2019/1/16 13:33
# @Author  :
import queue
import threading

from ldap3 import MODIFY_REPLACE

from apps.activeapi.th_creat_mail import UserCreatMail
from dbinfo.views import insert_log_table_name
from itops.settings import ldap3RESTARTABLE, ladp3search_base


def repeace_dn(message):
    promessage=message.replace('(',r'\28').replace(')',r'\29').replace('*',r'2a')
    return promessage

modifyusermessage = []

class MoveUserThread(threading.Thread):
    def __init__(self, que):
        threading.Thread.__init__(self)
        self.queue = que

    def run(self):
        while True: # 需要通过循环来不断的运行任务
            item = self.queue.get()
            getDatato = item[0]
            username = item[1]
            movetoou = item[2]
            objectClass = item[3]
            try:
                usermessage = {}
                result = {}
                if '' in getDatato:
                    getDatato.pop('')
                if '0' in getDatato:
                    getDatato.pop('0')
                if 'status' in getDatato:
                    getDatato.pop('status')
                attributesldap = list(getDatato.keys())
                if getDatato['sAMAccountName']:
                    sAMAccountName_repeace = repeace_dn(getDatato['sAMAccountName'])
                    if objectClass == 'user':
                        search_filter = '(&(sAMAccountName=' + sAMAccountName_repeace + ')(&(objectCategory=person)(objectClass=user)))'
                    elif objectClass == 'computer':
                        search_filter = '(&(|(sAMAccountName=' + sAMAccountName_repeace + '$)(sAMAccountName=' + sAMAccountName_repeace + '))(&(objectClass=computer)))'
                    else:
                        search_filter ='(sAMAccountName=' + sAMAccountName_repeace + ')'
                    with ldap3RESTARTABLE as conn:
                        conn.search(
                            search_base=ladp3search_base,
                            search_filter=search_filter,
                            attributes=attributesldap)
                        response = conn.response[0]
                        dn = response.get('dn', '')
                        if dn:
                            attributes = response.get('attributes', '')
                            dn = repeace_dn(dn)
                            relative_dn = dn.split(",")[0]
                            new_superior = repeace_dn(movetoou)
                            operation_id = conn.modify_dn(
                                dn=dn,
                                relative_dn=relative_dn,
                                delete_old_dn=True,
                                new_superior=new_superior)
                            if operation_id:
                                result.update(dict(attributes))
                                result.update({'status': '移动成功'})
                            else:
                                result.update(dict(attributes))
                                result.update({'status': '移动失败'})
                            modify_dn_result = conn.result
                            insert_log_table_name('log_ldap', '172.0.0.1', 'MoveUserThread', username, str(True), str(item), str(result), str(modify_dn_result))
                        else:
                            message_log = {'status': '没有查询到对象,或属性值传入有错'}
                            insert_log_table_name('log_ldap', '172.0.0.1', 'MoveUserThread_search', username, str(False), str(item), str(message_log), '')
                            result.update(message_log)
                            result.update(getDatato)
                else:
                    message_log = {'status': '移动用户失败：sAMAccountName不能为空'}
                    insert_log_table_name('log_ldap', '172.0.0.1', 'MoveUserThread', username, str(False), str(item), str(message_log), '')
                    result.update(message_log)
                    result.update(getDatato)
            except Exception as e:
                result.update({'status': '移动用户失败:'+str(e)})
                result.update(getDatato)

            modifyusermessage.append(result)
            self.queue.task_done()

q = queue.Queue(500)
def threxecutemoveuser(getDatatojson,username,movetoou,objectClass="user"):
    del modifyusermessage[:]
    # 开启线程
    for i in range(500):
        t = MoveUserThread(q)
        t.daemon = True
        t.start()

    for getDatato in getDatatojson:
        listvalue = [getDatato,username,movetoou,objectClass]
        q.put(listvalue)
    q.join()
    return modifyusermessage