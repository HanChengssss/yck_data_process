# !/usr/bin/env python
# -*-encoding: utf-8-*-
# author:Hancheng
# version:0.1
from yck_data_process.settingsManage import SettingsManage, MODEL, PipelinesTypeMap
import pymysql
from yck_data_process.logingDriver import Logger
import pymongo
from yck_data_process.pipelines.increment import IncrementPipeline
from yck_data_process.pipelines.incrementStock import IncrementStock
from yck_data_process.pipelines.Tools import ToolSave
from tqdm import tqdm
import traceback

class OutPutDataManage():
    data_dic_pipeline_dic = {
        "increment": IncrementPipeline,
        "incrementStock": IncrementStock
    }
    @staticmethod
    def out_put_data(out_put_queue, source_type):
        '''
        管理和加载所有的数据库存储类
        从out_put_queue中取出数据存到MySQL中
        :param out_put_queue:
        :return:
        '''

        sm = SettingsManage(model=MODEL)
        db_mange = sm.get_db_setting_instance()
        log_path_mange = sm.get_log_setting_instance()
        mysql_conn = pymysql.connect(**db_mange.get_save_mysql_normal_params())
        log_dir_full_path = log_path_mange.get_log_dir_full_path()
        log = Logger(filename="{}\outoutData.log".format(log_dir_full_path), level='error')
        q_size = out_put_queue.qsize()
        tq = tqdm(total=q_size, desc="数据处理进度：")
        try:
            while True:
                data_dic = out_put_queue.get()
                if data_dic == 'end':
                    print("data_output is end !")
                    break
                try:
                    data_type = data_dic.get("type")
                    pip_type = PipelinesTypeMap(data_type).get_pipeline_type()
                    data_pipeline = OutPutDataManage.data_dic_pipeline_dic.get(pip_type)
                    data_pipeline.process_data_dic(data_dic, mysql_conn)
                    is_update = PipelinesTypeMap(data_type).get_is_update()
                    if is_update:
                        ToolSave.update_is_process_status(db_mange, data_dic["_id"], data_type)
                except Exception as e:
                    log.logger.error(e)
                finally:
                    tq.update(1)
        finally:
            mysql_conn.close()
            tq.close()


if __name__ == '__main__':
    pass


