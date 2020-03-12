import time, threading
from test6 import fn_timer
import multiprocessing

'''
本次测试的目的：学习多线程的使用和特性。
1.不加锁：随机输出不同的数字，证明多线程已经把数据改乱了 用时2.6s
2.加锁：结果和预期相同，用时10s
3.使用 += 和 -= 不加锁结果一样会混乱
4.是否能使用全部cpu的性能测试， 测试结果，无论开多少条进程，都不能把cpu占满。
'''
# '''
# 运行顺序：
# 主线程先启动
# 子线程启动
# 子线程完成退出
# 主线程完成退出
# '''
#
# def loop():
#     print("thread %s is running..." % threading.current_thread().name)
#     n = 0
#     while n < 5:
#         n = n + 1
#         print('thread %s >>> %s' % (threading.current_thread().name, n))
#         time.sleep(1)
#     print('thread %s ended.' % threading.current_thread().name)
#
#
# print('thread %s is runing...' % threading.current_thread().name)
# t = threading.Thread(target=loop, name="LoopThread")
# t.start()
# t.join()
# print('thread %s ended' % threading.current_thread().name)


balance = 0
lock = threading.Lock()  # 加锁
# 按位异或逻辑运算符 ^

# def change_it(n):
#     global balance
#     balance = balance + n
#     balance = balance - n
#     # print(balance)
#
# @fn_timer
# def run_thread(n):
#     print("theading %s" % threading.current_thread().name)
#     for i in range(10000000):
#         lock.acquire()  # 获取锁
#         try:
#             change_it(n)
#         finally:
#             # 释放锁
#             lock.release()
#
#
# t1 = threading.Thread(target=run_thread, args=(5,))
# t2 = threading.Thread(target=run_thread, args=(20,))
# t1.start()
# t2.start()
# t1.join()
# t2.join()
# print(balance)

# def change_it(n):
#     global balance
#     balance = balance + n
#     balance = balance - n
#     # print(balance)
#
#
# @fn_timer
# def run_thread(n):
#     print("threading %s" % threading.current_thread().name)
#     for i in range(10000000):
#         change_it(n)
#
#
# t1 = threading.Thread(target=run_thread, args=(5,))
# t2 = threading.Thread(target=run_thread, args=(20,))
# t1.start()
# t2.start()
# t1.join()
# t2.join()
# print(balance)

# def change_it(n):
#     global balance
#     balance += n
#     balance -= n
#     # print(balance)
#
#
# @fn_timer
# def run_thread(n):
#     print("threading %s" % threading.current_thread().name)
#     for i in range(10000000):
#         change_it(n)
#
#
# t1 = threading.Thread(target=run_thread, args=(5,))
# t2 = threading.Thread(target=run_thread, args=(20,))
# t1.start()
# t2.start()
# t1.join()
# t2.join()
# print(balance)

# 是否能使用全部cpu的性能测试， 测试结果，无论开多少条进程，都不能把cpu占满。
# def loop():
#     x = 0
#     while True:
#         x = x ^ 1
#
#
# print(multiprocessing.cpu_count())
#
# for i in range(20):
#     t = threading.Thread(target=loop)
#     t.start()

# ThreadLocal 测试
local_school = threading.local()


def process_student():
    # 获取当前线程关联的students
    std = local_school.student
    print("Hello, %s (in %s)" % (std, threading.current_thread().name))


def process_thread(name):
    # 绑定ThreadLocal 的 student：
    local_school.student = name
    process_student()


t1 = threading.Thread(target=process_thread, args=('Alice', ), name='Thread-A')
t2 = threading.Thread(target=process_thread, args=('Bob', ), name='Thread-B')
t1.start()
t2.start()
t1.join()
t2.join()
