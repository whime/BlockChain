# -*- coding: utf-8 -*-
# @Time    : 2019-10-15 23:22
# @Author  : LXF
# @Site    : 
# @File    : user_serializer.py
# @Software: PyCharm
from rest_framework import serializers
from django.contrib.auth.models import User

# 创建用户
class UserCreationSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    email = serializers.EmailField()

# 更新用户信息
class UserUpdateSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    email = serializers.EmailField()

# 查看用户详情信息
class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'email')