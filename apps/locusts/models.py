from django.db import models

from utils.base_models import BaseModel


class Locusts(BaseModel):
    id = models.AutoField(verbose_name='id主键', primary_key=True, help_text='id主键')
    name = models.CharField('压力测试名称', max_length=200, unique=True, help_text='压力测试名称')
    project = models.ForeignKey('projects.Projects', on_delete=models.CASCADE,
                                related_name='locusts', help_text='所属项目')
    include = models.TextField('包含的用例', help_text='包含的接口')
    tester = models.CharField('测试人员', max_length=50, help_text='测试人员')
    desc = models.CharField('简要描述', max_length=200, null=True, blank=True, help_text='简要描述')

    class Meta:
        db_table = 'tb_locusts'
        verbose_name = '压测信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
