from pymongo import MongoClient
import pymysql
from yck_data_process import settings
from multiprocessing import Queue
from yck_data_process.output_data import OutPutDataManage


class ToolTestDriver():
    @staticmethod
    def get_mysql_data(mysqlConn, table):
        cursor = mysqlConn.cursor(pymysql.cursors.DictCursor)
        print("==========table", table)
        try:
            sql = "SELECT * FROM {TABLE}".format(TABLE=table)
            cursor.execute(sql)
            records = cursor.fetchall()
            print("get_mysql_data finish!")
            return records
        finally:
            cursor.close()

    @staticmethod
    def package_data(records, table, type):
        dataDic = dict()
        dataList = []
        dataDic["dataList"] = dataList
        dataDic["isProcess"] = False
        dataDic["processCount"] = 0
        dataDic["type"] = type
        dataDic["table"] = table
        for data in records:
            if "id" in data:
                data.pop("id")
            item = dict()
            item["data"] = data
            dataList.append(item)
        print("package_data finish!")
        return dataDic

    @staticmethod
    def insert_mongo_many(mongodb, coll_name, dataDicList):
        collection = ToolTestDriver.get_mongo_collection(mongodb, coll_name)
        try:
            ret = collection.insert_many(dataDicList)
            if ret.acknowledged:
                print("插入成功！")
            else:
                print("插入失败！")
        finally:
            pass

    @staticmethod
    def get_mongo_data(mongodb, coll_name):
        collection = mongodb.get_collection(name=coll_name)  # 获取一个集合对象
        cursor = collection.find({"isProcess": False})
        return cursor

    @staticmethod
    def get_mongo_collection(db, coll_name):
        collList = db.collection_names()

        if coll_name not in collList:
            collection = db.create_collection(name=coll_name, **settings.mongodbCollParm)  # 创建一个集合
        else:
            collection = db.get_collection(name=coll_name)  # 获取一个集合对象
        return collection



class AutoModelTestDriver():
    '''
    测试逻辑
    先将测试数据库中的车型库数据导入mongod
    '''
    @staticmethod
    def autodata_input_mongo():
        '''
        先将测试数据库中的车型库数据导入mongod
        '''
        mysqlConn = pymysql.connect(**settings.testMysqlParams)
        mongoConn = MongoClient('localhost', 27017)
        db = mongoConn.get_database(settings.mongodb)
        dataDicList = []
        for table in settings.auto_model_tables:
            records = ToolTestDriver.get_mysql_data(mysqlConn=mysqlConn, table=table)
            dataList = []
            for data in records:
                dataList.append(data)
                if len(dataList) >= 1000:
                    dataDic = ToolTestDriver.package_data(records=dataList, table=table, type="auto_model")
                    dataDicList.append(dataDic)
                    dataList.clear()
            if dataList:
                dataDic = ToolTestDriver.package_data(records=dataList, table=table, type="auto_model")
                dataDicList.append(dataDic)
                dataList.clear()

            if len(dataDicList) >= 10:
                ToolTestDriver.insert_mongo_many(mongodb=db, coll_name="autoModelCollection", dataDicList=dataDicList)
                dataDicList.clear()
        if dataDicList:
            ToolTestDriver.insert_mongo_many(mongodb=db, coll_name="autoModelCollection", dataDicList=dataDicList)
            dataDicList.clear()
        mysqlConn.close()
        mongoConn.close()

    @staticmethod
    def put_data_queue(mongodb, coll_name):
        '''
        将读取到的数据添加到队列中
        :param mongodb:
        :param coll_name:
        :return:
        '''
        q = Queue()
        qCount = 0
        cursor = ToolTestDriver.get_mongo_data(mongodb, coll_name)
        for dataDic in cursor:
            qCount += 1
            q.put(dataDic)
        q.put("end")
        cursor.close()
        return q

    @staticmethod
    def test_driver():
        mongoConn = MongoClient('localhost', 27017)
        db = mongoConn.get_database(settings.mongodb)
        q = AutoModelTestDriver.put_data_queue(db, settings.mongodbCollNameDict.get("auto_model"))
        OutPutDataManage.dataOutput(q)


if __name__ == '__main__':
    # AutoModelTestDriver.autodata_input_mongo()
    '''
    mysql高性能模式存在bug,猜测是由于有个别数据出现键值对不同的情况。
    '''
    AutoModelTestDriver.test_driver()












