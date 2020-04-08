schemaMysql = {
    "test": dict(
    host="192.168.0.10",
    port=3306,
    user="root",
    passwd="000000",
    db="information_schema",
    charset="utf8",
    ),
    "normal": dict(
    host="localhost",
    port=3306,
    user="root",
    passwd="123456",
    db="information_schema",
    charset="utf8",
    )
}

dataSaveMysql = {
    "normal": dict(
    host="192.168.0.10",
    port=3306,
    user="root",
    passwd="000000",
    db="yck-data-center",
    charset="utf8",
    ),
    "test": dict(
    host="localhost",
    port=3306,
    user="root",
    passwd="123456",
    db="test2",
    charset="utf8",
    )
}

# mongodb 类型集合映射表
mongodbCollNameDict = {"model": "model"}

# mongodb 数据库
mongoDBNameDic = {
    "normal": "normal",
    "test": "test"
}

mysqlDBNameDic = {
    "normal": "yck-data-center",
    "test": "test2"
}

# 创建集合的设置
createMongodbCollParm = dict(
    capped=True,
    size=1024 * 1024 * 500,
    max=1000000
)

# mongodb 连接信息
mongoClientParams = {
    "test": dict(
            host="localhost",
            port=27017
        ),
    "normal": dict(
            host="192.168.0.10",
            port=27017
        ),
}


class DbsManage():
    def __init__(self, model):
        self.model = model

    def get_schemaMysqlParams(self):
        if self.model not in schemaMysql:
            raise Exception("{} model in schemaMysql not exist!".format(self.model))
        return schemaMysql.get(self.model)

    def get_saveMysqlNormalParams(self):
        if self.model not in dataSaveMysql:
            raise Exception("{} model in get_saveMysqlNormalParams not exist!".format(self.model))
        return dataSaveMysql.get(self.model)

    def get_mongodbCollNameDict(self):
        return mongodbCollNameDict

    def get_mongodb(self):
        if self.model not in mongoDBNameDic:
            raise Exception("{} model in mongoDBNameDic not exist!".format(self.model))
        return mongoDBNameDic.get(self.model)

    def get_mysqlDBName(self):
        if self.model not in mysqlDBNameDic:
            raise Exception("{} model in mysqlDBNameDic not exist!".format(self.model))
        return mysqlDBNameDic.get(self.model)

    def get_creatMongodbCollParm(self):
        return createMongodbCollParm

    def get_mongoClientParams(self):
        if self.model not in mongoClientParams:
            raise Exception("{} model in mongoClientParams not exist!".format(self.model))
        return mongoClientParams.get(self.model)