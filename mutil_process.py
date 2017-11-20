# coding:utf-8
"""
多线程阻塞与非阻塞实现
网络请求时，用于断开请求端连接，后续逻辑继续执行
"""
import threading
import time
def thread_tst():
    def gen_thread():
        #方法一：将要执行的方法作为参数传给Thread的构造方法
        def action(arg):
            time.sleep(5)
            print 'the arg is:%s\r' %arg
        for i in xrange(4):
            t =threading.Thread(target=action,args=(i,))
            t.start()
        print 'main thread end!'

    def overload_parent():
        class MyThread(threading.Thread):
            def __init__(self,arg):
                super(MyThread, self).__init__()#注意：一定要显式的调用父类的初始化函数。
                self.arg=arg
            def run(self):#定义每个线程要运行的函数
                time.sleep(1)
                print 'the arg is:%s\r' % self.arg
        for i in xrange(4):
            t =MyThread(i)
            t.start()

        print 'main thread end!'

def deamon_tst():
    def deamon_false():
        '''主线程执行过程中，前台线程也在进行，主线程执行完毕后，等待前台线程也执行完成后，程序停止'''
        def action(arg):
            time.sleep(2)
            print  'sub thread start!the thread name is:%s\r' % threading.currentThread().getName()
            print 'the arg is:%s\r' % arg
            time.sleep(1)

        for i in xrange(50):
            t = threading.Thread(target=action, args=(i,))
            t.start()
        print 'main_thread end!'

    def deamon_true():
        '''主线程执行完毕后，后台线程不管是成功与否，主线程均停止'''
        def action(arg):
            time.sleep(1)
            print  'sub thread start!the thread name is:%s\r' % threading.currentThread().getName()
            print 'the arg is:%s\r' % arg
            time.sleep(1)
        thread_list = []
        for i in xrange(50):
            t = threading.Thread(target=action, args=(i,))
            t.daemon=True
            t.start()
            # thread_list.append(t)

        # for thread in thread_list:
        #     print thread.getName()
            # thread.join() # 调用json()阻塞至子进程结束
    st = time.time()
    # deamon_false()
    deamon_true()
    print time.time() - st
# deamon_tst()

"""
1、如果某个子线程的daemon属性为False，主线程结束时会检测该子线程是否结束，
   如果该子线程还在运行，则主线程会等待它完成后再退出；
2、如果某个子线程的daemon属性为True，主线程运行结束时不对这个子线程进行检查而直接退出，
   同时所有daemon值为True的子线程将随主线程一起结束，而不论是否运行完成。
   属性daemon的值默认为False，如果需要修改，必须在调用start()方法启动线程之前进行设置。
   另外要注意的是，上面的描述并不适用于IDLE环境中的交互模式或脚本运行模式，因为在该环境中的主线程只有在退出Python IDLE时才终止。
"""

import time
import threading

def fun():
    print "start fun"
    # time.sleep(2)
    print "end fun"
    return 'aaaaaa'

print "main thread"
t1 = threading.Thread(target=fun,args=())
t1.setDaemon(True)
t1.start()
t1.join()

# time.sleep(1)
# print "main thread end"
