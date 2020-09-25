import os
from utils import common
from django.conf import settings
from interfacemocks.models import Interfacemocks


mock_data_path = os.path.join(settings.BASE_DIR, 'mock_data')
if not os.path.exists(mock_data_path):
    os.makedirs(mock_data_path)


def read_mock(mock_file):
    """
    读取data_list数据(settings或接口文件)
    :param data_list:
    :return:
    """
    with open(mock_file,encoding="utf-8") as f:
        data_list = eval(f.read())
    return data_list

def scene_start(data):
    """
    读取具体的接口文件
    :param data:
    :return:
    """
    interface = data['interfacemocks']
    file_name = os.path.join(mock_data_path, str(interface) + '.json')
    try:
        scenes_list = read_mock(file_name) # 如果接口没启用，无文件
        uri = Interfacemocks.objects.get(pk=interface).uri.strip()
        if not [x for x in scenes_list if x['description'] == str(data['id'])]:
            # 如果没有找到本接口记录，则追加
            request = eval(data['request'])
            request['uri'] = uri
            scenes_list.append({'description': str(data['id']), 'request': request, 'response': eval(data['response'])})
            common.to_json_file(file_name, scenes_list)
    except FileNotFoundError:
        # 无文件，说明接口没启用
        pass


def scene_stop(data):
    interface = data['interfacemocks']
    file_name = os.path.join(mock_data_path, str(interface) + '.json')
    try:
        scenes_list = read_mock(file_name)
        uri = Interfacemocks.objects.get(pk=interface).uri.strip()
        # 直接删除，没有则报错不处理，文件也不会被修改
        request = eval(data['request'])
        request['uri'] = uri
        scenes_list.remove({'description': str(data['id']), 'request': request, 'response': eval(data['response'])})
        common.to_json_file(file_name, scenes_list)
    except ValueError :
        pass
    except FileNotFoundError :
        # 无文件，说明接口没启用
        pass
