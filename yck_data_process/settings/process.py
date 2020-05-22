# _*_ coding:utf-8_*_
# author: hancheng
# date: 2020/5/13 17:48
from yck_data_process.input.mongoDB import MongodbSource
from yck_data_process.input.mysqlDB import MysqldbSource
from yck_data_process.pipelines.increment import IncrementPipeline
from yck_data_process.pipelines.incrementStock import IncrementStock
from yck_data_process.pipelines.twoIncremtStock import TwoIncrementStock
from yck_data_process.process.autoModelProcess import ModelProcessManage
from yck_data_process.process.positionProcess import PositionProcessManage
from yck_data_process.process.bankInfoProcess import BankInfoProcessManage
from yck_data_process.process.rankZhiyunProcess import RankProcessManage
from yck_data_process.process.usedCarProcess import UsedCarProcessManage
from yck_data_process.process.usedCarAfterProcess import UsedCarProcessAfterManage
from yck_data_process.process.autoSettingProcess import SettingProcessManage

DATA_PROCESS_SETTING = {
    "mysql": {
        "input_func": MysqldbSource,
        "update_is_process": False,
        "coll_setting": {
            "spider_log_ali": {"pip_func": TwoIncrementStock, "process_func": UsedCarProcessAfterManage, "table": "spider_www_ali", "id_field_name": "car_id"},
            "spider_www_168": {"pip_func": TwoIncrementStock, "process_func": UsedCarProcessAfterManage, "table": "spider_www_168", "id_field_name": "car_id"},
            # "spider_log_58": {"pip_func": IncrementStock, "process_func": UsedCarProcessAfterManage, "table": "spider_www_58", "id_field_name": "car_id"},
            # "spider_log_xin": {"pip_func": IncrementStock, "process_func": UsedCarProcessAfterManage, "table": "spider_www_xin", "id_field_name": "car_id"},
            # "spider_log_yiche": {"pip_func": IncrementStock, "process_func": UsedCarProcessAfterManage, "table": "spider_www_yiche", "id_field_name": "car_id"},
            # "spider_log_renren": {"pip_func": IncrementStock, "process_func": UsedCarProcessAfterManage, "table": "spider_www_renren", "id_field_name": "car_id"},
            # "spider_log_guazi": {"pip_func": IncrementStock, "process_func": UsedCarProcessAfterManage, "table": "spider_www_guazi", "id_field_name": "car_id"},
            # "spider_log_273": {"pip_func": IncrementStock, "process_func": UsedCarProcessAfterManage, "table": "spider_www_273", "id_field_name": "car_id"},
            # "spider_log_czbused": {"pip_func": IncrementStock, "process_func": UsedCarProcessAfterManage, "table": "spider_www_czbused", "id_field_name": "car_id"},
            # "spider_log_iautos": {"pip_func": IncrementStock, "process_func": UsedCarProcessAfterManage, "table": "spider_www_iautos", "id_field_name": "car_id"},
            # "spider_log_chesupai": {"pip_func": IncrementStock, "process_func": UsedCarProcessAfterManage, "table": "spider_www_chesupai", "id_field_name": "car_id"},
            # "spider_log_kaixin": {"pip_func": IncrementStock, "process_func": UsedCarProcessAfterManage, "table": "spider_www_kaixin", "id_field_name": "car_id"},
            # "spider_log_chezhibao": {"pip_func": IncrementStock, "process_func": UsedCarProcessAfterManage, "table": "spider_www_chezhibao", "id_field_name": "car_id"},
            # "spider_log_akd": {"pip_func": IncrementStock, "process_func": UsedCarProcessAfterManage, "table": "spider_www_akd", "id_field_name": "car_id"},
            # "spider_log_ttp": {"pip_func": IncrementStock, "process_func": UsedCarProcessAfterManage, "table": "spider_www_ttp", "id_field_name": "car_id"},
            # "spider_log_huaxia": {"pip_func": IncrementStock, "process_func": UsedCarProcessAfterManage, "table": "spider_www_huaxia", "id_field_name": "car_id"},
        }
    },
    "mongo": {
        "input_func": MongodbSource,
        "update_is_process": True,
        "coll_setting": {
            "model_coll": {"pip_func": IncrementStock, "process_func": ModelProcessManage},
            "setting_coll": {"pip_func": IncrementStock, "process_func": SettingProcessManage},
            "used_car_pub_coll": {"pip_func": IncrementPipeline, "process_func": UsedCarProcessManage},
            "rank_zhiyun_coll": {"pip_func": IncrementPipeline, "process_func": RankProcessManage},
            "bank_coll": {"pip_func": IncrementStock, "process_func": BankInfoProcessManage},
            # "sale_coll": {"pip_func": None, "process_func": None},
            # "dealer_coll": {"pip_func": None, "process_func": None},
            # "complain_coll": {"pip_func": None, "process_func": None},
            # "opinions_coll": {"pip_func": None, "process_func": None},
            # "naked_price_coll": {"pip_func": None, "process_func": None},
            # "dealer_price_coll": {"pip_func": None, "process_func": None},
        }
    },
}