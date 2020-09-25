from rest_framework import serializers

from .models import Testcases
from projects.models import Projects
from modules.models import Modules
from utils import validates


class ModuleAnotherSerialzer(serializers.ModelSerializer):
    # 所属项目名
    project = serializers.StringRelatedField(label="所属项目名", help_text="所属项目名")
    # 所属项目id
    pid = serializers.IntegerField(write_only=True, label="所属项目id", help_text="所属项目id",
                                   validators=[validates.whether_existed_project_id])
    # 接口id
    iid = serializers.IntegerField(write_only=True, label="接口id", help_text="接口id",
                                   validators=[validates.whether_existed_module_id])

    class Meta:
        model = Modules
        fields = ('name', 'project', 'pid', 'iid')
        extra_kwargs = {
            'name': {
                'read_only': True
            }
        }

    def validate(self, attrs):
        """
        校验项目ID是否与接口ID一致
        :param attrs:
        :return:
        """
        if not Modules.objects.filter(id=attrs['iid'], project_id=attrs['pid']).exists():
            raise serializers.ValidationError("项目和接口信息不对应!")
        return attrs


class TestcasesSerializer(serializers.ModelSerializer):
    """
    用例序列化器
    """
    module = ModuleAnotherSerialzer(label="所属项目和接口", help_text="所属项目和接口")

    class Meta:
        model = Testcases
        fields = ('id', 'name', 'include', 'author', 'request', 'module','files')

        extra_kwargs = {
            'include': {
                'write_only': True
            },
            'request': {
                'write_only': True
            },
        }

    def create(self, validated_data):
        module_dict = validated_data.pop('module')
        validated_data['module_id'] = module_dict['iid']
        return Testcases.objects.create(**validated_data)

    def update(self, instance, validated_data):
        print(validated_data)
        if 'module' in validated_data:
            module_dict = validated_data.pop('module')
            validated_data['module_id'] = module_dict['iid']
        return super().update(instance, validated_data)


class TestcasesRunSerializer(serializers.ModelSerializer):
    """
    运行测试用例序列化器
    """
    env_id = serializers.IntegerField(write_only=True,
                                      help_text='环境变量ID',
                                      validators=[validates.whether_existed_env_id])

    class Meta:
        model = Testcases
        fields = ('env_id',)
