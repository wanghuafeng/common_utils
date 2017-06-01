#!-*- coding:utf-8 -*-
__author__= 'huafeng'

import re
def format_str(unformat_str, split_by=":"):
    """
    :arg
        unformat_str:待格式化字符串，一般为Request Header或者Post Parameters
        split_by: key,value切割符
    :return
        字典格式的参数
    格式化"""
    header_kv_param_list = unformat_str.split("\n")
    formate_header_kv_list = []
    for kv_param in header_kv_param_list:
        if not re.search('%s'%split_by, kv_param) or not kv_param:
            # print 'split_by:"%s"不存在, kv_param:%s' % (split_by, kv_param)
            continue
        kv_tuple = tuple(re.split("\s*%s\s*"%split_by, kv_param, 1))
        formate_header_kv_list.append('"%s":"%s",' % kv_tuple)
    return """{\n%s\n}""" % "\n".join(formate_header_kv_list)
