# _*_ coding:utf-8_*_
# author: hancheng
# date: 2020/5/22 11:08
from yck_data_process.pipelines.Tools import ToolSave
from datetime import datetime


class TwoIncrementStock(object):
    id_field_set_dic = {

    }
    @staticmethod
    def one_process(item, compare_dic, insert_list, id_field_set, mysql_conn, table, id_field_name):
        if "data" in item:
            data = item["data"]
        else:
            data = item
        id_field = data.get(id_field_name)
        ret = ToolSave.test_exist(id_field=id_field, id_field_set=id_field_set)
        if ret:
            if data["log_id"] not in compare_dic:
                compare_dic[data["log_id"]] = data
        else:
            insert_list.append(item)

    @staticmethod
    def two_process(compare_dic, update_list, mysql_conn, table):
        data_list = compare_dic.values()
        new_data_log_id_set = set([data["log_id"] for data in data_list])
        new_data_car_id_set = set([data["car_id"] for data in data_list])
        old_data_log_id_set = ToolSave.get_compare_set(mysql_conn=mysql_conn, table=table, id_field_name="log_id", condition_field="car_id", condition_list=new_data_car_id_set)
        diff_log_id_set = new_data_log_id_set - old_data_log_id_set
        for log_id in diff_log_id_set:
            update_list.append(compare_dic[log_id])

    @staticmethod
    def process_data_dic(data_dic, mysql_conn, sm_instance):
        table = data_dic.get("table")
        data_list = data_dic.get("dataList")
        update_list = []
        insert_list = []
        compare_dic = dict()
        id_field_name = data_dic["id_field_name"]
        if table not in TwoIncrementStock.id_field_set_dic:
            print("初始化id_field_set。。。")
            id_field_set = ToolSave.get_filter_set(mysql_conn=mysql_conn, id_field_name=id_field_name, table=table)
            TwoIncrementStock.id_field_set_dic[table] = id_field_set
        else:
            print("使用缓存的id_field_set。。。")
            id_field_set = TwoIncrementStock.id_field_set_dic[table]

        # 将数据进行分类
        print("==========", table)
        for item in data_list:
            TwoIncrementStock.one_process(item=item, compare_dic=compare_dic, insert_list=insert_list, id_field_set=id_field_set, mysql_conn=mysql_conn, table=table, id_field_name=id_field_name)
        TwoIncrementStock.two_process(compare_dic, update_list, mysql_conn, table)
        ToolSave.update_mysql_many(mysql_conn, update_list, table, id_field_name, sm_instance)
        ToolSave.insert_mysql_many(mysql_conn, insert_list, table, sm_instance)


