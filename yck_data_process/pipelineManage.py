# !/usr/bin/env python
# -*-encoding: utf-8-*-
# author:Hancheng
# version:0.1
import pymysql
from yck_data_process.logingDriver import Logger
from yck_data_process.pipelines.Tools import ToolSave
from tqdm import tqdm


class OutPutDataManage():
    @staticmethod
    def out_put_data(out_put_queue, sm_instance, dps_instance):
        '''
        管理和加载所有的数据库存储类
        从out_put_queue中取出数据存到MySQL中
        :param out_put_queue:
        :return:
        '''
        db_mange = sm_instance.get_db_setting_instance()
        log_path_mange = sm_instance.get_log_setting_instance()
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
                    coll = data_dic.get("coll_name")
                    data_pipeline_func = dps_instance.get_pip_func(coll)
                    data_pipeline_func().process_data_dic(data_dic, mysql_conn, sm_instance)
                    is_update = dps_instance.get_is_update()
                    if is_update:
                        ToolSave.update_is_process_status(db_mange, data_dic["_id"], coll)
                except Exception as e:
                    log.logger.error(e)
                finally:
                    tq.update(1)
        finally:
            mysql_conn.close()
            tq.close()


if __name__ == '__main__':
    pass


