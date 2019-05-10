# -*- coding: utf-8 -*-
# @Time    : 2019/3/18 14:30
# @Author  :
from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class Profile(AbstractUser):
    '''
    用户
    '''
    name = models.CharField(max_length=50, null=True, blank=True, verbose_name='姓名', help_text='姓名')
    department = models.CharField(max_length=255, null=True, blank=True, verbose_name='部门', help_text='部门')
    description = models.CharField(max_length=255, null=True, blank=True, verbose_name='描述', help_text='描述')
    class Mata:
        verbose_name = '用户'
        verbose_name_plural = '用户'

# class AttributesLevel(models.Model):
#     '''
#     AD属性等级
#     '''
#     apiname = models.CharField(max_length=255, verbose_name='apiname', help_text='apiname')
#     attributes = models.CharField(max_length=255, verbose_name='属性详情', help_text='属性详情')
#
#     class Mata:
#         verbose_name = 'AD属性等级'
#         verbose_name_plural = 'AD属性等级'
#
#
#
# class ApinamePermissions(models.Model):
#     '''
#     API权限限制
#     '''
#     username = models.ForeignKey(Profile, verbose_name='用户名')
#     apiname = models.CharField(max_length=50, verbose_name='API名称', help_text='API名称')
#
#     class Mata:
#         verbose_name = 'API权限限制'
#         verbose_name_plural = 'API权限限制'

