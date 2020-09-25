from rest_framework import serializers

from .models import Projects
from debugtalks.models import DebugTalks
from modules.models import Modules
from utils import validates
from testcases.models import Testcases


class ProjectModelSerializer(serializers.ModelSerializer):
    debugtalk = serializers.StringRelatedField(label='所属函数名称', help_text='所属函数名称', required=False)
    debugtalk_id = serializers.PrimaryKeyRelatedField(queryset=DebugTalks.objects.all(),
                                                      label='函数id', help_text='函数id',  required=False)

    class Meta:
        model = Projects
        fields = ('id', 'name', 'leader', 'tester', 'programmer', 'publish_app', 'create_time', 'desc', 'debugtalk',
                  'debugtalk_id')

        extra_kwargs = {
            'create_time': {
                'read_only': True
            }
        }

    def create(self, validated_data):
        if 'debugtalk_id' in validated_data:
            debugtalk = validated_data.pop('debugtalk_id')
            validated_data['debugtalk'] = debugtalk

        project_obj = super().create(validated_data)
        return project_obj

    def update(self, instance, validated_data):
        if 'debugtalk_id' in validated_data:
            debugtalk = validated_data.pop('debugtalk_id')
            validated_data['debugtalk'] = debugtalk
        else:
            validated_data['debugtalk'] = None

        return super().update(instance, validated_data)

class ProjectNamesModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Projects
        fields = ('id', 'name')




class ProjectsRunSerializer(serializers.ModelSerializer):
    """
    运行测试用例序列化器
    """
    env_id = serializers.IntegerField(write_only=True,
                                      help_text='环境变量ID',
                                      validators=[validates.whether_existed_env_id])

    class Meta:
        model = Testcases
        fields = ('id', 'env_id')
