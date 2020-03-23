### 基于区块链的公益众筹平台(后端代码)

#### 背景
本项目是一个基于区块链的公益众筹平台的后端restful API代码，主要实现用户注册管理，众筹项目管理以及和区块链交互。

#### 开发环境
![](https://img.shields.io/badge/python-3.6.6-green)
![](https://img.shields.io/badge/django-2.1.7-yellow)
![](https://img.shields.io/badge/web3-5.2.2-orange)
![](https://img.shields.io/badge/djangorestframework-3.10.3-blue)
![](https://img.shields.io/badge/solc-3.2.0-lightgrey)
> python -m pip install -r ./requirements.txt
#### 主要 API 介绍
|API | description|
|- | -|
|api/account/|用户登入登出，注册|
|api/fundraises/|用于处理用户请求代部署募捐项目的申请，同意/拒绝/删除申请等|
|api/contract/|智能合约部署，查询，关闭，驳回等。|

#### 其他说明
+ 智能合约使用本地solc.exe编译器编译，版本为0.5.12+commit.7709ece9.Windows.msvc
+ 本地数据库使用mysql,数据库名blockchain，需提前创建
+ 本地测试链使用Ganache部署，并使用postman测试API
