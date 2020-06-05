import pymysql


class MysqldbSource():

    @staticmethod
    def input_data(input_queue, sm_instance, dps_instance):
        db_setting = sm_instance.get_db_setting_instance()
        db_params = db_setting.get_save_mysql_normal_params()
        mysql_conn = pymysql.connect(**db_params)
        coll_names = dps_instance.get_coll_name_list()
        for coll in coll_names:
            query_sql = "SELECT * FROM {} WHERE id IN (SELECT MAX(id) AS m_id FROM {} WHERE TO_DAYS(add_time) BETWEEN TO_DAYS(DATE_ADD(NOW(), INTERVAL - 1 WEEK)) AND TO_DAYS(NOW()) GROUP BY car_id);".format(coll, coll)
            with mysql_conn.cursor(cursor=pymysql.cursors.DictCursor) as cursor:
                cursor.execute(query_sql)
                records = cursor.fetchall()
            print("============", len(records))
            table = dps_instance.get_table_name(coll)
            id_field_name = dps_instance.get_id_field_name(coll)
            data_info = {
                "coll_name": coll,
                "table": table,
                "id_field_name": id_field_name,
                "source_type": dps_instance.source_type
            }
            MysqldbSource.package_data_list(records, data_info, input_queue)

    @staticmethod
    def package_data(data_list, data_info):
        data_dic = dict()
        data_dic["dataList"] = data_list
        data_dic["coll_name"] = data_info.get("coll_name")
        data_dic["table"] = data_info.get("table")
        data_dic["id_field_name"] = data_info.get("id_field_name")
        data_dic["source_type"] = data_info.get("source_type")
        # print("package_data finish!")
        return data_dic

    @staticmethod
    def package_data_list(all_records, data_info, input_queue):
        max_len = 1000
        if len(all_records) == 0:
            return
        elif len(all_records) <= max_len:
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