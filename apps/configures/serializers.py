from rest_framework import serializers
from projects.models import Projects

from utils.validates import whether_existed_project_id, whether_existed_module_id
from .models import Configures






class ConfiguresSerializer(serializers.ModelSerializer):
    """
    配置序列化器
    """


    class Meta:
        model = Configures
        fields = ('id', 'name',  'author', 'request')
        extra_kwargs = {
            'request': {
                'write_only': True
            }
        }

    def create(self, validated_data):
        return Configures.objects.create(**validated_data)


