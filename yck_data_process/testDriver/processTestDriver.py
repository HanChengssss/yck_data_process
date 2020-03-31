from yck_data_process.testDriver.toolTestDriver import ToolTestDriver
from yck_data_process.process.autoModelProcess import ModelProcessManage
from yck_data_process.process.autoModelProcess import *
from yck_data_process.settingsManage import SettingsManage
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
        sm = SettingsManage()
        dbManage = sm.get_dbSettingInstance()
        mongoConn = pymongo.MongoClient(**dbManage.get_mongoClientParams())
        db = mongoConn.get_database(dbManage.get_mongodb())
        cursor = ToolTestDriver.get_mongo_data(db, dbManage.get_mongodbCollNameDict.get("auto_model"))
        logDriver = Logger("D:\YCK\代码\yck_data_process\yck_data_process\log_dir\modelProcess.log", level='warning')
        for dataDic in cursor:
            print(dataDic)
            ModelProcessManage.process_AutoModel_datas(dataDic, logDriver)
            print(dataDic)



if __name__ == '__main__':
    ProcessTestDriver.test_driver()
    # logDriver = Logger("D:\YCK\代码\yck_data_process\yck_data_process\log_dir\modelProcess.log", level='warning')