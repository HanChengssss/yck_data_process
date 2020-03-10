
'''
本次测试的目的在于明确类中__x变量与__x()方法的作用。
从网上资料查找中得到的解释是:这个双下划线更会造成更多混乱，但它并不是用来标识一个方法或属性是私有的，真正作用是用来避免子类覆盖其内容。
但是我觉的解释的还不够透彻，下面来验证一下。
验证结果：不能覆盖或者在类外部使用的原因是：Python将__x()或__x重命名了,在方法和或者变量名前加_类名，例如__method=_A__method,所以使用原来的名字就调用不到。
'''

# class TestA():
#     __instance = None
#     __isFirstInit = False
#
#     def __init__(self, name):
#         if not self.__instance:
#             self.__name = name
#             print("遇见" + name + ", 我一见钟情！")
#             TestA.__isFirstInit = True
#         else:
#             print("遇见" + name + "，我置若罔闻！")
#
# if __name__ == '__main__':
#     a1 = TestA("a1")
#     print(a1.__instance)
#     a2 = TestA("a2")
#     print(a2.__instance)
#     print(TestA.__instance)
# '''
# 测试1结果：在类的外部不能调用__x
# '''

# class TestA():
#     instance = None
#     isFirstInit = False
#
#     def __init__(self, name):
#         if not self.instance:
#             self.__name = name
#             print("遇见" + name + ", 我一见钟情！")
#             TestA.isFirstInit = True
#         else:
#             print("遇见" + name + "，我置若罔闻！")
#
#
# if __name__ == '__main__':
#     a1 = TestA("a1")
#     print(a1.isFirstInit)
#     a2 = TestA("a2")
#     print(a2.isFirstInit)
#     print(TestA.isFirstInit)
# '''
# 测试2结果：去掉__后，在类的外部可以调用
# '''

# class TestA():
#     _instance = None
#     _isFirstInit = False
#
#     def __init__(self, name):
#         if not self._instance:
#             self.__name = name
#             print("遇见" + name + ", 我一见钟情！")
#             TestA._isFirstInit = True
#         else:
#             print("遇见" + name + "，我置若罔闻！")
#
#
# if __name__ == '__main__':
#     a1 = TestA("a1")
#     print(a1._isFirstInit)
#     a2 = TestA("a2")
#     print(a2._isFirstInit)
#     print(TestA._isFirstInit)
# '''
# 测试结果3：加_后可以正常调用
# '''


class A(object):
    __a = "1"
    def __method(self):
        print("I'm a method in A")

    def method(self):
        self.__method()


class B(A):
    def __method(self):
        print("I'm a method in B")

a = A()
a.method()  # 输出：I'm a method in A
a._A__method()  # 输出：I'm a method in A

print(a._A__a)  # 1

print(A._A__a)  # 1

b = B()
b.method()  # 输出：I'm a method in A
'''
测试结果4输出：------------
I'm a method in A 
I'm a method in A
1
1
I'm a method in A # 不能调用重写后的方法，不能调用的原因是__将方法或者变量重命名了,在方法和或者变量名前加_类名，例如__method=_A__method。
'''

