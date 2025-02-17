"""a URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from main import views

urlpatterns = [
    # http://127.0.0.1:8080/dashboard
    # 用户聚类分析
    path('kmeanspage', views.kmeanspage),
    # 挖矿预测
    path('WKpage', views.WKpage),
    path('WKpage/t9inner', views.t9inner, name='t9inner'),
    # 下月缴费预测
    path('nextMonth', views.nextMonth),
    path('nextMonth/t10inner', views.t10inner, name='t10inner'),
    # 用户数据预测
    # path('use/',views.use),
    path('searcha/', views.searcha),
    # 用户相关性分析
    path('relax/',views.relax),
    # 用户数据查询
    path('onew/', views.dashboard),
    path('search/', views.search),
    path('onew/t7inner', views.t7inner, name='t7inner'),
    path('index' ,views.index),
    # 主界面
    path('', views.dash)

]
