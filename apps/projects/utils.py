# -*- coding: utf-8 -*-
"""
-------------------------------------------------
  @Time : 2020/1/16 21:43 
  @Auth : 可优
  @File : utils.py
  @IDE  : PyCharm
  @Motto: ABC(Always Be Coding)
  @Email: keyou100@qq.com
  @Company: 湖南省零檬信息技术有限公司
  @Copyright: 柠檬班
-------------------------------------------------
"""
from django.db.models import Count
from  projects.models import Projects
from interfaces.models import Interfaces
from testcases.models import Testcases
from testsuits.models import Testsuits



def get_count_by_project(datas):
    """
    1. 通过项目中的接口、用例、配置、套件的数量
    2. 对时间进行格式化
    :param datas:
    :return:
    """
    datas_list = []
    for item in datas:
        # create_time格式化
        create_time_list = item.get('create_time').split('T')
        first_part = create_time_list[0]
        second_part = create_time_list[1].split('.')[0]
        item['create_time'] = first_part + ' ' + second_part

        # 获取项目id值
        project_id = item['id']
        interfaces_testcases_objs = Interfaces.objects.values('id').annotate(testcases=Count('testcases')).\
            filter(project_id=project_id)
        # 获取接口总数
        interfaces_count = interfaces_testcases_objs.count()
        # 设置用例总数初始值为0
        testcases_count = 0
        for one_dict in interfaces_testcases_objs:
            testcases_count += one_dict['testcases']



        # 获取套件总数

        item['interfaces'] = interfaces_count
        item['testcases'] = testcases_count


        datas_list.append(item)
    return datas_list
