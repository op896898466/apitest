from rest_framework import serializers

from .models import Testsuites
from projects.models import Projects
from utils import validates


class TestsuitesSerializer(serializers.ModelSerializer):
    """
    套件序列化器
    """

    class Meta:
        model = Testsuites
        fields = '__all__'


class TestsuitesRunSerializer(serializers.ModelSerializer):
    """
    通过套件来运行测试用例序列化器
    """
    env_id = serializers.IntegerField(write_only=True,
                                      help_text='环境变量ID',
                                      validators=[validates.whether_existed_env_id])

    class Meta:
        model = Testsuites
        fields = ('id', 'env_id')
