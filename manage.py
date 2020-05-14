# !/usr/bin/env python
# -*-encoding: utf-8-*-
# author:LiYanwei
# version:0.1
from multiprocessing import Process, Pool, Queue
import time
from yck_data_process.processManage import ProcessManage
from yck_data_process.inputMange import InputDataMange
from yck_data_process.pipelineManage import OutPutDataManage
from functools import wraps
from yck_data_process.logingDriver import Logger
from yck_data_process.settingsManage import SettingsManage, MODEL
from datetime import datetime
import sys

def fn_timer(function):
    @wraps(function)
    def function_timer(*args, **kwargs):
        t0 = time.time()
        sm = SettingsManage(model=MODEL)
        log_dir_manage = sm.get_log_setting_instance()
        log_driver = Logger("{}\manage.log".format(log_dir_manage.get_log_dir_full_path()), level='info')
        try:
            log_driver.logger.info("start")
            result = function(*args, **kwargs)
            return result
        except Exception as e:
            log_driver.logger.error(str(e))
        finally:
            t1 = time.time()
            log_driver.logger.info("end spend %s seconds" % str(round((t1-t0), 0)))

    return function_timer


class Manage(object):

    @staticmethod
    def create_query():
        return Queue()

    @staticmethod
    @fn_timer
    def run_from_muiltiprocess(source_type):
        '''
        创建生产和消费队列
        往队列中装入待处理的数据
        开启处理进程和存储进程
        :return:
        '''
        sm = SettingsManage(MODEL)
        dps = sm.get_dsp_setting_instance(source_type)
        input_queue = Manage.create_query()
        output_queue = Manage.create_query()
        InputDataMange.input_data(input_queue, sm, dps)
        process_data_job = Process(target=ProcessManage.process_data, args=(input_queue, output_queue, sm, dps))
        out_put_data_job = Process(target=OutPutDataManage.out_put_data, args=(output_queue, sm, dps))
        process_data_job.start()
        out_put_data_job.start()
        process_data_job.join()
        out_put_data_job.join()


if __name__ == '__main__':
    source_type = sys.argv[1]
    Manage.run_from_muiltiprocess(source_type)