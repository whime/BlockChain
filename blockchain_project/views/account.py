# -*- coding: utf-8 -*-
# @Time    : 2019-10-16 0:26
# @Author  : LXF
# @Site    : 
# @File    : account.py
# @Software: PyCharm
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import permission_classes
from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from blockchain_project.serializers.account_serializer import AccountLoginSerializer, \
    AccountDetailSerializer, AccountDetailUpdateSerializer, \
    AccountRegistrationSerializer
import base64
import datetime


class AccountLoginView(APIView):

    def post(self, request, format=None):
        serializer = AccountLoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = authenticate(
                username=serializer.validated_data['username'], password=serializer.validated_data['password'])
            if user is not None:
                login(request=request, user=user)
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                return Response(status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class AccountRegistrationView(APIView):

    def post(self, request, format=None):
        serializer = AccountRegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            # Create User
            if User.objects.filter(username=serializer.validated_data["username"]).first() != None:
                return Response(data={"message": "该用户已经存在"}, status=status.HTTP_409_CONFLICT)
            user = User.objects.create_user(
                serializer.validated_data["username"], serializer.validated_data["email"],
                serializer.validated_data["password"])
            user.save()
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class AccountLogoutView(APIView):
    def post(self, request, format=None):
        logout(request)
        return Response(status=status.HTTP_204_NO_CONTENT)


class AccountDetailView(APIView):
    def get(self, request, format=None):
        serializer = AccountDetailSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, format=None):
        serializer = AccountDetailUpdateSerializer(
            request.user, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_202_ACCEPTED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
