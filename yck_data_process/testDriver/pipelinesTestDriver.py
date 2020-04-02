from pymongo import MongoClient
import pymysql
from yck_data_process.settingsManage import SettingsManage, MODEL
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
        sm = SettingsManage(model=MODEL)
        dbManage = sm.get_dbSettingInstance()
        tableMange = sm.get_tablesSettingsInstance()
        mysqlParms = dbManage.get_saveMysqlNormalParams()
        mysqlConn = pymysql.connect(**mysqlParms)

        mongoClientParams = dbManage.get_mongoClientParams()
        mongoConn = MongoClient(**mongoClientParams)
        dbName = dbManage.get_mongodb()
        db = mongoConn.get_database(dbName)

        tables = tableMange.get_tables("model")
        dataDicList = []
        for table in tables:
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
        sm = SettingsManage(model=MODEL)
        dbManage = sm.get_dbSettingInstance()

        mongoClientParams = dbManage.get_mongoClientParams()
        mongoConn = MongoClient(**mongoClientParams)
        dbName = dbManage.get_mongodb()
        db = mongoConn.get_database(dbName)
        collNameDic = dbManage.get_mongodbCollNameDict()
        q = AutoModelTestDriver.put_data_queue(db, collNameDic.get("auto_model"))
        OutPutDataManage.dataOutput(q)
        mongoConn.close()


if __name__ == '__main__':
    # AutoModelTestDriver.test_driver()
    AutoModelTestDriver.autodata_input_mongo()












