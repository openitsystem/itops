# -*- coding: utf-8 -*-
# @Time    : 2018/5/7 14:46
# @Site    :
# @File    : urls.py
# @Software: PyCharm
import requests
import json
import time
from django.http import HttpResponse
import datetime
from django.views import View

from dbinfo.encrypt_decode import encrypt_and_decode
from dbinfo.views import getpermsessage


class ZabbixApi(object):

    """
    Zabbix API类
    """
    #超时时间(5秒钟）
    TIMEOUT = 50
    class FailedError(Exception):
        """
        使用Zabbix API失败时出错
        """
        ERROR_MESSAGE_TEMPLATE = '"{message}({code}): {data}"'
        def __init__(self,name,reason = None):
            """
            构造函数
            :param name:  失败的方法名称
            :param reason: 错误响应
            """
            message = "Failed to {0}.".format(name)
            if reason is not None:
                message = ''.join([message,self.ERROR_MESSAGE_TEMPLATE.format(**reason)])
            super(ZabbixApi.FailedError,self).__init__(message)

    class AuthenticationFailedError(FailedError):
        """
        验证ZabbixToken失败
        """
        def __init__(self,reason = None):
            """
            构造函数
            :param reason: 失败的方法名称
            """
            super(ZabbixApi.AuthenticationFailedError,self).__init__('authenticate',reason)

    def __init__(self,encode = 'utf-8',zabbixurl=None, zabbixuser=None, zabbixpassword=None):
        """
        构造函数
        :param request_id:JSON-RPC请求标识符
        """
        getpermsessages = getpermsessage()
        if getpermsessages:
            self.uri = getpermsessages.get('zabbixurl', '')
            self.zabbixuser = getpermsessages.get('zabbixuser', '')
            self.zabbixpassword = encrypt_and_decode().decrypted_text(getpermsessages.get('zabbixpassword', ''))#解密
        if zabbixurl:
            self.uri = zabbixurl
        if zabbixuser:
            self.zabbixuser = zabbixuser
        if zabbixpassword:
            self.zabbixpassword = zabbixpassword


    def call(self,method,params,AUTH=None):
        """
        ZabbixAPI请求程序
        :param method: Zabbix API方法名称
        :param params: Zabbix API方法参数
        :param through_authenticate: 事前预认证
        :return:
        """
        if AUTH:
            body = json.dumps({
                'jsonrpc': '2.0',
                'method': method,
                'params': params,
                'auth': AUTH,
                'id': 2
            })
        else:
            body = json.dumps({
                'jsonrpc': '2.0',
                'method': method,
                'params': params,
                'id': 2
            })
        headers = {'Content-Type': 'application/json-rpc'}
        try:
            request = requests.post(self.uri,data=body,headers=headers,timeout=self.TIMEOUT)
            response_json = request.json()
            if 'result' in response_json:
                return response_json
            elif 'error' in response_json:
                return ZabbixApi.FailedError(name=method,reason=response_json['error'])
            else:
                return ZabbixApi.AuthenticationFailedError()
        except requests.exceptions.ConnectTimeout:
            return ZabbixApi.AuthenticationFailedError({'code': -1, 'message': 'Connect Timeout.', 'data': 'URI is incorrect.'})

    def authenticate(self):

        """
        执行认证
        :return:
        """
        response = self.call('user.login', {'user': self.zabbixuser, 'password': self.zabbixpassword})
        if 'result' in response:
            self.session_id = response['result']
            return response['result']
        elif 'error' in response:
            raise ZabbixApi.AuthenticationFailedError(response['error'])
        else:
            raise ZabbixApi.AuthenticationFailedError()


def get_hosts_template(template_name):
    '''
    根据模板 名称获取 模板templateid 再获取获取相关主机hostid
    :param template_name:
    :return:
    '''
    try:
        hosts = []
        zapi = ZabbixApi()
        token = zapi.authenticate()
        template_get = zapi.call('template.get', {
            "output": 'output',
            "filter": {
                "host": template_name}}, token)
        template_get_result = template_get['result']
        if template_get_result:
            templateid = template_get_result[0]['templateid']
            # 根据 templateid 获得 活动的 hostid
            host_get = zapi.call('host.get', {'output':['host'],'templateids':templateid,'filter': {"status": "0",'available': '1'}}, token)
            host_get_result = host_get['result']
            if host_get_result:
                for host in host_get_result:
                    hosts.append(host.get('host'))
                return hosts
            else:
                return hosts
        else:
            return hosts
    except Exception as e:
        return hosts


def get_hostid(ip):
    '''
    根据Ip 获取hostid
    :param ip:
    :return:
    '''
    method = 'host.get'
    params = {"filter": {"host": ip}}
    try:
        zapi = ZabbixApi()
        token = zapi.authenticate()
        result = zapi.call(method, params, token)
        return result['result'][0]['hostid']
    except Exception:
        return False

def get_item(hostid,item_name):
    '''
    根据hostid item_name 查找监控项
    :param hostid:
    :param item_name:
    :return:
    '''
    method = 'item.get'
    params = {"optput": ['name', 'itemid', 'value_type'],
              "hostids": hostid,
              "search": {'name': item_name},
              "filter": {'status': "0", "error": "", "state": 0}}
    try:
        zapi = ZabbixApi
        token = zapi.authenticate()
        result = zapi.call(method=method, params=params, AUTH=token)
        return result
    except Exception as e:
        print(e)
        return False

def get_item_trend(host,item_name,time_from=None,time_till=None):
    '''
    查找监控项的趋势数据
    :param ip:
    :param item_name:
    :param time_from:
    :param time_till:
    :return:
    '''
    try:
        zapi = ZabbixApi()
        token = zapi.authenticate()
        history = []
        get_hostid= zapi.call('host.get', {"filter": {"host": host}}, token)
        get_hostid_result = get_hostid.get('result','')
        if get_hostid_result:
            hostid = get_hostid_result[0].get("hostid", '')
            item_get = zapi.call('item.get', {"output": ['name', 'itemid', 'value_type'],
                                              'hostids': hostid,
                                              'search': {'name': item_name},
                                              'filter': {"status": "0", "error": "", "state": '0'}}, token)
            item_get_results = item_get.get('result','')
            for item_get_result in item_get_results:
                itemid = item_get_result['itemid']
                itemid_name = item_get_result['name']
                itemid_value_type = item_get_result['value_type']
                if time_from:
                    time_from = datetime.datetime.strptime(time_from, '%Y-%m-%d %H:%M:%S') #字符串转 datatime
                    time_from = time.mktime(time_from.timetuple())  # datetime 转 unix 时间戳
                else:
                    time_from = time.time() - 24 * 60 * 60 #默认获取一天前的时间
                if time_till:
                    time_till = datetime.datetime.strptime(time_till, '%Y-%m-%d %H:%M:%S')  # 字符串转 datatime
                    time_till = time.mktime(time_till.timetuple())  # datetime 转 unix 时间戳
                else:
                    time_till = time.time() # 默认获取当前时间
                trend_get = zapi.call('trend.get', {"output": 'extend', 'itemids': itemid,
                                                        'time_from': time_from,
                                                        'time_till': time_till}, token)
                history_get_results = trend_get.get('result','')

                if history_get_results:
                    for history_get_result in history_get_results:
                        clock = history_get_result['clock']
                        value_avg = history_get_result['value_avg']
                        value_max = history_get_result['value_max']
                        value_min = history_get_result['value_min']
                        num = history_get_result['num']
                        # 对时间格式化,转换成字符串
                        clocktime = (datetime.datetime.fromtimestamp(int(clock))).strftime('%Y-%m-%d %H:%M:%S')
                        history.append({"num": num, "value_min": value_min, "value_max": value_max, "value": value_avg, "clocktime": clocktime, 'name':itemid_name, "value_type": itemid_value_type})
        return history

    except Exception as e:
        print(e)
        return []

class get_item_history_api(View):
    def get(self, requests):
# def get_item_history_api(requests):
        try:
            ip = requests.GET.get('ip')
            item_name = requests.GET.get('item_name')
            time_from = requests.GET.get('time_from')
            time_till = requests.GET.get('time_till')
            datetime.datetime.strptime(time_till, "%Y-%m-%d %H:%M:%S")
            datetime.datetime.strptime(time_from, "%Y-%m-%d %H:%M:%S")
            if (datetime.datetime.strptime(time_till, "%Y-%m-%d %H:%M:%S") - datetime.datetime.strptime(time_from, "%Y-%m-%d %H:%M:%S")).days >= 1:
                a = get_item_trend(ip,item_name,time_from,time_till)
            else:
                a = get_item_history(ip,item_name,time_from,time_till)
            response = HttpResponse()
            response['Content-Type'] = "application/json"
            response.write(json.dumps(a, default=str).encode("UTF-8"))
            return response
        except Exception as e:
            response = HttpResponse()
            response['Content-Type'] = "application/json"
            response.write(json.dumps([], default=str).encode("UTF-8"))
            return response



class get_group_item_api(View):
    def get(self, requests):
# def get_group_item_api(requests):
        try:
            template_name = requests.GET.get('template_name')
            a = get_hosts_template(template_name)
            response = HttpResponse()
            response['Content-Type'] = "application/json"
            response.write(json.dumps(a, default=str).encode("UTF-8"))
            return response
        except Exception as e:
            response = HttpResponse()
            response['Content-Type'] = "application/json"
            response.write(json.dumps([], default=str).encode("UTF-8"))
            return response

def get_item_history(ip,item_name,time_from=None,time_till=None):
    try:
        zapi = ZabbixApi()
        token = zapi.authenticate()
        history = []
        get_hostid= zapi.call('host.get', {"filter": {"host": ip}}, token)
        get_hostid_result = get_hostid.get('result','')
        if get_hostid_result:
            hostid = get_hostid_result[0].get("hostid", '')
            item_get = zapi.call('item.get', {"output": ['name', 'itemid', 'value_type'],
                                              'hostids': hostid,
                                              'search': {'name': item_name},
                                              'filter': {"status": "0", "error": "", "state": '0'}}, token)
            item_get_results = item_get.get('result','')
            for item_get_result in item_get_results:
                itemid = item_get_result['itemid']
                itemid_name = item_get_result['name']
                itemid_value_type = item_get_result['value_type']
                if time_from:
                    time_from = datetime.datetime.strptime(time_from, '%Y-%m-%d %H:%M:%S')  # 字符串转 datatime
                    time_from = time.mktime(time_from.timetuple())  # datetime 转 unix 时间戳
                else:
                    time_from = time.time() - 1 * 60 * 60 #默认获取一个小时前的时间
                if time_till:
                    time_till = datetime.datetime.strptime(time_till, '%Y-%m-%d %H:%M:%S')  # 字符串转 datatime
                    time_till = time.mktime(time_till.timetuple())  # datetime 转 unix 时间戳
                else:
                    time_till = time.time() # 默认获取当前时间
                history_get = zapi.call('history.get', {"output": 'extend', 'itemids': itemid,
                                                        'history': itemid_value_type,
                                                        'time_from': time_from,
                                                        'time_till': time_till}, token)
                history_get_results = history_get.get('result','')

                if history_get_results:
                    for history_get_result in history_get_results:
                        clock = history_get_result['clock']
                        value = history_get_result['value']
                        ns = history_get_result['ns']
                        # 对时间格式化,转换成字符串
                        clocktime = (datetime.datetime.fromtimestamp(int(clock))).strftime('%Y-%m-%d %H:%M:%S')
                        history.append({"value": value, "clocktime": clocktime, 'name':itemid_name, "value_type": itemid_value_type})
        return history

    except Exception as e:
        print(e)
        return []




#查找多个监控项的趋势数据
def get_item_trends(host,item_name,time_from=None,time_till=None):
    '''
    查找多个监控项的趋势数据
    :param ip:
    :param item_name:
    :param time_from:
    :param time_till:
    :return:
    '''
    try:
        history = []
        zapi = ZabbixApi()
        token = zapi.authenticate()
        get_hostid= zapi.call('host.get', {"filter": {"host": host}}, token)
        get_hostid_result = get_hostid.get('result','')
        if get_hostid_result:
            hostid = get_hostid_result[0].get("hostid", '')
            item_get = zapi.call('item.get', {"output": ['name', 'itemid', 'value_type'],
                                              'hostids': hostid,
                                              'search': {'name': item_name},
                                              'filter': {"status": "0", "error": "", "state": '0'}}, token)
            item_get_results = item_get.get('result','')
            if time_from:
                time_from = datetime.datetime.strptime(time_from, '%Y-%m-%d %H:%M:%S')  # 字符串转 datatime
                time_from = time.mktime(time_from.timetuple())  # datetime 转 unix 时间戳
            else:
                time_from = time.time() - 24 * 60 * 60  # 默认获取一天前的时间
            if time_till:
                time_till = datetime.datetime.strptime(time_till, '%Y-%m-%d %H:%M:%S')  # 字符串转 datatime
                time_till = time.mktime(time_till.timetuple())  # datetime 转 unix 时间戳
            else:
                time_till = time.time()  # 默认获取当前时间
            for item_get_result in item_get_results:
                item_get_trend = []
                itemid = item_get_result['itemid']
                itemid_name = item_get_result['name']
                itemid_value_type = item_get_result['value_type']
                trend_get = zapi.call('trend.get', {"output": 'extend', 'itemids': itemid,
                                                        'time_from': time_from,
                                                        'time_till': time_till}, token)
                history_get_results = trend_get.get('result','')
                if history_get_results:
                    for history_get_result in history_get_results:
                        clock = history_get_result['clock']
                        value_avg = history_get_result['value_avg']
                        value_max = history_get_result['value_max']
                        value_min = history_get_result['value_min']
                        num = history_get_result['num']
                        # 对时间格式化,转换成字符串
                        clocktime = (datetime.datetime.fromtimestamp(int(clock))).strftime('%Y-%m-%d %H:%M:%S')
                        item_get_trend.append({"num": num, "value_min": value_min, "value_max": value_max, "value": value_avg, "clocktime": clocktime, 'name':itemid_name, "value_type": itemid_value_type})
                    history.append(item_get_trend)
        return history
    except Exception as e:
        print(e)
        return history

#查找多个监控项的历史数据
def get_item_historys(ip,item_name,time_from=None,time_till=None):
    '''
    查找多个监控项的历史数据
    :param ip:
    :param item_name:
    :param time_from:
    :param time_till:
    :return:
    '''
    try:
        history = []
        zapi = ZabbixApi()
        token = zapi.authenticate()
        get_hostid= zapi.call('host.get', {"filter": {"host": ip}}, token)
        get_hostid_result = get_hostid.get('result','')
        if get_hostid_result:
            hostid = get_hostid_result[0].get("hostid", '')
            item_get = zapi.call('item.get', {"output": ['name', 'itemid', 'value_type'],
                                              'hostids': hostid,
                                              'search': {'name': item_name},
                                              'filter': {"status": "0", "error": "", "state": '0'}}, token)
            item_get_results = item_get.get('result','')
            if time_from:
                time_from = datetime.datetime.strptime(time_from, '%Y-%m-%d %H:%M:%S')  # 字符串转 datatime
                time_from = time.mktime(time_from.timetuple())  # datetime 转 unix 时间戳
            else:
                time_from = time.time() - 1 * 60 * 60  # 默认获取一个小时前的时间
            if time_till:
                time_till = datetime.datetime.strptime(time_till, '%Y-%m-%d %H:%M:%S')  # 字符串转 datatime
                time_till = time.mktime(time_till.timetuple())  # datetime 转 unix 时间戳
            else:
                time_till = time.time()  # 默认获取当前时间
            for item_get_result in item_get_results:
                item_get_history = []
                itemid = item_get_result['itemid']
                itemid_name = item_get_result['name']
                itemid_value_type = item_get_result['value_type']
                history_get = zapi.call('history.get', {"output": 'extend', 'itemids': itemid,
                                                        'history': itemid_value_type,
                                                        'time_from': time_from,
                                                        'time_till': time_till}, token)
                history_get_results = history_get.get('result','')

                if history_get_results:
                    for history_get_result in history_get_results:
                        clock = history_get_result['clock']
                        value = history_get_result['value']
                        ns = history_get_result['ns']
                        # 对时间格式化,转换成字符串
                        clocktime = (datetime.datetime.fromtimestamp(int(clock))).strftime('%Y-%m-%d %H:%M:%S')
                        item_get_history.append({"value": value, "clocktime": clocktime, 'name':itemid_name, "value_type": itemid_value_type})
                    history.append(item_get_history)
        return history
    except Exception as e:
        print(e)
        return history





class get_items_history_api(View):
    def get(self, requests):
# def get_items_history_api(requests):
        try:
            ip = requests.GET.get('ip')
            item_name = requests.GET.get('item_name')
            time_from = requests.GET.get('time_from')
            time_till = requests.GET.get('time_till')
            datetime.datetime.strptime(time_till, "%Y-%m-%d %H:%M:%S")
            datetime.datetime.strptime(time_from, "%Y-%m-%d %H:%M:%S")
            if (datetime.datetime.strptime(time_till, "%Y-%m-%d %H:%M:%S") - datetime.datetime.strptime(time_from, "%Y-%m-%d %H:%M:%S")).days >= 1:
                a = get_item_trends(ip,item_name,time_from,time_till)
            else:
                a = get_item_historys(ip,item_name,time_from,time_till)
            response = HttpResponse()
            response['Content-Type'] = "application/json"
            response.write(json.dumps(a, default=str).encode("UTF-8"))
            return response
        except Exception as e:
            response = HttpResponse()
            response['Content-Type'] = "application/json"
            response.write(json.dumps([], default=str).encode("UTF-8"))
            return response