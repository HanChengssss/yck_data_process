import pymongo
from pymongo import MongoClient
import random
from yck_data_process.settings import auto_model_tables
from datetime import datetime
from multiprocessing import Queue

class RandomProdictData():
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
        self.client = MongoClient('localhost', 27017)
        self.db = self.client.get_database("test")
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
        for i in range(dataNum):
            dataDict = dict()
            # dataDict = deepcopy(dataDict)
            dataDict["table"] = random.choice(auto_model_tables)
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
        # ret.acknowledged 布尔值
        # ret.inserted_ids 插入数据的id列表



class queryMongoData():
    __instance = None

    def __new__(cls, coll_name):
        if not cls.__instance:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self, coll_name):
        self.client = MongoClient('localhost', 27017)
        self.db = self.client.get_database("test")
        collList = self.db.collection_names()
        if coll_name not in collList:
            collParm = dict(
                capped=True,
                size=1024*1024*50,
                max=1000000
            )
            self.collection = self.db.create_collection(name=coll_name, **collParm)  # 创建一个集合
        else:
            self.collection = self.db.get_collection(name=coll_name)  # 获取一个集合对象

    def find_data(self):
        '''
        查询mongodb中所有未处理的数据
        取出后将isProcess字段更新为True
        :return:
        '''
        cursor = self.collection.find({"isProcess": False})
        idList = []
        dataList = []
        for data in cursor:
            idList.append(data["_id"])
            dataList.append(data)
        ret = self.collection.update_many({"_id": {'$in': idList}, "isProcess": False}, {'$set': {"isProcess": True}})
        print(ret.modified_count)
        # self.client.close()
        return dataList

    def chongzhi(self):
        '''
        重置mongodb中的书数据状态
        取出后将isProcess字段更新为False
        :return:
        '''
        cursor = self.collection.find({"isProcess": True})
        idList = []
        dataList = []
        for data in cursor:
            idList.append(data["_id"])
            dataList.append(data)
        ret = self.collection.update_many({"_id": {'$in': idList}, "isProcess": True}, {'$set': {"isProcess": False}})
        print(ret.modified_count)
        # self.client.close()
        return dataList

class ProductQueue():
    '''
    将数据放入队列中
    '''

    def putDataToQueue(self, dataList):
        inputQueue = Queue()
        for data in dataList:
            inputQueue.put(data)
        return inputQueue


class InputDataMange():
    '''
    返回数据队列
    '''
    def run(self):
        try:
            self.qm = queryMongoData("autoModelCollection")
            self.pq = ProductQueue()
            dataList = self.qm.find_data()
            inputQueue = self.pq.putDataToQueue(dataList)
            return inputQueue
        finally:
            print("inputQueue finish")


if __name__ == '__main__':
    # R = RandomProdictData(coll_name='autoModelCollection')
    # R.insert_data(dataNum=1000)
    q = queryMongoData("autoModelCollection")
    # q.find_data()
    q.chongzhi()
    In = InputDataMange()
    In.run()

