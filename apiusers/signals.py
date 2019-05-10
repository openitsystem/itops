# -*- coding: utf-8 -*-
# @Time    : 2019/3/20 11:58
# @Author  :

# from django.db.models.signals import post_save
# from django.dispatch import receiver
# # from rest_framework.authtoken.models import Token
# from django.contrib.auth import get_user_model
#
# ApiUser = get_user_model()
#
# # sigmals  Django 信号量 当检测到model 保存的时候来调用 还需要app重载函数配置
# @receiver(post_save, sender = ApiUser)
# def create_auth_token(sender, instance=None, created=False, **kwargs):
#     if created:
#         # 密码加密
#         password = instance.password
#         instance.set_password(password)
#         instance.save()
#         # 创建token
#         # Token.objects.create(user=instance)