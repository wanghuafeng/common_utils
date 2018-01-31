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

关于ubuntu开机启动相关
1、/etc/profile:在登录时,操作系统定制用户环境时使用的第一个文件,此文件为系统的每个用户设置环境信息,当用户第一次登录时,该文件被执行。
2、/etc/environment:在登录时操作系统使用的第二个文件,系统在读取你自己的profile前,设置环境文件的环境变量。
3、~/.bash_profile:在登录时用到的第三个文件是.bash_profile文件,每个用户都可使用该文件输入专用于自己使用的shell信息,当用户登录时,该文件仅仅执行一次!默认情况下,他设置一些环境变量,执行用户的.bashrc文件。/etc/bash.bashrc:为每一个运行bash shell的用户执行此文件，当bash shell被打开时，该文件被读取。
4、~/.bashrc:该文件包含专用于你的bash shell的bash信息,当登录时以及每次打开新的shell时,该该文件被读取。
几个文件的优先级:1>2>3
在linux下，如果是bash环境，用户登录时读取设置文件的顺序是/etc/profile －－> ~/.bash_profile －－> ~/.bashrc －－> /etc/bash.bashrc。注意在~/.bash_profile这一步，如果没有~/.bash_profile ，则默认读取~/.bash_login，如果没有~/.bash_login 才读取~/.profile。
根据发行版本的情况，有两个基本的系统级配置文件：/etc/bash.bashrc和/etc/profile。这些配置文件包含两组不同的变量：shell变量和环境变量。前者只是在特定的shell中固定（如bash），后者在不同shell中固定。shell变量是局部的，而环境变量是全局的。
注意：尽量避免修改root用户的环境变量配置文件，因为那样可能会造成潜在的危险。最好不要把当前路径”./”放到PATH里，这样可能会受到意想不到的攻击。
使用：
把设置的环境变量给所有用户使用：/etc/bashrc；/etc/profile
修改全局的环境变量在/etc/profile
修改某个用户的环境变量在/home/用户名/.bash_profile
"""
