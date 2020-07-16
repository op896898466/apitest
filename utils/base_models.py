# -*- coding: utf-8 -*-
"""
-------------------------------------------------
  @Time : 2020/1/16 20:46 
  @Auth : 可优
  @File : base_models.py
  @IDE  : PyCharm
  @Motto: ABC(Always Be Coding)
  @Email: keyou100@qq.com
  @Company: 湖南省零檬信息技术有限公司
  @Copyright: 柠檬班
-------------------------------------------------
"""
from django.db import models


class BaseModel(models.Model):
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间", help_text="创建时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间", help_text="更新时间")

    class Meta:
        # 指定为抽象模型类
        # 在迁移时, 不会自动创建table表
        abstract = True
        verbose_name = "公共字段"

