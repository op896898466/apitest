import time
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import requests
from collections import OrderedDict
import os
import sys
from io import BufferedReader

# sys.path.append("..")
from utils.yamlparser import ordered_yaml_dump
import subprocess
import io
import logging
import json
from datetime import datetime

import yaml
from django.conf import settings
from httprunner.task import HttpRunner
from httprunner.exceptions import ParamsError
from rest_framework import status
from rest_framework.response import Response

from testcases.models import Testcases
from envs.models import Envs
from reports.models import Reports
from debugtalks.models import DebugTalks
from projects.models import Projects
from configures.models import Configures
from modules.models import Modules

logger = logging.getLogger('test')

os.environ[
    "PATH"] += os.pathsep + r'C:\Users\dell\PycharmProjects\DeployDjango\django_app_docker\DjangoDev03\venv\Scripts'


class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, bytes):
            return str(obj, encoding='utf-8')
        return json.JSONEncoder.default(self, obj)


def timestamp_to_datetime(summary, type=True):
    if not type:
        time_stamp = int(summary["time"]["start_at"])
        summary['time']['start_datetime'] = datetime. \
            fromtimestamp(time_stamp).strftime('%Y-%m-%d %H:%M:%S')

    for detail in summary['details']:
        try:
            time_stamp = int(detail['time']['start_at'])
            detail['time']['start_at'] = datetime.fromtimestamp(time_stamp).strftime('%Y-%m-%d %H:%M:%S')
        except Exception:
            pass

        for record in detail['records']:
            try:
                time_stamp = int(record['meta_data']['request']['start_timestamp'])
                record['meta_data']['request']['start_timestamp'] = \
                    datetime.fromtimestamp(time_stamp).strftime('%Y-%m-%d %H:%M:%S')
            except Exception:
                pass
    return summary


def generate_testcase_files(instance, env, testcase_dir_path):
    testcases_list = []
    config = {
        'config': {
            'name': instance.name,
            "variables": [],
            'request': {
                'base_url': env.base_url if env else ''
            }
        }
    }
    testcases_list.append(config)

    # include = eval(instance.include)
    # request = eval(instance.request)
    # 获取当前用例的前置配置和前置用例
    include = json.loads(instance.include, encoding='utf-8')
    # 获取当前用例的请求信息
    request = json.loads(instance.request, encoding='utf-8')

    module_name = instance.module.name  # 接口名称
    project_name = instance.module.project.name  # 项目名称

    testcase_dir_path = os.path.join(testcase_dir_path, project_name)
    # 创建项目名所在文件夹
    if not os.path.exists(testcase_dir_path):
        os.makedirs(testcase_dir_path)
        debugtalk_obj = Projects.objects.get(name=project_name).debugtalk
        if debugtalk_obj:
            debugtalk = debugtalk_obj.debugtalk
        else:
            debugtalk = ""

        # 创建debugtalk.py文件
        with open(os.path.join(testcase_dir_path, 'debugtalk.py'),
                  mode='w',
                  encoding='utf-8') as one_file:
            one_file.write(debugtalk)

    testcase_dir_path = os.path.join(testcase_dir_path, module_name)
    # 在项目目录下创建接口名所在文件夹
    if not os.path.exists(testcase_dir_path):
        os.makedirs(testcase_dir_path)

    # {'config': 2, 'testcases': [2,5]}
    # 如果include前置中有config, 那么添加到testcases_list中
    # if 'config' in include:
    #     config_id = include.get('config')
    #     config_obj = Configures.objects.filter(id=config_id).first()
    #     if config_obj:
    #         # 需要将请求头(当前为嵌套字典的列表), 需要转化为字典
    #         # config_request = eval(config_obj.request)
    #         config_request = json.loads(config_obj.request, encoding='utf-8')
    #
    #         # config_request = eval(config_obj.request)
    #         # config_request.get('config').get('request').setdefault('base_url', env.base_url)
    #         # config_dict = config_request.get('config')
    #         # config_dict['request']['base_url'] = env.base_url
    #         # config_request['config']['name'] = instance.name
    #         config_request['config']['request']['base_url'] = env.base_url
    #         # testcases_list.append(config_request)
    #         testcases_list[0] = config_request

    # 如果include前置中有testcases, 那么添加到testcases_list中
    if 'testcases' in include:
        for t_id in include.get('testcases'):
            testcase_obj = Testcases.objects.filter(id=t_id).first()
            if testcase_obj:
                try:
                    # testcase_request = eval(testcase_obj.request)
                    testcase_request = json.loads(testcase_obj.request, encoding='utf-8')
                except Exception as e:
                    logger.error(e)
                    continue
                else:
                    # 将前置用例提取的数据提前在全局变量中声明
                    extract = testcase_request["test"].get("extract")
                    if extract:
                        for e in extract:
                            testcases_list[0]["config"]["variables"].append({[i for i in e.keys()][0]: ''})
                    testcase_request["test"] = OrderedDict(testcase_request["test"])
                    testcases_list.append(OrderedDict(testcase_request))

    # 将当前用例的request添加到testcases_list
    request["test"] = OrderedDict(request["test"])
    testcases_list.append(request)
    with open(os.path.join(testcase_dir_path, instance.name + '.yml'),
              mode="w", encoding="utf-8") as one_file:
        ordered_yaml_dump(testcases_list, one_file, default_flow_style=False, allow_unicode=True)


def generate_debug_files(data, env, testcase_dir_path):
    testcases_list = []
    config = {
        'config': {
            'name': data["name"],
            'request': {
                'base_url': env.base_url if env else ''
            }
        }
    }
    testcases_list.append(config)

    # include = eval(instance.include)
    # request = eval(instance.request)
    # 获取当前用例的前置配置和前置用例
    include = json.loads(data["include"], encoding='utf-8')
    # 获取当前用例的请求信息
    request = json.loads(data["request"], encoding='utf-8')

    module = Modules.objects.get(id=data["module"]["iid"])  # 模块id
    project = Projects.objects.get(id=data["module"]["pid"])  # 项目id

    testcase_dir_path = os.path.join(testcase_dir_path, project.name)
    # 创建项目名所在文件夹
    if not os.path.exists(testcase_dir_path):
        os.makedirs(testcase_dir_path)
        debugtalk_obj = project.debugtalk
        if debugtalk_obj:
            debugtalk = debugtalk_obj.debugtalk
        else:
            debugtalk = ""

        # 创建debugtalk.py文件
        with open(os.path.join(testcase_dir_path, 'debugtalk.py'),
                  mode='w',
                  encoding='utf-8') as one_file:
            one_file.write(debugtalk)

    testcase_dir_path = os.path.join(testcase_dir_path, module.name)
    # 在项目目录下创建接口名所在文件夹
    if not os.path.exists(testcase_dir_path):
        os.makedirs(testcase_dir_path)

    # {'config': 2, 'testcases': [2,5]}
    # 如果include前置中有config, 那么添加到testcases_list中
    # if 'config' in include:
    #     config_id = include.get('config')
    #     config_obj = Configures.objects.filter(id=config_id).first()
    #     if config_obj:
    #         # 需要将请求头(当前为嵌套字典的列表), 需要转化为字典
    #         # config_request = eval(config_obj.request)
    #         config_request = json.loads(config_obj.request, encoding='utf-8')
    #
    #         # config_request = eval(config_obj.request)
    #         # config_request.get('config').get('request').setdefault('base_url', env.base_url)
    #         # config_dict = config_request.get('config')
    #         # config_dict['request']['base_url'] = env.base_url
    #         # config_request['config']['name'] = instance.name
    #         config_request['config']['request']['base_url'] = env.base_url
    #         # testcases_list.append(config_request)
    #         testcases_list[0] = config_request

    # 如果include前置中有testcases, 那么添加到testcases_list中
    if 'testcases' in include:
        for t_id in include.get('testcases'):
            testcase_obj = Testcases.objects.filter(id=t_id).first()
            if testcase_obj:
                try:
                    # testcase_request = eval(testcase_obj.request)
                    testcase_request = json.loads(testcase_obj.request, encoding='utf-8')
                    testcase_request["test"].pop('skip', 0)
                    testcase_request["test"].pop('skipIf', 0)
                    testcase_request["test"].pop('skipUnless', 0)

                except Exception as e:
                    logger.error(e)
                    continue
                else:
                    testcases_list.append(testcase_request)

    # 将当前用例的request添加到testcases_list
    testcases_list.append(request)

    with open(os.path.join(testcase_dir_path, data["name"] + '.yml'),
              mode="w", encoding="utf-8") as one_file:
        yaml.dump(testcases_list, one_file, allow_unicode=True)


def generate_locust_files(instance, env, testcase_dir_path, repeat_list):
    testcases_list = []
    if 0 not in repeat_list:
        config = {
            'config': {
                'name': instance.name,
                'request': {
                    'base_url': env.base_url if env else ''
                }
            }
        }
        testcases_list.append(config)
        repeat_list.append(0)

    # include = eval(instance.include)
    # request = eval(instance.request)
    # 获取当前用例的前置配置和前置用例
    include = json.loads(instance.include, encoding='utf-8')
    # 获取当前用例的请求信息
    request = json.loads(instance.request, encoding='utf-8')
    project_name = instance.module.project.name  # 项目名称
    debugtalk_obj = Projects.objects.get(name=project_name).debugtalk
    if debugtalk_obj:
        debugtalk = debugtalk_obj.debugtalk
    else:
        debugtalk = ""

        # 创建debugtalk.py文件
    with open(os.path.join(testcase_dir_path, 'debugtalk.py'),
              mode='w',
              encoding='utf-8') as one_file:
        one_file.write(debugtalk)

    if 'testcases' in include:
        for t_id in include.get('testcases'):
            if t_id not in repeat_list:
                testcase_obj = Testcases.objects.filter(id=t_id).first()
                if testcase_obj:
                    try:
                        testcase_request = json.loads(testcase_obj.request, encoding='utf-8')
                    except Exception as e:
                        logger.error(e)
                        continue
                    else:
                        testcases_list.append(testcase_request)
                        repeat_list.append(t_id)

    # 将当前用例的request添加到testcases_list
    if instance.id not in repeat_list:
        testcases_list.append(request)
        repeat_list.append(instance.id)

    with open(os.path.join(testcase_dir_path, "locust" + '.yml'),
              mode="a", encoding="utf-8") as one_file:
        yaml.dump(testcases_list, one_file, allow_unicode=True)


def create_report(runner, report_name=None):
    """
    创建测试报告
    :param runner:
    :param report_name:
    :return:
    """
    time_stamp = int(runner.summary["time"]["start_at"])
    start_datetime = datetime.fromtimestamp(time_stamp).strftime('%Y-%m-%d %H:%M:%S')
    runner.summary['time']['start_datetime'] = start_datetime
    # duration保留3位小数
    runner.summary['time']['duration'] = round(runner.summary['time']['duration'], 3)
    report_name = report_name if report_name else start_datetime
    runner.summary['html_report_name'] = report_name

    for item in runner.summary['details']:
        try:
            for record in item['records']:
                record['meta_data']['response']['content'] = record['meta_data']['response']['content']. \
                    decode('utf-8')
                record['meta_data']['response']['cookies'] = dict(record['meta_data']['response']['cookies'])

                request_body = record['meta_data']['request']['body']
                if 'files' in record['meta_data']['request'].keys():
                    files_request = record['meta_data']['request']['files']
                    record['meta_data']['request']['files'] = [files_request[file][0] for file in files_request]
                    record['meta_data']['request']['body'] = record['meta_data']['request']['files']
                if isinstance(request_body, bytes):
                    record['meta_data']['request']['body'] = request_body.decode('utf-8')
        except Exception as e:
            print(e)

    summary = json.dumps(runner.summary, cls=MyEncoder, ensure_ascii=False)

    report_name = report_name + '_' + datetime.strftime(datetime.now(), '%Y%m%d%H%M%S')
    report_path = runner.gen_html_report(html_report_name=report_name)

    # with open(report_path, encoding='utf-8') as stream:
    #     reports = stream.read()

    test_report = {
        'name': report_name,
        'result': runner.summary.get('success'),
        'success': runner.summary.get('stat').get('successes'),
        'count': runner.summary.get('stat').get('testsRun'),
        'html': report_path,
    }
    report_obj = Reports.objects.create(**test_report)
    return report_obj


def run_testcase(instance, testcase_dir_path, is_email=False, email='', debug=False):
    """
    运行用例
    :return:
    :param instance: 实例
    :param testcase_dir_path: 用例根目录路径
    :return dict
    """
    runner = HttpRunner()
    # runner.run(testcase_dir_path)
    try:
        runner.run(testcase_dir_path)
    except ParamsError:
        logger.error("用例参数有误")
        data = {
            "msg": "用例参数有误"
        }
        return Response(data, status=400)

    runner.summary = timestamp_to_datetime(runner.summary, type=False)

    if debug:
        return runner.summary

    try:
        report_name = instance.name
    except Exception as e:
        report_name = '被遗弃的报告' + '-' + datetime.strftime(datetime.now(), '%Y%m%d%H%M%S')

    report = create_report(runner, report_name=report_name)
    data_dict = {
        "id": report.id
    }
    if is_email:
        report_full_path = report.html
        content = "执行结果：{}，用例总数：{}，成功总数：{}，详情请查看测试报告。" \
            .format("Pass" if report.result == 1 else "Fail", report.count, report.success)
        send_email_text(report.name, content, report_full_path, email)

    return Response(data_dict, status=status.HTTP_200_OK)


def is_locust(data, env, testcase_objs):
    url = "http://192.168.0.147:8089"
    if "win" in sys.platform:
        url = "http://192.168.0.147:8089"
        taskinfo = os.popen('netstat -ano | findstr 8089')

        line = taskinfo.readline()

        aList = line.split()

        taskinfo.close()
        if aList:
            if aList[4] != '0':
                data_dict = {
                    "code": 3,
                    "msg": "压测端口已被占用，是否解除占用",
                }
                return Response(data_dict, status=status.HTTP_200_OK)
    elif "linux" in sys.platform:
        url = "http://47.107.176.177:8089"
        taskinfo = os.popen('lsof -i:8089')

        line = taskinfo.readline()

        aList = line.split()

        taskinfo.close()
        if aList:
            if aList[0] != '0':
                data_dict = {
                    "code": 3,
                    "msg": "压测端口已被占用，是否解除占用",
                }
                return Response(data_dict, status=status.HTTP_200_OK)

    testcase_dir_path = os.path.join(settings.SUITES_DIR,
                                     datetime.strftime(datetime.now(), "%Y%m%d%H%M%S%f" + "_locust"))
    if not os.path.exists(testcase_dir_path):
        os.makedirs(testcase_dir_path)
    repeat_list = []
    for one_obj in testcase_objs:
        generate_locust_files(one_obj, env, testcase_dir_path, repeat_list)
    run_locust(data, testcase_dir_path)
    while True:
        try:
            r = requests.get(url)
            r.raise_for_status()
            if r.status_code == 200:
                break
        except Exception:
            print("连接无效")
    data_dict = {
        "code": 2,
        "url": url
    }
    return Response(data_dict, status=status.HTTP_200_OK)


def is_locust_noweb(data, env, testcase_objs):
    testcase_dir_path = os.path.join(settings.SUITES_DIR,
                                     datetime.strftime(datetime.now(), "%Y%m%d%H%M%S%f" + "_locust"))
    if not os.path.exists(testcase_dir_path):
        os.makedirs(testcase_dir_path)
    repeat_list = []
    for one_obj in testcase_objs:
        generate_locust_files(one_obj, env, testcase_dir_path, repeat_list)
    run_locust_noweb(testcase_dir_path, data)
    csv_paths = list()
    csv_paths.append(os.path.join(testcase_dir_path, data["name"] + "_failures.csv"))
    csv_paths.append(os.path.join(testcase_dir_path, data["name"] + "_stats.csv"))
    csv_paths.append(os.path.join(testcase_dir_path, data["name"] + "_stats_history.csv"))
    send_email_text(data["name"], "压测详情请查看附件", csv_paths, data["email"])
    data_dict = {
        "msg": "压测完成",
    }
    return Response(data_dict, status=status.HTTP_200_OK)


def run_locust(data, testcase_dir_path):
    cmd1 = "cd " + testcase_dir_path
    cmd2 = "locusts -f locust.yml {} --web-host=0.0.0.0".format("--step-load" if data.get("step_load") else "")
    cmd = cmd1 + " && " + cmd2
    subprocess.Popen(cmd, shell=True)


def run_locust_noweb(testcase_dir_path, data):
    cmd1 = "cd " + testcase_dir_path
    if data.get("step_load"):
        cmd2 = "locusts -f locust.yml --no-web -c {} -r {} -t {} --csv={}" \
               " --step-load --step-clients {} --step-time {} ".format(data["clients"], data["hatch_rate"],
                                                                       data["run_time"], data["name"],
                                                                       data["step_clients"], data["step_time"]
                                                                       )
    else:
        cmd2 = "locusts -f locust.yml --no-web -c {} -r {} -t {} --csv={}".format(data["clients"], data["hatch_rate"],
                                                                                  data["run_time"],
                                                                                  data["name"])
    cmd = cmd1 + " && " + cmd2
    locust = subprocess.Popen(cmd, shell=True)
    locust.wait()


def to_json_file(json_file, data):
    """
    写入json文件
    :param json_file:
    :param data:
    :return:
    """
    with io.open(json_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, separators=(',', ': '), ensure_ascii=False)


def to_file(file_name, data):
    """
    写入文件
    :param python_file:
    :param data:
    :return:
    """
    with io.open(file_name, 'w', encoding='utf-8') as f:
        if isinstance(data, (list, tuple)):
            """可以按行写入"""
            f.writelines(data)
            return None
        f.write(data)


def send_email_text(subject, content, filepath, receive_email):
    sender = ""
    passwd = ""
    receivers = receive_email  # 收件人邮箱

    msgRoot = MIMEMultipart()
    msgRoot['Subject'] = subject
    msgRoot['From'] = sender

    msgRoot['To'] = receivers if isinstance(receivers, str) else ','.join(receivers)  # 群发邮件
    part = MIMEText(content)
    msgRoot.attach(part)
    #
    # 添加附件部分
    if isinstance(filepath, str):
        file_name = filepath.split("\\")[-1]
        part = MIMEApplication(open(filepath, 'rb').read())
        part.add_header('Content-Disposition', 'attachment', filename=file_name)
        msgRoot.attach(part)
    else:
        for path in filepath:
            file_name = path.split("\\")[-1]
            part = MIMEApplication(open(path, 'rb').read())
            part.add_header('Content-Disposition', 'attachment', filename=file_name)
            msgRoot.attach(part)

    try:
        if "win" in sys.platform:
            s = smtplib.SMTP()
            s.connect("smtp.qq.com")
        elif "linux" in sys.platform:
            s = smtplib.SMTP_SSL("smtp.qq.com", 465)
        s.login(sender, passwd)
        s.sendmail(sender, receivers, msgRoot.as_string())
        print("邮件发送成功")
    except smtplib.SMTPException as e:
        print("发送失败", e)
    finally:
        s.quit()
