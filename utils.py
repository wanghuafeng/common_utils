#!-*- coding:utf-8 -*-
__author__= 'huafeng'

import re
import sys
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

ip_pattern = r'((?:\d{1,3}\.){3}\d{1,3}\:\d+)'

def import_string(import_name, silent=False):
    """Imports an object based on a string.  This is useful if you want to
    use import paths as endpoints or something similar.  An import path can
    be specified either in dotted notation (``xml.sax.saxutils.escape``)
    or with a colon as object delimiter (``xml.sax.saxutils:escape``).

    If `silent` is True the return value will be `None` if the import fails.

    :param import_name: the dotted name for the object to import.
    :param silent: if set to `True` import errors are ignored and
                   `None` is returned instead.
    :return: imported object
    """
    # force the import name to automatically convert to strings
    # __import__ is not able to handle unicode strings in the fromlist
    # if the module is a package
    import_name = str(import_name).replace(':', '.')
    try:
        try:
            __import__(import_name)
        except ImportError:
            if '.' not in import_name:
                raise
        else:
            return sys.modules[import_name]

        module_name, obj_name = import_name.rsplit('.', 1)
        try:
            module = __import__(module_name, None, None, [obj_name])
        except ImportError:
            # support importing modules not yet set up by the parent module
            # (or package for that matter)
            module = import_string(module_name)

        try:
            return getattr(module, obj_name)
        except AttributeError as e:
            raise ImportError(e)

    except ImportError as e:
        if not silent:
            raise
