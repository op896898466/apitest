import os
import sys
from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from mocks.models import Mocks
from .models import Interfacemocks
from .serializers import InterfacemocksSerializer
from .utils import get_count_by_interface, interface_start, interface_stop, run_mock


class InterfacemocksViewSet(ModelViewSet):
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
    queryset = Interfacemocks.objects.all()
    serializer_class = InterfacemocksSerializer
    permission_classes = [permissions.IsAuthenticated]
    ordering_fields = ('id', 'name')

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        response.data['results'] = get_count_by_interface(response.data['results'])

        return response

    # def partial_update(self, request, *args, **kwargs):
    #     interface_id = kwargs.get('pk')
    #     isEnabled = request.data.get('enabled')
    #     interface_obj = self.queryset.filter(id=interface_id).first()
    #     super().partial_update(request, *args, **kwargs)
    #     resp = {}
    #     if isEnabled:
    #         interface_start(self.serializer_class(interface_obj).data)
    #     else:
    #         interface_stop(interface_id)
    #     resp['message'] = '接口{}成功'.format('启用' if isEnabled else '禁用')
    #
    #     return Response(resp)

    def update(self, request, *args, **kwargs):
        interface_obj = self.queryset.filter(id=kwargs.get('pk')).first()
        before_data = self.serializer_class(interface_obj).data
        if before_data.get('enabled') and request.data.get('enabled'):
            interface_stop(kwargs.get('pk'))
            interface_start(request.data)
        elif not before_data.get('enabled') and request.data.get('enabled'):
            if len(request.data) == 1:
                interface_start(before_data)
            else:
                interface_start(request.data)
        elif before_data.get('enabled') and not request.data.get('enabled'):
            interface_stop(kwargs.get('pk'))
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """
        接口删除前要删除接口文件和settings数据
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        interface_id = kwargs.get('pk')
        interface_stop(interface_id)
        return super().destroy(request, *args, **kwargs)

    @action(detail=True)
    def mocks(self, request, pk=None):
        interfacemock_obj = Interfacemocks.objects.get(pk=pk)
        mocks_obj = Mocks.objects.filter(interfacemocks_id=pk)
        one_list = []
        for obj in mocks_obj:
            one_list.append({
                "id": obj.id,
                "name": obj.name,
                "description": obj.description,
                "enabled": obj.enabled
            })
        response = {
            "interfacemock": {
                "id": interfacemock_obj.id,
                "name": interfacemock_obj.name,
                "uri": interfacemock_obj.uri,
                "description": interfacemock_obj.description,
                "enabled": "启用" if interfacemock_obj.enabled else "禁用 ",
            },
            "mocks_list": one_list
        }
        return Response(data=response)

    @action(methods=['post'], detail=False)
    def restart(self, request):
        if "win" in sys.platform:
            taskinfo = os.popen('netstat -ano | findstr 8899')
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
            taskinfo = os.popen('lsof -i:8899')
            lines = taskinfo.read()
            line_list = lines.split("\n")
            for line in line_list:
                aList = line.split()
                taskinfo.close()
                if aList:
                    pid = aList[1]
                    if pid:
                        os.popen('kill -9 %s' % pid)
        data = run_mock()

        return Response(data=data)
