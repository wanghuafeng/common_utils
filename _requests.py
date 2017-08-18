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


class ProxiesOpt(object):

    @property
    def proxies(self):
        """
        http参数设置及使用方式
        """
        proxies = { # http/https设置同样代理
            'all': '60.187.108.9:47586',
        }
        http_proxy = {
            'http': '60.187.108.9:47586',  # http://60.187.108.9:47586
        }
        https_proxy = {
            'https': '60.187.108.9:47586',  # http://60.187.108.9:47586
        }
        return proxies

    def use_proxy(self):
        requests.get(url, proxies=self.proxies)

class RequestsOpt(object):
    def _get(self):
        """
        get请求, 请求默认参数字段名称:params，
        网络请求时，params中的参数将会以query string 形式传输
        服务端的http server可以打印出以该方式传输的参数
        """
        params = {
            'k': 'v'
        }
        requests.get(url, params=params)

    def _post(self):
        """
        post请求，请求默认参数字段名称:data
        网络请求时，data中的参数将会被放在 body 中传输
        服务端http server不做特殊截获无法打印该部分参数
        """
        data = {
            'k': 'v'
        }
        requests.post(url, data=data)