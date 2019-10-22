from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import permission_classes
from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.contrib.auth.models import User
from blockchain.blockchain_project.models import DeployRequest
from blockchain.blockchain_project.serializers.deploy_serializer import DeploymentRequestCreationSerializer, \
    DeploymentDetailSerializer
import base64
import datetime


class DeployRequestView(APIView):
    '''
    POST /api/fundraises/
    ["name","owner_address","target_money","ipfs_hashes

    用户撤回请求代部署：
    DELETE /api/fundraises/delete/{id}
    '''

    def post(self, request, format=None):
        serializer = DeploymentRequestCreationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.status = 1
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        deployments = DeployRequest.objects.filter(pk=pk)
        if len(deployments) == 0:
            return Response(status=status.HTTP_404_NOT_FOUND)
        deployment = deployments.get(pk=pk)
        deployment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class DeploymentRejectView(APIView):
    '''
    管理员拒绝代部署合约
    POST /api/fundraises/request/{id}/reject
    '''
    permission_classes = (IsAdminUser,)

    def post(self, request, pk, format=None):
        deployments = DeployRequest.objects.filter(pk=pk)
        if len(deployments) == 0:
            return Response(status=status.HTTP_404_NOT_FOUND)
        deployment = deployments.get(pk=pk)
        deployment.status = 3
        deployment.save()
        return Response(status=status.HTTP_200_OK)


class DeploymentView(ListAPIView):
    '''
    管理员查询所有代部署申请
    GET /api/fundraises/request/
    '''
    queryset = DeployRequest.objects.all()
    serializer_class = DeploymentDetailSerializer
    permission_classes = (IsAdminUser,)


class DeploymentDetailView(APIView):
    '''
    管理员查询所有代部署申请
    GET /api/fundraises/request/
    GET /api/fundraises/request/{id}
    '''
    permission_classes = (IsAdminUser,)

    def get(self, request, pk, format=None):
        deployments = DeployRequest.objects.filter(pk=pk)
        if len(deployments) == 0:
            return Response(status=status.HTTP_404_NOT_FOUND)
        deployment = deployments.get(pk=pk)
        serializer = DeploymentDetailSerializer(deployment)
        return Response(serializer.data, status=status.HTTP_200_OK)
