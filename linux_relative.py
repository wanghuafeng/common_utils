#!-*- coding:utf-8 -*-
"""
CentOS查看系统信息

一：查看CPU
more /proc/cpuinfo | grep "model name"
grep "model name" /proc/cpuinfo
grep "model name" /proc/cpuinfo | cut -f2 -d:

二：查看内存
grep MemTotal /proc/meminfo
grep MemTotal /proc/meminfo | cut -f2 -d:
free -m |grep "Mem" | awk '{print $2}'

三：查看当前linux的版本
cat /proc/version
redhat:
    cat /etc/redhat-release

四:centos安装python3
sudo yum install -y epel-release
sudo yum install -y python34


五:ubuntu关闭防火墙:
ufw disable
开启防火墙
ufw enable

"""