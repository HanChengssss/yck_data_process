# !/usr/bin/env python
# -*-encoding: utf-8-*-
# author:HanCheng
# version:0.1
import re


# 车型库年款字段处理处理模块
class YearProcess():
    '''
    车型库年款字段处理处理模块
    '''
    @staticmethod
    def process_filed(filed):
        status_dic = {
            "isLog": False,
            "filed": None
        }
        try:
            ret = re.search(r'\d{4}', str(filed))
            if ret:
                status_dic["filed"] = ret.group()
            else:
                status_dic["isLog"] = True
        except:
            status_dic["isLog"] = True
        finally:
            return status_dic


# 车型库变速箱字段处理模块
class GearboxProcess():
    '''
    车型库变速箱字段处理模块
    '''

    @staticmethod
    def process_filed(filed):
        '''
        由于变速箱的字段名称有两个：gearbox,auto
        所以需要经过两次判断
        :param data:
        :param filed_name:
        :param log_driver:
        :param table:
        :return:
        '''
        status_dic = {
            "isLog": False,
            "filed": None
        }
        p1 = re.compile(r'自动|手动|电动')  # 标准
        p2 = re.compile(r'.*CVT|.*无级变速|手自一体|机械自动|双离合|双离合\.*手自动一体|DSG双离合|双离合器|G-DCT|DCT|DSG|AT|AMT智能手动版|AMT智能手动|AMT|EMT|IMT|ISR')  # --> 自动
        p3 = re.compile(r'单速变速箱')  # -->电动
        p4 = re.compile(r'.*序列')  # -->手动

        r1 = p1.search(filed)
        r2 = p2.search(filed)
        r3 = p3.search(filed)
        r4 = p4.search(filed)
        try:
            if r1:
                status_dic["filed"] = r1.group()
                # return status_dic
            elif r2:
                status_dic["filed"] = "自动"
                # return status_dic
            elif r3:
                status_dic["filed"] = "电动"
                # return status_dic
            elif r4:
                status_dic["filed"] = "手动"
                # return status_dic
            else:
                status_dic["isLog"] = True
        except:
            status_dic["isLog"] = True
        finally:
            return status_dic


# 指导价处理模块
class PriceProcess():
    '''
    指导价处理模块
    '''

    @staticmethod
    def process_filed(filed):
        status_dic = {
            "isLog": False,
            "filed": None
        }
        try:
            if int(float(filed)) < 10000:
                pass
            else:
                r1 = round(int(filed)/10000, 2)  # 四舍五入保留两位小数
                assert r1 < 10000
                status_dic["filed"] = r1
        except:
            status_dic["isLog"] = True
        finally:
            return status_dic


# 车型名称处理模块
class NameProcess():

    @staticmethod
    def process_filed(filed):
        status_dic = {
            "isLog": False,
            "filed": None
        }
        try:
            # 2008款 海狮 汽油系列三菱动力2.4(商务型)
            ret = re.search(r'\d{4}款 \w+|\d{4}款  \w+', filed)
            assert ret.group()
        except:
            status_dic["isLog"] = True
        finally:
            return status_dic


# 车型库排放标准处理模块
class DischargeProcess():

    @staticmethod
    def process_filed(filed):
        # discharge_standard
        status_dic = {
            "isLog": False,
            "filed": None
        }
        try:
            pattern = re.compile(r'国1|国2|国3|国4|国5|国6|京3|京5|欧1|欧2|欧3|欧4|欧5|欧6|新能源|-')
            ret = pattern.search(filed)
            if ret:
                status_dic["filed"] = ret.group()

            elif len(filed) >= 2 and isinstance(filed, str):
                rome_number_dic = {"Ⅰ": 1, "Ⅱ": 2, "Ⅲ": 3, "Ⅳ": 4, "Ⅴ": 5, "Ⅵ": 6}
                china_number_dic = {"一": 1, "二": 2, "三": 3, "四": 4, "五": 5, "六": 6, "七": 7}
                number_map = filed[1]
                number = str(rome_number_dic[number_map]) if number_map in rome_number_dic else None
                if not number:
                    number = str(china_number_dic[number_map]) if number_map in china_number_dic else None
                assert number
                status_dic["filed"] = filed.replace(number_map, str(number))
            else:
                status_dic["isLog"] = True
        except:
            status_dic["isLog"] = True
        finally:
            return status_dic


# 车级别处理模块
class CarLevelProcess():
    @staticmethod
    def process_filed(filed):
        status_dic = {
            "isLog": False,
            "filed": None
        }
        try:
            pattern = re.compile(r'微型车|小型车|紧凑型车|中型车|中大型车|豪华车|小型SUV|紧凑型SUV|中型SUV|中大型SUV|大型SUV|全尺寸SUV|跑车|MPV|客车|皮卡|微面|卡车|欧5|微卡|其它|-')
            ret = pattern.search(filed)
            assert ret.group()
            status_dic["filed"] = ret.group()
        except:
            status_dic["isLog"] = True
        finally:
            return status_dic


# 座位数处理模块
class SeatNumberProcess():
    @staticmethod
    def process_filed(filed):
        status_dic = {
            "isLog": False,
            "filed": None
        }
        try:
            filed = filed.replace("、", "/")
            status_dic["filed"] = filed
        except:
            status_dic["isLog"] = True
        finally:
            return status_dic


# 只有che300需要对model_name进行处理
def filter_table(func):

    print("filter_table...")

    def new_func(data, filed_name_list, log_driver, table, process_fun):
        if "model_name" in filed_name_list and table != "config_che300_major_info":
            log_driver.logger.info("过滤掉字段名称是model_name，且table不是che300数据")
            return
        return func(data, filed_name_list, log_driver, table, process_fun)
    return new_func


# 车型库字段管理模块
class ModelFiledProcess():

    @staticmethod
    @filter_table
    def process_data(data, filed_name_list, log_driver, table, process_fun):
        '''
        将字段的公共处理规则和私有处理规则分离
        :param data:
        :param filed_name_list:
        :param log_driver:
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
            log_driver.logger.warning("{}-->{}, source_table-->{}".format(filed_name, data.get(filed_name), table))
        elif status_dic.get("filed"):
            data[filed_name] = status_dic.get("filed")


# 车型库处理模块
class ModelProcessManage():
    '''
    车型库处理模块
    加载和管理车型库各个字段处理模块
    '''
    filed_process_dic = {
        "年款": {"func": YearProcess, "name_list": ["model_year"]},
        "变速箱": {"func": GearboxProcess, "name_list": ["gearbox", "auto"]},
        "指导价": {"func": PriceProcess, "name_list": ["model_price"]},
        "车型名称": {"func": NameProcess, "name_list": ["model_name"]},
        "排放标准": {"func": DischargeProcess, "name_list": ["discharge_standard"]},
        "车级别": {"func": CarLevelProcess, "name_list": ["car_level"]},
        "座位数": {"func": SeatNumberProcess, "name_list": ["seat_number"]},
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
            for process in ModelProcessManage.filed_process_dic.values():
                name_list = process.get("name_list")
                process_fun = process.get("func").process_filed
                ModelFiledProcess.process_data(data=data, filed_name_list=name_list, log_driver=log_driver, table=table, process_fun=process_fun)


if __name__ == '__main__':
    # ret = ModelGearboxProcess.process_filed("序列变速箱")
    # ret = ModelpriceProcess.process_filed(8.02)
    # ret = ModelDischargeProcess.process_filed("欧3")
    ret = NameProcess.process_filed("2018款  凯路威(进口) T6 2.0T 四驱 豪华商务车 美规")
    print(ret)







