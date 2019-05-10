# from line_profiler import LineProfiler
# import json
# import requests
#
# lp = LineProfiler()
# lp_wrapper = lp(testconn)
# lp_wrapper('')
# lp.print_stats()
#
# def get_api_token(username,password):
#     '''
#     根据账户，密码获取token
#     Api-token-auth
#     :return: {'token': 'xxx'} or {'non_field_errors': ['Unable to log in with provided credentials.']}
#     '''
#     url = 'http://itops./Api-token-auth/'
#     value = json.dumps({"username":username,"password":password})
#     headers = {
#         "Content-Type": "application/json"
#     }
#     r = requests.post(url, data=value, headers=headers)
#     resultinfo = r.json()
#     return resultinfo
#
# def ldap3_serch(search_filter):
#     '''
#     ldap3搜索
#     :param search_base:
#     :param search_filter:
#     :return: {'count': 1, 'code': 0, 'msg': '', 'message': [{'dn': 'xxxx', 'attributes': {}}], 'isSuccess': True}
#     '''
#     url = 'http://Ldap3Search/'
#     value = json.dumps({"search_filter":search_filter})
#     headers = {
#         "Authorization": "JWT eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjo1LCJlbWFpbCI6IiIsInVzZXJuYW1lIjoiYWRtaW4iLCJleHAiOjE1NTUzMjIzODJ9.6G4CdTJ1BCLAwYzl8mI9CVU47xDCopKY27aCMVsSu9g",
#         "Content-Type": "application/json"
#     }
#     r = requests.post(url, data=value, headers=headers)
#     resultinfo = r.json()
#     return resultinfo
