# -*- coding: utf-8 -*-
"""
-------------------------------------------------
  @Time : 2019/12/10 21:57 
  @Auth : 可优
  @File : urls.py
  @IDE  : PyCharm
  @Motto: ABC(Always Be Coding)
  @Email: keyou100@qq.com
  @Company: 湖南省零檬信息技术有限公司
  @Copyright: 柠檬班
-------------------------------------------------
"""
from django.urls import path, re_path, include
from rest_framework import routers

from . import views

router = routers.DefaultRouter()

router.register(r"interfaces", views.InterfacesViewSet)

urlpatterns = [
]

urlpatterns += router.urls
