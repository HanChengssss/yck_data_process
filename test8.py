from yck_data_process.input_data import queryMongoData, ProductQueueList
# from queue import Queue

from multiprocessing import Process, Queue
import os
'''
本次测试目的：测试不同进程间能否共享一个全局的Queue
测试结果：需使用：from multiprocessing import Queue
模块创建队列
才能在进程间共享数据
'''

def testFoo1():
    '''
    创建一个全局的queue
    开启两进程消费同一个队列
    观察是否会出现重复消费的现象
    :return:
    '''
    q = Queue()
    que = queryMongoData("autoModelCollection")
    que.chongzhi()
    dataList = que.find_data()
    for data in dataList:
        q.put(data)
    p1 = Process(target=get_data, args=(q,))
    p2 = Process(target=get_data, args=(q,))
    p1.start()
    p2.start()
    p1.join()
    p2.join()


def get_data(q):
    for i in range(10):
        print("process %s get" % os.getpid(), q.get())


if __name__ == '__main__':
    testFoo1()
