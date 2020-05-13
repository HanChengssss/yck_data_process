import pymysql
from yck_data_process.settingsManage import SettingsManage, MODEL

used_car_pub_after = [
    {"type": "used_car_pub_after",
     "table": "spider_www_ali",
     "source": "spider_log_ali",
     "id_field_name": "car_id",
     }
]


class MysqldbSource():

    @staticmethod
    def input_data(input_queue):
        sm = SettingsManage(MODEL)
        db_setting = sm.get_db_setting_instance()
        db_params = db_setting.get_save_mysql_normal_params()
        mysql_conn = pymysql.connect(**db_params)
        for data_info in used_car_pub_after:
            source = data_info.get("source")
            query_sql = "SELECT * FROM {table_a} A WHERE TO_DAYS(add_time) BETWEEN TO_DAYS(DATE_ADD(NOW(),INTERVAL -1 MONTH)) AND TO_DAYS(NOW()) AND id=(SELECT MAX(id) FROM {table_b} B WHERE A.car_id=B.car_id)".format(table_a=source, table_b=source)
            # query_sql = "SELECT * FROM {table}".format(table=source)
            with mysql_conn.cursor(cursor=pymysql.cursors.DictCursor) as cursor:
                cursor.execute(query_sql)
                records = cursor.fetchall()
            print("============", len(records))
            MysqldbSource.package_data_list(records, data_info, input_queue)

    @staticmethod
    def package_data(data_list, data_info):
        data_dic = dict()
        data_dic["dataList"] = data_list
        data_dic["type"] = data_info.get("type")
        data_dic["table"] = data_info.get("table")
        data_dic["id_field_name"] = data_info.get("id_field_name")
        # print("package_data finish!")
        return data_dic

    @staticmethod
    def package_data_list(all_records, data_info, input_queue):
        max_len = 1000
        if len(all_records) <= max_len:
            data_dic = MysqldbSource.package_data(all_records, data_info)
            input_queue.put(data_dic)
        else:
            n = int(len(all_records)/max_len)
            start_index = 0
            for i in range(n):
                end_index = (i + 1)*max_len
                # print("{}:{}".format(start_index, end_index))
                data_list = all_records[start_index: end_index]
                start_index = end_index
                data_dic = MysqldbSource.package_data(data_list, data_info)
                input_queue.put(data_dic)
            if len(all_records) % max_len != 0:
                data_list = all_records[start_index::]
                data_dic = MysqldbSource.package_data(data_list, data_info)
                input_queue.put(data_dic)