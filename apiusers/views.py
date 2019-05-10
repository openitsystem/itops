# -*- coding: utf-8 -*-
from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from rest_framework import mixins
from rest_framework import viewsets
from apiusers.serializers import ApiUserSerializer

from django.contrib.auth import get_user_model

from utils.permissions import AdapiPermissions

ApiUser = get_user_model()

class ApiUserViewset(viewsets.ModelViewSet):
    '''
    list:
        获取所有接口权限用户
    read:
        根据id获取单个接口权限用户
    create:
        创建新的接口权限用户
    update:
        根据id更新单个接口权限用户的全部字段
    partial_update:
        根据id更新单个接口权限用户的字段
    delete:
        根据id删除单个接口权限用户
    '''
    queryset = ApiUser.objects.all()
    serializer_class = ApiUserSerializer
    # permission_classes = (AdapiPermissions,)
