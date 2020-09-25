from django.db import models

from utils.base_models import BaseModel


class Interfacemocks(BaseModel):
    name = models.CharField('接口名称', max_length=100, unique=True)
    uri = models.CharField('uri', max_length=256)
    description = models.TextField('简要描述', blank=True)
    enabled = models.BooleanField('启用/禁用', default=False, blank=True)

    class Meta:
        db_table = 'tb_interfacemocks'
        verbose_name = 'Mock接口'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
