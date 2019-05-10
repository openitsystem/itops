import queue
import threading

from ldap3 import MODIFY_REPLACE

from ADapi.views import UserToExc, EnableMailbox
from apps.activeapi.th_creat_mail import UserCreatMail
from dbinfo.views import insert_log_table_name
from itops.settings import ldap3RESTARTABLE, ladp3search_base


def repeace_dn(message):
    promessage=message.replace('(',r'\28').replace(')',r'\29').replace('*',r'2a')
    return promessage

modifyusermessage = []

class CrearMailThread(threading.Thread):
    def __init__(self, que):
        threading.Thread.__init__(self)
        self.queue = que

    def run(self):
        while True: # 需要通过循环来不断的运行任务
            item = self.queue.get()
            getDatato = item[0]
            username = item[1]
            maildb = item[2]
            mailarchive = item[3]
            mailarchivedb = item[4]
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
                    with ldap3RESTARTABLE as conn:
                        conn.search(
                            search_base=ladp3search_base,
                            search_filter='(&(sAMAccountName=' + sAMAccountName_repeace + ')(&(objectCategory=person)(objectClass=user))(!(msExchHomeServerName=*))(!(mailNickname=*)))',
                            attributes=attributesldap)
                        response = conn.response[0]
                        dn = response.get('dn', '')
                        if dn:
                            attributes = response.get('attributes', '')
                            UserToExcs = UserToExc(sAMAccountName_repeace, maildb)
                            if UserToExcs['isSuccess']:
                                if mailarchive=='true':
                                    EnableMailboxs = EnableMailbox(sAMAccountName_repeace, mailarchivedb)
                                    if EnableMailboxs['isSuccess']:
                                        message_log = {'status': sAMAccountName_repeace+'：用户新建邮箱，并创建归档'}
                                    else:
                                        message_log = {'status': sAMAccountName_repeace+'：用户新建邮箱成功，并创建归档失败：'+str(EnableMailboxs)}
                                else:
                                    message_log = {'status': sAMAccountName_repeace + '：用户新建邮箱'}
                            else:
                                message_log = {'status': sAMAccountName_repeace + '：用户新建邮箱失败：'+str(UserToExcs)}
                            result.update(dict(attributes))
                            result.update(message_log)
                            insert_log_table_name('log_ldap', '172.0.0.1', 'CrearMailThread', username, str(True), str(item), str(result), '')
                        else:
                            message_log = {'status': '没有查询到对象,或属性值传入有错'}
                            insert_log_table_name('log_ldap', '172.0.0.1', 'CrearMailThread_search', username, str(False), str(item), str(message_log), '')
                            result.update(message_log)
                            result.update(getDatato)
                else:
                    message_log = {'status': '移动用户失败：sAMAccountName不能为空'}
                    insert_log_table_name('log_ldap', '172.0.0.1', 'CrearMailThread', username, str(False), str(item), str(message_log), '')
                    result.update(message_log)
                    result.update(getDatato)
            except Exception as e:
                result.update({'status': '移动用户失败:'+str(e)})
                result.update(getDatato)

            modifyusermessage.append(result)
            self.queue.task_done()

q = queue.Queue(500)
def threxecutecreatmail(getDatatojson,username,maildb,mailarchive,mailarchivedb):
    del modifyusermessage[:]
    # 开启线程
    for i in range(500):
        t = CrearMailThread(q)
        t.daemon = True
        t.start()

    for getDatato in getDatatojson:
        listvalue = [getDatato,username,maildb,mailarchive,mailarchivedb]
        q.put(listvalue)
    q.join()
    return modifyusermessage