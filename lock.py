# -*- coding: utf-8 -*-
__author__ = 'huafeng'
import time
import gevent
import random
import gevent.monkey
import threading
# gevent.monkey.patch_socket()
gevent.monkey.patch_all()

lock = threading.Lock()

class LockTst(object):
    cnt = 0

    @classmethod
    def random_sleep(cls):
        time.sleep(random.random())
        lock.acquire()
        cls.cnt += 1
        # print Tst.cnt
        lock.release()
        return cls.cnt


def asy_gevent_run(thread_count):
    threads = []
    for i in range(thread_count):
        threads.append(gevent.spawn(LockTst.random_sleep))
    gevent.joinall(threads)
    for thread_ret in threads:
        print thread_ret.value

if __name__ == '__main__':
    thread_count = 100
    asy_gevent_run(thread_count)

