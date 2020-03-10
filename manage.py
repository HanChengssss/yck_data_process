# !/usr/bin/env python
# -*-encoding: utf-8-*-
# author:LiYanwei
# version:0.1
from multiprocessing import Process, Pool, Queue
import os, time, random
from yck_data_process.process.auto_model_process import *
from yck_data_process.input_data import *
from yck_data_process.settings import *
from yck_data_process.output_data import *
from functools import wraps


class ManageBase():
    '''
    加载各个模块
    队列1：input 读取来自mysql的数据
    消费者1：从队列1获取数据，处理，输出队列2
    队列2：接收来自消费者1的数据
    消费这2:接收来自队列2的数据，输出到mysql
    调度各个模块

    '''

    def __init__(self):
        pass

    def run(self):

        pass


class TestManage(ManageBase):

    def __init__(self):
        super().__init__()
        '''
        初始化各个模块和创建共享队列
        '''
        self.inputQueue = Queue()
        self.outputQueue = Queue()
        self.g = GetTestMysqlData()
        self.p = ProcessManage()
        self.o = OutPutMysql()

    def create_query(self):
        return Queue()

    def long_time_task(self, name):
        print('Run task %s (%s)...' % (name, os.getpid()))
        start = time.time()
        time.sleep(random.random() * 3)
        end = time.time()
        print("Task %s runs %0.2f seconds" % (name, (end - start)))


    def run(self):
        p1 = Process(target=self.g.put_data_to_query, args=(auto_model_tables, dbparams, "model_year", True, self.inputQueue,))
        r1 = Process(target=self.p.process_data, args=(self.inputQueue, self.outputQueue,))
        r2 = Process(target=self.o.data_output, args=(self.outputQueue,))
        p1.start()
        r1.start()
        r2.start()
        p1.join()
        r1.join()
        r2.join()
        # r3.terminate()


def fn_timer(function):
    @wraps(function)
    def function_timer(*args, **kwargs):
        t0 = time.time()
        result = function(*args, **kwargs)
        t1 = time.time()
        print("Total time running %s: %s seconds" %
              ("text_foo", str(t1 - t0))
              )
        return result

    return function_timer


@fn_timer
def run():
    t = TestManage()
    t.run()


if __name__ == '__main__':
    run()
    # t.run()
    # p = Pool(4)
    # # p.apply_async(self.i.run)
    # for i in range(4):
    #     func = TestManage().long_time_task
    #     p.apply(func, args=(i,))
    # print("Waiting for all subprocess done...")
    # p.close()
    # p.join()
    # print("All subprocess done.")
    # 需要序列化示例方法
    # mc = MyClass()
    # t1 = pickle.dumps(t.long_time_task)
    # pool = Pool(processes=3)
    # pool.apply_async(t1, (3,))
    # pool.apply_async(t1, (4,))
    # pool.apply_async(t1, (5,))
    # pool.close()
    # pool.join()

'''
问题1：cannot serialize _io.BufferedReader object
原因：将不可序列化的对象传到进程中导致，根本原因进程间无法共享数据。
https://blog.csdn.net/chenyulancn/article/details/8013054
解决方式：每个方法各自使用参数，不依类的实例变量
问题2：穿入方法中队列需要将队列里的数据，完全消费完才会退出。
问题3：p1.join方法是等待，只有等待这个进程结束了，父进程才会退出。
问题4：经过测试，使用一个成产队列，多个消费进程，运行速度被没有明显的提升，猜测，某个消费进程在获取元素时，令一个进程处于等待中，并不能同时获取下一个元素。且每个进程处理元素的速度很快，所以看起来并没有明显的提升。
问题5：局部变量的作用域问题，当一个变量被当作参数传入函数内部时，这个变量对内存引用是否会发生改变。
'''








