#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2018/11/13 11:59
# @Author  : Center
from django.conf.urls import url


from . import zapi

import json


app_name = 'monitorurl'


urlpatterns = [
    url(r'^get_items_history_api/$', zapi.get_items_history_api.as_view(),name='get_items_history_api'),#模糊查找AD账号
    url(r'^getgroupitem/$', zapi.get_group_item_api.as_view(),name='get_items_history_api'),#模糊查找AD账号
    url(r'^getitem_history/$', zapi.get_item_history_api.as_view(),name='get_items_history_api'),#模糊查找AD账号
    ]