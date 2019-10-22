# -*- coding: utf-8 -*-
# @Time    : 2019-10-22 9:34
# @Author  : LXF
# @Site    : 
# @File    : blockchain.py
# @Software: PyCharm
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.contrib.auth.models import User
from blockchain_project.models import DeployRequest
from blockchain_project.serializers.deploy_serializer import DeploymentRequestCreationSerializer, \
    DeploymentDetailSerializer
from web3 import Web3, HTTPProvider
from web3.contract import ConciseContract

config = {
    "abi": [...],
    "address": "0x",
}

'''
管理员部署合约***：
POST /api/contract/charity/
["charity_name"]

管理员载入一个已经存在的合约***：
PUT /api/contract/charity/
["charity_address]

//上面两个方法互斥
# '''
# class DeployContractView(APIView):
#     permission_classes = (IsAdminUser,)
#
#     def post(self, request, format=None):
#         charity_name = request.data["charity_name"]
#         web3 = Web3(HTTPProvider('http://localhost:8545'))
#         contract_instance = web3.eth.contract(address=config['address'], abi=config['abi'],
#                                               ContractFactoryClass=ConciseContract)


'''
管理员驳回合约***：
POST /api/contract/fundraise/{合约地址}/disapproval
（调用Fundraise合约的disapproveFundraise方法）
'''
class ContractRejectView(APIView):
    permission_classes = (IsAdminUser,)

    def post(self, request, pk, format=None):
        web3 = Web3(HTTPProvider('http://localhost:8545'))
        # 调用Charity合约的getFundraiseCount和fundraises数组）
        contract_instance = web3.eth.contract(address=config['address'], abi=config['abi'],
                                              ContractFactoryClass=ConciseContract)
        contracts = contract_instance.getFundraiseCount()  # 获取所有捐款合约的地址
        found = 0
        # 遍历所有地址查找
        for contract_address in contracts:
            if str(pk) == str(contract_address):
                address = contract_address
                # 找出捐款合约地址
                found = 1
        if found == 0:  # 找不到返回错误
            return Response(status=status.HTTP_404_NOT_FOUND)

        donation_instance = web3.eth.contract(address=address, abi=config['abi'],
                                              ContractFactoryClass=ConciseContract)
        contract_reject = donation_instance.disapproveFundraise()
        return Response(status=status.HTTP_200_OK)


'''
管理员关闭合约***：
POST /api/contract/fundraise/{合约地址}/close
（调用Fundraise合约的closeFundraise方法）
'''
class ContractCloseView(APIView):
    permission_classes = (IsAdminUser,)

    def post(self, request, pk, format=None):
        web3 = Web3(HTTPProvider('http://localhost:8545'))
        # 调用Charity合约的getFundraiseCount和fundraises数组）
        contract_instance = web3.eth.contract(address=config['address'], abi=config['abi'],
                                              ContractFactoryClass=ConciseContract)
        contracts = contract_instance.getFundraiseCount()  # 获取所有捐款合约的地址
        found = 0
        # 遍历所有地址查找
        for contract_address in contracts:
            if str(pk) == str(contract_address):
                address = contract_address
                # 找出捐款合约地址
                found = 1
        if found == 0:  # 找不到返回错误
            return Response(status=status.HTTP_404_NOT_FOUND)
        donation_instance = web3.eth.contract(address=address, abi=config['abi'],
                                              ContractFactoryClass=ConciseContract)
        contract_reject = donation_instance.closeFundraise()
        return Response(status=status.HTTP_200_OK)


'''
管理员获取所有合约***：
GET /api/contract/fundraise/
（调用Charity合约的getFundraiseCount和fundraises数组）
'''
class GetContractView(APIView):
    permission_classes = (IsAdminUser,)

    def get(self, request, format=None):
        web3 = Web3(HTTPProvider('http://localhost:8545'))
        # 调用Charity合约的getFundraiseCount和fundraises数组）
        contract_instance = web3.eth.contract(address=config['address'], abi=config['abi'],
                                              ContractFactoryClass=ConciseContract)
        contracts = contract_instance.getFundraiseCount()  # 获取所有捐款合约的地址
        return Response(contracts, status=status.HTTP_200_OK)


'''
管理员同意代部署合约***：
POST /api/fundraises/request/{id}
（部署deploy一份新的fundraise合约）
从数据库中根据ID取出相关信息
'''
class AgreeDeployView(APIView):
    permission_classes = (IsAdminUser,)

    def post(self, request, pk, format=None):
        web3 = Web3(HTTPProvider('http://localhost:8545'))
        # 调用Charity合约的getFundraiseCount和fundraises数组）
        contract_instance = web3.eth.contract(address=config['address'], abi=config['abi'],
                                              ContractFactoryClass=ConciseContract)
        # contracts = contract_instance.getFundraiseCount() #获取所有捐款合约的地址
        deployments = DeployRequest.objects.filter(pk=pk)
        if len(deployments) == 0:
            return Response(status=status.HTTP_404_NOT_FOUND)
        deployment = deployments.get(pk=pk)
        # ["name", "owner_address", "target_money", "ipfs_hashes"]
        # 创建新合约
        contracts = contract_instance.createFundraise(deployment.name, deployment.owner_address,
                                                      deployment.target_money, deployment.ipfs_hashes)
        return Response(contracts, status=status.HTTP_200_OK)
