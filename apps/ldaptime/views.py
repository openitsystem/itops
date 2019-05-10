# -*- coding: utf-8 -*-
# @Time    : 2019/1/23 15:49
# @Author  :
import datetime
import time
def utc2local(utc_st):
    '''
    UTC时间转本地时间（+8:00）
    :param utc_st:
    :return:
    '''
    now_stamp = time.time()
    local_time = datetime.datetime.fromtimestamp(now_stamp)
    utc_time = datetime.datetime.utcfromtimestamp(now_stamp)
    offset = local_time - utc_time
    local_st = utc_st + offset
    return local_st

def local2utc(local_st):
    '''
        本地时间转UTC时间（-8:00）
        :param utc_st:
        :return:
        '''
    time_struct = time.mktime(local_st.timetuple())
    utc_st = datetime.datetime.utcfromtimestamp(time_struct)
    return utc_st
# # utc转本地
# local_time = utc2local(utc_time)
# print (local_time.strftime("%Y-%m-%d %H:%M:%S"))
# output：2014-09-18 18:42:16


# # 本地转utc
# utc_tran = local2utc(local_time)
# print (utc_tran.strftime("%Y-%m-%d %H:%M:%S"))
# output：2014-09-18 10:42:16