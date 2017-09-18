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
cat /etc/redhat-release

"""