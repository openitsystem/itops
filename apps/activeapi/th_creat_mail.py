# -*- coding: utf-8 -*-
# @Time    : 2018/3/15 17:59
# @Author  :
import threading
import time

from ADapi.views import UserToExc



#继承Thread，需要实现run方法
from dbinfo.views import insert_log_table_name


class user_to_exc(threading.Thread):
    """send wechat"""
    def __init__(self,sAMAccountName,maildb):
        self.sAMAccountName = sAMAccountName
        self.maildb = maildb
        threading.Thread.__init__(self)
    def run(self):
        try:
            time.sleep(50)
            UserToExcs = UserToExc(self.sAMAccountName, self.maildb)
            if UserToExcs['isSuccess']:
                result = {
                    "isSuccess": True,
                    "message": self.sAMAccountName + ",创建邮箱成功"}
            else:
                result = {
                    "isSuccess": False,
                    "message": self.sAMAccountName + ",创建邮箱失败：" + str(UserToExcs['message'])}
        except Exception as e:
            result = {
                "isSuccess": False,
                "message": self.sAMAccountName + ",创建邮箱失败：" + str(e)}
        insert_log_table_name('log', '', 'user_to_exc', '创建邮箱', str(result['isSuccess']), str(self.sAMAccountName), str(result), str(self.maildb))
        return result

#创建用户邮箱
def UserCreatMail(sAMAccountName,maildb):
    send_Exc = user_to_exc(sAMAccountName,maildb)
    send_Exc.start()

