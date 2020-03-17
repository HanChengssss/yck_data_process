# !/usr/bin/env python
# -*-encoding: utf-8-*-
# author:LiYanwei
# version:0.1
from multiprocessing import Process, Pool, Queue
# from queue import Queue
import os, time, random
from yck_data_process.process.auto_model_process import *
from yck_data_process.input_data import *
from yck_data_process.settings import *
from yck_data_process.output_data import *
from functools import wraps
from test6 import randomProdictData

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


    def create_query(self):
        return Queue()

    # def create_consumer(self, inputQueue, outputQueue):
    #     # 创建processData对象
    #     self.processData = ProcessManage()
    #     # 创建outputData对象
    #     self.outputData = OutPutDataManage()
    #     self.processData.process_data(inputQueue, outputQueue)
    #     self.outputData.dataOutput(outputQueue, 'autoModelCollection')



    def run_from_muiltiprocess(self):
        '''
        创建生产和消费队列
        往队列中装入待处理的数据
        开启处理进程和存储进程
        :return:
        '''
        inputQueue = self.create_query()
        outputQueue = self.create_query()
        self.inputData = InputDataMange()
        self.inputData.run(inputQueue)
        self.outputData = OutPutDataManage()
        p1 = Process(target=ProcessManage.process_data, args=(inputQueue, outputQueue))
        r1 = Process(target=self.outputData.dataOutput, args=(outputQueue, 'autoModelCollection'))
        p1.start()
        r1.start()
        p1.join()
        r1.join()


    def run_from_single_thread(self):
        pass

    def run_from_threading(self):
        pass


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


@fn_timer
def run_from_single_process():
    t = TestManage()
    t.run_from_single_thread()


@fn_timer
def run_from_muiltiprocess():
    t = TestManage()
    t.run_from_muiltiprocess()


@fn_timer
def run_from_threading():
    t = TestManage()
    t.run_from_threading()


if __name__ == '__main__':
    # run()
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
    # run_from_single_process()
    # run_from_muiltiprocess()
    run_from_muiltiprocess()
# '''
# 问题1：cannot serialize _io.BufferedReader object
# 原因：将不可序列化的对象传到进程中导致，根本原因进程间无法共享数据。
# https://blog.csdn.net/chenyulancn/article/details/8013054
# 解决方式：每个方法各自使用参数，不依类的实例变量
# 问题2：穿入方法中队列需要将队列里的数据，完全消费完才会退出。
# 问题3：p1.join方法是等待，只有等待这个进程结束了，父进程才会退出。
# 问题4：经过测试，使用一个成产队列，多个消费进程，运行速度被没有明显的提升，猜测，某个消费进程在获取元素时，令一个进程处于等待中，并不能同时获取下一个元素。且每个进程处理元素的速度很快，所以看起来并没有明显的提升。
# 问题5：局部变量的作用域问题，当一个变量被当作参数传入函数内部时，这个变量对内存引用是否会发生改变。
# '''








