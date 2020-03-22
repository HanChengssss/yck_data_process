import hashlib
import re
import pymysql
import traceback
import datetime
from yck_data_process import logingDriver
# from pipelinesTestDriver import ToolTestDriver
import pymongo
from yck_data_process import settings
# 创建一个工具类，将工具函数与存储逻辑分离
class ToolSave():

    # todo 需新增一个补齐缺失字段函数，防止在批量插入的过程中因为某条数据缺失某个字段而导致整体插入失败。

    @staticmethod
    def get_filter_set(mysqlConn, table, idField=None):
        '''
        :param mysqlConn: 连接
        :param idField: 数据唯一标识字段，必须是能被转换成整形的字段
        :param table: 数据表名
        :return:返回一个过滤集合
        '''

        mysqlCursor = mysqlConn.cursor()
        sql = "SELECT {idField} FROM {table}".format(idField=idField, table=table)
        # sql = "SELECT %s FROM {table}".format(table)
        mysqlCursor.execute(sql)
        model_id_list = mysqlCursor.fetchall()
        idFieldSet = set()
        try:
            for m in model_id_list:
                idFieldSet.add(str(m[0]))
            return idFieldSet
        finally:
            mysqlCursor.close()

    @staticmethod
    def compare_data(new_data, old_data):
        '''
        对比新旧数据的MD5值，判断是否相同
        必须要保证新旧数据字典key顺序一致
        对传入data前先对key进行排序
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
    def get_old_data(new_data, table_name, mysqlConn, idField):
        '''
        返回与新抓下的数据相对应的旧数据
        '''
        mysqlCursor = mysqlConn.cursor(pymysql.cursors.DictCursor)
        if "update_time" in new_data:
            new_data.pop("update_time")
        FieldId = new_data[idField]
        keys = ','.join(new_data.keys())
        query_sql = """select {keys} from {table_name} WHERE {idField}='{FieldId}'""".format(keys=keys, table_name=table_name, idField=idField, FieldId=FieldId)
        try:
            mysqlCursor.execute(query_sql)
            old_data = mysqlCursor.fetchone()
            mysqlCursor.close()
            return old_data
        finally:
            mysqlCursor.close()

    @staticmethod
    def get_old_data_many(updateList, table_name, mysqlConn, idField):
        for item in updateList:
            new_data = item["data"]
            if "update_time" in new_data:
                new_data.pop("update_time")
        # todo 待完善


    @staticmethod
    def sort_item(data):
        '''
        将字典的键按降序排列
        :param data:
        :return:
        '''
        data = dict(sorted(data.items(), key=lambda item: item[0], reverse=False))
        return data

    @staticmethod
    def test_exist(idField, idFieldSet):
        '''
        检测idField是否存在idFieldSet中
        存在返回True
        不存在返回False
        注意字段类型需要保持一致
        :param idField: 检测字段，必须能被转换成整形
        :param idFieldSet: 检测集合
        :return: boolean
        '''

        if str(idField) not in idFieldSet:
            return False
        else:
            return True

    # todo 更新后返回的状态待完善
    @staticmethod
    def update_mongodb(mongodb, data_id, coll_name):
        '''
        更新MongoDB中已处理数据的状态：
        isProcess: True, processCount+1
        :param mongodb:
        :param data_id:
        :param coll_name:
        :return:
        '''
        collection = mongodb.get_collection(coll_name)
        ret = collection.update_one({"_id": data_id}, {"$set": {"isProcess": True}, "$inc": {"processCount": 1}})
        print("pymongo 更新成功！")

    @staticmethod
    def update_mysql_one(mysqlConn, item, table, idField):
        if "data" in item:
            data = item["data"]
        else:
            data = item
        keys = "=%s,".join(data.keys()) + "=%s"
        sql = 'UPDATE {table} SET {keys} WHERE {idField} = "{filedId}"'.format(table=table, keys=keys, idField=idField, filedId=data[idField])
        cursor = mysqlConn.cursor()
        try:
            if cursor.execute(sql, tuple(data.values())):
                mysqlConn.commit()
                print("update_mysql finish!")
        except Exception as e:
            mysqlConn.rollback()
            print("保存失败！")
            print(e)
        finally:
            cursor.close()

    @staticmethod
    def update_mysql_many(mysqlConn, dataList, table, idField):
        for item in dataList:
            ToolSave.update_mysql_one(mysqlConn, item, table, idField)

    @staticmethod
    def insert_mysql_one(mysqlConn, item, table):
        cursor = mysqlConn.cursor()
        if "data" in item:
            data = item["data"]
        else:
            data = item

        keys = ",".join(data.keys())
        values = ",".join(["%s"] * len(data))
        sql = 'INSERT INTO {table} ({keys}) VALUES ({values})'.format(table=table, keys=keys, values=values)
        try:
            # raise Exception
            if cursor.execute(sql, tuple(data.values())):
                mysqlConn.commit()
                # print("保存成功！")
        except Exception as e:
            mysqlConn.rollback()
            ToolSave.log_error_data(item, table, str(e))
        finally:
            cursor.close()

    @staticmethod
    def insert_mysql_many(mysqlConn, dataList, table, hp=False):
        '''
        批量插入MySQL数据库
        两种模式：普通/高性能
        普通：一次插入1条
        高性能：一次插入多条（使用时出现pymysql.err.ProgrammingError: (1064, ''),目前还没有解决）
        :param mysqlConn:
        :param dataList:
        :param table:
        :param hp: boolean(是否高性能)
        :return:
        '''
        if not hp:
            for item in dataList:
                ToolSave.insert_mysql_one(mysqlConn, item, table)
        else:
            cursor = mysqlConn.cursor()
            if not dataList:
                cursor.close()
                return
            item = dataList[0]
            if "data" in item:
                data = item["data"]
            else:
                data = item
            dataLen = len(data)
            print(dataLen)
            keys = ",".join(data.keys())
            values = ",".join(["%s"] * len(data))
            bulkdata = []
            errorList = []
            for item in dataList:
                data = item["data"]  # todo
                # print("len(data)", len(data))
                data["add_time"] = ToolSave.dt_to_str(data["add_time"])
                data["update_time"] = ToolSave.dt_to_str(data["update_time"])
                if len(data) != dataLen:
                    errorList.append(data["model_id"])
                bulkdata.append(tuple(data.values()))
            # values = re.sub(r'\[|\]', "", str(bulkdata))
            print(errorList)
            sql = 'INSERT INTO {table} ({keys}) VALUES {values}'.format(table=table, keys=keys, values=values)
            print(sql)
            try:
                # cursor.execute(sql)
                cursor.executemany(sql, bulkdata)
                mysqlConn.commit()
            except Exception as e:
                mysqlConn.rollback()
                print("保存失败！")

                traceback.print_exc()
            finally:
                cursor.close()

    @staticmethod
    def dt_to_str(dtObject):
        if isinstance(dtObject, datetime.datetime):
            return dtObject.strftime("%Y-%m-%d")
        return dtObject


    @staticmethod
    def log_error_data(item, table, errorMsg):
        log = logingDriver.Logger(filename="D:\YCK\代码\yck_data_process\yck_data_process\log_dir\dataError.log", level='error')
        log.logger.error("{} 的数据存储失败，错误信息{}".format(table, errorMsg))
        mongoDic = dict(
            host="localhost",
            port=27017
        )
        mongoConn = pymongo.MongoClient(**mongoDic)
        db = mongoConn.get_database(settings.mongodb)

        ToolSave.insert_mongo_one(db, "error", item, table)
        c = db.get_collection()
        c.insert()

        mongoConn.close()

    @staticmethod
    def insert_mongo_one(mongodb, coll_name, item, table):
        collection = ToolSave.get_mongo_collection(mongodb, coll_name)
        dataDic = ToolSave.package_data(item, table, type="auto_model")
        try:
            ret = collection.insert(dataDic)
            print(ret)
        finally:
            pass

    @staticmethod
    def get_mongo_collection(db, coll_name):
        collList = db.collection_names()

        if coll_name not in collList:
            collection = db.create_collection(name=coll_name, **settings.mongodbCollParm)  # 创建一个集合
        else:
            collection = db.get_collection(name=coll_name)  # 获取一个集合对象
        return collection

    @staticmethod
    def package_data(item, table, type):
        dataDic = dict()
        dataList = []
        dataDic["dataList"] = dataList
        dataDic["isProcess"] = False
        dataDic["processCount"] = 0
        dataDic["type"] = type
        dataDic["table"] = table
        dataList.append(item)
        print("package_data finish!")
        return dataDic