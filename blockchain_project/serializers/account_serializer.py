# -*- coding: utf-8 -*-
# @Time    : 2019-10-16 0:27
# @Author  : LXF
# @Site    : 
# @File    : account_serializer.py
# @Software: PyCharm
from rest_framework import serializers
from django.contrib.auth.models import User


class AccountRegistrationSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    email = serializers.CharField(max_length=254)
    password = serializers.CharField(max_length=254, allow_null=True)


class AccountLoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(max_length=254, allow_null=True)


class AccountDetailSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    username = serializers.CharField(max_length=150)
    email = serializers.CharField(max_length=254)


class AccountDetailUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'username', 'password')

     # 重写update方法
    def update(self,instance,validated_data):

        password = validated_data.pop('password',None)
        for (key,value) in validated_data.items():
            setattr(instance,key,value)
        if password is not None:
            # 单独调用set_password方法设置，否则密码无法加密保存
            instance.set_password(password)
        instance.save()

        return instance

