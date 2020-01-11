# -*- coding: utf-8 -*-
# @Time    : 2019-10-29 21:35
# @Author  : whime
# @Site    :
# @File    : compiled_contract.py
# @Software: PyCharm

"""
此模块单独运行，保存合约编译之后的字典进contracts.pk
"""

from solc import compile_files
import os
import pickle


def getCompiledContract():

    PROJECT_CONFIG="."
    compile_sol=compile_files([os.path.join(PROJECT_CONFIG,"Charity.sol"),os.path.join(PROJECT_CONFIG,"Fundraise.sol")])

    with open("contracts.pk","wb") as f:
        pickle.dump(compile_sol,f)

if __name__=='__main__':
    getCompiledContract()