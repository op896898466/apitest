# -*- coding: utf-8 -*-
"""
-------------------------------------------------
  @Time : 2020/2/18 12:35 
  @Auth : 可优
  @File : urls.py.py
  @IDE  : PyCharm
  @Motto: ABC(Always Be Coding)
  @Email: keyou100@qq.com
  @Company: 湖南省零檬信息技术有限公司
  @Copyright: 柠檬班
-------------------------------------------------
"""
from django.urls import path
from rest_framework import routers

from .views import SummaryAPIView


urlpatterns = [
    path('summary/', SummaryAPIView.as_view(), name='summary'),
]
