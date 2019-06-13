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


if __name__ == "__main__":
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

if __name__ == "__main__":
    m1 = Base()
    m2 = Base()
    print id(m1) == id(m2)


# ===============================================================================

class Singleton(type):    # 推荐使用 1
    def __init__(cls, name, bases, dict):
        super(Singleton, cls).__init__(name, bases, dict)
        cls._instance = None

    def __call__(cls, *args, **kw):
        if cls._instance is None:
            cls._instance = super(Singleton, cls).__call__(*args, **kw)

class Singleton(type):    # 推荐使用 2
    def __init__(self, *args, **kwargs):
        self.__instance = None
        super(Singleton,self).__init__(*args, **kwargs)

    def __call__(self, *args, **kwargs):
        if self.__instance is None:
            self.__instance = super(Singleton,self).__call__(*args, **kwargs)
        return self.__instance

# 使用方式:
class Mclass(object):
    __metaclass__ = Singleton    # 该种方式，__init__函数无论实例化多少次，最终该只执行一次
    def __init__(self):
        print '====='

mc = Mclass()
mc2 = Mclass()
print id(mc), id(mc2)

"""
输出:
    =====    (这里无论实例化，只打印一次)
    506046184 506046184
"""
# ------------------------------------------------------------------------------------------


class Singleton(object):
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            orig = super(Singleton, cls)
            cls._instance = orig.__new__(cls, *args, **kwargs)
        return cls._instance

# 使用方式:
class Mclass(Singleton):      # 该种方式，每次实例化__init__函数都会被执行
    def __init__(self):
        print '====='
mc = Mclass()
mc2 = Mclass()
print id(mc), id(mc2)
"""
输出:
    =====    (第一次实例化，打印)
    =====    (第二次实例化， 打印)
    61000056 61491856
"""