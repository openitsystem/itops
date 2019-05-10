# -*- coding: utf-8 -*-
# @Time    : 2019/1/16 18:33
# @Author  :
import queue
import threading

from ldap3 import MODIFY_REPLACE

from apps.admanager.pwd import getpwd
from apps.ldaptime.views import utc2local
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
            radiovaule = item[2]
            pwdLastSet = item[3]
            add_passwd_count = item[4]
            add_passwd1 = item[5]
            try:
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
                            search_filter='(&(sAMAccountName=' + sAMAccountName_repeace + ')(&(objectCategory=person)(objectClass=user)))',attributes=['sAMAccountName','pwdLastSet'])
                        response = conn.response[0]
                        dn = response.get('dn', '')
                        if dn:
                            attributes = (response.get('attributes', ''))
                            attributes['pwdLastSet'] = (utc2local(attributes['pwdLastSet'])).strftime("%Y-%m-%d %H:%M:%S")
                            if attributes['pwdLastSet'] == '1601-01-01 08:00:00':
                                attributes['pwdLastSet'] = 0
                            if radiovaule == '随机密码':
                                passwd = getpwd(int(add_passwd_count))
                            elif radiovaule == '输入密码':
                                passwd = add_passwd1
                            else:
                                passwd = getDatato['password']
                            port = conn.server.port
                            if int(port) == 636:
                                modify_password = conn.extend.microsoft.modify_password(dn, passwd)
                                if modify_password:
                                    if pwdLastSet=='true' or (str(getDatato.get('pwdLastSet',1)) == '0'):
                                        modify_dn = conn.modify(dn=dn, changes={'pwdLastSet': [(MODIFY_REPLACE, [0])]})
                                        if modify_dn:
                                            message_log = {'status': '密码修改成功并设置用户下次必须更改密码','pwdLastSet':0}
                                        else:
                                            message_log = {'status': '密码修改成功，设置用户下次必须更改密码：失败','pwdLastSet':attributes['pwdLastSet']}
                                    else:
                                        message_log = {'status': '密码修改成功', 'pwdLastSet': attributes['pwdLastSet']}
                                else:
                                    message_log = {'status': '密码修改：失败','pwdLastSet':attributes['pwdLastSet']}
                                result.update({'sAMAccountName':getDatato['sAMAccountName'],'password':passwd})
                                result.update(message_log)
                                insert_log_table_name('log_ldap', '172.0.0.1', 'ModifyUserThread', username, str(modify_password), str(item), message_log, '')
                            else:
                                message_log = {'status': '修改密码LDAP必须采用加密连接，端口636，现在连接的端口：'+str(port)}
                                result.update({'sAMAccountName': getDatato['sAMAccountName']})
                                result.update(message_log)
                                insert_log_table_name('log_ldap', '172.0.0.1', 'ModifyUserThread', username, str(False), str(item), message_log, '')
                        else:
                            message_log = {'status': '密码修改：失败,根据sAMAccountName没有找到对象'}
                            result.update({'sAMAccountName': getDatato['sAMAccountName']})
                            result.update(message_log)
                            insert_log_table_name('log_ldap', '172.0.0.1', 'ModifyUserThread', username, str(False), str(item), message_log, '')
                else:
                    message_log = {'status': '密码修改失败：sAMAccountName不能为空'}
                    insert_log_table_name('log_ldap', '172.0.0.1', 'ModifyUserThread', username, str(False), str(item), message_log, '')
                    result.update(message_log)
                    result.update(getDatato)
            except Exception as e:
                result.update({'status': '密码修改失败:'+str(e)})
                result.update(getDatato)

            modifyusermessage.append(result)
            self.queue.task_done()

q = queue.Queue(500)
def thrmodifyalluserpasswd(getDatatojson,username,radiovaule,pwdLastSet,add_passwd_count,add_passwd1):
    del modifyusermessage[:]
    # 开启线程
    for i in range(500):
        t = ModifyUserThread(q)
        t.daemon = True
        t.start()
    for getDatato in getDatatojson:
        listvalue = [getDatato,username,radiovaule,pwdLastSet,add_passwd_count,add_passwd1]
        q.put(listvalue)
    q.join()
    return modifyusermessage