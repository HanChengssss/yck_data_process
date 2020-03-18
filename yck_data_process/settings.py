# !/usr/bin/env python
# -*-encoding: utf-8-*-
# author:HanCheng
# version:0.1

# mysql 所有车型库表名
auto_model_tables = [
"config_autohome_major_info_tmp",
"config_che300_major_info",
"config_chezhibao_major_info",
"config_souhu_major_info",
"config_yiche_major_info",
"config_youxin_major_info_tmp",
"config_youxin_major_info_tmp",
"config_firstauto_major_info",
"config_xcar_major_info",
"config_tc5u_major_info",
"config_guazi_major_info",
"config_auto12365_major_info_tmp",
"config_wyauto_major_info"
]

# mysql 连接信息
dbparams = dict(
            host="192.168.0.10",
            port=3306,
            user="root",
            passwd="000000",
            db="yck-data-center",
            charset="utf8",
        )

# mongodb 集合列表
collNameList = [{"coll": "autoModelCollection", "name": "车型库"}]

# mongodb 数据库
mongodb = "test"

# 创建集合的设置
collParm = dict(
    capped=True,
    size=1024 * 1024 * 50,
    max=1000000
)