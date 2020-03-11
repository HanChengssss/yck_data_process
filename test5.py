from abc import ABCMeta, abstractclassmethod
from multiprocessing import Process, Pool
import os
'''
1.测试目的：是否能通过继承来实现单例模式
测试结论：可以通过继承的方式实现，不同的子类都能实现其各自的单例，互不影响。

2.测试目的：在多进程情况下，单例模式是如何实现的
结论：单例模式的适用范围是在进程内，不能约束其他进程的实例创建。
'''


class A(metaclass=ABCMeta):

    __instanse = None
    __isFirstInit = False

    def __new__(cls):
        print("__new__")
        if not cls.__instanse:
            cls.__instanse = super().__new__(cls)  # todo
        return cls.__instanse

    def foo(self):
        print('the method from A')

class B(A):
    def __init__(self):
        super().__init__()
        print(id(self))

    def foo(self):
        print("pid: %s" % os.getpid())
        print("the method from B")


class C(A):
    def __init__(self):
        super().__init__()
        print(id(self))

    def foo(self):
        print("the method from C")


# if __name__ == '__main__':
#     b = B()
#     b1 = B()
#     c = C()
#     c1 = C()
# '''
# ----输出-----
# __new__
# 1829507239104
# __new__
# 1829507239104
# __new__
# 1829507239048
# __new__
# 1829507239048
# '''



def run():
    B().foo()
    B().foo()
    B().foo()
    B().foo()


if __name__ == '__main__':
    p1 = Process(target=run)
    p2 = Process(target=run)
    p1.start()
    p2.start()
    p1.join()
    p2.join()
'''
------输出------
__new__
1925975930192
pid: 19532
the method from B
__new__
1925975930192
pid: 19532
the method from B
__new__
1925975930192
pid: 19532
the method from B
__new__
1925975930192
pid: 19532
the method from B
__new__
2116867028360
pid: 13756
the method from B
__new__
2116867028360
pid: 13756
the method from B
__new__
2116867028360
pid: 13756
the method from B
__new__
2116867028360
pid: 13756
the method from B
'''




