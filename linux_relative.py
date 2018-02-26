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
（1）/etc/profile
全局（公有）配置，不管是哪个用户，登录时都会读取该文件。

（2）/ect/bashrc
Ubuntu没有此文件，与之对应的是/ect/bash.bashrc
它也是全局（公有）的
bash执行时，不管是何种方式，都会读取此文件。

（3）~/.profile
若bash是以login方式执行时，读取~/.bash_profile，若它不存在，则读取~/.bash_login，若前两者不存在，读取~/.profile。
另外，图形模式登录时，此文件将被读取，即使存在~/.bash_profile和~/.bash_login。

（4）~/.bash_login
若bash是以login方式执行时，读取~/.bash_profile，若它不存在，则读取~/.bash_login，若前两者不存在，读取~/.profile。

（5）~/.bash_profile
Unbutu默认没有此文件，可新建。
只有bash是以login形式执行时，才会读取此文件。通常该配置文件还会配置成去读取~/.bashrc。

（6）~/.bashrc
当bash是以non-login形式执行时，读取此文件。若是以login形式执行，则不会读取此文件。

（7）~/.bash_logout
注销时，且是longin形式，此文件才会读取。也就是说，在文本模式注销时，此文件会被读取，图形模式注销时，此文件不会被读取。

下面是在本机的几个例子：
1. 图形模式登录时，顺序读取：/etc/profile和~/.profile
2. 图形模式登录后，打开终端时，顺序读取：/etc/bash.bashrc和~/.bashrc
3. 文本模式登录时，顺序读取：/etc/bash.bashrc，/etc/profile和~/.bash_profile
4. 从其它用户su到该用户，则分两种情况：
（1）如果带-l参数（或-参数，--login参数），如：su -l username，则bash是lonin的，它将顺序读取以下配置文件：/etc/bash.bashrc，/etc/profile和~/.bash_profile。
（2）如果没有带-l参数，则bash是non-login的，它将顺序读取：/etc/bash.bashrc和~/.bashrc
5. 注销时，或退出su登录的用户，如果是longin方式，那么bash会读取：~/.bash_logout
6. 执行自定义的shell文件时，若使用“bash -l a.sh”的方式，则bash会读取行：/etc/profile和~/.bash_profile，若使用其它方式，如：bash a.sh， ./a.sh，sh a.sh（这个不属于bash shell），则不会读取上面的任何文件。
7. 上面的例子凡是读取到~/.bash_profile的，若该文件不存在，则读取~/.bash_login，若前两者不存在，读取~/.profile。
"""
