#!-*- coding:utf-8 -*-
import requests

"""
封装常用requests的一些方法
"""
session_obj = requests.Session()
url = 'http://www.baidu.com'


class CookiesOpt(object):

    def cookie_opt(self):
        """cookie的相关操作"""
        session_obj.cookies.set('key', None)  # 清楚cookie中为key的值
        session_obj.cookies.set('k', 'v')  # 重置cookie值
        session_obj.cookies.get_dict()  # 取当前session的所有cookie值
        session_obj.cookies.get('k')  # 获取指定k的cookie值

    def specify_cookies(self):
        """指定cookie值的请求"""
        cookies = {
            'key1': 'val1',
            'key2': 'val2'
        }
        session_obj.get(url, cookies=cookies)
