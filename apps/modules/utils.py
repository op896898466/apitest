import re

from django.db.models import Count

from modules.models import Modules
from testcases.models import Testcases
from configures.models import Configures


def get_count_by_module(datas):
    datas_list = []
    for item in datas:
        create_time_list = item.get('create_time').split('T')
        first_part = create_time_list[0]
        second_part = create_time_list[1].split('.')[0]
        item['create_time'] = first_part + ' ' + second_part
        module_id = item['id']
        # 计算用例数
        testcases_count = Testcases.objects.filter(module_id=module_id).count()
        item['testcases'] = testcases_count
        datas_list.append(item)
    return datas_list
