# -*- coding: utf-8 -*-
# @Time    : 2019-10-15 23:37
# @Author  : LXF
# @Site    :
# @File    : deployment.py
# @Software: PyCharm

from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from blockchain_project.serializers.user_serializer import UserCreationSerializer, UserDetailSerializer, \
    UserUpdateSerializer


class UserView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer

    # 创建账户
    def post(self, request, format=None):
        serializer = UserCreationSerializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.create_user(
                serializer.validated_data["username"], serializer.validated_data["email"],
                serializer.validated_data["password"])
            user.save()
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class UserDetailView(APIView):
    # 更改账户信息
    def put(self, request, pk, format=None):
        serializer = UserUpdateSerializer(data=request.data)
        if serializer.is_valid():
            users = User.objects.filter(pk=pk)
            if len(users) == 0:
                return Response(status=status.HTTP_404_NOT_FOUND)
            user = users.get(pk=pk)
            user.username = serializer.validated_data["username"]
            user.password = serializer.validated_data["password"]
            user.email = serializer.validated_data["email"]
            user.save()
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    # 获取账号信息
    def get(self, request, pk, format=None):
        users = User.objects.filter(pk=pk)
        if len(users) == 0:
            return Response(status=status.HTTP_404_NOT_FOUND)
        user = users.get(pk=pk)
        serializer = UserDetailSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
