# -*- coding: utf-8 -*-

from rest_framework import routers

from . import views

router = routers.DefaultRouter()

router.register(r"mocks", views.MocksViewSet)

urlpatterns = [
]

urlpatterns += router.urls
