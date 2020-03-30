schemaMysqlNormal = dict(
    host="192.168.0.10",
    port=3306,
    user="root",
    passwd="000000",
    db="information_schema",
    charset="utf8",
)

dcMysqlNormal = dict(
    host="192.168.0.10",
    port=3306,
    user="root",
    passwd="000000",
    db="yck-data-center",
    charset="utf8",
)

schemaMysqlTest = dict(
    host="localhost",
    port=3306,
    user="root",
    passwd="123456",
    db="information_schema",
    charset="utf8",
)

test2MysqlTest = dict(
    host="localhost",
    port=3306,
    user="root",
    passwd="123456",
    db="test2",
    charset="utf8",
)
# mongodb 类型集合映射表
mongodbCollNameDict = {"auto_model": "autoModelCollection"}

# mongodb 数据库
testMongodb = "test"
normalMongodb = "normal"

# 创建集合的设置
createMongodbCollParm = dict(
    capped=True,
    size=1024 * 1024 * 500,
    max=1000000
)

# mongodb 连接信息
mongoClientParams = dict(
            host="localhost",
            port=27017
        )


class DbsManage():
    def __init__(self, model):
        self.model = model

    def get_schemaMysqlParams(self):
        if self.model == "test":
            return schemaMysqlTest
        else:
            return schemaMysqlNormal


    def get_dcMysqlNormalParams(self):
        if self.model == "test":
            return test2MysqlTest
        else:
            return dcMysqlNormal

    def get_mongodbCollNameDict(self):
        return mongodbCollNameDict

    def get_mongodb(self):
        if self.model == "test":
            return testMongodb
        else:
            return normalMongodb

    def get_creatMongodbCollParm(self):
        return createMongodbCollParm

    def get_mongoClientParams(self):
        if self.model == "test":
            return mongodbCollNameDict
        else:
            return mongodbCollNameDict