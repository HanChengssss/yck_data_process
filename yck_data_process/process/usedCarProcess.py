# coding=utf-8
import hashlib
from datetime import datetime
def str_to_hash(strs):
    hash_code = hashlib.sha1(strs.encode("utf8")).hexdigest()
    return hash_code

class CarIdProcess(object):
    pass


class LogIdProcess(object):
    pass

class UsedCarFieldProcess():

    @staticmethod
    def process_data(data):
        if "update_time" in data:
            data.pop("update_time")
        if "add_time" not in data:
            data["add_time"] = datetime.today()
        car_id_filed = data["detail_url"]
        log_id_filed = data["detail_url"] + str(data["currentPrice"]) + str(data["startPrice"])
        data["car_id"] = str_to_hash(car_id_filed)
        data["log_id"] = str_to_hash(log_id_filed)

class UsedCarProcessManage():
    @staticmethod
    def process_data_dic(data_dict, log_driver):
        data_list = data_dict.get("dataList")
        if data_dict["id_field_name"] == "detail_url":
            data_dict["id_field_name"] = "log_id"
        if data_dict["table"] == "spider_www_ali":
            data_dict["table"] = "spider_log_ali"
        table = data_dict.get("table")
        for d in data_list:
            if "data" in d:
                data = d["data"]
            else:
                data = d
            UsedCarFieldProcess.process_data(data)
