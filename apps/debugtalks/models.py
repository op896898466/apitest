from django.db import models

from utils.base_models import BaseModel


class DebugTalks(BaseModel):
    id = models.AutoField(verbose_name='id主键', primary_key=True, help_text='id主键')
    name = models.CharField('debugtalk文件名称', unique=True,max_length=200, default='debugtalk.py', help_text='debugtalk文件名称')
    debugtalk = models.TextField(null=True, default='#debugtalk.py', help_text='debugtalk.py文件')
    is_delete = models.IntegerField(default=0)

    class Meta:
        db_table = 'tb_debugtalks'
        verbose_name = 'debugtalk.py文件'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
