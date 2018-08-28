#!-*- coding:utf-8 -*-
import time


def retries(times=3, timeout=1):
    """对未捕获异常进行重试"""
    def decorator(func):
        def _wrapper(*args, **kw):
            att, retry = 0, 0
            while retry < times:
                retry += 1
                try:
                    return func(*args, **kw)
                except:
                    att += timeout
                    if retry < times:
                        time.sleep(att)
        return _wrapper
    return decorator


def empty_content_retries(times=3, timeout=2):
    """响应为空的进行重试"""
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


def use_logging(level):
    """带参数的装饰器"""
    def decorator(func):
        print func.__name__
        def wrapper(*args, **kwargs):
            if level == "warn":
                print ("level:%s, %s is running" % (level, func.__name__))
            elif level == "info":
                print ("level:%s, %s is running" % (level, func.__name__))
            return func(*args, **kwargs)
        return wrapper
    return decorator

if __name__ == "__main__":
    @use_logging(level="warn")
    def foo(name='foo'):
        print("i am %s" % name)
    foo()