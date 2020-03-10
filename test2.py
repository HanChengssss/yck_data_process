

# a = "xxx"  # 赋值一个全局变量a
# print(id(a))  # 打印a的唯一标识
#
#
# def change(a):
#     a = a.__add__("s")  # 对 a 进行新增操作，并用新的变量名接收这个对象
#     print(a)
#     print(id(a))
#
#
# if __name__ == '__main__':
#     change(a)
#     print(id(a))
#     print(a)

# b = ["1"]
# print(id(b))
#
# def change(b):
#     b.append("2")
#     print(b)
#     print(id(b))
#
#
# if __name__ == '__main__':
#     change(b)
#     print(b)
#     print(id(b))

# a = "xxx"  # 赋值一个全局变量a
# print(id(a))  # 打印a的唯一标识
#
# def change(a):
#     a += "s"  # 对 a 进行新增操作，并用新的变量名接收这个对象
#     print(a)
#     print(id(a))
#
#
# if __name__ == '__main__':
#     change(a)
#     print(a)
#     print(id(a))

# b = ["1"]
# print(id(b))
#
# def change(b):
#     b += ["2"]
#     print(b)
#     print(id(b))
#
#
# if __name__ == '__main__':
#     change(b)
#     print(b)
#     print(id(b))

# b = ["1"]
# print(id(b))
#
# def change(b):
#     b = b + ["2"]
#     print(b)
#     print(id(b))
#
#
# if __name__ == '__main__':
#     change(b)
#     print(b)
#     print(id(b))

class Test():

    @staticmethod
    def foo1():
        print("foo1")
        T = Test2()
        T.foo4()

    @staticmethod
    def foo2():
        print("foo2")

    def foo3(self):
        print("foo3")

class Test2():
    def foo4(self):
        print("foo4")

if __name__ == '__main__':
    T = Test()
    T.foo1()
'''
结论：类的静态方法就像一个函数，可以不用创建出实例就能调用，但是不能使用类中的任何放法和变量
但是可以是类外部的方法
'''