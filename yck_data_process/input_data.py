import pymongo
from pymongo import MongoClient
import random
from yck_data_process.settings import auto_model_tables, mongodb
from datetime import datetime
from multiprocessing import Queue
from yck_data_process.settings import collNameList, collParm

class RandomProdictData():
    '''
    插入测试数据
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
        self.client = MongoClient('localhost', 27017)
        self.db = self.client.get_database(mongodb)
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
        # ret.acknowledged 布尔值
        # ret.inserted_ids 插入数据的id列表


class InputDataMange():

    def input_data(self, inputQueue):
        '''
        初始化mongodb连接
        加载待查询的collection
        查询数据
        将数据添加到队列
        :return:
        '''
        # 创建集合的配置
        client = MongoClient('localhost', 27017)
        try:
            db = client.get_database("test")
            collList = db.collection_names()
            # 如果现有集合中没有，新建一个集合
            for collDict in collNameList:
                coll = collDict.get("coll")
                if coll not in collList:
                    collection = db.create_collection(name=coll, **collParm)  # 创建一个集合
                else:
                    collection = db.get_collection(name=coll)  # 获取一个集合对象
                self.find_data(collection, inputQueue)  # 将数据装载到队列中
            inputQueue.put("end")
            print("inputQueue have been finished !")
        finally:
            client.close()


    def find_data(self, collection, inputQueue):
        '''
        查询mongodb中所有isProcess为FALSE的数据
        将数据装入队列中
        '''
        cursor = collection.find({"isProcess": False})
        for data in cursor:
            inputQueue.put(data)


if __name__ == '__main__':
    q = Queue()
    i = InputDataMange()
    i.input_data(q)
    print(q.get())


