# _*_ coding:utf-8_*_
# author: hancheng
# date: 2020/5/22 15:39
from yck_data_process.pipelines.Tools import ToolSave


class BaseStorePipeline(object):
    id_field_set_dic = {

    }

    @staticmethod
    def process_data_dic(data_dic, mysql_conn, sm_instance):
        table = data_dic.get("table")
        data_list = data_dic.get("dataList")
        id_field_name = data_dic["id_field_name"]
        id_field_set = BaseStorePipeline.get_filter_set(table, mysql_conn, id_field_name)
        BaseStorePipeline.process_data_list(data_list, id_field_set, mysql_conn, table, id_field_name)

    @staticmethod
    def process_data_list(data_list, id_field_set, mysql_conn, table, id_field_name):
        container = BaseStorePipeline.creat_data_container()
        for item in data_list:
            if "data" in item:
                data = item["data"]
            else:
                data = item
            BaseStorePipeline.process_data(data, container, id_field_set, mysql_conn, table, id_field_name)
            BaseStorePipeline.store_data(container)

    @staticmethod
    def get_filter_set(table, mysql_conn, id_field_name):
        if table not in BaseStorePipeline.id_field_set_dic:
            print("初始化id_field_set。。。")
            id_field_set = ToolSave.get_filter_set(mysql_conn=mysql_conn, id_field_name=id_field_name, table=table)
            BaseStorePipeline.id_field_set_dic[table] = id_field_set
        else:
            print("使用缓存的id_field_set。。。")
            id_field_set = BaseStorePipeline.id_field_set_dic[table]
        return id_field_set

    @staticmethod
    def creat_data_container():
        return dict()

    @staticmethod
    def process_data(data, container, id_field_set, mysql_conn, table, id_field_name):
        pass

    @staticmethod
    def store_data(container):
        pass