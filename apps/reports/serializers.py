# -*- coding: utf-8 -*-
"""
-------------------------------------------------
  @Time : 2020/1/21 20:16 
  @Auth : 可优
  @File : serializers.py
  @IDE  : PyCharm
  @Motto: ABC(Always Be Coding)
  @Email: keyou100@qq.com
  @Company: 湖南省零檬信息技术有限公司
  @Copyright: 柠檬班
-------------------------------------------------
"""
from rest_framework import serializers

from .models import Reports


class ReportsSerializer(serializers.ModelSerializer):
    """
    报告序列化器类
    """

    class Meta:
        model = Reports
        exclude = ('update_time', )

        extra_kwargs = {
            'create_time': {
                'read_only': True
            },

        }
