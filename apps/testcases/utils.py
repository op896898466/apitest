import json
import re


def bytes2str(data):
    """
    如果data中包含有bytes类型数据，在使用JsonResponse时会报错
    函数用于把请求响应中的bytes转成str
    :param data:字典类型
    :return:
    """
    if isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, bytes):
                data[key] = value.decode()
            elif isinstance(value, dict):
                data[key] = bytes2str(value)
            elif isinstance(value, list):
                for i in range(len(value)):
                    value[i] = bytes2str(value[i])
                data[key] = value
    elif isinstance(data, list):
        for i in range(len(data)):
            data[i] = bytes2str(data[i])
    return data


def python2js(value, check_list=(None, True, False)):
    """
    把check_list中的值从python类型转成js(json)类型，以适配前端显示
    :param value:
    :param check_list:
    :return:
    """
    if check_list is not None and value in check_list:
        value = json.dumps(value)
    else:
        value = str(value)
    return value


def tidy_tree_data(data, tree_list, parent_path=None, disabled=False):
    '''
    此函数为递归函数, 用于整理返回给前端显示的树形结果数据
    初始的data为响应数据response，是字典类型
    所以初始化数据不能是字典或列表以外的类型
    :parent_path：为None即表示为顶层。子层向下传入时应该把当前parent_path+本身路径(key)
    :param data:
    :param tree_list:传入要保存数据的列表，建议传[]（适配ztree框架的数据要求）
    :return:
    '''
    if isinstance(data, list):
        for i, v in enumerate(data):
            '''
            假设响应数据如下：
            [
                {
                    "id": 53,
                    "title": "xxxxxxxxxx",
                    "content": "<p>123</p>",
                    "author": "123",
                    "pub_date": "2019-07-24T13:45:33.755000"
                },
                {
                    "id": 54,
                    "title": "324",
                    "content": "<p>234</p>",
                    "author": "234",
                    "pub_date": "2019-07-24T13:45:44.484000"
                }
            ]
            如果想取出第一条数据的id,httprunner提取数据，则使用json.0.id
            所以在前端做结果树形显示时，把列表数据的索引作为一级，也是为了后面做数据自动提取作铺垫。
            '''
            # 保存本次节点数据的字典对象
            node = {}
            if isinstance(v, (str, int, float, bool)):
                node['title'] = str(i) + '-->' + python2js(v)
                node['expect'] = v
                node['disabled'] = disabled
            else:
                node['title'] = i
                node['disabled'] = disabled
                sub_parent_path = str(i) if parent_path is None else parent_path + '.' + str(i)  # 下一层的父路径
                node['children'] = tidy_tree_data(v, [], parent_path=sub_parent_path, disabled=disabled)
            # 保存本数据节点的路径(父路径.本节点路径)
            node['path'] = str(i) if parent_path is None else parent_path + '.' + str(i)
            node['name'] = i
            if node:
                tree_list.append(node)
    elif isinstance(data, dict):
        for key, value in data.items():
            if key in ['content_type', 'content_size', 'response_time_ms', 'elapsed_ms']:
                # 这三个字段在httprunner中不支持提取，所以过滤掉。
                continue
            # 保存本次节点数据的字典对象
            node = {}
            # 下一层的父路径
            sub_parent_path = key if parent_path is None else parent_path + '.' + key
            if isinstance(value, (list, dict, tuple)):
                # 列表或字典 递归解释
                node['children'] = tidy_tree_data(value, [], parent_path=sub_parent_path,disabled=disabled)
                node['title'] = key if node['children'] else key + '-->' + python2js(value)
                node['disabled'] = disabled
            else:
                if key in ['text', 'content']:
                    '''
                    text类型为字节和 content类型为字串，但是为了适配前端显示，把这两字段的内容解释成功字典或列表
                    如果解释失败，有可以是内容为空，或者包含不可解释成python对象的内容。
                    此时直接按字串输出
                    '''
                    try:
                        value = json.loads(value)
                        # node['name'] = key
                        if isinstance(value, (list, dict)):
                            node['children'] = tidy_tree_data(value, [], parent_path=sub_parent_path,disabled=disabled)
                            node['title'] = key if node['children'] else key + '-->[]'
                            node['disabled'] = disabled
                        else:
                            node['title'] = key + '-->' + python2js(value)
                            node['expect'] = value
                            node['disabled'] = disabled
                    except Exception as e:
                        print(e)
                        node['title'] = key + '-->' + python2js(value)
                        node['expect'] = value
                        node['disabled'] = disabled
                else:
                    # 字串直接输出
                    node['title'] = key + '-->' + python2js(value)
                    node['expect'] = value
                    node['disabled'] = disabled
            # 保存本数据节点的路径(父路径.本节点路径)
            node['path'] = key if parent_path is None else parent_path + '.' + key
            node['name'] = key
            if node:
                tree_list.append(node)
    return tree_list
