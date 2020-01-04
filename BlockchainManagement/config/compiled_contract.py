# -*- coding: utf-8 -*-
# @Time    : 2019-10-29 21:35
# @Author  : whime
# @Site    :
# @File    : compiled_contract.py
# @Software: PyCharm

"""
此模块用于返回编译之后的机构合约，项目合约版本
"""

from solc import compile_files
import os

contracts = {}  # 存储编译之后的合约接口


def getCompiledContract():

    PROJECT_ROOT="BlockchainManagement/config"
    compile_sol=compile_files([os.path.join(PROJECT_ROOT,"Charity.sol"),os.path.join(PROJECT_ROOT,"Fundraise.sol")])

    charity_interface=compile_sol['BlockchainManagement/config/Charity.sol:Charity']
    fundraise_interface=compile_sol['BlockchainManagement/config/Fundraise.sol:Fundraise']

    # 保留合约入口
    contracts['charity']=charity_interface
    contracts['fundraise']=fundraise_interface

    return contracts
