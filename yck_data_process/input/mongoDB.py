from pymongo import MongoClient
from yck_data_process.settingsManage import SettingsManage, MODEL


class MongodbSource():

    @staticmethod
    def input_data(input_queue):
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
                MongodbSource.find_data(collection, input_queue)  # 将数据装载到队列中
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