# _*_ coding:utf-8_*_
# author: hancheng
# date: 2020/5/13 16:35
from datetime import datetime


class UsedCarFieldAfterProcess():
    @staticmethod
    def process_data(data):
        if "add_time" in data:
            data["update_time"] = data["add_time"]
        else:
            data["update_time"] = datetime.today()
            data["add_time"] = datetime.today()


class UsedCarProcessAfterManage():
    @staticmethod
    def process_data_dic(data_dict, log_driver):
        data_list = data_dict.get("dataList")
        for d in data_list:
            if "data" in d:
                data = d["data"]
            else:
                data = d
            UsedCarFieldAfterProcess.process_data(data)