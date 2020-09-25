# -*- coding: utf-8 -*-

from rest_framework import serializers

from .models import Modules
from projects.models import Projects
from utils import validates


class ModulesSerializer(serializers.ModelSerializer):
    # read_only = True
    project = serializers.StringRelatedField(label='所属项目名称', help_text='所属项目名称', allow_empty=True, allow_null=True,
                                             required=False)
    project_id = serializers.PrimaryKeyRelatedField(queryset=Projects.objects.all(),
                                                    label='项目id', help_text='项目id', allow_empty=True, allow_null=True,
                                                    required=False)

    class Meta:
        model = Modules
        fields = ('id', 'name', 'tester', 'create_time', 'desc', 'project', 'project_id')
        extra_kwargs = {
            'create_time': {
                'read_only': True
            }
        }

    def create(self, validated_data):
        project = validated_data.pop('project_id')
        validated_data['project'] = project
        module = Modules.objects.create(**validated_data)
        return module

    def update(self, instance, validated_data):
        if 'project_id' in validated_data:
            project = validated_data.pop('project_id')
            validated_data['project'] = project

        return super().update(instance, validated_data)


class ModuleRunSerializer(serializers.ModelSerializer):
    """
    通过接口来运行测试用例序列化器
    """
    env_id = serializers.IntegerField(write_only=True,
                                      help_text='环境变量ID',
                                      validators=[validates.whether_existed_env_id])


    class Meta:
        model = Modules
        fields = ('id', 'env_id')
