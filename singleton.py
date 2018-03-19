#!-*- coding:utf-8 -*-
"""
单例
"""
class Singleton(type):
    def __init__(cls, name, bases, dict):
        super(Singleton, cls).__init__(name, bases, dict)
        cls._instance = None
    def __call__(cls, *args, **kw):
        if cls._instance is None:
            cls._instance = super(Singleton, cls).__call__(*args, **kw)
        return cls._instance

class MyClass(object):
    __metaclass__ = Singleton

if __name__ == "__main__":
    c = MyClass()
    c1 = MyClass()
    print c is c1
    assert id(c) == id(c1)