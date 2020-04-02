# !/usr/bin/env python
# -*-encoding: utf-8-*-
# author:LiYanwei
# version:0.1
from multiprocessing import Process, Pool, Queue
import time
from yck_data_process.processManage import ProcessManage
from yck_data_process.input_data import InputDataMange
from yck_data_process.output_data import OutPutDataManage
from functools import wraps
from yck_data_process.logingDriver import Logger
from yck_data_process.settingsManage import SettingsManage, MODEL
from datetime import datetime
class Manage(object):

    @staticmethod
    def create_query():
        return Queue()

    @staticmethod
    def run_from_muiltiprocess():
        '''
        创建生产和消费队列
        往队列中装入待处理的数据
        开启处理进程和存储进程
        :return:
        '''
        inputQueue = Manage.create_query()
        outputQueue = Manage.create_query()
        InputDataMange.input_data(inputQueue)
        p1 = Process(target=ProcessManage.process_data, args=(inputQueue, outputQueue))
        r1 = Process(target=OutPutDataManage.dataOutput, args=(outputQueue,))
        p1.start()
        r1.start()
        p1.join()
        r1.join()


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
def run_from_muiltiprocess():
    sm = SettingsManage(model=MODEL)
    logDirManage = sm.get_logSettingsInstance()
    logDriver = Logger("{}\manage.log".format(logDirManage.get_logDirFullPath()), level='info')
    try:
        logDriver.logger.info("start")
        Manage.run_from_muiltiprocess()
    except Exception as e:
        logDriver.logger.error(str(e))
    finally:
        logDriver.logger.info("end")


if __name__ == '__main__':
    run_from_muiltiprocess()







