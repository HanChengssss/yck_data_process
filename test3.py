'''
测试目的：由于项目中的字段处理实例需要频繁的创建（每处理一次创建一次），可能会对内存造成不必要的负担
所以希望引入单例模式来减少对象创建的次数。
虽然可以通过改变代码的结构实现这个目的，但是却会破会整体的结构，影响阅读性。
'''

class MyBeautifulGirl(object):
    __instance = None
    __isFirstInit = False

    def __new__(cls, name):
        if not cls.__instance:
            MyBeautifulGirl.__instance = super().__new__(cls)
            return cls.__instance

    def __init__(self, name):
        if not self.__instance:
            self.__name = name
            print("遇见" + name + ", 我一见钟情！")
            MyBeautifulGirl.__isFirstInit = True
        else:
            print("遇见" + name + "，我置若罔闻！")

    def showMyHeart(self):
        print(self.__name + "就我心中的唯一！")

