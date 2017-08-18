# -*- coding: utf-8 -*-
__author__ = 'huafeng'
import sys, os, re, time
import gevent
import requests
import gevent.monkey
gevent.monkey.patch_socket()

TIMEOUT = 1
total_time = 0

"""
使用gevent进行压力测试
指定thread_count并发数
"""

def check_proxy_ip(ip=''):
    global  total_time
    try:
        url = 'http://192.168.4.151:5100/getProxy'
        post_data = {
            'ip_group':'common',
            'count':1
        }
        st = time.time()
        content = requests.post(url,data=post_data, timeout=TIMEOUT).content
        interval =  time.time()- st
        total_time += interval
        return content
    except:
        return False

def proxy_check():
    proxies = {
        'all':'60.187.108.9:47586',
    }
    url = 'https://www.sogou.com/web?query=1879875360'
    try:
        return requests.get(url, proxies=proxies, timeout=5)
    except BaseException, e:
        print e
        return False


# proxy_check()
# exit()

def asy_gevent_run(thread_count):
    threads = []
    for i in range(thread_count):
        # threads.append(gevent.spawn(check_proxy_ip, ''))
        threads.append(gevent.spawn(proxy_check))
    gevent.joinall(threads)
    for thread_ret in threads:
        print thread_ret.value.status_code
    print 'total fail count:%s' % len([item for item in threads if not item.value])

if __name__ == '__main__':
    thread_count = 10
    asy_gevent_run(thread_count)
    print 'average time consume:%s' % (total_time/float(thread_count))

