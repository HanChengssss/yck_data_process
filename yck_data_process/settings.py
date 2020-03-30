# !/usr/bin/env python
# -*-encoding: utf-8-*-
# author:HanCheng
# version:0.1

# mysql 所有车型库表名
from yck_data_process.settings.dbs import DbsManage
from yck_data_process.settings.tables import TablesManage


class SettingsManage():
    def __init__(self, model):
        self.model = model

    def get_dbSettingInstance(self):
        return DbsManage(self.model)

    def get_tablesSettingsInstance(self):
        return TablesManage()

    def get_logSettingsInstance(self):
        pass


