# coding=utf8
from yck_data_process.pipelines.Tools import ToolSave


class BankInfoOutput(object):
    id_set_dic = {}  # 去重集合
    @staticmethod
    def process_item(item, update_list, insert_list, id_field_set, mysql_conn, table, id_field_name):
        '''
        车型库更新逻辑
        只负责把不同存储逻辑的数据进行
        分类不作任何修改数据库的操作。
        --------------------------
        分类逻辑：
        首先判断该条数据是否已存在
        如果不存在加入到insert_list
        否则，判断数据是否出现变化
        如果有变化：将数据加入到
        update_list
        如果没变化：抛弃
        :param item: 一条车型数据
        :param update_list:待更新列表
        :param insert_list:待插入列表
        :param id_field_set:过滤集合
        :param mysql_conn:数据库连接
        :return:
        '''
        if "data" in item:
            data = item["data"]
        else:
            data = item
        id_filed = data.get(id_field_name)
        ret = ToolSave.test_exist(id_field=id_filed, id_field_set=id_field_set)
        data["isSync"] = "false"
        data["isManual"] = "false"
        if ret:
            update_time = None
            if "add_time" in data:
                data.pop("add_time")
            if "update_time" in data:
                update_time = data.pop("update_time")
            new_data = ToolSave.sort_item(data)
            old_data = ToolSave.get_old_data(new_data=data, table_name=table, mysql_conn=mysql_conn, id_field=id_field_name)
            if not old_data:
                """爬下来的数据有重复，所以可能出现新数据没入库，但是id已经在set中"""
                pass
            else:
                old_data = ToolSave.sort_item(old_data)
                compare_ret = ToolSave.compare_data(new_data=new_data, old_data=old_data)
                if not compare_ret:
                    if update_time:
                        data["update_time"] = update_time
                    # item["id_field"] = "autohome_id"
                    update_list.append(item)
                else:
                    pass
                    # print("数据无变化！")
        else:
            insert_list.append(item)

    @staticmethod
    def process_data_dic(data_dic, mysql_conn):
        '''
        将data_dic中数据进行分类
        不同存储逻辑的数据分别放到不同的列表中
        最后再统一处理，将存逻辑和数据存储操作分离
        # todo 新旧对比需要优化，初步决定先统一将已有数据全字段取出，加密后放到集合中
        :param data_dic:
        :param mysql_conn:
        :return:
        '''
        table = data_dic.get("table")
        data_list = data_dic.get("dataList")
        update_list = []
        insert_list = []
        id_field_name = data_dic["id_field_name"]
        id_field_set = ToolSave.get_filter_set(mysql_conn=mysql_conn, id_field_name=id_field_name, table=table)
        # 将数据进行分类
        print("==========", table)
        for item in data_list:
            BankInfoOutput.process_item(item=item, update_list=update_list, insert_list=insert_list, id_field_set=id_field_set, mysql_conn=mysql_conn, table=table, id_field_name=id_field_name)
        # 将分类后的数据进行批存储操作
        # print(len(update_list))
        # print(len(insert_list))
        ToolSave.update_mysql_many(mysql_conn=mysql_conn, data_list=update_list, table=table, id_field_name=id_field_name)
        ToolSave.insert_mysql_many(mysql_conn=mysql_conn, data_list=insert_list, table=table, hp=False)