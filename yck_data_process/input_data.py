import pymongo
from pymongo import MongoClient
import random
from datetime import datetime
from multiprocessing import Queue
from yck_data_process.settingsManage import SettingsManage, MODEL



class InputDataMange():

    @staticmethod
    def input_data(inputQueue):
        '''
        初始化mongodb连接
        加载待查询的collection
        查询数据
        将数据添加到队列
        :return:
        '''
        # 创建集合的配置
        sm = SettingsManage(model=MODEL)
        dbManage = sm.get_dbSettingInstance()
        client = MongoClient(**dbManage.get_mongoClientParams())
        try:
            db = client.get_database(dbManage.get_mongodb())
            collList = db.collection_names()
            # 如果现有集合中没有，新建一个集合
            for coll in dbManage.get_mongodbCollNameDict().values():
                if coll not in collList:
                    collection = db.create_collection(name=coll, **dbManage.get_creatMongodbCollParm())  # 创建一个集合
                else:
                    collection = db.get_collection(name=coll)  # 获取一个集合对象
                InputDataMange.find_data(collection, inputQueue)  # 将数据装载到队列中
            inputQueue.put("end")
            print("inputQueue have been finished !")
        finally:
            client.close()

    @staticmethod
    def find_data(collection, inputQueue):
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


