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
    email = serializers.CharField(max_length=254)
    password = serializers.CharField(max_length=254, allow_null=True)


class AccountDetailSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    username = serializers.CharField(max_length=150)
    email = serializers.CharField(max_length=254)


class AccountDetailUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'username', 'password')
