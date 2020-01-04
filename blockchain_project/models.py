from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from django.contrib.auth.models import User


# Create your models here.

class DeployRequest(models.Model):
    '''
    用户请求部署
    status:
    1为未处理 2为通过 3为不通过
    用户请求代部署合约：
    POST /api/fundraises/
    ["name","owner_address","target_money","ipfs_hashes"]

    用户撤回请求代部署：
    DELETE /api/fundraises/{id}

    管理员拒绝代部署合约
    POST /api/fundraises/request/{id}/reject

    管理员查询所有代部署申请
    GET /api/fundraises/request/
    GET /api/fundraises/request/{id}
    '''
    id = models.AutoField(primary_key=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.TextField()
    owner_address = models.TextField()
    target_money = models.IntegerField()
    # 使用string存储ipfs_hash地址
    ipfs_hashes = models.CharField(max_length=255)
    add_time = models.DateTimeField(auto_now=True)
    state = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(2)]
    )
    # 0为未处理 1为通过 2为不通过
    # status = models.IntegerField(
    #     validators=[MinValueValidator(1), MaxValueValidator(5)]
    # )
    #将ipfs_hashes转化为列表返回
    # def getIpfsHashList(self):
    #     import ast
    #     return ast.literal_eval(self.ipfs_hashes)




# 已部署的机构合约
class DeployedCharityContract(models.Model):
    owner = models.CharField(max_length=20)
    charityName = models.CharField(max_length=100)
    contractAddr = models.CharField(max_length=100)

# 已部署的募捐项目合约
class DeployedFundraiseContract(models.Model):
    owner = models.CharField(max_length=100)
    fundraiseName = models.CharField(max_length=100)
    targetMoney = models.IntegerField()
    contractAddr = models.CharField(max_length=100)
