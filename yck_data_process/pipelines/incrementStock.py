from yck_data_process.pipelines.Tools import ToolSave
from datetime import datetime


class IncrementStock(object):
    @staticmethod
    def process_item(item, update_list, insert_list, id_field_set, mysql_conn, table, id_field_name):
        if "data" in item:
            data = item["data"]
        else:
            data = item
        id_field = data.get(id_field_name)
        ret = ToolSave.test_exist(id_field=id_field, id_field_set=id_field_set)
        if ret:
            update_time = None
            add_time = None
            if "add_time" in data:
                add_time = data.pop("add_time")
            if "update_time" in data:
                update_time = data.pop("update_time")
            new_data = ToolSave.sort_item(data)
            old_data = ToolSave.get_old_data(new_data=data, table_name=table, mysql_conn=mysql_conn, id_field_name=id_field_name)
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
                update_list.append(item)
            else:
                pass
                # print("数据无变化！")
        else:
            insert_list.append(item)

    @staticmethod
    def process_data_dic(data_dic, mysql_conn):
        table = data_dic.get("table")
        data_list = data_dic.get("dataList")
        update_list = []
        insert_list = []
        id_field_name = data_dic["id_field_name"]
        id_field_set = ToolSave.get_filter_set(mysql_conn=mysql_conn, id_field_name=id_field_name, table=table)
        # 将数据进行分类
        print("==========", table)
        for item in data_list:
            IncrementStock.process_item(item=item, update_list=update_list, insert_list=insert_list, id_field_set=id_field_set, mysql_conn=mysql_conn, table=table, id_field_name=id_field_name)
        ToolSave.update_mysql_many(mysql_conn=mysql_conn, data_list=update_list, table=table, id_field_name=id_field_name)
        ToolSave.insert_mysql_many(mysql_conn=mysql_conn, data_list=insert_list, table=table, hp=False)



