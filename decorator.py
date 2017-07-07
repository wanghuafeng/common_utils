#!-*- coding:utf-8 -*-
import time

def retries(times=3, timeout=1):
    """ 网络请求装饰器 """
    def decorator(func):
        def _wrapper(*args, **kw):
            att, retry = 0, 0
            while retry < times:
                retry += 1
                try:
                    return func(*args, **kw)
                except Exception as e:
                    att += timeout
                    time.sleep(att)

        return _wrapper

    return decorator

def empty_content_retries(times=3, timeout=2):
    """ 网络请求装饰器 """
    def decorator(func):
        def _wrapper(*args, **kw):
            att, retry = 0, 0
            while retry < times:
                retry += 1
                ret = func(*args, **kw)
                if ret:
                    return ret
                att += timeout
                time.sleep(att)
        return _wrapper
    return decorator
