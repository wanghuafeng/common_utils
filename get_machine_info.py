#!-*- coding:utf-8 -*-
import socket
import getpass
"""
获取机器参数的一些函数
"""
MACHINE_NAME = socket.getfqdn(socket.gethostname())
USER_NAME = getpass.getuser()
