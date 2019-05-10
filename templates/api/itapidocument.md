### Api方法调用说明
#### 1.找管理员新建API 用户，密码。并添加相应的权限

#### 2.用账号，密码 json post调用 Api-token-auth
> {"username":"admin","password":"123456"}

* 生成token
##### ==注意token过期时间,默认2小时==

#### 3.调用方法
* 注意方法的类型，正常都是POST
* 把上面获取的token 填写到Headers ,注意 JWT 后面有一个空格
```
headers = {
        "Authorization": "JWT eyJ0eXAiOiJKV1QiLCJhbGciOiJIiJ9.eyJleHAiOjE1NTQ5OTExMTUsInVzZXJuYW1lIjoiYWRtaW4iLCJ1c2VyX2lkIjo1LCJlbWFpbCI6IiJ9.lfUCokn_V6wPCopE4tMMl",
        "Content-Type": "application/json"
    }
```
* body 传入对应格式的json
```
# python 
value = json.dumps({"dn":"CN=sss,OU=users,OU=SUZ,DC=contos,DC=cn",
"attributesName":"ipphone",
"attributesVaule":"sew12",
"displayname":"displayname1",
"Office":"Office1"})
```

#### 4.python 调用示例
```
import json
import requests


def get_api_token(username,password):
    '''
    根据账户，密码获取token
    Api-token-auth
    :return: {'token': 'xxx'} or {'non_field_errors': ['Unable to log in with provided credentials.']}

    '''
    url = 'http://itops.test.com/Api-token-auth/'
    value = json.dumps({"username":username,"password":password})
    headers = {
        "Content-Type": "application/json"
    }
    r = requests.post(url, data=value, headers=headers)
    resultinfo = r.json()
    return resultinfo

def ldap3_serch(search_filter):
    '''
    ldap3搜索
    :param search_filter:
    :return: {'count': 1, 'code': 0, 'msg': '', 'message': [{'dn': 'xxxx', 'attributes': {}}], 'isSuccess': True}
    '''
    url = 'http://itops.test.com/Ldap3Search/'
    value = json.dumps({"search_filter":search_filter})
    headers = {
        "Authorization": "JWT eyJ0eXAiOiJKV1QiLJ9.eyJ1c2VyX2lkIjo1bCI6IiIslIjoiYWRtaW4iLCJleHAiOjE1NTUzMjIzODJ9.6G4CdTJ1BCLAwY",
        "Content-Type": "application/json"
    }
    r = requests.post(url, data=value, headers=headers)
    resultinfo = r.json()
    return resultinfo
```

#### 5.返回值说明
* 200 状态码返回 200
```
{
    "msg": "", # 报错原因
    "code": 0, #code值对应说明 返回
    "message": '', # 返回值 list or str
    "isSuccess": true,  # 执行结果
    "count": 10 #返回值数量
}
code值对应说明
0 =>> 执行成功

ldap3 
1 =>> ldap3执行完成,详情见msg
2 =>> ldap3执行报错,系统报错

Exchang
200 =>> 执行失败，缺少必须参数
201 =>> 执行失败，详情见msg
202 =>> 未知
```
* 403  没有权限 状态码返回 403 
    - 解决方案：找管理员申请权限
```
{
    "detail": "You do not have permission to perform this action."
}
```
* 401  token 错误 状态码返回 401 
    - 解决方案：传入正确的token
```
{
    "detail": "Error decoding signature."
}
```
* 400  传入值错误 状态码返回 400 
    - 解决方案：请看对应报错
``` 
# 例子
{
    "password": [
        "This field is required."
    ],
}
```
   
#### 6.其他
##### 可以通过修改settings 来修改token过期时间
```
import datetime
JWT_AUTH = {
    "JWT_EXPIRATION_DELTA": datetime.timedelta(days=0, hours=2, seconds=0),
    'JWT_AUTH_HEADER_PREFIX': 'JWT',
}
```
> 关于JWT 认证 [https://lion1ou.win/2017/01/18/](https://lion1ou.win/2017/01/18/)]

> [Django REST framework 官网](https://www.django-rest-framework.org/)