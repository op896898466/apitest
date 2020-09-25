import os
from django.conf import settings

from mocks.models import Mocks

from utils import common
from subprocess import Popen, PIPE

mock_data_path = os.path.join(settings.BASE_DIR, 'mock_data')
if not os.path.exists(mock_data_path):
    os.makedirs(mock_data_path)

mock_settings = os.path.join(mock_data_path, 'settings.json')
if not os.path.exists(mock_settings):
    common.to_json_file(mock_settings, [])


def get_count_by_interface(datas):
    datas_list = []
    for item in datas:
        create_time_list = item.get('create_time').split('T')
        first_part = create_time_list[0]
        second_part = create_time_list[1].split('.')[0]
        item['create_time'] = first_part + ' ' + second_part
        interfacemocks_id = item['id']
        # 计算用例数
        mocks_count = Mocks.objects.filter(interfacemocks_id=interfacemocks_id).count()
        item['mocks'] = mocks_count
        datas_list.append(item)
    return datas_list


def read_mock(mock_file):
    """
    读取data_list数据(settings或接口文件)
    :param data_list:
    :return:
    """
    with open(mock_file, encoding="utf-8") as f:
        data_list = eval(f.read())
    return data_list


def interface_start(data):
    """
    接口实例数据，包括外键数据集
    数据文件以本数据的id命名， ${id}.json
    settings: [
        {"include": "${id}.json"}
    ]
    :return:
    """
    # 数据文件以本数据的id命名， ${id}.json
    file_name = str(data['id']) + '.json'
    data_file = os.path.join(mock_data_path, file_name)
    # 写入数据文件
    scenes = Mocks.objects.filter(interfacemocks_id=data['id'], enabled=True)  # data.get('scenes', [])
    # scenes = [{'description': str(scene['id']), 'request': eval(scene['request']), 'response': eval(scene['response'])}
    #           for scene in scenes if scene['enabled']]
    tmp_list = []
    for scene in scenes:
        request = eval(scene.request)
        request['uri'] = data['uri'].strip()
        tmp_list.append({'description': str(scene.id), 'request': request, 'response': eval(scene.response)})
    common.to_json_file(data_file, tmp_list)
    # 先读取，再写入settings
    settings_list = read_mock(mock_settings)
    if not [x for x in settings_list if x['include'] == file_name]:
        # 如果没有找到本接口记录，则追加
        settings_list.append({'include': file_name})
        common.to_json_file(mock_settings, settings_list)


def interface_stop(interface_id):
    file_name = str(interface_id) + '.json'
    settings_list = read_mock(mock_settings)
    try:
        # 直接删除，没有则报错不处理，文件也不会被修改
        settings_list.remove({'include': file_name})
        common.to_json_file(mock_settings, settings_list)
    except ValueError as e:
        print('接口关闭错误：')

    try:
        # 删除接口文件
        os.remove(os.path.join(mock_data_path, file_name))
    except FileNotFoundError as e:
        print('接口关闭错误：')


def run_mock():
    cmd1 = "cd " + mock_data_path
    cmd2 = "java -Dfile.encoding=utf-8 -jar   moco-runner-1.1.0-standalone.jar http -p 8899 -g settings.json"
    cmd = cmd1 + " && " + cmd2
    result = Popen(cmd, shell=True, stdout=PIPE)  # 将输出内容存至缓存中
    while True:
        pr = result.stdout.readline().decode("utf-8").strip()
        print(pr)
        if "started" in pr:
            return {"code": 1, "msg": "启动成功"}
        elif "ERROR" in pr:
            return {"code": 0, "msg": pr.split("[main] ")[1]}
