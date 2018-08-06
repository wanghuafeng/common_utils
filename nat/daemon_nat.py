# -*- coding: utf-8 -*-

import os
import re
import json
import time
import codecs
import urllib2
import subprocess

ssh_command = 'ps aux | grep ssh'
thread_no_pattern = r'\d+'
nat_ssh_thread_pattern = r'\s\d+:127\.0\.0\.1:\d+\s'
thread_kill_command = 'kill -9 %s'

ssh_nat_command = r'ssh -f -NR %(server_port)s:127.0.0.1:%(proxy_port)s %(server_login_name)s@%(server_name)s'
squid_restart_command = 'sudo service squid3 restart'

PATH = os.path.dirname(os.path.abspath(__file__))
conf_file_path = os.path.join(PATH, 'nat.conf') #配置文件

proxy_alive_check_url = ''

conf_dic=dict([line.strip().split(':') for line in codecs.open(conf_file_path, encoding='utf-8').readlines() if not line.startswith('#') and  line.strip()])

# def ip_upload():

def get_ssh_thread_list():
    '''获取ssh进程'''
    popen = subprocess.Popen(ssh_command, stdout=subprocess.PIPE, shell=True)
    thread_line_list = popen.stdout.readlines()
    ssh_threads_list = []
    for thread_str in thread_line_list:
        if re.search(nat_ssh_thread_pattern, thread_str):
            ssh_threads_list.append(thread_str)
    return ssh_threads_list

def get_thread_no(thread_str):
    '''获取进程号'''
    match = re.search(thread_no_pattern, thread_str)
    if match:
        return match.group()
    else:
        print 'thread_no_pattern:%s, get thread no failed...'

def kill_ssh_exists_tunnel():
    '''杀死所有当前nat不可用进程'''
    ssh_threads_list = get_ssh_thread_list()
    for thread_str in ssh_threads_list:
        thread_no = get_thread_no(thread_str)
        kill_command = thread_kill_command % thread_no
        print kill_command
        subprocess.call(kill_command, shell=True)

def create_nat_ssh_tunnel():
    '''生成新的穿透通道'''
    # conf_dic=dict([line.strip().split(':') for line in codecs.open(conf_file_path, encoding='utf-8').readlines() if not line.startswith('#') and  line.strip()])
    nat_create_command = ssh_nat_command%(conf_dic)
    subprocess.call(nat_create_command, shell=True)

def restart_squid():
    '''重启squid服务'''
    subprocess.call(squid_restart_command, shell=True)

def check_tunnel_exists():
    '''检测通道是否存在'''
    popen = subprocess.Popen(ssh_command, stdout=subprocess.PIPE, shell=True)
    threads_str = popen.stdout.read()
    if re.search(nat_ssh_thread_pattern, threads_str):
        print 'nat tunnel exists...'
        return True
    else:
        print 'nat tunnel not exists...'
        return False
def proxy_alive_check():
    '''检测代理是否存活'''
    alive_check_url = proxy_alive_check_url % conf_dic['server_port']
    content = urllib2.urlopen(alive_check_url, timeout=30).read()
    try:
        json_data = json.loads(content)
        return json_data.get('is_alive')
    except:
        return False

def main():
    '''若通道不存在，新建通道；若通道存在，重启服务，新建连接通道'''
    if check_tunnel_exists():
        restart_squid()
        kill_ssh_exists_tunnel()
        create_nat_ssh_tunnel()
    else:
        kill_ssh_exists_tunnel() #防止检测有误
        create_nat_ssh_tunnel()
if __name__ == '__main__':
    current = time.strftime('%Y-%m-%d %H:%M:%S')
    is_proxy_alive = proxy_alive_check() 
    if not is_proxy_alive:
        print '%s proxy dead, restart now...'%current
        main()
    else:
        print '%s proxy work normal...' %current
