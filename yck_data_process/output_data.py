# !/usr/bin/env python
# -*-encoding: utf-8-*-
# author:Hancheng
# version:0.1
from yck_data_process import settings
import pymysql
from yck_data_process.logingDriver import Logger
import pymongo
from yck_data_process.pipelines.AutoModel import AutoModelPipeline
from yck_data_process.pipelines.Tools import ToolSave
from tqdm import tqdm

class OutPutDataManage():
    @staticmethod
    def dataOutput(outputQueue):
        conn = pymysql.connect(**settings.testMysqlParams)
        log = Logger(filename="D:\YCK\代码\yck_data_process\yck_data_process\log_dir\outoutData.log", level='error')
        mongoConn = pymongo.MongoClient(host="localhost", port=27017)
        db = mongoConn.get_database(settings.mongodb)
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
                    coll_name = settings.mongodbCollNameDict.get(type)
                    # 车型库数据存储逻辑
                    if type == "auto_model":
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


