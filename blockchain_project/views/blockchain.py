# -*- coding: utf-8 -*-
# @Time    : 2019-10-22 9:34
# @Author  : LXF
# @Site    : 
# @File    : blockchain.py
# @Software: PyCharm
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.contrib.auth.models import User

from BlockchainManagement.config import compiled_contract
from blockchain_project.models import DeployRequest
from blockchain_project.serializers.deploy_serializer import CharityDeploymentResponseSerializer
from web3 import Web3, HTTPProvider,eth
from web3.contract import ConciseContract
from copy import deepcopy
from blockchain_project.models import DeployedCharityContract
from blockchain_project.serializers.deploy_serializer import CharitySerializer,FundraiseSerializer


compiledContracts = compiled_contract.getCompiledContract()
charityContract = compiledContracts['charity']
fundraiseContract = compiledContracts['fundraise']

CharityConfig = {
    "abi": charityContract['abi'],
    "bin":charityContract['bin']
}
FundraiseConfig = {
    "abi": fundraiseContract['abi'],
    "bin":fundraiseContract['bin']
}

'''
管理员部署合约***：
POST /api/contract/charity
["charity_name","private_key]


管理员载入一个已经存在的合约***：
PUT /api/contract/charity/
["charity_address]

//上面两个方法互斥
'''

class DeployContractView(APIView):
    permission_classes = (IsAdminUser,)

    def post(self, request, format=None):

        private_key = request.data['private_key']
        charity_name = request.data["charity_name"]
        w3 = Web3(HTTPProvider('http://localhost:7545'))

        # 创建部署合约事务
        Charity = w3.eth.contract(abi=CharityConfig['abi'],bytecode=CharityConfig['bin'])
        # tx_hash = Charity.constructor(charity_name).transact(transaction={'from':w3.eth.accounts[0],'gas':6000000})
        estimate_gas = Charity.constructor(charity_name).estimateGas()
        transaction = Charity.constructor(charity_name).buildTransaction({
            'from':w3.eth.accounts[0],
            'nonce':w3.eth.getTransactionCount(w3.eth.coinbase),
            'gasPrice': w3.toWei('20', 'gwei'),
            'gas': estimate_gas
        })
        # 签名事务并发送
        signed_transaction = w3.eth.account.sign_transaction(transaction,private_key=private_key)
        tx_hash = w3.eth.sendRawTransaction(Web3.toHex(signed_transaction.rawTransaction))

        # 获取交易回执并保存合约地址进数据库
        tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
        serializer=CharitySerializer(data={'owner':str(request.user),'charityName':charity_name,'contractAddr':tx_receipt.contractAddress})
        if serializer.is_valid():
            serializer.save()
            # 根据合约地址获取合约实例
            contract_instance=w3.eth.contract(abi=CharityConfig['abi'],address=tx_receipt.contractAddress)
            addressList=[]
            # 逐一获取机构合约里的慈善项目合约
            fundraisesCount = contract_instance.functions.getFundraiseCount().call()
            for i in range(fundraisesCount):
                addressList.append(contract_instance.functions.fundraises(i).call())
            resSerializer=CharityDeploymentResponseSerializer(data={
                'name':charity_name,
                'owner':str(request.user),
                'fundraises':addressList})
            if resSerializer.is_valid():
                # fundraise = w3.eth.contract(abi=FundraiseConfig['abi'], bytecode=FundraiseConfig['bin'])
                # fundraise_tx_hash = fundraise.constructor("慈善机构1",contract_instance.address,w3.eth.accounts[1],100).transact({'from':w3.eth.accounts[0],'gas':6000000})
                # fund_tx_receipt = w3.eth.waitForTransactionReceipt(fundraise_tx_hash)
                #
                # print(contract_instance.functions.fundraises(0).call())
                # fundddd = contract_instance.functions.getFundraiseWithIndex(0).call()
                # print(fundddd)
                # fund_instance=w3.eth.contract(abi=FundraiseConfig['abi'],address=fundddd)
                # print(fund_instance.functions.name().call())
                return Response(resSerializer.data,status=status.HTTP_200_OK)
            else:   return Response(resSerializer.errors,status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


    def get(self,request):
        user = request.user
        contractObject = DeployedCharityContract.objects.get(owner=user)

        if contractObject is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        contractAddr = contractObject.contractAddr
        charityName = contractObject.charityName

        w3 = Web3(HTTPProvider('http://localhost:7545'))
        charity = w3.eth.contract(address=contractAddr,abi=CharityConfig['abi'])

        if charity is not None:
            addressList = []
            # 逐一获取机构合约里的慈善项目合约
            fundraisesCount = charity.functions.getFundraiseCount().call()
            for i in range(fundraisesCount):
                addressList.append(charity.functions.fundraises(i).call())
            resSerializer = CharityDeploymentResponseSerializer(data={
                'name': charityName,
                'owner': str(request.user),
                'fundraises': addressList})
            if resSerializer.is_valid():
                return Response(resSerializer.data, status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)




class DeployExistedContractView(APIView):
    permission_classes = (IsAdminUser,)

    def post(self,request):
        charity_address = request.data['charity_address']
        w3 = Web3(HTTPProvider('http://localhost:7545'))

        charity = w3.eth.contract(address=charity_address, abi=CharityConfig['abi'])
        if charity is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        charity_name = charity.functions.name().call()
        # 保存机构地址等信息进数据库
        serializer = CharitySerializer(
            data={'owner': str(request.user), 'charityName': charity_name, 'contractAddr': charity.address})
        if serializer.is_valid():
            serializer.save()
            addressList = []
            # 逐一获取机构合约里的慈善项目合约
            fundraisesCount = charity.functions.getFundraiseCount().call()
            for i in range(fundraisesCount):
                addressList.append(charity.functions.fundraises(i).call())
            resSerializer = CharityDeploymentResponseSerializer(data={
                'name': charity_name,
                'owner': str(request.user),
                'fundraises': addressList})
            if resSerializer.is_valid():
                return Response(resSerializer.data,status=status.HTTP_200_OK)
            else:   return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR,data={'机构名或合约地址验证不通过..'})



'''
查询是否已经存在合约
GET /api/contract/charity/
'''
class QueryExistingContractView(APIView):
    def get(self,request):
        user = request.data['user']
        contractObject = DeployedCharityContract.objects.get(owner=user)
        if contractObject is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        contractAddr = contractObject.contractAddr
        charityName = contractObject.charityName

        w3 = web3(HTTPProvider('http://lcalhost:7545'))
        charity = w3.eth.contract(address=contractAddr,abi=CharityConfig['abi'])

        if charity is not None:
            addressList = []
            # 逐一获取机构合约里的慈善项目合约
            fundraisesCount = charity.functions.getFundraiseCount().call()
            for i in range(fundraisesCount):
                addressList.append(charity.functions.fundraises(i).call())
            resSerializer = CharityDeploymentResponseSerializer(data={
                'name': charity_name,
                'owner': str(request.user),
                'fundraises': addressList})
            if resSerializer.is_valid():
                return Response(resSerializer.data, status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)



'''
管理员驳回合约***：
POST /api/contract/fundraise/disapproval/{合约地址}
（调用Fundraise合约的disapproveFundraise方法）
'''

class ContractRejectView(APIView):
    permission_classes = (IsAdminUser,)

    def post(self, request, pk, format=None):
        # 管理员获取机构合约实例
        contractObject = DeployedCharityContract.objects.get(owner=str(request.user))

        if contractObject is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        contractAddr = contractObject.contractAddr

        web3 = Web3(HTTPProvider('http://localhost:7545'))
        charity_contract = web3.eth.contract(address=contractAddr, abi=CharityConfig['abi'],
                                              ContractFactoryClass=ConciseContract)

        # 部署一个募捐项目
        # TODO(whime):解决部署合约时用户的私钥和账户来源,项目名称
        result=deployOneFundraiseContract(web3,'252a71ee8377c202ddcaaabd4eafa8f9a61185b523a05ce262e298509f33f0c2'
                                          ,'mujuan9',contractAddr,web3.eth.accounts[1],1000)
        if True in result:
             res=charity_contract.addFundraise(result[1],transact={'from':web3.eth.accounts[0]})
        else:
            return Response({'detail':'部署募捐项目出错'},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # 遍历机构的所有募捐项目
        fundraisesCount = charity_contract.getFundraiseCount()
        found = 0
        # 遍历所有地址查找是否有对应的募捐项目合约
        for i in range(fundraisesCount):
            contract_address=charity_contract.fundraises(i)
            print(str(i)+":"+str(contract_address))
            if str(pk) == str(contract_address):
                address = contract_address
                # 找出捐款合约地址
                found = 1
                break
        if found == 0:  # 找不到返回错误
            return Response(status=status.HTTP_404_NOT_FOUND)

        donation_instance = web3.eth.contract(address=pk, abi=FundraiseConfig['abi'])
        contract_reject = donation_instance.functions.disapproveFundraise().call(transaction={'from':web3.eth.accounts[0]})
        return Response(status=status.HTTP_200_OK)


'''
管理员关闭合约***：
POST /api/contract/fundraise/close/{合约地址}
（调用Fundraise合约的closeFundraise方法）
'''
class ContractCloseView(APIView):
    permission_classes = (IsAdminUser,)

    def post(self, request, pk, format=None):
        # 管理员获取机构合约实例
        contractObject = DeployedCharityContract.objects.get(owner=str(request.user))

        if contractObject is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        contractAddr = contractObject.contractAddr

        web3 = Web3(HTTPProvider('http://localhost:7545'))
        charity_contract = web3.eth.contract(address=contractAddr, abi=CharityConfig['abi'],
                                             ContractFactoryClass=ConciseContract)

        # 预先部署一个募捐项目，测试用，最后将删除
        # TODO(whime):解决部署合约时用户的私钥和账户来源,项目名称
        result = deployOneFundraiseContract(web3, '252a71ee8377c202ddcaaabd4eafa8f9a61185b523a05ce262e298509f33f0c2'
                                            , 'mujuan10', contractAddr, web3.eth.accounts[1], 1000)
        if True in result:
            res = charity_contract.addFundraise(result[1], transact={'from': web3.eth.accounts[0]})
        else:
            return Response({'detail': '部署募捐项目出错'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # 遍历机构的所有募捐项目
        fundraisesCount = charity_contract.getFundraiseCount()
        found = 0
        # 遍历所有地址查找是否有对应的募捐项目合约
        for i in range(fundraisesCount):
            contract_address = charity_contract.fundraises(i)
            print(str(i) + ":" + str(contract_address))
            if str(pk) == str(contract_address):
                address = contract_address
                # 找出捐款合约地址
                found = 1
                break
        if found == 0:  # 找不到返回错误
            return Response(status=status.HTTP_404_NOT_FOUND)

        donation_instance = web3.eth.contract(address=result[1], abi=FundraiseConfig['abi'])
        contract_close = donation_instance.functions.closeFundraise().call(transaction={'from': web3.eth.accounts[0]})
        print(contract_close)
        return Response(status=status.HTTP_200_OK)


'''
管理员获取所有合约***：
GET /api/contract/fundraise/
（调用Charity合约的getFundraiseCount和fundraises数组）
'''
class GetContractView(APIView):
    permission_classes = (IsAdminUser,)

    def get(self, request, format=None):
        # 根据用户名获取合约地址
        charity_contract = DeployedCharityContract.objects.get(owner=str(request.user))
        web3 = Web3(HTTPProvider('http://localhost:7545'))

        # 获取Charity合约对象
        contract_instance = web3.eth.contract(address=charity_contract.contractAddr,abi=CharityConfig['abi'] ,
                                              ContractFactoryClass=ConciseContract)
        fundraiseCount=contract_instance.getFundraiseCount()
        fundraiseAddrList=[]
        for i in range(0,fundraiseCount):
            fundraiseAddrList.append(contract_instance.fundraises(i))

        return Response(data={'addressList':fundraiseAddrList}, status=status.HTTP_200_OK)


'''
管理员获取单个合约信息***
GET /api/contract/fundraise/{合约地址}
'''
class GetOneContractView(APIView):
    permission_classes=(IsAdminUser,)

    def get(self,request,pk,format=None):
        # 获取合约的信息
        fundraiseInfo = {}
        web3 = Web3(HTTPProvider('http://localhost:7545'))
        fundraiseContract = web3.eth.contract(address=pk, abi=FundraiseConfig['abi'],ContractFactoryClass=ConciseContract)
        if fundraiseContract is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        fundraiseInfo['address'] = pk
        fundraiseInfo['name'] = fundraiseContract.name()
        fundraiseInfo['owner_address'] = fundraiseContract.owner()
        fundraiseInfo['target_money'] = fundraiseContract.targetMoney()
        fundraiseInfo['now_money'] = fundraiseContract.nowMoney()
        fundraiseInfo['state'] = fundraiseContract.state()

        ipfsInfo=[]
        # ipfs文件数量
        ipfsCount=fundraiseContract.getFileCount()
        for i in range(ipfsCount):
            ipfsInfo.append(fundraiseContract.ipfsHashes(i))
        fundraiseInfo['ipfs_hashes'] = ipfsInfo

        return Response(data={'fundraiseInfo':fundraiseInfo},status=status.HTTP_200_OK)

'''
部署一个募捐项目合约
'''

def deployOneFundraiseContract(web3,private_key,name,charity,owner,targetMoney):
    fundraise = web3.eth.contract(abi=FundraiseConfig['abi'],bytecode=FundraiseConfig['bin'])
    estimate_gas = fundraise.constructor(name,charity,owner,targetMoney).estimateGas()
    fundraise_transaction = fundraise.constructor(name,charity,owner,targetMoney).buildTransaction(
        {
            # TODO(whime):from 字段如何确定？参数化？
            'from': web3.eth.accounts[0],
            'nonce': web3.eth.getTransactionCount(owner),
            'gasPrice': web3.toWei('20', 'gwei'),
            'gas': estimate_gas
        }
    )
    signed_transaction = web3.eth.account.sign_transaction(fundraise_transaction,private_key=private_key)
    tx_hash = web3.eth.sendRawTransaction(Web3.toHex(signed_transaction.rawTransaction))
    tx_receipt = web3.eth.waitForTransactionReceipt(tx_hash)
    # 将部署的募捐合约信息写入数据库
    serializer = FundraiseSerializer(data={'owner':owner,'fundraiseName':name,'targetMoney':targetMoney,
                                           'contractAddr':tx_receipt.contractAddress})
    print(repr(serializer))
    if serializer.is_valid():
        serializer.save()
        return [True,tx_receipt.contractAddress]
    else:
        print(serializer.errors)
        return [False]

