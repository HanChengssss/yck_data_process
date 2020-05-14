# scheam库连接参数
SCHEAM_MySQL = {
    "normal": dict(
    host="192.168.0.10",
    port=3306,
    user="root",
    passwd="000000",
    db="information_schema",
    charset="utf8",
    ),
    "test": dict(
    host="localhost",
    port=3306,
    user="root",
    passwd="123456",
    db="information_schema",
    charset="utf8",
    )
}

# 存储库连接参数
DATA_SAVE_MySQL = {
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


# mongodb 数据库
MONGODB_NAME_DIC = {
    "normal": "normal",
    "test": "test"
}

MYSQLDB_NAME_DIC = {
    "normal": "yck-data-center",
    "test": "test2"
}

# 创建集合的设置
CREATE_MONGODB_COLL_PARM = {"capped": True, "max": 1000000}

# mongodb 连接信息
MONGO_CLIENT_PARAMS = {
    "test": dict(
            host="localhost",
            port=27017
        ),
    "normal": dict(
            host="192.168.0.10",
            port=27017
        ),
}
