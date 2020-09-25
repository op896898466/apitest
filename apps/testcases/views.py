import json
import os
import datetime
from datetime import datetime
from rest_framework import status
from django.db import IntegrityError
from django.conf import settings
from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Testcases
from modules.models import Modules
from envs.models import Envs
from .serializers import TestcasesSerializer, TestcasesRunSerializer
from utils import handle_datas, common
from .utils import bytes2str, tidy_tree_data
import random


class TestcasesViewSet(ModelViewSet):
    """
    """
    queryset = Testcases.objects.all()
    serializer_class = TestcasesSerializer
    permission_classes = [permissions.IsAuthenticated]
    ordering_fields = ('id', 'name')

    def retrieve(self, request, *args, **kwargs):
        """获取用例详情信息"""
        testcase_obj = self.get_object()

        # 用例前置信息
        testcase_include = json.loads(testcase_obj.include, encoding='utf-8')

        # 用例请求信息
        testcase_request = json.loads(testcase_obj.request, encoding='utf-8')
        testcase_request_datas = testcase_request.get('test').get('request')
        if testcase_request.get('test').get('skip'):
            is_skip = [{"key": "skip", "value": testcase_request.get('test').get('skip')}]
        elif testcase_request.get('test').get('skipIf'):
            is_skip = [{"key": "skipIf", "value": testcase_request.get('test').get('skipIf')}]
        elif testcase_request.get('test').get('skipUnless'):
            is_skip = [{"key": "skipUnless", "value": testcase_request.get('test').get('skipUnless')}]
        else:
            is_skip = [{"key": "", "value": ""}]

        # 处理用例的validate列表
        # 将[{'check': 'status_code', 'expected':200, 'comparator': 'equals'}]
        # 转化为[{key: 'status_code', value: 200, comparator: 'equals', param_type: 'string'}]
        testcase_validate = testcase_request.get('test').get('validate')

        testcase_validate_list = handle_datas.handle_data1(testcase_validate)

        # 处理用例的param数据
        testcase_params = testcase_request_datas.get('params')
        testcase_params_list = handle_datas.handle_data4(testcase_params)

        # 处理用例的header列表
        testcase_headers = testcase_request_datas.get('headers')
        testcase_headers_list = handle_datas.handle_data4(testcase_headers)

        # 处理用例variables变量列表
        testcase_variables = testcase_request.get('test').get('variables')
        testcase_variables_list = handle_datas.handle_data2(testcase_variables)

        # 处理form表单数据
        testcase_form_datas = testcase_request_datas.get('data')
        testcase_form_datas_list = handle_datas.handle_data6(testcase_form_datas)

        # 处理json数据
        # testcase_json_datas = str(testcase_request_datas.get('json'))
        testcase_json_datas = json.dumps(testcase_request_datas.get('json'), ensure_ascii=False)

        # 处理extract数据
        testcase_extract_datas = testcase_request.get('test').get('extract')
        testcase_extract_datas_list = handle_datas.handle_data3(testcase_extract_datas)

        # 处理parameters数据
        testcase_parameters_datas = testcase_request.get('test').get('parameters')
        testcase_parameters_datas_list = handle_datas.handle_data3(testcase_parameters_datas)

        # 处理setupHooks数据
        testcase_setup_hooks_datas = testcase_request.get('test').get('setup_hooks')
        testcase_setup_hooks_datas_list = handle_datas.handle_data5(testcase_setup_hooks_datas)

        # 处理teardownHooks数据
        testcase_teardown_hooks_datas = testcase_request.get('test').get('teardown_hooks')
        testcase_teardown_hooks_datas_list = handle_datas.handle_data5(testcase_teardown_hooks_datas)

        files = json.loads(testcase_obj.files, encoding='utf-8')

        selected_configure_id = testcase_include.get('config')
        selected_module_id = testcase_obj.module_id
        selected_project_id = Modules.objects.get(id=selected_module_id).project_id
        selected_testcase_id = testcase_include.get('testcases')
        selected_testcase = []
        if selected_testcase_id:
            for i in selected_testcase_id:
                selected_testcase.append({
                    "id": i,
                    "name": Testcases.objects.get(id=i).name
                })
        selected_testcase_after_id = testcase_include.get('testcases_after')
        selected_testcase_after = []
        if selected_testcase_after_id:
            for i in selected_testcase_after_id:
                selected_testcase_after.append({
                    "id": i,
                    "name": Testcases.objects.get(id=i).name
                })
        datas = {
            "author": testcase_obj.author,
            "testcase_name": testcase_obj.name,
            "selected_configure_id": selected_configure_id,
            "selected_module_id": selected_module_id,
            "selected_project_id": selected_project_id,
            "selected_testcase": selected_testcase,
            # "selected_testcase_after": selected_testcase_after,
            "method": testcase_request_datas.get('method'),
            "url": testcase_request_datas.get('url'),
            "param": testcase_params_list,
            "header": testcase_headers_list,
            "variable": testcase_form_datas_list,  # form表单请求数据
            "jsonVariable": testcase_json_datas,

            "extract": testcase_extract_datas_list,
            "validate": testcase_validate_list,
            "globalVar": testcase_variables_list,  # 变量
            "parameterized": testcase_parameters_datas_list,
            "setupHooks": testcase_setup_hooks_datas_list,
            "teardownHooks": testcase_teardown_hooks_datas_list,
            "is_skip": is_skip,
            "files": files
        }
        return Response(datas)

    @action(methods=['post'], detail=True)
    def run(self, request, pk=None):
        # 1. 获取模型类对象
        instance = self.get_object()
        # 2. 校验
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        datas = serializer.validated_data
        env = Envs.objects.get(id=datas.get('env_id'))

        # 3. 生成yaml测试用例文件
        testcase_dir_path = os.path.join(settings.SUITES_DIR,
                                         datetime.strftime(datetime.now(), '%Y%m%d%H%M%S%f'))

        common.generate_testcase_files(instance, env, testcase_dir_path)
        # 4. 运行用例
        return common.run_testcase(instance, testcase_dir_path)

    @action(methods=['post'], detail=False)
    def debug(self, request):
        # 1. 获取模型类对象
        env = Envs.objects.get(id=request.data["env_id"])

        # 3. 生成yaml测试用例文件
        testcase_dir_path = os.path.join(settings.SUITES_DIR,
                                         datetime.strftime(datetime.now(), '%Y%m%d%H%M%S%f' + "_debug"))

        common.generate_debug_files(request.data, env, testcase_dir_path)
        summary = common.run_testcase(request.data, testcase_dir_path, False, debug=True)
        for i, item in enumerate(summary['details']):
            for j, record in enumerate(item['records']):
                if 'files' in record['meta_data']['request'].keys():
                    files_request = record['meta_data']['request']['files']
                    summary['details'][i]['records'][j]['meta_data']['request']['files'] = [files_request[file][0] for file in files_request]
                    summary['details'][i]['records'][j]['meta_data']['request']['body'] = record['meta_data']['request']['files']
        summary = bytes2str(summary)
        # 返回用例中全部请求的结果树数据
        tree = []
        case_metas = []  # 保存用例的元数据,包括运行是否成功,断言结果等
        for record in summary['details'][0]['records']:
            # 调试结果树增加请求信息
            result = [
                {
                    'title': '请求',
                    'expand': True,
                    'children': tidy_tree_data(record['meta_data']['request'], [], disabled=True),
                    'disabled': True,
                },
                {
                    'title': '响应',
                    'expand': True,
                    'children': tidy_tree_data(record['meta_data']['response'], [])
                }
            ]
            # one_record = tidy_tree_data(record['meta_data']['response'], [])
            # one_request = tidy_tree_data(record['meta_data']['request'], [])
            # 当前请求是否成功的标志、traceback（attachment）、validators
            case_run_info = dict()
            case_run_info['flag'] = record['status'] == 'success'
            case_run_info['attachment'] = record['attachment']
            case_run_info['validators'] = record['meta_data']['validators']
            case_run_info['name'] = record['name']
            # 此为附加信息,页面展示时要先取出该数据
            case_metas.append(case_run_info)
            tree.append(result)

        return_info = {
            'tree': tree,
            'case_metas': case_metas,
            'summary': summary
        }

        return Response(return_info)

    @action(methods=['post'], detail=True)
    def copy_testcase(self, request, pk=None):
        data = request.data
        try:
            obj = Testcases.objects.get(pk=pk)
            obj.id = None
            obj.name = data.get('name')
            obj.save()
            return Response({'msg': '用例复制成功', "id": obj.id})
        except Testcases.DoesNotExist:
            return Response({'msg': '复制用例不存在'}, status=status.HTTP_400_BAD_REQUEST)
        except IntegrityError:
            return Response({'msg': '复制用例不能重名'}, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['post'], detail=False)
    def upload_file(self, request):
        if not request.FILES:
            return Response({"msg": "上传失败"}, status=status.HTTP_400_BAD_REQUEST)
        files_list = []
        for filename in request.FILES:
            file = request.FILES.get(filename)
            file_path = os.path.join(settings.UPLOAD_DIR,
                                     datetime.strftime(datetime.now(), '%Y%m%d%H%M%S%f' + "_") + file.name.replace('"',
                                                                                                                   ''))
            files_list.append(file_path)
            with open(file_path,
                      mode='wb+') as destination:  # 打开特定的文件进行二进制的写操作
                for chunk in file.chunks():  # 分块写入文件
                    destination.write(chunk)

        return Response({"files_list":files_list})

    def get_serializer_class(self):
        if self.action == "run" or self.action == "debug":
            return TestcasesRunSerializer
        else:
            return self.serializer_class
