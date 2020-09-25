# ApiTest

线上Demo：http://47.107.176.177/      
wangjiaqi     123456

# 前言
apitest是一个接口测试平台, 能帮助用户高效快捷地完成接口自动化用例的开发, 覆盖较为复杂的流程接口场景。该平台支持在线的用例编写及调试，并集成了Mock服务。可以根据测试计划自由的组合需要执行的测试用例，还可以直接使用接口测试用例完成压力测试，无需二次编写压测脚本。大大提高团队协作程度和测试效率，让测试的自动化程度得到了进一步的提升。

# 介绍
本平台基于Django restframework  + vue +  elementUI开发， 驱动框架使用httprunner、mocorunner、locusts

强烈建议使用平台前先了解httprunner的基本用法

# 平台特性
用例管理：按项目-模块-用例的层级管理，并可用过套件自由组合测试用例

编写用例：可以调用python函数处理请求/响应数据，支持参数化运行，可以在线调试，以树型展示接口响应数据，并可一键提取结果和断言

mock管理：mock数据按接口-场景的层级管理，均支持独立启/禁用

性能测试：可以直接使用接口测试用例进行性能测试，并支持无界面启动、逐步负载

测试报告：支持筛选/检索测试结果，简洁地展示任务情况

# 项目搭建
目录中apitest_vue为前端代码，其他为后端代码

后端运行：

配置完数据库后，cmd进入项目根目录

pip install -r requirements.txt

python manage.py makemigrations

python manage.py migrate 

python manage.py createsuperuser

python manage.py runserver 0.0.0.0:8000

前端运行：

安装VUE环境，下载node.js并配置环境，下载npm包管理器，cmd进入前端目录

npm install --global vue-cli

npm install

npm run dev

