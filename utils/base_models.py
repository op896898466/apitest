# -*- coding: utf-8 -*-

from django.db import models


class BaseModel(models.Model):
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间", help_text="创建时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间", help_text="更新时间")

    class Meta:
        # 指定为抽象模型类
        # 在迁移时, 不会自动创建table表
        abstract = True
        verbose_name = "公共字段"

