# -*- coding: utf-8 -*-
# @Time    : 2019/1/16 18:33
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

class ModifyUserThread(threading.Thread):
    def __init__(self, que):
        threading.Thread.__init__(self)
        self.queue = que

    def run(self):
        while True: # 需要通过循环来不断的运行任务
            item = self.queue.get()
            getDatato = item[0]
            username = item[1]
            try:
                usermessage = {}
                result = {}
                if '' in getDatato:
                    getDatato.pop('')
                if '0' in getDatato:
                    getDatato.pop('0')
                attributesldap = list(getDatato.keys())
                if getDatato['sAMAccountName']:
                    sAMAccountName_repeace = repeace_dn(getDatato['sAMAccountName'])
                    with ldap3RESTARTABLE as conn:
                        conn.search(
                            search_base=ladp3search_base,
                            search_filter='(&(sAMAccountName=' + sAMAccountName_repeace + ')(&(objectCategory=person)(objectClass=user)))',
                            attributes=attributesldap)
                        response = conn.response[0]
                        dn = response.get('dn', '')
                        if dn:
                            attributes = response.get('attributes', '')
                            cn = None
                            for key, vaule in dict(attributes).items():
                                if key == 'cn':
                                    cn = "CN=" + getDatato.get('cn', None)
                                else:
                                    attributesVaule = getDatato.get(key, None)
                                    if attributesVaule:
                                        attributesVaule = [attributesVaule]
                                    else:
                                        attributesVaule = []
                                    modify_dn = conn.modify(dn=dn, changes={key: [(MODIFY_REPLACE, attributesVaule)]})
                                message = dn +'的属性'+key+'：的值'+str(attributes[key])+'修改成'+str(getDatato[key])
                                insert_log_table_name('log_ldap', '172.0.0.1', 'ModifyUserThread_modify_dn', username, str(modify_dn), str(item), message, str(attributes))
                            if cn:
                                modify_cn = conn.modify_dn(dn, cn)
                                message_cn = dn + '的属性cn：的值' + str(attributes.get('cn','')) + '修改成' + str(getDatato.get('cn',''))
                                insert_log_table_name('log_ldap', '172.0.0.1', 'ModifyUserThread_modify_cn', username, str(modify_cn), str(item), message_cn, str(attributes))
                            conn.search(
                                search_base=ladp3search_base,
                                search_filter='(&(sAMAccountName=' + sAMAccountName_repeace + ')(&(objectCategory=person)(objectClass=user)))',
                                attributes=attributesldap)
                            response = conn.response[0]
                            attributesmodify = response.get('attributes', '')
                            if attributesmodify:
                                result.update(dict(attributesmodify))
                                result.update({'status': '修改成功'})
                        else:
                            message_log = {'status': '没有查询到对象,或属性值传入有错'}
                            insert_log_table_name('log_ldap', '172.0.0.1', 'ModifyUserThread_search', username, str(False), str(item), message_log, '')
                            result.update(message_log)
                            result.update(getDatato)
                else:
                    message_log = {'status': '修改属性创建失败：sAMAccountName不能为空'}
                    insert_log_table_name('log_ldap', '172.0.0.1', 'ModifyUserThread', username, str(False), str(item), message, '')
                    result.update(message_log)
                    result.update(getDatato)
            except Exception as e:
                result.update({'status': '用户创建失败:'+str(e)})
                result.update(getDatato)

            modifyusermessage.append(result)
            self.queue.task_done()

q = queue.Queue(500)
def thrmodifyalluser(getDatatojson,username):
    del modifyusermessage[:]
    # 开启线程
    for i in range(500):
        t = ModifyUserThread(q)
        t.daemon = True
        t.start()

    for getDatato in getDatatojson:
        listvalue = [getDatato,username]
        q.put(listvalue)
    q.join()
    return modifyusermessage