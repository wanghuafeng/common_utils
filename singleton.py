#!-*- coding:utf-8 -*-
# 使用原类
class Singleton(type):
    def __init__(cls, name, bases, dict):
        super(Singleton, cls).__init__(name, bases, dict)
        cls._instance = None
    def __call__(cls, *args):
        if cls._instance is None:
            cls._instance = super(Singleton, cls).__call__(*args)
        return cls._instance

class Base():
    __metaclass__ = Singleton

m1 = Base()
m2 = Base()
print id(m1) == id(m2)


# 装饰器方法实现
def singleton(cls, *args, **kw):
    instances = {}
    def _singleton():
        if cls not in instances:
            instances[cls] = cls(*args, **kw)
        return instances[cls]
    return _singleton

@singleton
class Base():
    pass

m1 = Base()
m2 = Base()
print id(m1) == id(m2)
