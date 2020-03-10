# !/usr/bin/env python
# -*-encoding: utf-8-*-
# author:LiYanwei
# version:0.1
import pymysql
from yck_data_process.logingDriver import *
from yck_data_process.settings import *
class OutPutBase():
    '''
    将处理后的数据输出到目标数据库
    '''


    # def data_input(self, data):
    #     pass
    #
    # def data_output(self, datas):
    #     pass
    #
    # def get_db_conn(self, **kwargs):
    #     pass
    pass

class OutPutMysql():

    def data_output(self, outputQueue):
        while True:
            datas = outputQueue.get()
            if datas == 'end':
                print("data_output is end !")
                break
            print("save data...")


