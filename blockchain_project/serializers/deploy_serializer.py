# -*- coding: utf-8 -*-
# @Time    : 2019-10-15 23:23
# @Author  : LXF
# @Site    : 
# @File    : deploy_serializer.py
# @Software: PyCharm

from rest_framework import serializers
from blockchain_project.models import DeployedCharityContract,DeployedFundraiseContract,DeployRequest
from rest_framework.validators import UniqueValidator
from django.contrib.auth.models import User



# 代部署申请序列化器
class DeploymentRequestSerializer(serializers.ModelSerializer):
    owner = serializers.PrimaryKeyRelatedField(many=False,queryset=User.objects.all())

    class Meta:
        model=DeployRequest
        fields=['name','owner','owner_address','target_money','ipfs_hashes','status']
    # name = serializers.CharField()
    # owner = User
    # owner_address = serializers.CharField()
    # target_money = serializers.CharField()
    # ipfs_hashes = serializers.CharField()
    # status = serializers.IntegerField()

    # def update(self, instance, validated_data):
    #     instance.name = validated_data.get('name',instance.name)
    #     instance.owner_address = validated_data.get('owner_address',instance.owner_address)
    #     instance.target_money = validated_data.get('target_money',instance.target_money)
    #     instance.ipfs_hashes = validated_data.get('ipfs_hashes',instance.ipfs_hashes)
    #     instance.status = validated_data.get('status',instance.status)
    #
    #     instance.save()
    #     return instance
    #
    # def create(self, validated_data):
    #     return DeployRequest.objects.create(**validated_data)

# 已部署机构合约序列化器
class CharitySerializer(serializers.Serializer):
    owner = serializers.CharField(max_length=20)
    # 机构名唯一
    charityName = serializers.CharField(max_length=100,validators=[UniqueValidator(queryset=DeployedCharityContract.objects.all())])
    contractAddr = serializers.CharField(max_length=100)

    def update(self, instance, validated_data):
        instance.owner = validated_data.get('owner',instance.owner)
        instance.charityName = validated_data.get('charity_name',instance.charityName)
        instance.contractAddr = validated_data.get('contractAddr',instance.contractAddr)
        instance.save()

        return instance

    def create(self, validated_data):
        return DeployedCharityContract.objects.create(**validated_data)

# 已部署的募捐合约序列化器
class FundraiseSerializer(serializers.ModelSerializer):
    # fundraiseName = serializers.CharField(max_length=100,validators=[UniqueValidator(queryset=DeployedFundraiseContract.objects.all())])
    class Meta:
        model = DeployedFundraiseContract
        fields = ('owner','fundraiseName','targetMoney','contractAddr')

# string[] fundraises的序列化器
class StringListField(serializers.ListField):
    fundraiseAddr = serializers.CharField()


# 部署机构合约后 response 序列化器
class CharityDeploymentResponseSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    owner = serializers.CharField(max_length=20)
    fundraises = StringListField()
