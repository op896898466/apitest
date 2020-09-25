# -*- coding: utf-8 -*-

from django.db.models import Count
from  projects.models import Projects
from modules.models import Modules
from testcases.models import Testcases
from testsuites.models import Testsuites



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
        modules_testcases_objs = Modules.objects.values('id').annotate(testcases=Count('testcases')).\
            filter(project_id=project_id)
        # 获取模块总数

        modules_count = modules_testcases_objs.count()
        # 设置用例总数初始值为0
        testcases_count = 0
        for one_dict in modules_testcases_objs:
            testcases_count += one_dict['testcases']



        # 获取套件总数
        item['modules'] = modules_count
        item['testcases'] = testcases_count
        item['testsuites'] = Testsuites.objects.filter(project_id=item['id']).count()

        datas_list.append(item)
    return datas_list
