# !/usr/bin/env python
# -*-encoding: utf-8-*-
# author:HanCheng
# version:0.1

# mysql 所有车型库表名
from yck_data_process.settings.dbs import DbsManage
from yck_data_process.settings.tables import TablesManage
from yck_data_process.settings.logPaths import LogPathManage


class SettingsManage():
    __model = "test"

    def set_model(self, model):
        self.__model = model

    def get_model(self):
        return self.__model

    def get_dbSettingInstance(self):
        return DbsManage(self.__model)

    def get_tablesSettingsInstance(self):
        return TablesManage()

    def get_logSettingsInstance(self):
        return LogPathManage(self.__model)



