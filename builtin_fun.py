#!-*- coding:utf-8 -*-
"""
整理一些比较好的内建函数实现
"""
def setdefault(k, d=None):
    """
    D.setdefault(k[,d]) -> D.get(k,d), also set D[k]=d if k not in D
    """
    dic = {}
    dic.setdefault('k', 'v')    # 如果dic中存在有k的键值，则返回dic['k']; 如果没有k键值，则赋值dic['d']='v',并返回'v'值
