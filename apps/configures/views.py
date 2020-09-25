import json

from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions
from rest_framework import filters
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Configures
from .serializers import ConfiguresSerializer
from modules.models import Modules
from utils import handle_datas


class ConfiguresViewSet(ModelViewSet):
    """
    list:
    返回配置信息（多个）列表数据

    create:
    创建配置信息

    retrieve:
    返回配置信息（单个）详情数据

    update:
    更新（全）配置信息

    partial_update:
    更新（部分）配置信息

    destroy:
    删除配置信息

    retrieve:
    获取配置详情
    """
    queryset = Configures.objects.all()
    serializer_class = ConfiguresSerializer
    permission_classes = (permissions.IsAuthenticated,)
    ordering_fields = ('id', 'name')

    def retrieve(self, request, *args, **kwargs):
        config_obj = self.get_object()
        config_request = json.loads(config_obj.request, encoding='utf-8')

        # 处理请求头数据
        config_headers = config_request['config']['request'].get('headers')
        config_headers_list = handle_datas.handle_data4(config_headers)

        # 处理全局变量数据
        config_variables = config_request['config'].get('variables')
        config_variables_list = handle_datas.handle_data2(config_variables)

        config_name = config_obj.name

        datas = {
            "author": config_obj.author,
            "configure_name": config_name,
            "header": config_headers_list,
            "globalVar": config_variables_list
        }

        return Response(datas)

    @action(methods=['get'], detail=False)
    def names(self,request, *args, **kwargs):
        """
        Returns a list of all the testcases names by module id
        """
        configures_objs = Configures.objects.all()
        one_list = []
        for obj in configures_objs:
            one_list.append({
                'id': obj.id,
                'name': obj.name
            })
        return Response(data=one_list)
