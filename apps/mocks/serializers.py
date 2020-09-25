# -*- coding: utf-8 -*-

from rest_framework import serializers
from .models import Mocks


class MocksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mocks
        fields = '__all__'
