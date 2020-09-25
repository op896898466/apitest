# -*- coding: utf-8 -*-

from rest_framework import serializers
from .models import Interfacemocks



class InterfacemocksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interfacemocks
        fields = '__all__'

