import hashlib
import re
import pymysql
import traceback
import datetime
from yck_data_process import logingDriver
import pymongo
from yck_data_process.settingsManage import SettingsManage, MODEL

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
    def get_old_data(new_data, table_name, mysqlConn, idField):
        '''
        返回与新抓下的数据相对应的旧数据
        :param new_data:新数据字典 {name:value,...} 没有嵌套
        :param table_name:MySQL table String
        :param mysqlConn:MySQL 连接
        :param idField:该条数据的Id（唯一标识字段）名称<String>
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
    def sort_item(data):
        '''
        将字典的键按升序排列
        :param data:数据字典 {name:value,...} 没有嵌套
        :return:返回排列好的数据
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
        :param mongodb: mongodb数据库连接（已选择数据库）
        :param data_id: 一条doc的id
        :param coll_name: mongodb中集合的名称
        :return:
        '''
        collection = mongodb.get_collection(coll_name)
        ret = collection.update_one({"_id": data_id}, {"$set": {"isProcess": True}, "$inc": {"processCount": 1}})
        print("pymongo 更新成功！")

    @staticmethod
    def update_mysql_one(mysqlConn, item, table, idField):
        '''
        更新车型库中有变化的一条数据
        :param mysqlConn: MySQL 连接
        :param item: 数据字典（可能有嵌套）
        :param table: Mysql table <String>
        :param idField: 该条数据的Id（唯一标识字段）名称<String>
        :return:
        '''
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

        except Exception as e:
            mysqlConn.rollback()
            ToolSave.log_error_data(item, table, str(e))
        finally:
            cursor.close()

    @staticmethod
    def update_mysql_many(mysqlConn, dataList, table, idField):
        '''
        :param mysqlConn: MySQL 连接
        :param dataList: 包含多条数据的列表 [itemA, itemB, itemC ...]
        :param table: Mysql table <String>
        :param idField: 该条数据的Id（唯一标识字段）名称<String>
        :return:
        '''
        if not dataList:
            return
        for item in dataList:
            ToolSave.update_mysql_one(mysqlConn, item, table, idField)
        print("update_mysql finish!")

    @staticmethod
    def insert_mysql_one(mysqlConn, item, table):
        '''
        插入一条数据到mysql
        :param mysqlConn: MySQL 连接
        :param item: 数据字典（可能有嵌套）
        :param table: Mysql table <String>
        :return:
        '''
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
        # else:
        #     cursor = mysqlConn.cursor()
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
        #         mysqlConn.commit()
        #     except Exception as e:
        #         mysqlConn.rollback()
        #         print("保存失败！")
        #
        #         traceback.print_exc()
        #     finally:
        #         cursor.close()

    @staticmethod
    def dt_to_str(dtObject):
        '''
        将日期类型转换成<String>
        'xxxx(year)-xx(month)-xx(day)'
        :param dtObject: <class datetime.datetime>
        :return: <String>
        '''
        if isinstance(dtObject, datetime.datetime):
            return dtObject.strftime("%Y-%m-%d")
        return dtObject

    @staticmethod
    def log_error_data(item, table, errorMsg):
        '''
        记录更新失败和插入失败的数据
        将失败的原因记录在dataError.log
        中，将错误数据插入mongodb中的error集合
        :param item: 数据字典（可能有嵌套）
        :param table: Mysql table <String>
        :param errorMsg: 错误原因 <String>
        :return:
        '''
        sm = SettingsManage(model=MODEL)
        dbManage = sm.get_dbSettingInstance()
        logPathManage = sm.get_logSettingsInstance()
        logDirFullPath = logPathManage.get_logDirFullPath()

        log = logingDriver.Logger(filename="{}\dataError.log".format(logDirFullPath), level='error')
        log.logger.error("{} 的数据存储失败，错误信息{}".format(table, errorMsg))

        mongoConn = pymongo.MongoClient(**dbManage.get_mongoClientParams())
        db = mongoConn.get_database(dbManage.get_mongodb())
        ToolSave.insert_mongo_one(db, "error", item, table)
        c = db.get_collection()
        c.insert()
        mongoConn.close()

    @staticmethod
    def insert_mongo_one(mongodb, coll_name, item, table):
        '''
        将一条doc插入mongodb
        :param mongodb: mongodb数据库连接（已选择数据库）
        :param coll_name: mongodb中集合的名称
        :param item: 数据字典（可能有嵌套）
        :param table: Mysql table <String>
        :return:
        '''
        collection = ToolSave.get_mongo_collection(mongodb, coll_name)
        dataDic = ToolSave.package_data(item, table, type="auto_model")
        try:
            collection.insert(dataDic)
        finally:
            pass

    @staticmethod
    def get_mongo_collection(db, coll_name):
        '''
        获取mongodb中集合
        如果集合不存在则创建
        :param db: mongodb数据库连接（已选择数据库）
        :param coll_name: mongodb中集合的名称
        :return: 返回collection对象
        '''
        sm = SettingsManage(model=MODEL)
        dbManage = sm.get_dbSettingInstance()

        collList = db.collection_names()

        if coll_name not in collList:
            collection = db.create_collection(name=coll_name, **dbManage.get_creatMongodbCollParm())  # 创建一个集合
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