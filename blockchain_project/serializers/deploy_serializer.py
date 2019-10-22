# -*- coding: utf-8 -*-
# @Time    : 2019-10-15 23:23
# @Author  : LXF
# @Site    : 
# @File    : deploy_serializer.py
# @Software: PyCharm

from rest_framework import serializers
from django.contrib.auth.models import User


# 用户请求代部署合约：
class DeploymentRequestCreationSerializer(serializers.Serializer):
    name = serializers.CharField()
    owner_address = serializers.CharField()
    target_money = serializers.CharField()
    ipfs_hashes = serializers.CharField()
    status = serializers.CharField()


# 管理员查询所有代部署申请
class DeploymentDetailSerializer(serializers.Serializer):
    name = serializers.CharField()
    owner_address = serializers.CharField()
    target_money = serializers.CharField()
    ipfs_hashes = serializers.CharField()
    status = serializers.CharField()
