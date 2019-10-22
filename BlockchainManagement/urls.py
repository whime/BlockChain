"""BlockchainManagement URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
import os
from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView
from django.conf.urls.static import static
from django.conf import settings
from blockchain.blockchain_project.views.account import *
from blockchain.blockchain_project.views.deployment import *
from blockchain.blockchain_project.views.blockchain import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/account/login', AccountLoginView.as_view()),
    path('api/account/logout/', AccountLogoutView.as_view()),
    path('api/account/register', AccountRegistrationView.as_view()),
    path('api/account/', AccountDetailView.as_view()),
    path('api/account/<int:pk>/', AccountDetailView.as_view()),
    path('api/fundraises/', DeployRequestView.as_view()),
    path('api/fundraises/delete/<int:pk>', DeployRequestView.as_view()),
    path('api/fundraises/request/<int:pk>/reject', DeploymentRejectView.as_view()),
    path('api/fundraises/request/', DeploymentView.as_view()),
    path('api/fundraises/request/<int:pk>', DeploymentDetailView.as_view()),
    path('api/contract/fundraise/(?P<pk>[0-9a-zA-Z]+)/disapproval', ContractRejectView.as_view()),  # 管理员驳回合约
    path('api/contract/fundraise/(?P<pk>[0-9a-zA-Z]+)/close', ContractCloseView.as_view()),  # 管理员关闭合约
    path('api/contract/fundraise/', GetContractView.as_view()),  # 管理员获取所有合约
    path('/api/fundraises/request/<int:pk>', AgreeDeployView.as_view()),  # 管理员同意代部署合约

    # url(r'^album/(?P<pk>[0-9]+)/$', views.AlbumDetail.as_view())
]
