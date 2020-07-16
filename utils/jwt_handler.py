# -*- coding: utf-8 -*-
"""
-------------------------------------------------
  @Time : 2020/1/9 20:38 
  @Auth : 可优
  @File : jwt_handler.py
  @IDE  : PyCharm
  @Motto: ABC(Always Be Coding)
  @Email: keyou100@qq.com
  @Company: 湖南省零檬信息技术有限公司
  @Copyright: 柠檬班
-------------------------------------------------
"""


def jwt_response_payload_handler(token, user=None, request=None):
    """
    对返回的数据进行重写
    添加用户的信息
    :param token:
    :param user:
    :param request:
    :return:
    """
    return {
        'token': token,
        'user_id': user.id,
        'username': user.username
    }

