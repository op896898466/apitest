from django.db import models

from utils.base_models import BaseModel


class Modules(BaseModel):
    name = models.CharField('模块名称', max_length=200, unique=True, help_text='模块名称')
    project = models.ForeignKey('projects.Projects', on_delete=models.CASCADE,
                                related_name='modules', help_text='所属项目')
    tester = models.CharField('测试人员', max_length=50, help_text='测试人员')
    desc = models.CharField('简要描述', max_length=200, null=True, blank=True, help_text='简要描述')

    class Meta:
        db_table = 'tb_modules'
        verbose_name = '模块信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
