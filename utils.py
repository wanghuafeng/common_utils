#!-*- coding:utf-8 -*-
__author__= 'huafeng'

import re
from urlparse import urlparse
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
        kv_tuple = tuple(re.split("\s*%s\s*"%split_by, kv_param.strip(), 1))
        formate_header_kv_list.append('"%s":"%s",' % kv_tuple)
    return """{\n%s\n}""" % "\n".join(formate_header_kv_list)

def select_proxy(url, proxies):
    """Select a proxy for the url, if applicable.

    :param url: The url being for the request
    :param proxies: A dictionary of schemes or schemes and hosts to proxy URLs
    """
    proxies = proxies or {}
    urlparts = urlparse(url)
    if urlparts.hostname is None:
        return proxies.get(urlparts.scheme, proxies.get('all'))

    proxy_keys = [
        urlparts.scheme + '://' + urlparts.hostname,
        urlparts.scheme,
        'all://' + urlparts.hostname,
        'all',
    ]
    proxy = None
    for proxy_key in proxy_keys:
        if proxy_key in proxies:
            proxy = proxies[proxy_key]
            break
    return proxy

def b64tohex(b64_str):
    """base64编码转化为16进制"""
    import binascii
    import base64
    b64_decode_str = base64.b64decode(b64_str)
    hex_str = binascii.b2a_hex(b64_decode_str) #b64_decode_str.encode('hex')
    return hex_str