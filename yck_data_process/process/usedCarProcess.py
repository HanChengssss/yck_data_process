# coding=utf-8
import hashlib
from datetime import datetime

data_info_list = [
    {"table": "spider_log_168", "car_id": ["url"], 'log_id': ["url", "quotes"], "type": 1},
    {"table": "spider_log_58", "car_id": ["url"], 'log_id': ["url", "quotes"], "type": 1},
    {"table": "spider_log_xin", "car_id": ["url"], 'log_id': ["url", "quotes"], "type": 1},
    {"table": "spider_log_yiche", "car_id": ["url"], 'log_id': ["url", "quotes"], "type": 1},
    {"table": "spider_log_renren", "car_id": ["url"], 'log_id': ["url", "quotes"], "type": 1},
    {"table": "spider_log_guazi", "car_id": ["url"], 'log_id': ["url", "quotes"], "type": 1},
    {"table": "spider_log_273", "car_id": ["url"], 'log_id': ["url", "quotes"], "type": 1},
    {"table": "spider_log_czbused", "car_id": ["url"], 'log_id': ["url", "quotes"], "type": 1},
    {"table": "spider_log_chesupai", "car_id": ["url"], 'log_id': ["url", "quotes"], "type": 1},
    {"table": "spider_log_kaixin", "car_id": ["car_id"], 'log_id': ["car_id", "quotes"], "type": 2},  # todo 特殊
    {"table": "spider_log_akd", "car_id": ["car_id"], 'log_id': ["car_id", "quotes"], "type": 2},  # todo 特殊
    {"table": "spider_log_ttp", "car_id": ["car_id"], 'log_id': ["car_id", "quotes"], "type": 2},  # todo 特殊
    {"table": "spider_log_huaxia", "car_id": ["car_id"], 'log_id': ["car_id", "quotes"], "type": 2},  # todo 特殊
    {"table": "spider_log_iautos", "car_id": ["id"], 'log_id': ["id", "quotes"], "type": 3},  # 第一车的id就是这辆车的唯一标识
    {"table": "spider_log_chezhibao", "car_id": ["car_id"], 'log_id': ["car_id", "bid_price"], "type": 4},  # todo 特殊
    {"table": "spider_log_ali", "car_id": ["detail_url"], 'log_id': ["detail_url", "currentPrice", "startPrice"], "type": 5},  # todo 特殊

]


class BaseProcess():

    def process_data(self, data):
        self.process_time(data)
        car_id_str = self.product_car_id_str(data)
        log_id_str = self.product_log_id_str(data)
        data["car_id"] = self.str_to_hash(car_id_str)
        data["log_id"] = self.str_to_hash(log_id_str)

    def process_time(self, data):
        if "update_time" in data:
            data.pop("update_time")
        if "add_time" not in data:
            data["add_time"] = datetime.today()

    def str_to_hash(self, strs):
        hash_code = hashlib.sha1(strs.encode("utf8")).hexdigest()
        return hash_code

    def product_car_id_str(self, data):
        return "-"

    def product_log_id_str(self, data):
        return "-"


class OneProcess(BaseProcess):

    def product_car_id_str(self, data):
        if data.get("url"):
            car_id_str = str(data["url"])
        else:
            car_id_str = "-"
        return car_id_str

    def product_log_id_str(self, data):
        if data.get("url") and data.get("quotes"):
            log_id_str = str(data["url"]) + str(data["quotes"])
        else:
            log_id_str = "-"
        return log_id_str


class TwoProcess(BaseProcess):
    def product_car_id_str(self, data):
        if data.get("car_id"):
            car_id_str = str(data["car_id"])
        else:
            car_id_str = "-"
        return car_id_str

    def product_log_id_str(self, data):
        if data.get("car_id") and data.get("quotes"):
            log_id_str = str(data["car_id"]) + str(data["quotes"])
        else:
            log_id_str = "-"
        return log_id_str


class ThreeProcess(BaseProcess):
    def product_car_id_str(self, data):
        if data.get("id"):
            car_id_str = str(data["id"])
        else:
            car_id_str = "-"
        return car_id_str

    def product_log_id_str(self, data):
        if data.get("id") and data.get("quotes"):
            log_id_str = str(data["id"]) + str(data["quotes"])
        else:
            log_id_str = "-"
        return log_id_str

    def process_data(self, data):
        self.process_time(data)
        car_id_str = self.product_car_id_str(data)
        log_id_str = self.product_log_id_str(data)
        data["car_id"] = self.str_to_hash(car_id_str)
        data["log_id"] = self.str_to_hash(log_id_str)
        data.pop("id")


class FourProcess(BaseProcess):
    def product_car_id_str(self, data):
        if data.get("car_id"):
            car_id_str = str(data["car_id"])
        else:
            car_id_str = "-"
        return car_id_str

    def product_log_id_str(self, data):
        if data.get("car_id") and data.get("bid_price"):
            log_id_str = str(data["car_id"]) + str(data["bid_price"])
        else:
            log_id_str = "-"
        return log_id_str


class FiveProcess(BaseProcess):
    def product_car_id_str(self, data):
        if data.get("detail_url"):
            car_id_str = str(data["detail_url"])
        else:
            car_id_str = "-"
        return car_id_str

    def product_log_id_str(self, data):
        if data.get("detail_url") and data.get("currentPrice") and data.get("startPrice"):
            log_id_str = str(data["detail_url"]) + str(data["currentPrice"]) + str(data["startPrice"])
        else:
            log_id_str = "-"
        return log_id_str


class UsedCarProcessManage():
    @staticmethod
    def process_data_dic(data_dict, log_driver):
        func_dic = {
            'spider_log_168': OneProcess,
            'spider_log_58': OneProcess,
            'spider_log_xin': OneProcess,
            'spider_log_yiche': OneProcess,
            'spider_log_renren': OneProcess,
            'spider_log_guazi': OneProcess,
            'spider_log_273': OneProcess,
            'spider_log_czbused': OneProcess,
            'spider_log_chesupai': OneProcess,
            'spider_log_kaixin': TwoProcess,
            'spider_log_akd': TwoProcess,
            'spider_log_ttp': TwoProcess,
            'spider_log_huaxia': TwoProcess,
            'spider_log_iautos': ThreeProcess,
            'spider_log_chezhibao': FourProcess,
            'spider_log_ali': FiveProcess,
        }
        if data_dict["id_field_name"] == "detail_url":
            data_dict["id_field_name"] = "log_id"
        if data_dict["table"] == "spider_www_ali":
            data_dict["table"] = "spider_log_ali"
        table = data_dict.get("table")
        data_list = data_dict.get("dataList")
        for d in data_list:
            if "data" in d:
                data = d["data"]
            else:
                data = d
            func = func_dic.get(table)
            func().process_data(data)



