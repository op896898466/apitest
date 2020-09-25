import os
import sys
import time
from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

from .models import Locusts
from .serializers import LocustsSerializer, LocustsRunSerializer
from testcases.models import Testcases
from envs.models import Envs
from utils import common


class LocustsViewSet(ModelViewSet):
    """
    list:
    返回接口（多个）列表数据

    create:
    创建接口

    retrieve:
    返回接口（单个）详情数据

    update:
    更新（全）接口

    partial_update:
    更新（部分）接口

    destroy:
    删除接口

    testcases:
    返回某个接口的所有用例信息（ID和名称）

    configures:
    返回某个接口的所有配置信息（ID和名称）
    """
    queryset = Locusts.objects.all()
    serializer_class = LocustsSerializer
    permission_classes = [permissions.IsAuthenticated]
    ordering_fields = ('id', 'name')

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        for item in response.data["results"]:
            create_time_list = item['create_time'].split('T')
            first_part = create_time_list[0]
            second_part = create_time_list[1].split('.')[0]
            item['create_time'] = first_part + ' ' + second_part
            item["testcase_count"] = len(eval(item["include"]))
        return response

    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        response.data["include"] = [{"id": i, "name": Testcases.objects.get(id=i).name} for i in eval(self.get_object().
                                                                                                      include)]
        return response

    @action(methods=['post'], detail=False)
    def kill(self, request):
        if "win" in sys.platform:
            taskinfo = os.popen('netstat -ano | findstr 8089')
            lines = taskinfo.read()
            line_list = lines.split("\n")
            for line in line_list:
                aList = line.split()
                taskinfo.close()
                if aList:
                    pid = aList[4]
                    if pid:
                        os.popen('taskkill /pid %s /f' % pid)
        elif "linux" in sys.platform:
            taskinfo = os.popen('lsof -i:8089')
            lines = taskinfo.read()
            line_list = lines.split("\n")
            for line in line_list:
                aList = line.split()
                taskinfo.close()
                if aList:
                    pid = aList[1]
                    if pid:
                        os.popen('kill -9 %s' % pid)

        data_dict = {
            "msg": "已解除端口占用"
        }
        return Response(data_dict, status=status.HTTP_200_OK)

    @action(methods=['post'], detail=True)
    def run(self, request, pk=None):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        env_id = data.get('env_id')  # 获取环境变量env_id
        env = Envs.objects.get(id=env_id)
        testcase_objs = Testcases.objects.filter(id__in=eval(instance.include))
        if not testcase_objs.exists():  # 如果此接口下没有用例, 则无法运行
            data_dict = {
                "msg": "此压测接口下无用例, 无法运行!"
            }
            return Response(data_dict, status=status.HTTP_400_BAD_REQUEST)

        return common.is_locust(request.data, env, testcase_objs)

    @action(methods=['post'], detail=True)
    def run_noweb(self, request, pk=None):
        instance = self.get_object()
        data = request.data
        data["name"] = instance.name
        data["email"] = request.user.email
        env_id = data.get('env_id')  # 获取环境变量env_id
        env = Envs.objects.get(id=env_id)
        testcase_objs = Testcases.objects.filter(id__in=eval(instance.include))
        if not testcase_objs.exists():  # 如果此接口下没有用例, 则无法运行
            data_dict = {
                "msg": "此压测接口下无用例, 无法运行!"
            }
            return Response(data_dict, status=status.HTTP_400_BAD_REQUEST)

        return common.is_locust_noweb(data, env, testcase_objs)

    def get_serializer_class(self):
        """
        不同的action选择不同的序列化器
        :return:
        """
        return LocustsRunSerializer if self.action == 'run' else self.serializer_class
