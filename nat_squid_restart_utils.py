#!-*- coding:utf-8 -*-
"""
远程重启squid
"""
import re
s = """121.201.14.61:9000   qing
121.201.29.165:9000 qing
"""
pattern = r'(?:\d{1,3}\.){3}\d{1,3}'
proxy_list =  re.findall(pattern, s)

restart_squid_command = "systemctl restart squid; ps aux | grep squid"      # 重启squid服务
restart_proxy_manager_command = 'service NetworkManager restart;  ps -aux | sort -k4nr | head -1;'   # 重启远程服务，查看内存占用top1进程
command = restart_proxy_manager_command
for ip_port in proxy_list:
    print 'ssh root@%s "%s"; sleep 2;' %(ip_port, command)



