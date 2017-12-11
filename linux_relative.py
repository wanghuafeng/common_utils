#!-*- coding:utf-8 -*-
"""
CentOS查看系统信息

1：查看CPU
more /proc/cpuinfo | grep "model name"
grep "model name" /proc/cpuinfo
grep "model name" /proc/cpuinfo | cut -f2 -d:

2：查看内存
grep MemTotal /proc/meminfo
grep MemTotal /proc/meminfo | cut -f2 -d:
free -m |grep "Mem" | awk '{print $2}'

3：查看当前linux的版本
cat /proc/version
redhat:
    cat /etc/redhat-release

4:centos安装python3
sudo yum install -y epel-release
sudo yum install -y python34


5:ubuntu关闭防火墙:
ufw disable
开启防火墙
ufw enable

6、修改环境变量配置
add to ~/.bashrc
export PATH="$PATH:/usr/lib/"

7、inux下which、whereis、locate、find 命令的区别
which       查看可执行文件的位置
whereis    查看文件的位置
locate       配 合数据库查看文件位置
find          实际搜寻硬盘查询文件名称
"""