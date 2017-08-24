#!-*- coding:utf-8 -*-
import socket
import getpass

"""
获取机器参数的一些函数
"""

MACHINE_NAME = socket.getfqdn(socket.gethostname())
username = getpass.getuser()   # 获取用户名

hostname = socket.gethostname()  # 计算机名称, MS-20170412UOGQ
ip_addr = socket.gethostbyname(hostname)    # 内网IP地址 192.168.1.82
host_ip = socket.gethostbyname('localhost')  # 127.0.0.1

class Server(object):
    def __init__(self,host,port):
        self._host = host
        self._port = port
    def __enter__(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
        sock.bind((self._host,self._port))
        sock.listen(10)
        self._sock = sock
        return self._sock
    def __exit__(self,*exc_info):
        if exc_info[0]:
            import traceback
            traceback.print_exception(*exc_info)
        self._sock.close()

if __name__ == '__main__':
    host = 'localhost'
    port = 5566
    with Server(host,5566) as s:
        while True:
            conn, addr = s.accept()
            msg = conn.recv(1024)
            conn.send(msg)
            conn.close()
