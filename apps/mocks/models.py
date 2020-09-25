from django.db import models

from utils.base_models import BaseModel


class Mocks(BaseModel):
    name = models.CharField('场景名称', max_length=100)
    description = models.TextField('简要描述', blank=True)
    enabled = models.BooleanField('启用/禁用', default=False, blank=True)
    request = models.TextField('请求json')
    response = models.TextField('响应json')
    interfacemocks = models.ForeignKey('interfacemocks.Interfacemocks', on_delete=models.CASCADE, related_name='mocks')

    class Meta:
        db_table = 'tb_mocks'
        verbose_name = '接口名'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
