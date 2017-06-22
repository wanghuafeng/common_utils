#!-*- coding:utf-8 -*-
try:
    import cPickle as pickle
except ImportError:
    import pickle

"""
抓取过程中,如需调试N多步骤中的某一步进行调试而不是每次都从新走一遍流程，
可以将session对象持久化到本地,
然后,使用该持久化对象进行调试
"""

def save_obj(obj, filename):
    pickle.dump(obj, open(filename, "w"))

def get_obj(filename):
    return pickle.load(open(filename))
