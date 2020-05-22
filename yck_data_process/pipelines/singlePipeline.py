from yck_data_process.pipelines.Tools import ToolSave
from yck_data_process.pipelines.basePipeline import BaseStorePipeline

# class IncrementPipeline(object):
#     """
#     增量更新管道
#     """
#     @staticmethod
#     def process_item(item, insert_list, id_field_set, mysql_conn, table, id_field_name):
#         if "data" in item:
#             data = item["data"]
#         else:
#             data = item
#         # print("*******", data)
#         id_field = data.get(id_field_name)
#         ret = ToolSave.test_exist(id_field=id_field, id_field_set=id_field_set)
#         if not ret:
#             insert_list.append(item)
#
#     @staticmethod
#     def process_data_dic(data_dic, mysql_conn, sm_instance):
#         table = data_dic.get("table")
#         data_list = data_dic.get("dataList")
#         insert_list = []
#         id_field_name = data_dic["id_field_name"]
#         id_field_set = ToolSave.get_filter_set(mysql_conn=mysql_conn, id_field_name=id_field_name, table=table)
#         # 将数据进行分类
#         print("==========", table)
#         for item in data_list:
#             IncrementPipeline.process_item(item=item, insert_list=insert_list, id_field_set=id_field_set, mysql_conn=mysql_conn, table=table, id_field_name=id_field_name)
#         ToolSave.insert_mysql_many(mysql_conn, insert_list, table, sm_instance)


class SinglePipeline(BaseStorePipeline):
    @staticmethod
    def process_data(data, container, id_field_set, mysql_conn, table, id_field_name):
        insert_list = container["insert_list"]
        id_field = data.get(id_field_name)
        ret = ToolSave.test_exist(id_field=id_field, id_field_set=id_field_set)
        if not ret:
            insert_list.append(data)
        else:
            pass

    @staticmethod
    def creat_data_container():
        container = dict()
        container["insert_list"] = []
        return container

    @staticmethod
    def store_data(container, mysql_conn, table, sm_instance):
        insert_list = container["insert_list"]
        ToolSave.insert_mysql_many(mysql_conn, insert_list, table, sm_instance)
