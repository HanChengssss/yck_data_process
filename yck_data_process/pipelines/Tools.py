import hashlib
import re
import pymysql
import traceback
import datetime
from yck_data_process import logingDriver
import pymongo


# 创建一个工具类，将工具函数与存储逻辑分离
class ToolSave():

    # todo 需新增一个补齐缺失字段函数，防止在批量插入的过程中因为某条数据缺失某个字段而导致整体插入失败。

    @staticmethod
    def get_filter_set(mysql_conn, table, id_field_name=None):
        '''
        :param mysql_conn: 连接
        :param id_field: 数据唯一标识字段，必须是能被转换成整形的字段
        :param table: 数据表名
        :return:返回一个过滤集合
        '''

        mysql_cursor = mysql_conn.cursor()
        # count_query = "SELECT COUNT(1) FROM {table}".format(table=table)
        # print(sql)
        # sql = "SELECT %s FROM {table}".format(table)
        # mysql_cursor.execute(count_query)
        # count = int(mysql_cursor.fetchone()[0])
        # if count > 500000:
        #     query_sql = "SELECT {id_field} FROM {table} ORDER BY add_time DESC LIMIT {count}".format(id_field=id_field_name, table=table, count=int(count/3))
        # else:
        query_sql = "SELECT {id_field} FROM {table}".format(id_field=id_field_name, table=table)
        mysql_cursor.execute(query_sql)
        model_id_list = mysql_cursor.fetchall()
        id_field_set = set()
        try:
            for m in model_id_list:
                id_field_set.add(str(m[0]))
            return id_field_set
        finally:
            mysql_cursor.close()

    @staticmethod
    def get_compare_set(mysql_conn, table, id_field_name, condition_field, condition_list):
        '''
        :param mysql_conn: 连接
        :param id_field: 数据唯一标识字段，必须是能被转换成整形的字段
        :param table: 数据表名
        :return:返回一个过滤集合
        '''

        mysql_cursor = mysql_conn.cursor()
        # count_query = "SELECT COUNT(1) FROM {table}".format(table=table)
        # print(sql)
        # sql = "SELECT %s FROM {table}".format(table)
        # mysql_cursor.execute(count_query)
        # count = int(mysql_cursor.fetchone()[0])
        # if count > 500000:
        #     query_sql = "SELECT {id_field} FROM {table} ORDER BY add_time DESC LIMIT {count}".format(id_field=id_field_name, table=table, count=int(count/3))
        # else:
        list_len = len(condition_list)
        if list_len == 1:
            query_sql = "SELECT `{id_field}` FROM `{table}` WHERE `{condition_field}`='{condition}'".format(id_field=id_field_name, table=table, condition_field=condition_field, condition=condition_list.pop())
        else:
            query_sql = "SELECT `{id_field}` FROM `{table}` WHERE `{condition_field}` IN {condition_list}".format(id_field=id_field_name, table=table, condition_field=condition_field, condition_list=tuple(condition_list))
        print("compare_set-------", query_sql)
        mysql_cursor.execute(query_sql)
        model_id_list = mysql_cursor.fetchall()
        id_field_set = set()
        try:
            for m in model_id_list:
                id_field_set.add(str(m[0]))
            return id_field_set
        finally:
            mysql_cursor.close()


    @staticmethod
    def compare_data(new_data, old_data):
        '''
        对比新旧数据的MD5值，判断是否相同
        必须要保证新旧数据字典key顺序一致
        对传入data前先对key进行排序
        :param new_data:新数据字典 {name:value,...} 没有嵌套
        :param old_data:旧数据字典 {name:value,...} 没有嵌套
        '''
        if "update_time" in new_data:
            new_data.pop("update_time")
        if "update_time" in old_data:
            old_data.pop("update_time")
        new_data_str = "".join(list(map(lambda x: str(x), list(new_data.values()))))
        old_data_str = "".join(list(map(lambda x: str(x), list(old_data.values()))))
        new_data_md5 = hashlib.md5(new_data_str.encode('utf8')).hexdigest()
        old_data_md5 = hashlib.md5(old_data_str.encode('utf8')).hexdigest()
        return new_data_md5 == old_data_md5

    @staticmethod
    def get_old_data(new_data, table_name, mysql_conn, id_field_name):
        '''
        返回与新抓下的数据相对应的旧数据
        :param new_data:新数据字典 {name:value,...} 没有嵌套
        :param table_name:MySQL table String
        :param mysql_conn:MySQL 连接
        :param id_field:该条数据的Id（唯一标识字段）名称<String>
        '''
        mysql_cursor = mysql_conn.cursor(pymysql.cursors.DictCursor)
        if "update_time" in new_data:
            new_data.pop("update_time")
        field_id = new_data[id_field_name]
        keys = '`' + "`,`".join(new_data.keys()) + '`'
        query_sql = """select {keys} from {table_name} WHERE {id_field_name}='{field_id}'""".format(keys=keys, table_name=table_name, id_field_name=id_field_name, field_id=field_id)
        try:
            mysql_cursor.execute(query_sql)
            old_data = mysql_cursor.fetchone()
            mysql_cursor.close()
            return old_data
        finally:
            mysql_cursor.close()

    @staticmethod
    def sort_item(data):
        '''
        将字典的键按升序排列
        :param data:数据字典 {name:value,...} 没有嵌套
        :return:返回排列好的数据
        '''
        data = dict(sorted(data.items(), key=lambda item: item[0], reverse=False))
        return data

    @staticmethod
    def test_exist(id_field, id_field_set):
        '''
        检测id_field是否存在id_field_set中
        存在返回True
        不存在返回False
        注意字段类型需要保持一致
        :param id_field: 检测字段，必须能被转换成整形
        :param id_field_set: 检测集合
        :return: boolean
        '''

        if str(id_field) not in id_field_set:
            id_field_set.add(id_field)
            return False
        else:
            return True

    # todo 更新后返回的状态待完善
    @staticmethod
    def update_is_process_status(db_mange, data_id, coll_name):
        '''
        更新MongoDB中已处理数据的状态：
        isProcess: True, processCount+1
        :param mongodb: mongodb数据库连接（已选择数据库）
        :param data_id: 一条doc的id
        :param coll_name: mongodb中集合的名称
        :return:
        '''
        mongo_conn = pymongo.MongoClient(**db_mange.get_mongo_client_params())
        mongodb = mongo_conn.get_database(db_mange.get_mongodb())
        collection = mongodb.get_collection(coll_name)
        ret = collection.update_one({"_id": data_id}, {"$set": {"isProcess": True}, "$inc": {"processCount": 1}})
        print("pymongo 更新成功！")
        mongo_conn.close()

    @staticmethod
    def update_mysql_one(mysql_conn, item, table, id_field_name, sm_instance):
        '''
        更新车型库中有变化的一条数据
        :param mysql_conn: MySQL 连接
        :param item: 数据字典（可能有嵌套）
        :param table: Mysql table <String>
        :param id_field: 该条数据的Id（唯一标识字段）名称<String>
        :return:
        '''
        if "data" in item:
            data = item["data"]
        else:
            data = item
        if "id" in data:
            data.pop("id")
        print("update data:", data)
        keys = "`" + "`=%s,`".join(data.keys()) + "`=%s"
        sql = 'UPDATE {table} SET {keys} WHERE {id_field} = "{filedId}"'.format(table=table, keys=keys, id_field=id_field_name, filedId=data[id_field_name])
        cursor = mysql_conn.cursor()
        try:
            if cursor.execute(sql, tuple(data.values())):
                mysql_conn.commit()

        except Exception as e:
            mysql_conn.rollback()
            ToolSave.log_error_data(item, table, str(e), sm_instance)
        finally:
            cursor.close()

    @staticmethod
    def update_mysql_many(mysql_conn, data_list, table, id_field_name, sm_instance):
        '''
        :param mysql_conn: MySQL 连接
        :param dataList: 包含多条数据的列表 [itemA, itemB, itemC ...]
        :param table: Mysql table <String>
        :param id_field: 该条数据的Id（唯一标识字段）名称<String>
        :return:
        '''
        if not data_list:
            return
        for item in data_list:
            ToolSave.update_mysql_one(mysql_conn, item, table, id_field_name, sm_instance)
        print("update_mysql finish!")

    @staticmethod
    def insert_mysql_one(mysql_conn, item, table, sm_instance):
        '''
        插入一条数据到mysql
        :param mysql_conn: MySQL 连接
        :param item: 数据字典（可能有嵌套）
        :param table: Mysql table <String>
        :return:
        '''
        cursor = mysql_conn.cursor()
        if "data" in item:
            data = item["data"]
        else:
            data = item

        keys = '`' + "`,`".join(data.keys()) + '`'
        values = ",".join(["%s"] * len(data))
        sql = 'INSERT INTO {table} ({keys}) VALUES ({values})'.format(table=table, keys=keys, values=values)
        # print(sql)
        print("insert data:", data)
        try:
            # raise Exception
            if cursor.execute(sql, tuple(data.values())):
                mysql_conn.commit()
                # print("保存成功！")
        except Exception as e:
            mysql_conn.rollback()
            ToolSave.log_error_data(item, table, str(e), sm_instance)
        finally:
            cursor.close()

    @staticmethod
    def insert_mysql_many(mysql_conn, data_list, table, sm_instance, hp=False):
        '''
        批量插入MySQL数据库
        两种模式：普通/高性能
        普通：一次插入1条
        高性能：一次插入多条（使用时出现pymysql.err.ProgrammingError: (1064, ''),目前还没有解决）
        :param mysql_conn:
        :param data_list:
        :param table:
        :param hp: boolean(是否高性能)
        :return:
        '''
        if not hp:
            for item in data_list:
                ToolSave.insert_mysql_one(mysql_conn, item, table, sm_instance)
        # else:
        #     cursor = mysql_conn.cursor()
        #     if not dataList:
        #         cursor.close()
        #         return
        #     item = dataList[0]
        #     if "data" in item:
        #         data = item["data"]
        #     else:
        #         data = item
        #     dataLen = len(data)
        #     print(dataLen)
        #     keys = ",".join(data.keys())
        #     values = ",".join(["%s"] * len(data))
        #     bulkdata = []
        #     errorList = []
        #     for item in dataList:
        #         data = item["data"]  # todo
        #         # print("len(data)", len(data))
        #         data["add_time"] = ToolSave.dt_to_str(data["add_time"])
        #         data["update_time"] = ToolSave.dt_to_str(data["update_time"])
        #         if len(data) != dataLen:
        #             errorList.append(data["model_id"])
        #         bulkdata.append(tuple(data.values()))
        #     # values = re.sub(r'\[|\]', "", str(bulkdata))
        #     print(errorList)
        #     sql = 'INSERT INTO {table} ({keys}) VALUES {values}'.format(table=table, keys=keys, values=values)
        #     print(sql)
        #     try:
        #         # cursor.execute(sql)
        #         cursor.executemany(sql, bulkdata)
        #         mysql_conn.commit()
        #     except Exception as e:
        #         mysql_conn.rollback()
        #         print("保存失败！")
        #
        #         traceback.print_exc()
        #     finally:
        #         cursor.close()

    @staticmethod
    def dt_to_str(dt_object):
        '''
        将日期类型转换成<String>
        'xxxx(year)-xx(month)-xx(day)'
        :param dt_object: <class datetime.datetime>
        :return: <String>
        '''
        if isinstance(dt_object, datetime.datetime):
            return dt_object.strftime("%Y-%m-%d")
        return dt_object

    @staticmethod
    def log_error_data(item, table, error_msg, sm_instance):
        '''
        记录更新失败和插入失败的数据
        将失败的原因记录在dataError.log
        中，将错误数据插入mongodb中的error集合
        :param item: 数据字典（可能有嵌套）
        :param table: Mysql table <String>
        :param error_msg: 错误原因 <String>
        :return:
        '''
        db_manage = sm_instance.get_db_setting_instance()
        log_path_manage = sm_instance.get_log_setting_instance()
        log_dir_full_Path = log_path_manage.get_log_dir_full_path()
        log = logingDriver.Logger(filename="{}\dataError.log".format(log_dir_full_Path), level='error')
        log.logger.error("{} 的数据存储失败，错误信息{}".format(table, error_msg))
        mongo_conn = pymongo.MongoClient(**db_manage.get_mongo_client_params())
        db = mongo_conn.get_database(db_manage.get_mongodb())
        ToolSave.insert_mongo_one(db, "error", item, table, "error", sm_instance)
        mongo_conn.close()

    @staticmethod
    def insert_mongo_one(mongodb, coll_name, item, table, type, sm_instance):
        '''
        将一条doc插入mongodb
        :param mongodb: mongodb数据库连接（已选择数据库）
        :param coll_name: mongodb中集合的名称
        :param item: 数据字典（可能有嵌套）
        :param table: Mysql table <String>
        :return:
        '''
        collection = ToolSave.get_mongo_collection(mongodb, coll_name, sm_instance)
        data_dic = ToolSave.package_data(item, table, type=type)
        try:
            collection.insert(data_dic)
        finally:
            pass

    @staticmethod
    def get_mongo_collection(db, coll_name, sm_instance):
        '''
        获取mongodb中集合
        如果集合不存在则创建
        :param db: mongodb数据库连接（已选择数据库）
        :param coll_name: mongodb中集合的名称
        :return: 返回collection对象
        '''
        db_manage = sm_instance.get_db_setting_instance()

        coll_list = db.collection_names()

        if coll_name not in coll_list:
            collection = db.create_collection(name=coll_name, **db_manage.get_creat_mongodb_coll_parm())  # 创建一个集合
        else:
            collection = db.get_collection(name=coll_name)  # 获取一个集合对象
        return collection

    @staticmethod
    def package_data(item, table, type):
        data_dic = dict()
        data_list = []
        data_dic["dataList"] = data_list
        data_dic["isProcess"] = False
        data_dic["processCount"] = 0
        data_dic["type"] = type
        data_dic["table"] = table
        data_list.append(item)
        print("package_data finish!")
        return data_dic


class StandardDataStructure():
    def __init__(self):
        self.__data_dic = {
            # "isProcess": False,
            # "table": "",
            # "type": "",
            # "dataList": []
        }

    def set_value(self, key, value):
        self.__data_dic[key] = value

    def test(self, data_dic):
        standard_type = {"isProcess": bool, "table": str, "dataList": list, "type": str}
        for filed in standard_type:
            if filed not in data_dic:
                raise Exception(f"data_dict is not standard, {filed} no exist!")
            if not isinstance(self.__data_dic.get(filed), standard_type.get(filed)):
                raise Exception(f"{filed} type no standard! it should be {standard_type.get(filed)}")

    def get_data(self):
        self.test(self.__data_dic)
        return self.__data_dic