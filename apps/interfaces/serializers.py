# -*- coding: utf-8 -*-
"""
-------------------------------------------------
  @Time : 2019/12/28 9:54 
  @Auth : 可优
  @File : serializers.py.py
  @IDE  : PyCharm
  @Motto: ABC(Always Be Coding)
  @Email: keyou100@qq.com
  @Company: 湖南省零檬信息技术有限公司
  @Copyright: 柠檬班
-------------------------------------------------
"""
from rest_framework import serializers

from .models import Interfaces
from projects.models import Projects
from utils import validates


class InterfacesSerializer(serializers.ModelSerializer):
    # read_only = True
    project = serializers.StringRelatedField(label='所属项目名称', help_text='所属项目名称', allow_empty=True, allow_null=True,
                                             required=False)
    project_id = serializers.PrimaryKeyRelatedField(queryset=Projects.objects.all(),
                                                    label='项目id', help_text='项目id', allow_empty=True, allow_null=True,
                                                    required=False)

    class Meta:
        model = Interfaces
        fields = ('id', 'name', 'tester', 'create_time', 'desc', 'project', 'project_id')
        extra_kwargs = {
            'create_time': {
                'read_only': True
            }
        }

    def create(self, validated_data):
        project = validated_data.pop('project_id')
        validated_data['project'] = project
        interface = Interfaces.objects.create(**validated_data)
        return interface

    def update(self, instance, validated_data):
        if 'project_id' in validated_data:
            project = validated_data.pop('project_id')
            validated_data['project'] = project

        return super().update(instance, validated_data)


class InterfaceRunSerializer(serializers.ModelSerializer):
    """
    通过接口来运行测试用例序列化器
    """
    env_id = serializers.IntegerField(write_only=True,
                                      help_text='环境变量ID',
                                      validators=[validates.whether_existed_env_id])


    class Meta:
        model = Interfaces
        fields = ('id', 'env_id')
