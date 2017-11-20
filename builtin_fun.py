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

def update(E=None, **F): # known special case of dict.update
    """
    D.update(E, **F) -> None.  Update D from dict/iterable E and F.
    If E has a .keys() method, does:     for k in E: D[k] = E[k]
    If E lacks .keys() method, does:     for (k, v) in E: D[k] = v
    In either case, this is followed by: for k in F: D[k] = F[k]
    """
    pass