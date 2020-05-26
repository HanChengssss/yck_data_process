# _*_ coding:utf-8_*_
# author: hancheng
# date: 2020/5/26 18:05


# class BaseClass(object):
#
#     @staticmethod
#     def base_fun_1():
#         BaseClass.base_fun_2()
#
#     @staticmethod
#     def base_fun_2():
#         print("this fun is BaseClass's base_fun_2!")
#
#
# class SubClass(BaseClass):
#     @staticmethod
#     def base_fun_2():
#         print("this fun is SubClass's base_fun_2!")
#
#
# if __name__ == '__main__':
#     SubClass.base_fun_1()

class BaseClass(object):

    def base_fun_1(self):
        self.base_fun_2()

    def base_fun_2(self):
        print("this fun is BaseClass's base_fun_2!")


class SubClass(BaseClass):
    def base_fun_2(self):
        print("this fun is SubClass's base_fun_2!")


if __name__ == '__main__':
    SubClass().base_fun_1()