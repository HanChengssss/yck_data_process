# !/usr/bin/env python
# -*-encoding: utf-8-*-
# author:Hancheng
# version:0.1
from yck_data_process.settingsManage import SettingsManage, MODEL
import pymysql
from yck_data_process.logingDriver import Logger
import pymongo
from yck_data_process.pipelines.autoModelOutput import AutoModelPipeline
from yck_data_process.pipelines.Tools import ToolSave
from tqdm import tqdm


class OutPutDataManage():
    @staticmethod
    def dataOutput(outputQueue):
        '''
        管理和加载所有的数据库存储类
        从outputQueue中取出数据存到MySQL中
        :param outputQueue:
        :return:
        '''
        sm = SettingsManage(model=MODEL)
        dbMange = sm.get_dbSettingInstance()
        logPathMange = sm.get_logSettingsInstance()
        conn = pymysql.connect(**dbMange.get_saveMysqlNormalParams())
        logDirFullPath = logPathMange.get_logDirFullPath()
        log = Logger(filename="{}\outoutData.log".format(logDirFullPath), level='error')
        mongoConn = pymongo.MongoClient(**dbMange.get_mongoClientParams())
        db = mongoConn.get_database(dbMange.get_mongodb())
        qSize = outputQueue.qsize()
        tq = tqdm(total=qSize, desc="数据处理进度：")
        try:
            while True:
                dataDic = outputQueue.get()
                if dataDic == 'end':
                    print("data_output is end !")
                    break
                try:
                    type = dataDic.get("type")
                    coll_name = dbMange.get_mongodbCollNameDict().get(type)
                    # 车型库数据存储逻辑
                    if type == "model":
                        AutoModelPipeline.process_dataDic(dataDic=dataDic, mysqlConn=conn)
                    ToolSave.update_mongodb(mongodb=db, data_id=dataDic["_id"], coll_name=coll_name)
                except Exception as e:
                    log.logger.error(e)
                finally:
                    tq.update(1)
        finally:
            conn.close()
            mongoConn.close()
            tq.close()


if __name__ == '__main__':
    pass


