# -*- coding: utf-8 -*-

from django.urls import path, re_path, include
from rest_framework import routers

from . import views

router = routers.DefaultRouter()

router.register(r"modules", views.ModulesViewSet)

urlpatterns = [
]

urlpatterns += router.urls
