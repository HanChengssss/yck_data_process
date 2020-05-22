from yck_data_process.pipelines.Tools import ToolSave
from yck_data_process.pipelines.basePipeline import BaseStorePipeline
from datetime import datetime


# class IncrementStock(object):
#     @staticmethod
#     def process_item(item, update_list, insert_list, id_field_set, mysql_conn, table, id_field_name):
#         if "data" in item:
#             data = item["data"]
#         else:
#             data = item
#         id_field = data.get(id_field_name)
#         ret = ToolSave.test_exist(id_field=id_field, id_field_set=id_field_set)
#         if ret:
#             update_time = None
#             add_time = None
#             if "add_time" in data:
#                 add_time = data.pop("add_time")
#             if "update_time" in data:
#                 update_time = data.pop("update_time")
#             new_data = ToolSave.sort_item(data)
#             old_data = ToolSave.get_old_data(new_data=data, table_name=table, mysql_conn=mysql_conn, id_field_name=id_field_name)
#             if not old_data:
#                 # print("数据不存在！")
#                 pass
#             else:
#                 old_data = ToolSave.sort_item(old_data)
#                 compare_ret = ToolSave.compare_data(new_data=new_data, old_data=old_data)
#                 if not compare_ret:
#                     if update_time:
#                         data["update_time"] = update_time
#                     elif add_time:
#                         data["update_time"] = add_time
#                     else:
#                         data["update_time"] = datetime.today()
#                     # item["id_field"] = "model_id"
#                     update_list.append(item)
#                 else:
#                     # print("数据无变化！")
#                     pass
#         else:
#             insert_list.append(item)
#
#     @staticmethod
#     def process_data_dic(data_dic, mysql_conn, sm_instance):
#         table = data_dic.get("table")
#         data_list = data_dic.get("dataList")
#         update_list = []
#         insert_list = []
#         id_field_name = data_dic["id_field_name"]
#         id_field_set = ToolSave.get_filter_set(mysql_conn=mysql_conn, id_field_name=id_field_name, table=table)
#         # 将数据进行分类
#         print("==========", table)
#         for item in data_list:
#             IncrementStock.process_item(item=item, update_list=update_list, insert_list=insert_list, id_field_set=id_field_set, mysql_conn=mysql_conn, table=table, id_field_name=id_field_name)
#         ToolSave.update_mysql_many(mysql_conn, update_list, table, id_field_name, sm_instance)
#         ToolSave.insert_mysql_many(mysql_conn, insert_list, table, sm_instance)
#
#
# class TwoIncrementStock(object):
#     id_field_set_dic = {
#
#     }
#
#     @staticmethod
#     def one_process(item, compare_dic, insert_list, id_field_set, mysql_conn, table, id_field_name):
#         if "data" in item:
#             data = item["data"]
#         else:
#             data = item
#         id_field = data.get(id_field_name)
#         ret = ToolSave.test_exist(id_field=id_field, id_field_set=id_field_set)
#         if ret:
#             if data["log_id"] not in compare_dic:
#                 compare_dic[data["log_id"]] = data
#         else:
#             insert_list.append(item)
#
#     @staticmethod
#     def two_process(compare_dic, update_list, mysql_conn, table):
#         data_list = compare_dic.values()
#         new_data_log_id_set = set([data["log_id"] for data in data_list])
#         new_data_car_id_set = set([data["car_id"] for data in data_list])
#         old_data_log_id_set = ToolSave.get_compare_set(mysql_conn=mysql_conn, table=table, id_field_name="log_id", condition_field="car_id", condition_list=new_data_car_id_set)
#         diff_log_id_set = new_data_log_id_set - old_data_log_id_set
#         for log_id in diff_log_id_set:
#             update_list.append(compare_dic[log_id])
#
#     @staticmethod
#     def process_data_dic(data_dic, mysql_conn, sm_instance):
#         table = data_dic.get("table")
#         data_list = data_dic.get("dataList")
#         update_list = []
#         insert_list = []
#         compare_dic = dict()
#         id_field_name = data_dic["id_field_name"]
#         if table not in TwoIncrementStock.id_field_set_dic:
#             print("初始化id_field_set。。。")
#             id_field_set = ToolSave.get_filter_set(mysql_conn=mysql_conn, id_field_name=id_field_name, table=table)
#             TwoIncrementStock.id_field_set_dic[table] = id_field_set
#         else:
#             print("使用缓存的id_field_set。。。")
#             id_field_set = TwoIncrementStock.id_field_set_dic[table]
#
#         # 将数据进行分类
#         print("==========", table)
#         for item in data_list:
#             TwoIncrementStock.one_process(item=item, compare_dic=compare_dic, insert_list=insert_list, id_field_set=id_field_set, mysql_conn=mysql_conn, table=table, id_field_name=id_field_name)
#         TwoIncrementStock.two_process(compare_dic, update_list, mysql_conn, table)
#         ToolSave.update_mysql_many(mysql_conn, update_list, table, id_field_name, sm_instance)
#         ToolSave.insert_mysql_many(mysql_conn, insert_list, table, sm_instance)


class OneMixPipeline(BaseStorePipeline):
    @staticmethod
    def process_data(data, container, id_field_set, mysql_conn, table, id_field_name):
        insert_list = container["insert_list"]
        update_list = container["update_list"]
        id_field = data.get(id_field_name)
        ret = ToolSave.test_exist(id_field=id_field, id_field_set=id_field_set)
        if not ret:
            insert_list.append(data)
        else:
            update_time = None
            add_time = None
            if "add_time" in data:
                add_time = data.pop("add_time")
            if "update_time" in data:
                update_time = data.pop("update_time")
            new_data = ToolSave.sort_item(data)
            old_data = ToolSave.get_old_data(new_data=data, table_name=table, mysql_conn=mysql_conn,
                                             id_field_name=id_field_name)
            if not old_data:
                # print("数据不存在！")
                pass
            else:
                old_data = ToolSave.sort_item(old_data)
                compare_ret = ToolSave.compare_data(new_data=new_data, old_data=old_data)
                if not compare_ret:
                    if update_time:
                        data["update_time"] = update_time
                    elif add_time:
                        data["update_time"] = add_time
                    else:
                        data["update_time"] = datetime.today()
                    # item["id_field"] = "model_id"
                    update_list.append(data)
                else:
                    # print("数据无变化！")
                    pass

    @staticmethod
    def creat_data_container():
        container = dict()
        container["insert_list"] = []
        container["update_list"] = []
        return container

    @staticmethod
    def store_data(container, mysql_conn, table, sm_instance, id_field_name):
        insert_list = container["insert_list"]
        update_list = container["update_list"]
        ToolSave.update_mysql_many(mysql_conn, update_list, table, id_field_name, sm_instance)
        ToolSave.insert_mysql_many(mysql_conn, insert_list, table, sm_instance)


class TwoMixPipeline(BaseStorePipeline):
    @staticmethod
    def process_data(data, container, id_field_set, mysql_conn, table, id_field_name):
        insert_list = container["insert_list"]
        update_list = container["update_list"]
        compare_dic = container["compare_dic"]
        id_field = data.get(id_field_name)
        ret = ToolSave.test_exist(id_field=id_field, id_field_set=id_field_set)
        if not ret:
            insert_list.append(data)
        else:
            if data["log_id"] not in compare_dic:
                compare_dic[data["log_id"]] = data

    @staticmethod
    def creat_data_container():
        container = dict()
        container["insert_list"] = []
        container["update_list"] = []
        container["compare_dic"] = dict()
        return container

    @staticmethod
    def store_data(container, mysql_conn, table, sm_instance, id_field_name):
        insert_list = container["insert_list"]
        update_list = container["update_list"]
        compare_dic = container["compare_dic"]
        TwoMixPipeline.sub_process_data(compare_dic, update_list, mysql_conn, table)
        ToolSave.update_mysql_many(mysql_conn, update_list, table, id_field_name, sm_instance)
        ToolSave.insert_mysql_many(mysql_conn, insert_list, table, sm_instance)

    @staticmethod
    def sub_process_data(compare_dic, update_list, mysql_conn, table):
        data_list = compare_dic.values()
        new_data_log_id_set = set([data["log_id"] for data in data_list])
        new_data_car_id_set = set([data["car_id"] for data in data_list])
        old_data_log_id_set = ToolSave.get_compare_set(mysql_conn=mysql_conn, table=table, id_field_name="log_id",
                                                       condition_field="car_id", condition_list=new_data_car_id_set)
        diff_log_id_set = new_data_log_id_set - old_data_log_id_set
        for log_id in diff_log_id_set:
            update_list.append(compare_dic[log_id])
