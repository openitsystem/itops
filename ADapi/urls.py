#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2018/11/13 11:59
# @Author  : Center
from django.conf.urls import url


from . import views

import json


app_name = 'api'

urlpatterns = [
    url(r'^GetConMessage/$', views.GetConMessage.as_view(),name='GetConMessage'),#模糊查找AD账号
    url(r'^GetOnlyConMessage/$', views.GetOnlyConMessage.as_view(),name='GetOnlyConMessage'),#模糊查找用户账号
    url(r'^GetUserMessage/$', views.GetUserMessage.as_view(),name='GetUserMessage'),#精准查找AD
    url(r'^GetMailMessage/$', views.GetMailMessage.as_view(),name='GetMailMessage'),#精准查找邮箱信息
    url(r'^ChangeUserMessage/$', views.ChangeUserMessage.as_view(),name='ChangeUserMessage'),#修改AD账号属性
    url(r'^GetGroupAnrMessage/$', views.GetGroupAnrMessage.as_view(),name='GetGroupAnrMessage'),#模糊查找组信息
    url(r'^GetGroupPreMessage/$', views.GetGroupPreMessage.as_view(),name='GetGroupPreMessage'),#精准查找组信息
    url(r'^GetMailContact/$', views.GetMailContact.as_view(),name='GetMailContact'),#查找联系人邮箱信息
    url(r'^DelGroupUser/$', views.DelGroupUser.as_view(),name='DelGroupUser'),#删除组成员
    url(r'^DelGroupUserMore/$', views.DelGroupUserMore.as_view(),name='DelGroupUserMore'),#批量删除组成员
    url(r'^EmUserGroup/$', views.EmUserGroup.as_view(),name='EmUserGroup'),#清空用户隶属于
    url(r'^EmGroupAllUser/$', views.EmGroupAllUser.as_view(),name='EmGroupAllUser'),#一键清空组成员
    url(r'^AddUserToGroup/$', views.AddUserToGroup.as_view(),name='AddUserToGroup'),#添加用户到多个组
    url(r'^AddGroupsTo/$', views.AddGroupsTo.as_view(),name='AddGroupsTo'),#组添加成员或组
    # url(r'^ChangePassword/$', views.ChangePassword.as_view(),name='ChangePassword'),#更改密码
    url(r'^ChangeDN/$', views.ChangeDN.as_view(), name='ChangeDN'),  # 修改DN
    url(r'^ChangeaccountExpires/$', views.ChangeaccountExpires.as_view(),name='ChangeaccountExpires'),#修改账号过期时间
    url(r'^ChangeMail/$', views.ChangeMail.as_view(),name='ChangeMail'),#修改邮箱信息
    url(r'^ChangeMailcapacity/$', views.ChangeMailcapacity.as_view(),name='ChangeMail'),#修改邮箱容量
    url(r'^GetDBMessage/$', views.GetDBMessage.as_view(),name='GetDBMessage'),#获取邮箱DB
    url(r'^UserSmtpAdd/$', views.UserSmtpAdd.as_view(),name='UserSmtpAdd'),#新增Smtp地址
    url(r'^MailContactSmtpAdd/$', views.MailContactSmtpAdd.as_view(),name='MailContactSmtpAdd'),#新增联系人Smtp地址
    url(r'^setDistributionGroupsmtp/$', views.setDistributionGroupsmtp.as_view(),name='setDistributionGroupsmtp'),#新增邮箱群组Smtp地址
    url(r'^UserDBMove/$', views.UserDBMove.as_view(),name='UserDBMove'),#用户数据库迁移
    url(r'^EmUserSmtp/$', views.EmUserSmtp.as_view(),name='EmUserSmtp'),#删除smtp
    url(r'^RemoveUserRequest/$', views.RemoveUserRequest.as_view(),name='RemoveUserRequest'),#删除移动请求
    url(r'^GetCompMessage/$', views.GetCompMessage.as_view(),name='GetCompMessage'),#精准查找计算机
    url(r'^EnContactMail/$', views.EnContactMail.as_view(),name='EnContactMail'),#开启联系人邮箱
    url(r'^SetContactMail/$', views.SetContactMail.as_view(),name='SetContactMail'),#新建用户联系人
    url(r'^EnableMailContact/$', views.EnableMailContact.as_view(),name='EnableMailContact'),#已有联系人启用邮箱
    url(r'^SetUserMail/$', views.SetUserMail.as_view(),name='SetUserMail'),#用户开启邮箱
    url(r'^GetLeaveUser/$', views.GetLeaveUser.as_view(),name='GetLeaveUser'),#高级查找
    url(r'^GetPasswordDate/$', views.GetPasswordDate.as_view(),name='GetPasswordDate'),#获取密码过期时间
    url(r'^EnUserMailArchive/$', views.EnUserMailArchive.as_view(),name='EnUserMailArchive'),#开启归档
    url(r'^GetMailGroup/$', views.GetMailGroup.as_view(),name='GetMailGroup'),#获取邮箱群组
    url(r'^MOUserMailArchive/$', views.MOUserMailArchive.as_view(),name='MOUserMailArchive'),#迁移存档
    url(r'^EnDistributionGroup/$', views.EnDistributionGroup.as_view(),name='EnDistributionGroup'),#开启邮箱群组
    url(r'^SetCasMailbox/$', views.SetCasMailbox.as_view(),name='SetCasMailbox'),#设置邮箱pop等状态
    url(r'^GetCasMailbox/$', views.GetCasMailbox.as_view(),name='GetCasMailbox'),#获取邮箱pop等状态
    url(r'^ReMailboxPermission/$', views.ReMailboxPermission.as_view(),name='ReMailboxPermission'),#移除完全访问权限
    url(r'^getallmessagenummber/$', views.getallmessagenummber.as_view(),name='getallmessagenummber'),#首页获取用户数据数量接口
    url(r'^getallgroupmessagenummber/$', views.getallgroupmessagenummber.as_view(),name='getallgroupmessagenummber'),#首页获取群组数据数量接口
    url(r'^getallmailmessagenummber/$', views.getallmailmessagenummber.as_view(),name='getallmailmessagenummber'),#首页获取邮箱数据数量接口
    url(r'^getallcomputermessagenummber/$', views.getallcomputermessagenummber.as_view(),name='getallcomputermessagenummber'),#首页获取计算机数据数量接口
    url(r'^GetPermission/$', views.GetPermission.as_view(),name='GetPermission'),#获取完全访问权限
    url(r'^AddPermission/$', views.AddPermission.as_view(),name='AddPermission'),# 添加完全访问权限
    url(r'^SetDistrGroup/$', views.SetDistrGroup.as_view(),name='SetDistrGroup'),# 设置群组属性
    url(r'^SetMailContact/$', views.SetMailContact.as_view(),name='SetMailContact'),# 设置联系人邮箱属性
    url(r'^AddMailPermission/$', views.AddMailPermission.as_view(),name='AddMailPermission'),# #添加代理发送权限
    url(r'^GetADPermission/$', views.GetADPermission.as_view(),name='GetADPermission'),# #获取代理发送权限
    url(r'^RemovePermission/$', views.RemovePermission.as_view(),name='RemovePermission'),# #移除代理发送权限
    url(r'^GetDown/$', views.GetDown.as_view(),name='GetDown'),# #计算机表格导出
    url(r'^GetUserDown/$', views.GetUserDown.as_view(),name='GetUserDown'),# #用户表格导出
    url(r'^GetMailDown/$', views.GetMailDown.as_view(),name='GetMailDown'),# #邮箱表格导出
    url(r'^GetGroupDown/$', views.GetGroupDown.as_view(),name='GetGroupDown'),# #用户表格导出
    url(r'^ChangeUserMessagebylist/$', views.ChangeUserMessagebylist.as_view(), name='ChangeUserMessagebylist'),# 修改AD账号属性(by_list)



]
