from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import permission_classes
from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.contrib.auth.models import User
from blockchain_project.models import DeployRequest
from blockchain_project.serializers.deploy_serializer import DeploymentRequestSerializer

from rest_framework import serializers
from blockchain_project.views.blockchain import deployOneFundraiseContract,CharityConfig
from web3 import Web3, HTTPProvider,eth
from blockchain_project.models import DeployedCharityContract
from web3.contract import ConciseContract

class DeployRequestView(APIView):
    '''
    用户请求代部署合约
    POST /api/fundraises
    ["name","owner_address","target_money","ipfs_hashes"]

    用户撤回请求代部署：
    DELETE /api/fundraises/delete/{id}

    用户查询代部署合约的申请记录
    GET /api/fundraises
    '''

    def post(self, request, format=None):
        # request.data 无法修改，重新复制一份data
        InfoDict=request.data.copy()
        InfoDict['state']=1
        InfoDict['owner']=User.objects.get(username=str(request.user)).id
        serializer = DeploymentRequestSerializer(data=InfoDict)

        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        else:
            print(serializer.errors)
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        deployments = DeployRequest.objects.filter(id=pk)
        if len(deployments) == 0:
            return Response(status=status.HTTP_404_NOT_FOUND)
        deployment = deployments.get(id=pk)
        deployment.delete()
        return Response(status=status.HTTP_200_OK)

    def get(self, request, format=None):
        user = User.objects.get(username=str(request.user))
        deployments = DeployRequest.objects.filter(owner=user.id)
        if len(deployments) == 0:
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            InfoList = []
            deploymentInfo = {}
            from copy import deepcopy
            for deployment in deployments:
                deploymentInfo['id'] = deployment.id
                deploymentInfo['name'] = deployment.name
                deploymentInfo['owner_address'] = deployment.owner_address
                deploymentInfo['target_money'] = str(deployment.target_money)
                deploymentInfo['ipfs_hashes'] = deployment.ipfs_hashes.split(',')
                deploymentInfo['state'] = deployment.state
                InfoList.append(deepcopy(deploymentInfo))
            return Response(InfoList, status=status.HTTP_200_OK)


class DeploymentRejectView(APIView):
    '''
    管理员拒绝代部署合约
    POST /api/fundraises/request/{id}/reject
    '''
    permission_classes = (IsAdminUser,)

    def post(self, request, pk, format=None):
        deployments = DeployRequest.objects.filter(id=pk)
        if len(deployments) == 0:
            return Response(status=status.HTTP_404_NOT_FOUND)
        deployment = deployments.get(id=pk)
        deployment.state = 2
        deployment.save()
        return Response(status=status.HTTP_200_OK)


class AllDeployRequestView(APIView):
    '''
    管理员查询所有代部署申请
    GET /api/fundraises/request
    '''
    permission_classes = (IsAdminUser,)

    def get(self,request,format=None):
        # 查询所有代部署的申请
        deployments = DeployRequest.objects.all()
        if len(deployments) == 0:
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            InfoList = []
            deploymentInfo = {}
            from copy import deepcopy
            for deployment in deployments:
                deploymentInfo['id'] = deployment.id
                deploymentInfo['name'] = deployment.name
                deploymentInfo['owner_address'] = deployment.owner_address
                deploymentInfo['target_money'] = str(deployment.target_money)
                deploymentInfo['ipfs_hashes'] = deployment.ipfs_hashes.split(',')
                deploymentInfo['state'] = deployment.state
                InfoList.append(deepcopy(deploymentInfo))
            return Response(InfoList, status=status.HTTP_200_OK)

class AgreeDeployView(APIView):
    '''
    管理员同意代部署合约***：
    POST /api/fundraises/request/{id}
    (部署deploy一份新的fundraise合约）
    '''
    def post(self,request,pk,format=None):
        # 获取代部署申请的对象和信息
        try:
            deployment = DeployRequest.objects.get(id=pk)
        except:
            print("找不到对应的代部署申请!!!")
            return Response(status=status.HTTP_404_NOT_FOUND)
        web3=Web3(HTTPProvider('http://localhost:7545'))
        private_key='c022dd3263290ae3ad5bddf9d15028b4ae5ee5cb449f6b206004168dbea4cd29'
        name=deployment.name
        # 获取管理员对应的机构地址
        charityAddr=DeployedCharityContract.objects.get(owner=str(request.user)).contractAddr
        # 获取对应的机构合约
        charity_contract = web3.eth.contract(address=charityAddr, abi=CharityConfig['abi'],
                                             ContractFactoryClass=ConciseContract)
        targetMoney=deployment.target_money
        # TODO(whime): 部署的用户账户应该是哪个？
        result=deployOneFundraiseContract(web3, private_key, name, charityAddr,deployment.owner_address , targetMoney)

        if True in result:
            res = charity_contract.addFundraise(result[1], transact={'from': web3.eth.accounts[0]})
            deployment.state=1
            deployment.save()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response({'detail': '部署募捐项目出错'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



