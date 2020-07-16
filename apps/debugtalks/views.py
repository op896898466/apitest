from rest_framework.viewsets import GenericViewSet
from rest_framework.viewsets import ModelViewSet
from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework import permissions
from rest_framework import filters
from rest_framework.response import Response
from .untils import get_projects

from .models import DebugTalks
from .serializers import DebugTalksSerializer


class DebugTalksViewSet(ModelViewSet):
    """
    list:
    返回debugtalk（多个）列表数据

    update:
    更新（全）debugtalk

    partial_update:
    更新（部分）debugtalk
    """
    queryset = DebugTalks.objects.all()
    serializer_class = DebugTalksSerializer
    permission_classes = [permissions.IsAuthenticated]
    ordering_fields = ('id',)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        data_dict = {
            "id": instance.id,
            "debugtalk": instance.debugtalk
        }
        return Response(data_dict)

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        response.data['results'] = get_projects(response.data['results'])

        return response

    @action(methods=['get'], detail=False)
    def names(self, request):
        """
        Returns a list of all the testcases names by interface id
        """
        debugtalks_objs = DebugTalks.objects.all()
        one_list = []
        for obj in debugtalks_objs:
            one_list.append({
                'id': obj.id,
                'name': obj.name
            })
        return Response(data=one_list)
