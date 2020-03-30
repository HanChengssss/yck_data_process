import pymysql
from yck_data_process import settings
from pymongo import MongoClient
import random
from datetime import datetime


class ToolTestDriver():
    '''
    测试工具：提供各种测试用的工具
    '''
    @staticmethod
    def get_mysql_data(mysqlConn, table):
        '''
        返回制定表格中所有的数据
        :param mysqlConn:MySQL 连接
        :param table: Mysql table <String>
        :return: 数据字典列表 [dataa, datab, datac ....]
        '''
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
        '''
        将MySQL取出的数据列表，
        打包成标准格式的数据。
        :param records: 数据字典列表 [dataa, datab, datac ....]
        :param table: Mysql table <String>
        :param type: 数据所属维度，如：auto_model,...
        :return: 标准格式的数据字典
        '''
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
        '''
        将多条数据插入mongodb中
        :param mongodb:  mongodb数据库连接（已选择数据库）
        :param coll_name: mongodb中集合的名称
        :param dataDicList: 标准格式的数据字典的列表 [dataDic_a, dataDic_b, dataDic_c, ...]
        :return:
        '''
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
    def get_mongo_data(mongodb, coll_name, dataSourceTable=None):
        '''
        获取Mongodb中所有符合"isProcess": False的数据, dataSourceTable:数据归属的mysqltable
        :param mongodb: mongodb数据库连接（已选择数据库）
        :param coll_name: mongodb中集合的名称
        :return: cursor对象
        '''
        condition = {"isProcess": False}
        if dataSourceTable:
            condition["table"] = dataSourceTable
        collection = mongodb.get_collection(name=coll_name)  # 获取一个集合对象
        cursor = collection.find(condition)
        return cursor

    @staticmethod
    def get_mongo_collection(db, coll_name):
        '''
        获取mongodb中集合
        如果集合不存在则创建
        :param db: mongodb数据库连接（已选择数据库）
        :param coll_name: mongodb中集合的名称
        :return: 返回collection对象
        '''
        collList = db.collection_names()
        if coll_name not in collList:
            collection = db.create_collection(name=coll_name, **settings.mongodbCollParm)  # 创建一个集合
        else:
            collection = db.get_collection(name=coll_name)  # 获取一个集合对象
        return collection


class RandomProdictData():
    '''
    插入随机创建测试数据
    '''
    __instance = None

    def __new__(cls, coll_name):
        if not cls.__instance:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self, coll_name):
        '''
        获取一个集合对象，如果不存在则创建一个
        :param coll_name:
        '''
        self.client = MongoClient(**settings.mongoClientParams)
        self.db = self.client.get_database(settings.mongodb)
        collList = self.db.collection_names()
        if coll_name not in collList:
            self.collection = self.db.create_collection(name=coll_name)  # 创建一个集合
        else:
            self.collection = self.db.get_collection(name=coll_name)  # 获取一个集合对象

    def insert_data(self, dataNum):
        '''
        插入随机创建的数据
        :return:
        '''
        typeList = ["auto_model"]
        modelyearList = ["xx2012ss", "2098 n ", "2019", "1998 款x"]
        grarBoxList = ["xx自动ss", "半自动 n ", "全自动形式上", "电动sx马s达"]
        datas = []
        try:
            for i in range(dataNum):
                dataDict = dict()
                dataDict["processCount"] = 0
                # dataDict = deepcopy(dataDict)
                dataDict["table"] = 'autoModelTest'
                dataDict["type"] = random.choice(typeList)
                dataDict["isProcess"] = False
                dataDict["add_time"] = datetime.today()
                dataDict["update_time"] = datetime.today()
                dataDict["dataList"] = []
                for i in range(1000):
                    dataDict["dataList"].append(
                        {"model_year": random.choice(modelyearList), "gearbox": random.choice(grarBoxList)})
                datas.append(dataDict)
            ret = self.collection.insert_many(datas)
            if ret.acknowledged:
                print("插入成功！")
        finally:
            self.client.close()
