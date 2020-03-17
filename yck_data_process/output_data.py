# !/usr/bin/env python
# -*-encoding: utf-8-*-
# author:LiYanwei
# version:0.1
import pymysql
from yck_data_process.logingDriver import *
from yck_data_process.settings import *
import re
import pymysql
from yck_data_process.logingDriver import Logger
import pymongo
from yck_data_process.input_data import InputDataMange

class OutPutBase():
    '''
    将处理后的数据输出到目标数据库
    '''


    # def data_input(self, data):
    #     pass
    #
    # def data_output(self, datas):
    #     pass
    #
    # def get_db_conn(self, **kwargs):
    #     pass
    pass


class OutPutDataManage():

    def dataOutput(self, outputQueue, coll_name):
        conn = pymysql.connect(**dbparams)
        log = Logger(filename="D:\YCK\代码\yck_data_process\yck_data_process\log_dir\outoutData.log", level='error')
        mongoConn = pymongo.MongoClient(host="localhost", port=27017)
        mongodb = mongoConn.get_database('test')
        while True:
            datas = outputQueue.get()
            if datas == 'end':
                print("data_output is end !")
                conn.close()
                break
            self.insert_to_mysql(dataDic=datas, conn=conn, log=log, mongodb=mongodb, coll_name=coll_name)

    def insert_to_mysql(self, dataDic, conn, log, mongodb, coll_name):
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
            self.update_mongodb(mongodb, dataDic['_id'], coll_name)
            print("保存成功！")
        except Exception as e:
            log.logger.error(msg=str(e))

    def update_mongodb(self, mongodb, data_id, coll_name):
        collection = mongodb.get_collection(coll_name)
        ret = collection.update_one({"_id": data_id}, {"$set": {"isProcess": True}})
        print("pymongo 更新成功！")

    def sort_item(self, data):
        '''
        对字典中的key进行排序，保证每个字典的key顺序一致
        :param data:
        :return:
        '''
        data = dict(sorted(data.items(), key=lambda item: item[0], reverse=False))
        return data


if __name__ == '__main__':
    i = InputDataMange()
    inputQueue = i.run()
    o = OutPutMysql()
    o.dataOutput(inputQueue, "autoModelCollection")


