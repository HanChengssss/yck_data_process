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

# mongodb 类型:集合
MONGODB_COLL_NAME_DICT = {"model": "model_coll",  # 车型库
                       "sale": "sale_coll",  # 销量
                       "setting": "setting_coll",  # 配置信息
                       # "used_car_pub": "used_car_pub_coll",  # 二手车发布
                       "dealer": "dealer_coll",  # 经销商数据
                       "complain": "complain_coll",  # 投诉
                       "opinions": "opinions_coll",  # 口碑
                       "naked_price": "naked_price_coll",  # 裸车价/车主价格
                       "dealer_price": "dealer_price_coll",  # 经销商报价
                        "bank": "bank_coll"  # 银行数据
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

# 车型库表名
AUTO_MODEL_TABLES = [
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

# 数据类型：表名字典
MYSQL_TABLES_DIC = {
    "model": AUTO_MODEL_TABLES
}

