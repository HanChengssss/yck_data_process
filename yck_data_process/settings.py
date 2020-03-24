# !/usr/bin/env python
# -*-encoding: utf-8-*-
# author:HanCheng
# version:0.1

# mysql 所有车型库表名
auto_model_tables = [
"config_autohome_major_info_tmp",
"config_che300_major_info",
"config_chezhibao_major_info",
"config_autoowner_major_info_tmp",
"config_souhu_major_info",
"config_yiche_major_info",
"config_youxin_major_info_tmp",
"config_firstauto_major_info",
"config_xcar_major_info",
"config_tc5u_major_info",
"config_auto12365_major_info_tmp",
"config_wyauto_major_info"
]

# mysql 连接信息
mysqlParams = dict(
            host="192.168.0.10",
            port=3306,
            user="root",
            passwd="000000",
            db="yck-data-center",
            charset="utf8",
        )

mysqlSchemaParams = dict(
            host="192.168.0.10",
            port=3306,
            user="root",
            passwd="000000",
            db="information_schema",
            charset="utf8",
        )


testMysqlParams = dict(
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
mongodb = "test"

# 创建集合的设置
mongodbCollParm = dict(
    capped=True,
    size=1024 * 1024 * 500,
    max=1000000
)

# mongodb 连接信息
mongoClientParams = dict(
            host="localhost",
            port=27017
        )