# -*- coding: utf-8 -*-
# @Time    : 2019/3/18 14:30
# @Author  :
from rest_framework import serializers

from itops.settings import ladp3search_base
'''
这个是Django rest framework 序列化 对象的方法
视图中一般做三件事:
            1 .将请求的数据（如JSON格式）转换为模型类对象 -反序列化
            2 .操作数据库
            3 .将模型类对象转换为响应的数据（如JSON格式） -序列化
            我们在第一步和第三步的时候我们都会涉及到将json数据转化成模型类对象,以及将模型类对象转化成json的数据返回回去.
            这里就会涉及到一个来回重复转化的问题,所以我们使用序列化,以及反序列化.
distinguishedName = distinguishedName.replace(
            '(', r'\28').replace(
            ')', r'\29').replace(
            '*', r'2a')
'''

#搜索
class Ldap3SearchSerializers(serializers.Serializer):
    search_base = serializers.CharField(default=ladp3search_base, help_text='str,例:OU=auth groups,DC=contos,DC=com,开始搜索的根路径(组织单位),默认设置为域根路径DC=XX,DC=XX')
    search_filter = serializers.CharField(required=True, help_text='str,例:(&(objectCategory=person)(objectClass=user)(sAMAccountName=XX)) ,搜索了ldap语句', error_messages={
        'required' : "search_filter是必填字段",
        'blank' : "search_filter字段不能为空",
    })
    search_scope = serializers.ChoiceField(choices=['SUBTREE', 'BASE', 'LEVEL'], default='SUBTREE', help_text='str,例：SUBTREE ,搜索范围,默认设置SUBTREE ,可选设置 BASE , LEVEL',
                                           error_messages={
                                              'choices' :'search_scope的值必须为SUBTREE,BASE,LEVEL 中的其中一个',
                                           })
    attributes = serializers.ListField(default=[], help_text='list,例：["sAMAccountName", "objectClass"] ,默认设置None,需要搜索的属性,如果设置为["*"],则搜索所有属性')
    size_limit = serializers.IntegerField(default=0, help_text='int, 例：0,默认设置0,搜索返回值的数量,如果设置为0,则全部返回')
    time_limit = serializers.IntegerField(default=0, help_text='int, 例：0,默认设置0,超时时间,如果设置为0,则为ldap3连接的超时时间设置')
    paged_size = serializers.IntegerField(default=None, help_text='int, 例：None,默认设置None,分页,如果paged_size是大于0的int，则为简单的分页搜索')
    paged_criticality = serializers.BooleanField(default=False, help_text='bool, 例：False,默认设置False,分页设置')
    paged_cookie = serializers.ListField(default=[], help_text='list, 例：None,默认设置list,分页设置,Cookie是上次分页搜索中收到的不透明字符串,并且必须在下一页的搜索响应中使用')

    # def validate(self, attrs):
    #     if attrs.get('attributes', ''):
    #         attrs['attributes'] = None
    #     if attrs.get('paged_cookie', ''):
    #         attrs['paged_cookie'] = None
    #     return attrs
    # def validate_search_scope(self, search_scope):
    #     if search_scope in ['SUBTREE', 'BASE', 'LEVEL']:
    #         return search_scope
    #     else:
    #         raise serializers.ValidationError('search_scope的值必须为SUBTREE,BASE,LEVEL 中的其中一个')

#新建用户
class Ldap3AddUserSerializers(serializers.Serializer):
    dn = serializers.CharField(default=ladp3search_base, help_text='str,例:OU=nuser,DC=contos,DC=com,新建用户所在路径(组织单位),默认设置为域根路径DC=XX,DC=XX')
    cn = serializers.CharField(required=True, help_text='str,例:xxxx,必填,用户的cn属性值,也是name的属性值,同一组织单位上不能有相同的cn')
    sAMAccountName = serializers.CharField(required=True, help_text='str,例:xxxx,必填,重要,用户的sAMAccountName属性值,也是用户的唯一标识,建议英文,不能中文，不能包含/ \ [ ] : ; | = , + * ? < > @ "等特殊字符')
    userPrincipalName = serializers.EmailField(required=False, help_text='str,例:xxxx@xx,重要,登录名,用户的userPrincipalName属性值,建议英文')
    sn = serializers.CharField(required=False, help_text='str,例:xxxx,姓氏')
    givenName = serializers.CharField(required=False, help_text='str,例:xxxx,名字')
    displayName = serializers.CharField(required=False, help_text='str,例:xxxx,显示名称')
    mail = serializers.ChoiceField(choices=['yes', 'no'], default='no', help_text='str,例：no,默认设置no 不新建邮箱.新建邮箱:mail传入yes,maildb传入邮箱数据库名称',
                                           error_messages={
                                              'choices':'mail的值必须为yes，no中的其中一个',
                                           })
    userAccountControl = serializers.ChoiceField(choices=[544, 546], default=544, help_text='int,例：544,默认设置544账户是启用状态,546是禁用',
                                           error_messages={
                                              'choices':'userAccountControl的值必须为544，546中的其中一个',
                                           })
    maildb = serializers.CharField(required=False, help_text='str,例:xxxx,邮箱数据库名称,新建邮箱:mail传入yes,maildb传入邮箱数据库名称')
    password = serializers.CharField(required=False, help_text='str,例:xxxx,密码,传入则设置用户密码')
    attributes = serializers.DictField(default={}, help_text='dict,例：{"givenName":"xx", "displayName":"xx"} ,设置其他ldap参数')

#新建组
class Ldap3AddGroupSerializers(serializers.Serializer):
    dn = serializers.CharField(default=ladp3search_base, help_text='str,例:OU=nuser,DC=contos,DC=com,新建对象所在路径(组织单位),默认设置为域根路径DC=XX,DC=XX')
    cn = serializers.CharField(required=True, help_text='str,例:xxxx,必填,cn属性值,也是name的属性值,同一组织单位上不能有相同的cn')
    sAMAccountName = serializers.CharField(required=True, help_text='str,例:xxxx,必填,重要,sAMAccountName属性值,也是的唯一标识,建议英文,不能中文，不能包含/ \ [ ] : ; | = , + * ? < > @ "等特殊字符')
    groupType = serializers.ChoiceField(choices=[-2147483646, -2147483644, -2147483640, 2, 4, 8], default=-2147483646, help_text='int,例：{全局 安全组:-2147483646,本地域 安全组:-2147483644,'
                                                                                                                                 '通用 安全组:-2147483640,全局 通讯组:2,'
                                                                                                                                 '本地域 通讯组:4,通用  通讯组:6,',
                                                 error_messages={
                                                     'choices': 'groupType的值必须为-2147483646, -2147483644, -2147483640, 2, 4, 8中的其中一个',
                                                 })
    attributes = serializers.DictField(default={}, help_text='dict,例：{"description":"xx", "displayName":"xx"} ,设置其他ldap参数')

#新建计算机
class Ldap3AddComputerSerializers(serializers.Serializer):
    dn = serializers.CharField(default=ladp3search_base, help_text='str,例:OU=nuser,DC=contos,DC=com,新建对象所在路径(组织单位),默认设置为域根路径DC=XX,DC=XX')
    cn = serializers.CharField(required=True, help_text='str,例:xxxx,必填,cn属性值,也是name的属性值,同一组织单位上不能有相同的cn')
    attributes = serializers.DictField(default={}, help_text='dict,例：{"description":"xx","displayName":"xx"} ,设置其他ldap参数')

# 新建联系人
class Ldap3AddContactSerializers(serializers.Serializer):
    dn = serializers.CharField(default=ladp3search_base, help_text='str,例:OU=nuser,DC=contos,DC=com,新建对象所在路径(组织单位),默认设置为域根路径DC=XX,DC=XX')
    cn = serializers.CharField(required=True, help_text='str,例:xxxx,必填,cn属性值,也是name的属性值,同一组织单位上不能有相同的cn')
    sn = serializers.CharField(required=False, help_text='str,例:xxxx,姓氏')
    givenName = serializers.CharField(required=False, help_text='str,例:xxxx,名字')
    displayName = serializers.CharField(required=False, help_text='str,例:xxxx,显示名称')
    description = serializers.CharField(required=False, help_text='str,例:xxxx,描述')
    mail = serializers.ChoiceField(choices=['yes', 'no'], default='no', help_text='str,例：no,默认设置no 不新建邮箱.新建邮箱:mail传入yes',
                                   error_messages={
                                       'choices': 'mail的值必须为yes，no中的其中一个',
                                   })
    name = serializers.CharField(required=False, help_text='str,例:xxxx,重要,邮箱别名')
    smtpvalue = serializers.EmailField(required=False, help_text='str,例:xxxx@xx,重要,电子邮件地址')

    attributes = serializers.DictField(default={}, help_text='dict,例：{"description":"xx", "displayName":"xx"}} ,设置其他ldap参数')

# 新建组织单位
class Ldap3AddOrganizationalUnitSerializers(serializers.Serializer):
    dn = serializers.CharField(default=ladp3search_base, help_text='str,例:OU=nuser,DC=contos,DC=com,新建对象所在路径(组织单位),默认设置为域根路径DC=XX,DC=XX')
    cn = serializers.CharField(required=True, help_text='str,例:xxxx,必填,cn属性值,也是name的属性值,同一组织单位上不能有相同的cn')
    prevent = serializers.ChoiceField(choices=['yes', 'no'], default='yes', help_text='str,例：yes,默认设置yes 添加防止意外删除',
                                   error_messages={
                                       'choices': 'prevent的值必须为yes，no中的其中一个',
                                   })
    attributes = serializers.DictField(default={}, help_text='dict,例：{"description":"xx", "displayName":"xx"} ,设置其他ldap参数')

# 重命名对象
class Ldap3RenameObjectSerializers(serializers.Serializer):
    dn = serializers.CharField(required=True, help_text='str,例:OU=nuser,DC=contos,DC=com,重命名对象的distinguishedName属性值')
    cn = serializers.CharField(required=True, help_text='str,例:xxxx,必填,cn属性值,也是name的属性值,同一组织单位上不能有相同的cn')
    sn = serializers.CharField(required=False, help_text='str,例:xxxx,姓氏')
    givenName = serializers.CharField(required=False, help_text='str,例:xxxx,名字')
    displayName = serializers.CharField(required=False, help_text='str,例:xxxx,显示名称')
    sAMAccountName = serializers.CharField(required=False, help_text='str,例:xxxx,必填,重要,用户的sAMAccountName属性值,也是用户的唯一标识,建议英文,不能中文，不能包含/ \ [ ] : ; | = , + * ? < > @ "等特殊字符')
    userPrincipalName = serializers.EmailField(required=False, help_text='str,例:xxxx@xx,重要,登录名,用户的userPrincipalName属性值,建议英文')
    objectClass = serializers.ListField(required=True,
                                          help_text='list,例：类型["top", "organizationalUnit"], ["top", "container"], ["top", "group"],["top", "person", "organizationalPerson", "user"], ["top", "person", "organizationalPerson", "contact"]',
                                        )

# 多dn 移动到新OU
class Ldap3DnMoveToOuSerializers(serializers.Serializer):
    dns = serializers.ListField(required=True, help_text='list,例:["OU=nuser,DC=contos,DC=com"],需要移动对象的distinguishedName属性值集')
    new_superior = serializers.CharField(required=True, help_text='str,例:OU=nuser,DC=contos,DC=com,必填,异动目的组织单位的distinguishedName属性值')

# 删除对象 例:[("1.2.840.113556.1.4.805", False, None)],重要,特殊的附加值，用来删除OU下所有对象，或其他
class Ldap3DeleteObjectSerializers(serializers.Serializer):
    dn = serializers.CharField(required=True, help_text='str,例:"OU=nuser,DC=contos,DC=com",需要删除对象的distinguishedName属性值')
    controls = serializers.ListField(required=False, help_text='list,例:[("", False, None)],重要,特殊的附加值')

# 判断容器或OU内是否有对象
class Ldap3inspectObjectSerializers(serializers.Serializer):
    dn = serializers.CharField(required=True, help_text='str,例:"OU=nuser,DC=contos,DC=com",容器或OU的distinguishedName属性值')

# 修改对象属性
class Ldap3SetAccountSerializers(serializers.Serializer):
    dn = serializers.CharField(required=True, help_text='str,例:"OU=nuser,DC=contos,DC=com",对象的distinguishedName属性值')
    attributesName = serializers.CharField(required=True, help_text='str,例:"displayName" 显示名称, 对象的属性名')
    attributesVaule = serializers.CharField(required=True, help_text='str,例:"xxx",对象的attributesName属性值')

# 基础的用户的sAMAccountName属性  用户的distinguishedName属性 Ldap3UserSerializers
class Ldap3UserSerializers(serializers.Serializer):
    distinguishedName = serializers.CharField(required=False, help_text='str,例:"CN=nuser11,DC=contos,DC=com" 用户的distinguishedName属性,和sAMAccountName必填其中一项,用于确定用户')
    sAMAccountName = serializers.CharField(required=False, help_text='str,例:"xxx",用户的sAMAccountName属性,和distinguishedName必填其中一项,用于确定用户')

    def validate(self, attrs):
        distinguishedName = attrs.get('distinguishedName', None)
        sAMAccountName = attrs.get('sAMAccountName', None)
        if distinguishedName or sAMAccountName:
            return attrs
        else:
            raise serializers.ValidationError("distinguishedName or sAMAccountName 必须填写其中一个")

# 修改用户密码
class Ldap3ResetPasswordSerializers(Ldap3UserSerializers):
    newpassword = serializers.CharField(required=True, help_text='str,例:"fas#$sa1213",用户密码建议大于8位，并符合安全策略')
    pwdLastSet = serializers.CharField(required=False, help_text='str,例:"xxx",用户的pwdLastSet属性,传入值：则设置用户下次登陆时须更改密码')
    unlock = serializers.CharField(required=False, help_text='str,例:"xxx",传入值：解锁用户的账户')
    ip = serializers.IPAddressField(required=False, help_text='IPAddress,例:"192.168.0.1"，域控的IP,在哪台域控上解锁用户')

# 解锁用户锁定
class Ldap3UnlockUserSerializers(Ldap3UserSerializers):
    ip = serializers.IPAddressField(required=False, help_text='IPAddress,例:"192.168.0.1"，域控的IP,在哪台域控上解锁用户')

# 基础的用户的sAMAccountName属性Ldap3sAMAccountNameSerializers
class Ldap3sAMAccountNameSerializers(serializers.Serializer):
    search_base = serializers.CharField(default=ladp3search_base, help_text='str,例:OU=auth groups,DC=contos,DC=com,开始搜索的根路径(组织单位),默认设置为域根路径DC=XX,DC=XX')
    sAMAccountName = serializers.CharField(required=True, help_text='str,例:"xxx",用户的sAMAccountName属性,和distinguishedName必填其中一项,用于确定用户')
    attributes = serializers.ListField(required=False, help_text='list,例：["sAMAccountName", "objectClass"] ,默认设置None,需要搜索的属性,如果设置为["*"],则搜索所有属性')

# 添加删除组权限相关
class Ldap3Group(serializers.Serializer):
    members = serializers.ListField(required=True, help_text='list,例：["CN=nuser11,DC=contos,DC=com"], 传入用户的distinguishedName属性集合')
    groups = serializers.ListField(required=True, help_text='list,例：["CN=nugroup11,DC=contos,DC=com"], 传入组的distinguishedName属性集合')

# 根据用户工号获取信息
class Ldap3GetUserSerializers(serializers.Serializer):
    jobnumber = serializers.CharField(required=False, help_text='str,"新工号')
    sAMAccountName = serializers.CharField(required=False, help_text='str,例:"xxx",用户的sAMAccountName属性,和jobnumber必填其中一项,用于确定用户')
    def validate(self, attrs):
        jobnumber = attrs.get('jobnumber', None)
        sAMAccountName = attrs.get('sAMAccountName', None)
        if jobnumber or sAMAccountName:
            return attrs
        else:
            raise serializers.ValidationError("jobnumber or sAMAccountName 必须填写其中一个")