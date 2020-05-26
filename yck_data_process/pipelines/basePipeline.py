# _*_ coding:utf-8_*_
# author: hancheng
# date: 2020/5/22 15:39
from yck_data_process.pipelines.Tools import ToolSave


class BaseStorePipeline(object):
    id_field_set_dic = {

    }

    def process_data_dic(self, data_dic, mysql_conn, sm_instance):
        table = data_dic.get("table")
        print(f"正在处理的数据来自{table}...")
        data_list = data_dic.get("dataList")
        id_field_name = data_dic["id_field_name"]
        container = self.creat_data_container()
        id_field_set = self.get_filter_set(table, mysql_conn, id_field_name)
        self.process_data_list(data_list, id_field_set, mysql_conn, table, id_field_name, sm_instance, container)
        self.store_data(container, mysql_conn, table, sm_instance, id_field_name)

    def process_data_list(self, data_list, id_field_set, mysql_conn, table, id_field_name, sm_instance, container):
        # print(data_list)
        for item in data_list:
            if "data" in item:
                data = item["data"]
            else:
                data = item
            self.process_data(data, container, id_field_set, mysql_conn, table, id_field_name)

    def get_filter_set(self, table, mysql_conn, id_field_name):
        if table not in self.id_field_set_dic:
            # print("初始化id_field_set。。。")
            id_field_set = ToolSave.get_filter_set(mysql_conn=mysql_conn, id_field_name=id_field_name, table=table)
            self.id_field_set_dic[table] = id_field_set
        else:
            # print("使用缓存的id_field_set。。。")
            id_field_set = self.id_field_set_dic[table]
        return id_field_set

    def creat_data_container(self):
        return dict()

    def process_data(self, data, container, id_field_set, mysql_conn, table, id_field_name):
        pass

    def store_data(self, container, mysql_conn, table, sm_instance, id_field_name):
        pass