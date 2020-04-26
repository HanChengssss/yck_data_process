# !/usr/bin/env python
# -*-encoding: utf-8-*-
# author:Hancheng
# version:0.1
from yck_data_process.settingsManage import SettingsManage, MODEL
import pymysql
from yck_data_process.logingDriver import Logger
import pymongo
from yck_data_process.pipelines.autoModelOutput import AutoModelPipeline
from yck_data_process.pipelines.autoSettingOutput import AutoSettingPipeline
from yck_data_process.pipelines.bankInfoOutput import BankInfoOutput
from yck_data_process.pipelines.Tools import ToolSave
from tqdm import tqdm
import traceback

class OutPutDataManage():
    data_dic_pipeline_dic = {
        "model": {"func": AutoModelPipeline},
        "setting": {"func": AutoSettingPipeline},
        "bank": {"func": BankInfoOutput},
    }
    @staticmethod
    def out_put_data(out_put_queue):
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
        mongo_mysql_conn = pymongo.MongoClient(**db_mange.get_mongo_client_params())
        mongodb = mongo_mysql_conn.get_database(db_mange.get_mongodb())
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
                    coll_name = db_mange.get_mongodb_coll_name(data_type)
                    data_pipeline = OutPutDataManage.data_dic_pipeline_dic.get(data_type).get("func")
                    data_pipeline.process_data_dic(data_dic, mysql_conn)
                    ToolSave.update_is_process_status(mongodb, data_dic["_id"], coll_name)
                except Exception as e:
                    log.logger.error(e)
                finally:
                    tq.update(1)
        finally:
            mysql_conn.close()
            mongo_mysql_conn.close()
            tq.close()


if __name__ == '__main__':
    pass


