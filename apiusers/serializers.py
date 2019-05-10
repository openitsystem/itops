# -*- coding: utf-8 -*-
# @Time    : 2019/3/18 19:12
# @Author  :
from datetime import datetime, timedelta

from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth import get_user_model

# from apiusers.models import AttributesLevel, ApinamePermissions

ApiUser = get_user_model()


class ApiUserSerializer(serializers.ModelSerializer):
    # code = serializers.CharField(max_length=4, min_length=4, required=True, help_text='验证码', label='验证码', write_only=True,
    #                              error_messages={
    #                                  "blank":"请输入验证码",
    #                                  "required" : "请输入验证码",
    #                                  "max_length": "max_length>4",
    #                                  "min_length": "min_length>4",
    #                              })
    # mobile = serializers.CharField(required=False, write_only=True,)
    username = serializers.CharField(required=True, allow_blank=True, validators=[UniqueValidator(queryset=ApiUser.objects.all(), message='用户已存在')],
                                     label='用户名', help_text='用户名')
    password = serializers.CharField(
        required=True, style={'input_type': 'password'}, label='密码', write_only=True,
        help_text='密码'
    )
    name = serializers.CharField(label='姓名', required=False, help_text='姓名')
    department = serializers.CharField(label='部门', required=False, help_text='部门')
    description = serializers.CharField(label='描述', required=False, help_text='描述')
    # def create(self, validated_data):
    #     user = super(UserSerializer, self).create(validated_data=validated_data)
    #     user.set_password(validated_data['password'])
    #     user.save()
    #     return user
    # def validate_code(self,code):
    #     one_mintes_age = datetime.now() - timedelta(hours=0, minutes=1, seconds=0)
    #     if code == '1111':
    #         raise serializers.ValidationError('验证码不能为1111')

    def validate(self, attrs):
        if attrs.get('password', ''):
            attrs['password'] = make_password(attrs['password'])
        return attrs

    class Meta:
        model = ApiUser
        # fields = ('id', 'username',)
        fields = ('id', 'username', 'password','name', 'department', 'description')
        # fields = "__all__"

# class ApiAttributesLevelSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = AttributesLevel
#         fields = "__all__"
#
# class ApinamePermissionsSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ApinamePermissions
#         fields = "__all__"
