from pymongo import MongoClient
import pymysql
from yck_data_process import settings
from multiprocessing import Queue
from yck_data_process.output_data import OutPutDataManage
from yck_data_process.testDriver.toolTestDriver import ToolTestDriver


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
        mongoConn = MongoClient(**settings.mongoClientParams)
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
        '''
        从队列中取出待存储的数据
        测试存储过程是否有bug
        :return:
        '''
        mongoConn = MongoClient(settings.mongoClientParams)
        db = mongoConn.get_database(settings.mongodb)
        q = AutoModelTestDriver.put_data_queue(db, settings.mongodbCollNameDict.get("auto_model"))
        OutPutDataManage.dataOutput(q)
        mongoConn.close()


if __name__ == '__main__':
    AutoModelTestDriver.test_driver()












