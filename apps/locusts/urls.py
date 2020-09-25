# -*- coding: utf-8 -*-

from django.urls import path, re_path, include
from rest_framework import routers

from . import views

router = routers.DefaultRouter()

router.register(r"locusts", views.LocustsViewSet)

urlpatterns = [
]

urlpatterns += router.urls
