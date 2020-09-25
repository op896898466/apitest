import os
import sys
from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from .utils import scene_start, scene_stop

from .models import Mocks
from .serializers import MocksSerializer


class MocksViewSet(ModelViewSet):
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
    queryset = Mocks.objects.all()
    serializer_class = MocksSerializer
    permission_classes = [permissions.IsAuthenticated]
    ordering_fields = ('id', 'name')

    # def partial_update(self, request, *args, **kwargs):
    #     super().partial_update(request, *args, **kwargs)
    #     scene_id = kwargs.get('pk')
    #     isEnabled = request.data.get('enabled')
    #     scene_obj = self.queryset.filter(id=scene_id).first()
    #     resp = {}
    #     action = scene_start if isEnabled else scene_stop
    #     action(self.serializer_class(scene_obj).data)
    #     resp['message'] = '场景{}成功'.format('启用' if isEnabled else '禁用')
    #     # 保存状态
    #     return Response(resp)

    def update(self, request, *args, **kwargs):
        mock_obj = self.queryset.filter(id=kwargs.get('pk')).first()
        before_data = self.serializer_class(mock_obj).data
        if before_data.get('enabled') and request.data.get('enabled'):
            scene_stop(before_data)
            scene_start(request.data)
        elif not before_data.get('enabled') and request.data.get('enabled'):
            if len(request.data) == 1:
                scene_start(before_data)
            else:
                scene_start(request.data)
        elif before_data.get('enabled') and not request.data.get('enabled'):
            scene_stop(before_data)
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """
        接口删除前要删除接口文件和settings数据
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        scene_id = kwargs.get('pk')
        scene_obj = self.queryset.filter(id=scene_id).first()
        scene_stop(self.serializer_class(scene_obj).data)
        return super().destroy(self, request, *args, **kwargs)
