# !/usr/bin/env python
# -*-encoding: utf-8-*-
# author:HanCheng
# version:0.1

import os
from yck_data_process.settings.dbs import *
from yck_data_process.settings.logPaths import *
from yck_data_process.settings.process import DATA_PROCESS_SETTING
# 全局模式
MODEL = "normal"


# 所有配置的管理类
class SettingsManage():

    def __init__(self, model):
        self.__model = model
        # print("SettingMange model is {}".format(self.__model))

    def set_model(self, model):
        self.__model = model

    def get_model(self):
        return self.__model

    def get_db_setting_instance(self):
        return DBSetting(self.__model)

    def get_log_setting_instance(self):
        return LogPathSetting(self.__model)

    def get_dsp_setting_instance(self, source_type):
        return DataProcessSetting(source_type)


# 管理数据库配置
class DBSetting():
    def __init__(self, model):
        self.model = model

    def get_schema_mysql_params(self):
        if self.model not in SCHEAM_MySQL:
            raise Exception("{} model in SCHEAM_MySQL not exist!".format(self.model))
        return SCHEAM_MySQL.get(self.model)

    def get_save_mysql_normal_params(self):
        if self.model not in DATA_SAVE_MySQL:
            raise Exception("{} model in DATA_SAVE_MySQL not exist!".format(self.model))
        return DATA_SAVE_MySQL.get(self.model)

    def get_mongodb(self):
        if self.model not in MONGODB_NAME_DIC:
            raise Exception("{} model in MONGODB_NAME_DIC not exist!".format(self.model))
        return MONGODB_NAME_DIC.get(self.model)

    def get_mysql_db_name(self):
        if self.model not in MYSQLDB_NAME_DIC:
            raise Exception("{} model in MYSQLDB_NAME_DIC not exist!".format(self.model))
        return MYSQLDB_NAME_DIC.get(self.model)

    def get_creat_mongodb_coll_parm(self, size=50):
        '''
        集合默认大小50M
        :param size:
        :return:
        '''
        CREATE_MONGODB_COLL_PARM["size"] = 1024 * 1024 * size
        return CREATE_MONGODB_COLL_PARM

    def get_mongo_client_params(self):
        if self.model not in MONGO_CLIENT_PARAMS:
            raise Exception("{} model in MONGO_CLIENT_PARAMS not exist!".format(self.model))
        return MONGO_CLIENT_PARAMS.get(self.model)


# 管理日志链接配置
class LogPathSetting():
    def __init__(self, model):
        self.model = model

    def get_log_dir_name(self):
        if self.model not in LOG_DIR_Name_DIC:
            raise Exception("{} model in LOG_DIR_Name_DIC not exist!".format(self.model))
        return LOG_DIR_Name_DIC.get(self.model)

    def get_project_base_path(self):
        # 检查文件夹是否存在
        project_base_path = None
        for pbp in PROJECT_BASE_PATH_DIC.values():
            if os.path.exists(pbp):
                project_base_path = pbp
                break
        if not project_base_path:
            raise Exception("projectBasePath not exist !")
        return project_base_path

    def get_log_dir_full_path(self):
        log_dir_full_path = None
        project_base_path = self.get_project_base_path()
        log_dir_name = self.get_log_dir_name()
        for relPath, dirs, files in os.walk(project_base_path):
            if log_dir_name in dirs:
                log_dir_full_path = os.path.join(project_base_path, relPath, log_dir_name)
                break
        if not log_dir_full_path:
            raise Exception("log_dir_full_path not exist !")
        return log_dir_full_path


class DataProcessSetting():
    def __init__(self, source_type):
        self.source_type = source_type
        self.test_type_exist()

    def test_type_exist(self):
        if self.source_type not in DATA_PROCESS_SETTING:
            raise Exception("{} model in DATA_PROCESS_SETTING not exist!".format(self.source_type))
        
    def get_coll_name_list(self):
        return list(DATA_PROCESS_SETTING.get(self.source_type).get("coll_setting").keys())

    def get_pip_func(self, coll_name):
        return DATA_PROCESS_SETTING.get(self.source_type).get("coll_setting").get(coll_name).get("pip_func")

    def get_process_func(self, coll_name):
        return DATA_PROCESS_SETTING.get(self.source_type).get("coll_setting").get(coll_name).get("process_func")

    def get_input_func(self):
        return DATA_PROCESS_SETTING.get(self.source_type).get("input_func")

    def get_is_update(self):
        return DATA_PROCESS_SETTING.get(self.source_type).get("update_is_process")

    def get_id_field_name(self, coll_name):
        if self.source_type != "mysql":
            raise Exception("{} model in DATA_PROCESS_SETTING not have get_id_field_name!".format(self.source_type))
        return DATA_PROCESS_SETTING.get(self.source_type).get("coll_setting").get(coll_name).get("id_field_name")

    def get_table_name(self, coll_name):
        if self.source_type != "mysql":
            raise Exception("{} model in DATA_PROCESS_SETTING not have get_table_name!".format(self.source_type))
        return DATA_PROCESS_SETTING.get(self.source_type).get("coll_setting").get(coll_name).get("table")


