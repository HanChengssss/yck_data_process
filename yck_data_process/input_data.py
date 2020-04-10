import pymongo
from pymongo import MongoClient
import random
from datetime import datetime
from multiprocessing import Queue
from yck_data_process.settingsManage import SettingsManage, MODEL


class InputDataMange():

    @staticmethod
    def input_data(input_queue):
        '''
        初始化mongodb连接
        加载待查询的collection
        查询数据
        将数据添加到队列
        :return:
        '''
        # 创建集合的配置
        sm = SettingsManage(model=MODEL)
        db_manage = sm.get_db_setting_instance()
        client = MongoClient(**db_manage.get_mongo_client_params())
        try:
            db = client.get_database(db_manage.get_mongodb())
            coll_list = db.collection_names()
            # 如果现有集合中没有，新建一个集合
            for coll in db_manage.get_coll_name_list():
                if coll not in coll_list:
                    collection = db.create_collection(name=coll, **db_manage.get_creat_mongodb_coll_parm())  # 创建一个集合
                else:
                    collection = db.get_collection(name=coll)  # 获取一个集合对象
                InputDataMange.find_data(collection, input_queue)  # 将数据装载到队列中
            input_queue.put("end")
            print("input_queue have been finished !")
        finally:
            client.close()

    @staticmethod
    def find_data(collection, input_queue):
        '''
        查询mongodb中所有isProcess为FALSE的数据
        将数据装入队列中
        '''
        cursor = collection.find({"isProcess": False})
        for data in cursor:
            input_queue.put(data)


if __name__ == '__main__':
    q = Queue()
    i = InputDataMange()
    i.input_data(q)
    print(q.get())


