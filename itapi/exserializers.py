# -*- coding: utf-8 -*-
# @Time    : 2019/3/18 14:30
# @Author  :
from rest_framework import serializers

'''
这个是Django rest framework 序列化 对象的方法

这边主要用于邮箱方法的序列化
'''

# 启用用户邮箱
class EnableMailboxhighSerializers(serializers.Serializer):
    identity = serializers.CharField(required=True, help_text='str, 用户唯一标识')
    alias = serializers.CharField(required=True, help_text='str, 邮箱别名')
    database = serializers.CharField(required=True, help_text='str, 数据库')

# 启用用户邮箱(启用归档邮箱)
class EnableMailboxarchiveSerializers(serializers.Serializer):
    identity = serializers.CharField(required=True, help_text='str, 用户唯一标识')
    ArchiveDatabase = serializers.CharField(required=True, help_text='str, 数据库')

# 获取所有数据库名称/获取单一数据库信息

# 迁移用户邮箱和存档数据库
class NewMoveRequestSerializers(serializers.Serializer):
    identity = serializers.CharField(required=True, help_text='str, 用户唯一标识')
    TargetDatabase = serializers.CharField(help_text='str, 迁移用户邮箱的目标数据库')
    ArchiveTargetDatabase = serializers.CharField(help_text='str, 迁移用户归档邮箱的目标数据库')
    def validate(self, attrs):
        TargetDatabase = attrs.get('TargetDatabase', None)
        ArchiveTargetDatabase = attrs.get('ArchiveTargetDatabase', None)
        if TargetDatabase or ArchiveTargetDatabase:
            return attrs
        else:
            raise serializers.ValidationError("TargetDatabase or ArchiveTargetDatabase 必须填写其中一个")


# 用户唯一标识
class IdentitySerializers(serializers.Serializer):
    identity = serializers.CharField(required=True, help_text='str, 用户唯一标识')

#获取邮箱群组信息
# 禁用邮箱群组

# 启用邮箱群组
class EnableDistributionGroupSerializers(IdentitySerializers):
    alias = serializers.CharField(required=True, help_text='str, 邮箱别名')

# 用户邮箱信息，一般用作获取用户邮箱大小使用情况

# 获取邮箱服务器

# 获取邮箱用户权限，获取代理发送权限
class getADPermissionSerializers(serializers.Serializer):
    identity = serializers.CharField(required=True, help_text='str, 用户DN，如果有空格，需要用双引号括起来')

# 获取邮箱联系人信息
# 获取邮箱用户权限

# 删除邮箱用户权限，一般用作删除用户完全访问权限
class RemoveMailboxPermissionSerializers(IdentitySerializers):
    User = serializers.CharField(required=True, help_text='str, 删除哪个用户的权限（必须）')

# 添加邮箱用户权限，添加完全访问权限
class AddMailboxPermissionSerializers(IdentitySerializers):
    User = serializers.CharField(required=True, help_text='str, 添加哪个用户的权限（必须）')

# 添加邮箱用户权限，添加代理发送权限
class AddADPermissionSerializers(serializers.Serializer):
    identity = serializers.CharField(required=True, help_text='str, 用户DN，如果有空格，需要用双引号括起来')
    User = serializers.CharField(required=True, help_text='str, 添加哪个用户的权限（必须）')

# 删除邮箱用户权限 代理发送权限
class RemoveADPermissionSerializers(serializers.Serializer):
    identity = serializers.CharField(required=True, help_text='str, 用户DN，如果有空格，需要用双引号括起来')
    User = serializers.CharField(required=True, help_text='str, 删除哪个用户的权限（必须）')

# 开启联系人邮箱
class EnableMailContactSerializers(serializers.Serializer):
    identity = serializers.CharField(required=True, help_text='str, 联系人唯一标识')
    ExternalEmailAddress = serializers.CharField(required=True, help_text='str, 邮箱地址')

#删除用户邮箱迁移请求
#IdentitySerializers

# 新建联系人
class NewMailContactSerializers(serializers.Serializer):
    Name = serializers.CharField(required=True, help_text='str, CN，（displayname如果不写也会赋此值）  必须')
    ExternalEmailAddress = serializers.CharField(required=True, help_text='str, 邮箱地址')

# 设置联系人邮箱
#IdentitySerializers

# 设置pop mapi信息
#IdentitySerializers

# 新增/删除 用户smtp地址
class SetMailboxEmailAddressesSerializers(IdentitySerializers):
    ExternalEmailAddress = serializers.CharField(required=True, help_text='str, 邮箱地址')

# 设置用户邮箱
#IdentitySerializers

# Set-DistributionGroup
# 设置群组邮箱
#IdentitySerializers