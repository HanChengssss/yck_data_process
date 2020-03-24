from yck_data_process.testDriver.toolTestDriver import ToolTestDriver
from yck_data_process.process.autoModelProcess import AutoModelProcess
from yck_data_process import settings
import pymongo
from yck_data_process.logingDriver import Logger
'''
测试流程
从mongodb取出数据
放到AutoModelProcess中
'''

class ProcessTestDriver():
    @staticmethod
    def test_driver():
        mongoConn = pymongo.MongoClient(**settings.mongoClientParams)
        db = mongoConn.get_database(settings.mongodb)
        cursor = ToolTestDriver.get_mongo_data(db, settings.mongodbCollNameDict.get("auto_model"))
        dataDic = cursor.next()
        print(dataDic)
        logDriver = Logger("D:\YCK\代码\yck_data_process\yck_data_process\log_dir\modelProcess.log", level='warning')
        AutoModelProcess.process_AutoModel_datas(dataDic, logDriver)
        print(dataDic)


if __name__ == '__main__':
    ProcessTestDriver.test_driver()
