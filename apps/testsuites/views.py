import os
from datetime import datetime

from django.conf import settings
from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from testcases.models import Testcases
from projects.models import Projects
from modules.models import Modules
from .models import Testsuites
from envs.models import Envs
from .serializers import TestsuitesSerializer, TestsuitesRunSerializer
from .utils import modify_output, get_testcases_by_module_ids
from utils import common


class TestsuitesViewSet(ModelViewSet):
    """
    """
    queryset = Testsuites.objects.all()
    serializer_class = TestsuitesSerializer
    permission_classes = [permissions.IsAuthenticated]
    ordering_fields = ('id', 'name')

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        response.data['results'] = modify_output(response.data['results'])



        return response

    def retrieve(self, request, *args, **kwargs):
        testsuite_obj = self.get_object()
        datas = {
            "name": testsuite_obj.name,
            "include": [{"id": i, "name": Modules.objects.get(id=i).name} for i in eval(testsuite_obj.include)],
            "project_id": testsuite_obj.project_id
        }
        return Response(datas)

    @action(methods=['post'], detail=True)
    def run(self, request, pk=None):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        datas = serializer.validated_data
        env_id = datas.get('env_id')  # 获取环境变量env_id
        env = Envs.objects.get(id=env_id)

        # 创建测试用例所在目录名
        testcase_dir_path = os.path.join(settings.SUITES_DIR,
                                         datetime.strftime(datetime.now(), "%Y%m%d%H%M%S%f"))
        if not os.path.exists(testcase_dir_path):
            os.mkdir(testcase_dir_path)

        include = eval(instance.include)
        if len(include) == 0:
            data_dict = {
                "msg": "此套件下未添加用例, 无法运行!"
            }
            return Response(data_dict, status=status.HTTP_400_BAD_REQUEST)

        # 将include中的接口id转化为此接口下的用例id
        include = get_testcases_by_module_ids(include)
        for testcase_id in include:
            testcase_obj = Testcases.objects.filter(id=testcase_id).first()
            if testcase_obj:
                common.generate_testcase_files(testcase_obj, env, testcase_dir_path)

        return common.run_testcase(instance, testcase_dir_path, request.data.get('is_email'), email=request.user.email)

    def get_serializer_class(self):
        """
        不同的action选择不同的序列化器
        :return:
        """
        return TestsuitesRunSerializer if self.action == 'run' else self.serializer_class
