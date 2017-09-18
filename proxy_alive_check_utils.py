#!-*- coding:utf-8 -*-
"""
代理存活检测工具
结合gevent指定并发数进行并发存活检测
仿Yii框架中的console application执行方式
"""
import os
import time
import codecs
import gevent
import requests
import json
import sys

import gevent.monkey

gevent.monkey.patch_socket()

from gevent import monkey

monkey.patch_ssl()

sys.path.append('..')

from model.proxyRequest import *

PATH = os.path.abspath(os.path.dirname(__file__))
proxy_pool_path = os.path.join(PATH, '../extention/proxy_pool')

defaule_timeout_limit = 2  # 默认代理超时时间
online_proxy_timeout = 5  # 公网代理超时时间

daxiang_service_name = 'daxiang'  # 大象代理service名称
asy_thread_count = 50  # 并发线程数
asy_check_sleep_interval = 10

alive_check_url = ProxyConfig.alive_check_url

def check_proxy(ip_port):
    '''待测代理IP的存活
    @:return
    {
        ip_port：
        resObj:
        time_consume:
    }'''
    result = {}
    ip_port = ip_port.strip()
    result['ip_port'] = ip_port
    st = time.time()
    try:
        proxy = {
            'http': ip_port,
            'https': ip_port
        }
        retObj = requests.get(alive_check_url, proxies=proxy, timeout=defaule_timeout_limit)
        result['resObj'] = retObj
    except:
        result['resObj'] = False
    result['time_consume'] = time.time() - st
    return result


def asy_proxy_list_check(ip_port_list):
    proxyobj_list = []
    if not ip_port_list:
        return proxyobj_list
    thread_count = len(ip_port_list)
    threads = []
    for i in range(thread_count):
        ip_port = ip_port_list[i]
        threads.append(gevent.spawn(check_proxy, ip_port))
    gevent.joinall(threads)
    for thread_ret in threads:
        proxyobj_list.append(thread_ret.value)
    return proxyobj_list


def check_common_proxy_pool():
    '''common proxy alive check'''
    redisModel = RedisBase()
    proxy_services_list = ['ali']

    # check proxy in redis
    for proxy_service in proxy_services_list:
        proxy_key = ProxyConfig.hermes_proxy_prefix + proxy_service
        proxies_set = redisModel.smembers(proxy_key)
        logger.info('proxy_service=%s\ttotal_alive_count=%s' % (proxy_service, len(proxies_set)))
        for proxy in proxies_set:
            proxies = {
                'http': proxy,
                'https': proxy
            }
            try:
                ret = requests.get(ProxyConfig.alive_check_url, proxies=proxies, timeout=defaule_timeout_limit)
                html_content = ret.content
                if ret.status_code != 200 or 'html' not in html_content:  # proxy dead
                    redisModel.srem(proxy_key, proxy)
                    logger.warn('common proxy pool redis check, failed, ip_port:%s' % proxy)
            except BaseException, e:
                redisModel.srem(proxy_key, proxy)
                logger.warn('common proxy pool redis check, failed, ip_port:%s' % proxy)

    # check proxies in proxy file
    if not os.path.isfile(proxy_pool_path):
        logger.error('file not exists:%s' % proxy_pool_path)
        return
    line_list = codecs.open(proxy_pool_path, encoding='utf-8').readlines()
    for line in line_list:
        line = line.strip()
        if line.startswith('#') or not line:
            continue
        proxy, service = line.split()
        proxies = {
            'http': proxy,
            'https': proxy
        }
        start_time = time.time()
        proxy_key = ProxyConfig.hermes_proxy_prefix + service
        try:
            ret = requests.get(ProxyConfig.alive_check_url, proxies=proxies, timeout=defaule_timeout_limit)
            time_consume = time.time() - start_time
            html_content = ret.content

            if ret.status_code == 200 and 'html' in html_content:
                redisModel.sadd(proxy_key, proxy)  # alive, add to proxy pool
                logger.info(
                    '%s proxy alive check, sucess, ip_port:%s, time_consume:%s' % (service, proxy, time_consume))
            else:
                redisModel.srem(proxy_key, proxy)  # dead, remove from proxy_pool
                logger.warn(
                    '%s proxy alive check, failed, ip_port:%s, time_consume:%s' % (service, proxy, time_consume))
        except:
            redisModel.srem(proxy_key, proxy)  # dead, remove from proxy_pool
            logger.warn('%s proxy alive check, failed, ip_port:%s' % (service, proxy))


def redis_proxy_alive_check(proxy_service):
    '''通用redis代理存活检测'''
    redisModel = RedisBase()
    proxy_key = ProxyConfig.hermes_proxy_prefix + proxy_service
    proxies_set = redisModel.smembers(proxy_key)
    proxy_list = list(proxies_set)

    partial_count = len(proxy_list) / asy_thread_count
    for i in range(partial_count + 1):
        partial_proxy_list = proxy_list[i * asy_thread_count: (i + 1) * asy_thread_count]
        proxyobj_list = asy_proxy_list_check(partial_proxy_list)
        time.sleep(asy_check_sleep_interval)
        for proxyobj in proxyobj_list:
            resobj = proxyobj.get('resObj')
            ip_port = proxyobj.get('ip_port')
            time_consume = proxyobj.get('time_consume')
            if resobj and resobj.status_code == 200:
                logger.info('%s redis alive check, sucess, ip_port:%s, time_consume:%s' %
                            (proxy_service, ip_port, time_consume))
            else:
                redisModel.srem(proxy_key, ip_port)
                logger.warn('%s redis alive check, failed, ip_port:%s, time_consume:%s' %
                            (proxy_service, ip_port, time_consume))


def daxiang_api_proxy_check():
    ''' check daxiang proxy alive status'''
    global defaule_timeout_limit, alive_check_url
    defaule_timeout_limit = 40
    alive_check_url = ProxyConfig.daxiang_proxy_public_alive_check_url
    redisModel = RedisBase()
    proxy_key = ProxyConfig.hermes_proxy_prefix + daxiang_service_name
    try:
        ip_port_lines = requests.get(ProxyConfig.daxiang_proxy_api_url, timeout=20).content
        if ip_port_lines.strip():
            ip_port_list = ip_port_lines.split('\n')
            partial_count = len(ip_port_list) / asy_thread_count
            for i in range(partial_count + 1):
                partial_proxy_list = ip_port_list[i * asy_thread_count: (i + 1) * asy_thread_count]
                proxyobj_list = asy_proxy_list_check(partial_proxy_list)
                time.sleep(asy_check_sleep_interval)
                for proxyobj in proxyobj_list:
                    resobj = proxyobj.get('resObj')
                    ip_port = proxyobj.get('ip_port')
                    time_consume = proxyobj.get('time_consume')
                    if resobj and resobj.status_code == 200:
                        redisModel.sadd(proxy_key, ip_port)
                        logger.info('%s proxy alive check, sucess, ip_port:%s, time_consume:%s' % (ProxyConfig.service_daxiang, ip_port, time_consume))
                    else:
                        logger.warn('%s proxy alive check, failed, ip_port:%s, time_consume:%s' % (ProxyConfig.service_daxiang, ip_port, time_consume))
                        redisModel.srem(proxy_key, ip_port)
            total_proxies = redisModel.smembers(proxy_key)
            logger.info('proxy_service=%s\ttotal_alive_count=%s' % (ProxyConfig.service_daxiang, len(total_proxies)))
    except BaseException, e:
        logger.warn(e)

def daxiang_redis_proxy_alive_check():
    '''大象代理池中代理存活检测'''
    global defaule_timeout_limit
    defaule_timeout_limit = ProxyConfig.public_net_timeout_interval
    ProxyConfig.alive_check_url = ProxyConfig.daxiang_proxy_public_alive_check_url
    redis_proxy_alive_check(daxiang_service_name)


def kuai_api_proxy_check():
    redisModel = RedisBase()
    proxy_key = ProxyConfig.hermes_proxy_prefix + ProxyConfig.service_kuai
    uncheck_proxy_list = []
    try:
        content = requests.get(ProxyConfig.kuai_proxy_api_url, timeout=20).content
        json_data = json.loads(content)
        if not json_data.get('list'):
            logger.warn('%s proxy api response null' % ProxyConfig.service_kuai)
            return
        for ip_port_dic in json_data.get('list'):
            proxy = '%(ip)s:%(port)s' % ip_port_dic
            uncheck_proxy_list.append(proxy)
    except BaseException, e:
        logger.warn('%s proxy net request timed out, err_msg:%s' % (ProxyConfig.service_kuai, e))
        return

    partial_count = len(uncheck_proxy_list) / asy_thread_count
    for i in range(partial_count + 1):
        partial_proxy_list = uncheck_proxy_list[i * asy_thread_count: (i + 1) * asy_thread_count]
        proxyobj_list = asy_proxy_list_check(partial_proxy_list)
        time.sleep(asy_check_sleep_interval)
        for proxyobj in proxyobj_list:
            resobj = proxyobj.get('resObj')
            ip_port = proxyobj.get('ip_port')
            time_consume = proxyobj.get('time_consume')
            if resobj and resobj.status_code == 200:
                redisModel.sadd(proxy_key, ip_port)
                logger.info('%s proxy alive check, sucess, ip_port:%s, time_consume:%s' % (
                ProxyConfig.service_kuai, ip_port, time_consume))
            else:
                redisModel.srem(proxy_key, ip_port)
                logger.warn('%s proxy alive check, failed, ip_port:%s, time_consume:%s' % (
                    ProxyConfig.service_kuai, ip_port, time_consume))
    total_proxies = redisModel.smembers(proxy_key)
    logger.info('proxy_service=%s\ttotal_alive_count=%s' % (ProxyConfig.service_kuai, len(total_proxies)))


def kuai_redis_proxy_check():
    redis_proxy_alive_check(ProxyConfig.service_kuai)


if __name__ == '__main__':
    args = sys.argv[1:]
    if len(args) < 1:
        print 'shell param error'
        sys.exit(1)
    funName = args[0].strip()
    eval('%s()' % funName)
