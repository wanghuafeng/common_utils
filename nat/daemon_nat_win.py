# -*- coding: utf-8 -*-

import os
import re 
import sys
import json
import time
import codecs
import urllib2
import logging

kill_ssh_command = 'taskkill /F /IM ssh.exe'
ssh_nat_command = r'ssh -f -NR %(server_port)s:127.0.0.1:%(proxy_port)s %(server_login_name)s@%(server_name)s'

PATH = os.path.dirname(sys.argv[0])

conf_file_path = os.path.join(PATH, 'nat.conf') #配置文件

proxy_alive_check_url = ''
conf_dic=dict([line.strip().split(':') for line in codecs.open(conf_file_path, encoding='utf-8').readlines() if not line.startswith('#') and  line.strip()])

logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename=os.path.join(PATH, 'nat.log'),
                filemode='a')

def create_nat_ssh_tunnel():
    '''生成新的穿透通道'''
    nat_create_command = ssh_nat_command%(conf_dic)
    print nat_create_command
    os.system(nat_create_command)

def proxy_alive_check():
    '''检测代理是否存活'''
    alive_check_url = proxy_alive_check_url % conf_dic['server_port']
    content = urllib2.urlopen(alive_check_url, timeout=30).read()
    try:
        json_data = json.loads(content)
        return json_data.get('is_alive')
    except:
        return False
def kill_all_ssh_threads():
    '''杀掉所有当前运行的ssh进程'''
    os.system(kill_ssh_command)

def main():
    '''杀掉所有当前运行的ssh进程, 生成新的穿透通道'''
    kill_all_ssh_threads()
    create_nat_ssh_tunnel()

if __name__ == '__main__':
    current = time.strftime('%Y-%m-%d %H:%M:%S')
    is_proxy_alive = proxy_alive_check()
    if not is_proxy_alive:
        print '%s proxy dead, restart now...'%current
        logging.info('proxy dead, restart now...')
        main()
    else:
        print '%s proxy work normal...' %current
        logging.info('proxy work normal...')
        
