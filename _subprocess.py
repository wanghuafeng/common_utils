#!-*- coding:utf-8 -*-
__author__ = 'huafeng'

import os
import time
import subprocess


"""
*************************************************************
多个子进程连在一起，构成管道 （Popen对象创建以后并不会等待子进程运行结束再继续执行，此时如果要保证管道间通讯正常（即c2完全获取c1的stdout）必须手动调用wait()方法，是其以阻塞方式运行）

c1 = subprocess.Popen('ls -l', stdout=subprocess.PIPE, shell=True)
c1.wait()#此处保证在c1运行结束以后才开始执行c2
c2 = subprocess.Popen('wc', stdin=c1.stdout, stdout=subprocess.PIPE, shell=True)#c1的输出作为c2的输入执行'wc'操作
print c2.stdout.readline()

******************************************
standard USAGE:
     returncode = subprocess.call(command, shell=True)#0 if sucessed else 1

call(*popenargs, **kwargs)封装了Popen(*popenargs, **kwargs)并加入了wait()操作
即：call(*popenargs, **kwargs) == Popen(*popenargs, **kwargs).wait()
******************************************
stdin:          若为PIPE，则该属性为句柄，供子进程使用，作为子进程的输入
    If the stdin argument is PIPE, this attribute is a file object
    that provides input to the child process.  Otherwise, it is None.

stdout：     若为PIPE，则该属性为句柄，获取子进程输出，通过popen.stdout.read()读取正确输出
    If the stdout argument is PIPE, this attribute is a file object
    that provides output from the child process.  Otherwise, it is
    None.

stderr：     若为PIPE，则该属性为句柄，获取子进程输出，通过popen.stderr.read()读取错误信息
    If the stderr argument is PIPE, this attribute is file object that
    provides error output from the child process.  Otherwise, it is
    None.
popen = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
print popen.stdout.readl()#打印popen的标准输出
popen = subprocess.Popen(command, stderr=subprocess.PIPE, shell=True)#（若把stderr设置为subprocess.STDOUT，则会将标准信息与错误信息一起作为stdout输出）
print popen.stderr.readl()#打印popen的错误信息
此处popen.stdout，popen.stderr皆为句柄（只读）
# Parent                   Child
# ------                   -----
# p2cwrite   ---stdin--->  p2cread
# c2pread    <--stdout---  c2pwrite
# errread    <--stderr---  errwrite
#
另：
     fileObj = open('info.out', 'w')
     popen = subprocess.Popen(command, stdout=fileObj, shell=True)#此处将stdout标准输出写入到info.out文件中（stderr同理），
     但是无法在这里设置编码方式，fileObj= codecs.open('info.out', mode='w', encoding='utf-8') popen写入的编码方式依旧是ASCII

"""

PATH = os.path.dirname(os.path.abspath(__file__))

def call_shell():
    command = 'ls *.py'
    popen = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    all_spiders_list = popen.stdout.readlines()
    for spider in [item for item in all_spiders_list if item !='execute_all_spiders.py\n']:
        print 'python %s'%spider.strip()
        os.system('python %s'%spider.strip())
    mv_and_update_db_filename = os.path.join(os.path.dirname(PATH), 'mv_json_file.py')
    os.system('python %s'%mv_and_update_db_filename)
if __name__ ==  '__main__':
    call_shell()

