# !/usr/bin/env python
# -*-encoding: utf-8-*-
# author:Hancheng
# version:0.1
import pymysql
from yck_data_process.logingDriver import *
from yck_data_process.settings import mongodb, dbparams
import re
import pymysql
from yck_data_process.logingDriver import Logger
import pymongo
from yck_data_process.input_data import InputDataMange
import re
import hashlib


class OutPutDataManage():

    def dataOutput(self, outputQueue):
        conn = pymysql.connect(**dbparams)
        log = Logger(filename="D:\YCK\代码\yck_data_process\yck_data_process\log_dir\outoutData.log", level='error')
        mongoConn = pymongo.MongoClient(host="localhost", port=27017)
        db = mongoConn.get_database(mongodb)
        try:
            while True:
                datas = outputQueue.get()
                if datas == 'end':
                    print("data_output is end !")
                    conn.close()
                    break
                try:
                    type = datas.get("type")

                    dataList = datas.get("dataList")
                    if type == "auto_model":
                        updateList = []
                        insertList = []

                        for item in dataList:

                            AutoModelPipeline.process_item(item=item,updateList=updateList, insertList=insertList,mysqlConn=conn, )

                except Exception as e:
                    log.logger.error(e)
        finally:
            conn.close()
            mongoConn.close()

    def insert_to_mysql(self, dataDic, conn, mongodb):
        # 将多条数据拼接成一条sql再执行比使用executemany的效率提高将近1倍
        try:
            conn.ping()
            cursor = conn.cursor()
            table = dataDic['table']
            dataList = dataDic["dataList"]
            data = dataList[0]
            bulkdata = []
            for data in dataList:
                data = self.sort_item(data)
                bulkdata.append(tuple(data.values()))
            keys = ",".join(data.keys())
            values = re.sub(r'\[|\]', "", str(bulkdata))
            sql = 'INSERT INTO {table} ({keys}) VALUES {values}'.format(table=table, keys=keys, values=values)
            cursor.execute(sql)
            conn.commit()
            cursor.close()
            coll_name = dataDic.get("coll_name")
            self.update_mongodb(mongodb, dataDic['_id'], coll_name)
            print("保存成功！")
        except:
            conn.rollback()
            raise

    def update_mongodb(self, mongodb, data_id, coll_name):
        collection = mongodb.get_collection(coll_name)
        ret = collection.update_one({"_id": data_id}, {"$set": {"isProcess": True}, "$inc": {"processCount": 1}})
        print("pymongo 更新成功！")

    def sort_item(self, data):
        '''
        对字典中的key进行排序，保证每个字典的key顺序一致
        :param data:
        :return:
        '''
        data = dict(sorted(data.items(), key=lambda item: item[0], reverse=False))
        return data


# config_autohome_major_info_tmp
class AutoModelPipeline(object):
    @staticmethod
    def process_item(item, updateList, insertList, idFieldSet, mysqlConn):
        '''
        车型库更新逻辑
        只负责把不同存储逻辑的数据进行
        分类不作任何修改数据库的操作。
        --------------------------
        分类逻辑：
        首先判断该条数据是否已存在
        如果不存在加入到insertList
        否则，判断数据是否出现变化
        如果有变化：将数据加入到
        updateList
        如果没变化：抛弃
        :param item: 一条车型数据
        :param updateList:待更新列表
        :param insertList:待插入列表
        :param idFieldSet:过滤集合
        :param mysqlConn:数据库连接
        :return:
        '''
        data = item["data"]
        model_id = data.get("model_id")
        ret = ToolSave.test_exist(idField=model_id, idFieldSet=idFieldSet)
        table = "config_autohome_major_info_tmp"
        item["table"] = table
        if ret:
            data.pop("add_time")
            update_time = data.pop("update_time")
            new_data = ToolSave.sort_item(data)
            old_data = ToolSave.get_old_data(new_data=data, table_name=table, mysqlConn=mysqlConn, idField="model_id")
            old_data = ToolSave.sort_item(old_data)
            compare_ret = ToolSave.compare_data(new_data=new_data, old_data=old_data)
            if not compare_ret:
                data["update_time"] = update_time
                item["idField"] = "model_id"
                updateList.append(item)
            else:
                print("数据无变化！")
        else:
            insertList.append(item)
    


# 创建一个工具类，将工具函数与存储逻辑分离
class ToolSave():
    @staticmethod
    def get_filter_set(mysqlCursor, idField, table):
        '''
        :param Mysqlcursor: 句柄
        :param idField: 数据唯一标识字段，必须是能被转换成整形的字段
        :param table: 数据表名
        :return:返回一个过滤集合
        '''
        sql = "SELECT {idField} FROM {table}".format(idField, table)
        mysqlCursor.execute(sql)
        model_id_list = mysqlCursor.fetchall()
        idFieldSet = set()
        for m in model_id_list:
            idFieldSet.add(int(m.get(idField)))
        mysqlCursor.close()
        return idFieldSet

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
        mysqlCursor = mysqlConn.cursor()
        if "update_time" in new_data:
            new_data.pop("update_time")
        FieldId = new_data[idField]
        keys = ','.join(new_data.keys())
        query_sql = """select {keys} from {table_name} WHERE {idField}={FieldId}""".format(keys=keys, table_name=table_name, idField=idField, FieldId=FieldId)
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

        if int(idField) not in idFieldSet:
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
    def update_mysql(mysqlConn, data, table, idField):

        keys = "=%s,".join(data.keys()) + "=%s"
        sql = 'UPDATE {table} SET {keys} WHERE {idField} = "{filedId}"'.format(table=table, keys=keys, idField=idField, filedId=data[idField])
        cursor = mysqlConn.cursor()
        try:
            if cursor.execute(sql, tuple(data.values())):
                mysqlConn.commit()
                print("update_mysql finish!")
        except:
            mysqlConn.rollback()
            raise
        finally:
            cursor.close()

    @staticmethod
    def foo():
        pass



if __name__ == '__main__':
    pass


