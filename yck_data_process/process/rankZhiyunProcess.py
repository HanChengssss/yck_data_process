# coding=utf-8
import re


# 将字段转成字符串类型
class FiledToStr():
    @staticmethod
    def process_filed(filed):
        status_dic = {
            "isLog": False,
            "filed": None
        }
        try:
            if filed == "-":
                filed = "0"
            status_dic["filed"] = str(int(filed))
        except:
            status_dic["isLog"] = True
        finally:
            return status_dic

class ManfNameProcess():
    @staticmethod
    def process_filed(filed):
        status_dic = {
            "isLog": False,
            "filed": None
        }
        try:
            status_dic["filed"] = filed.encode("utf8").decode("utf8")
        except:
            status_dic["isLog"] = True
        finally:
            return status_dic

class RankFieldProcess():

    @staticmethod
    def process_data(data, filed_name_list, logDriver, table, process_fun):
        '''
        将字段的公共处理规则和私有处理规则分离
        :param data:
        :param filed_name_list:
        :param logDriver:
        :param table:
        :param process_fun:
        :return:
        '''
        filed_name = None
        for fn in filed_name_list:
            if fn in data:
                filed_name = fn
        if not filed_name:
            return
        filed = data.get(filed_name)
        if not filed:
            return
        # 字段处理规则
        status_dic = process_fun(filed)
        # print(status_dic)
        if status_dic.get("isLog"):
            logDriver.logger.warning("{}-->{}, source_table-->{}".format(filed_name, data.get(filed_name), table))
        elif status_dic.get("filed"):
            data[filed_name] = status_dic.get("filed")


class RankProcessManage():
    '''
    职位信息处理模块
    加载和管理车型库各个字段处理模块
    '''
    filed_process_dic = {
       "排名变化": {"func": FiledToStr, "name_list": ["rank_change"]},
        "排名": {"func": FiledToStr, "name_list": ["rank_num"]},
        "销量": {"func": FiledToStr, "name_list": ["sales_num"]},
        "厂家": {"func": ManfNameProcess, "name_list": ["manf_name"]},
    }

    @staticmethod
    def process_data_dic(data_dict, log_driver):
        data_list = data_dict.get("dataList")
        table = data_dict.get("table")
        for d in data_list:
            if "data" in d:
                data = d["data"]
            else:
                data = d
            for process in RankProcessManage.filed_process_dic.values():
                name_list = process.get("name_list")
                process_fun = process.get("func").process_filed
                RankFieldProcess.process_data(data=data, filed_name_list=name_list, logDriver=log_driver, table=table, process_fun=process_fun)
