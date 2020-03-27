# !/usr/bin/env python
# -*-encoding: utf-8-*-
# author:HanCheng
# version:0.1
import re
from abc import ABCMeta, abstractmethod
from yck_data_process.logingDriver import Logger
import os
from multiprocessing import Queue, Process
from yck_data_process import settings

# 过滤掉字段名称是model_name，且table不是che300数据
def filterTable(func):

    print("filterTable...")

    def new_func(data, filedNameList, logDriver, table, processFun):
        if "model_name" in filedNameList and table != "config_che300_major_info":
            logDriver.logger.info("过滤掉字段名称是model_name，且table不是che300数据")
            return
        return func(data, filedNameList, logDriver, table, processFun)
    return new_func


# 车型库年款字段处理处理模块
class ModelYearProcess():
    '''
    车型库年款字段处理处理模块
    '''
    @staticmethod
    def process_filed(filed):
        statusDic = {
            "isLog": False,
            "filed": None
        }
        ret = re.search(r'\d{4}', filed)
        if ret:
            statusDic["filed"] = ret.group()
            return statusDic
        statusDic["isLog"] = True
        return statusDic


# 车型库变速箱字段处理模块
class ModelGearboxProcess():
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
        :param logDriver:
        :param table:
        :return:
        '''
        statusDic = {
            "isLog": False,
            "filed": None
        }
        p1 = re.compile(r'自动|手动|电动')  # 标准
        p2 = re.compile(r'.*CVT|.*无级变速|手自一体|机械自动|双离合|双离合\.*手自动一体|DSG双离合|双离合器|G-DCT|DCT|DSG|AT|AMT智能手动版|AMT智能手动|AMT|EMT|IMT')  # --> 自动
        p3 = re.compile(r'单速变速箱')  # -->电动
        p4 = re.compile(r'.*序列')  # -->手动
        r1 = p1.search(filed)

        r1 = r1.group() if r1 else None
        if r1:
            statusDic["filed"] = r1
            return statusDic

        r2 = p2.search(filed)
        r2 = r2.group() if r2 else None
        if r2:
            statusDic["filed"] = "自动"
            return statusDic

        r3 = p3.search(filed)
        r3 = r3.group() if r3 else None
        if r3:
            statusDic["filed"] = "电动"
            return statusDic

        r4 = p4.search(filed)
        r4 = r4.group() if r4 else None
        if r4:
            statusDic["filed"] = "手动"
            return statusDic

        statusDic["isLog"] = True
        return statusDic


# 指导价处理模块
class ModelPriceProcess():
    '''
    指导价处理模块
    '''

    @staticmethod
    def process_filed(filed):
        statusDic = {
            "isLog": False,
            "filed": None
        }
        if int(filed) < 10000:
            return statusDic
        try:
            r1 = round(int(filed)/10000, 2)  # 四舍五入保留两位小数
            statusDic["filed"] = r1
            return statusDic
        except:
            statusDic["isLog"] = True
            return statusDic


# 车型名称处理模块
class ModelNameProcess():

    @staticmethod
    def process_filed(filed):
        statusDic = {
            "isLog": False,
            "filed": None
        }
        try:
            # 2008款 海狮 汽油系列三菱动力2.4(商务型)
            ret = re.search(r'\d{4}款 \w+ \w+', filed)
            assert ret.group()
            return statusDic
        except:
            statusDic["isLog"] = True
            return statusDic


# 车型库排放标准处理模块
class ModelDischargeProcess():

    @staticmethod
    def process_filed(filed):
        # discharge_standard
        statusDic = {
            "isLog": False,
            "filed": None
        }
        pattern = re.compile(r'国1|国2|国3|国4|国5|国6|京3|欧4')
        ret = pattern.search(filed)
        if ret:
            statusDic["filed"] = ret.group()
            return statusDic

        if len(filed) == 2 and isinstance(filed, str):
            try:
                romeNumberDic = {"Ⅰ": 1, "Ⅱ": 2, "Ⅲ": 3, "Ⅳ": 4, "Ⅴ": 5}
                romeNumber = filed[1]
                assert romeNumber in romeNumberDic
                statusDic["filed"] = filed.replace(romeNumber, str(romeNumberDic[romeNumber]))
                return statusDic
            except:
                statusDic["isLog"] = True
                return statusDic
        statusDic["isLog"] = True
        return statusDic


# 车级别处理模块
class ModelAutoCarLevelProcess():
    @staticmethod
    def process_filed(filed):
        statusDic = {
            "isLog": False,
            "filed": None
        }
        try:
            pattern = re.compile(r'微型车|小型车|紧凑型车|中型车|中大型车|豪华车|小型SUV|紧凑型SUV|中型SUV|中大型SUV|大型SUV|全尺寸SUV|跑车|MPV|客车|皮卡|微面|卡车|其它')
            ret = pattern.search(filed)
            assert ret.group()
            statusDic["filed"] = ret.group()
            return statusDic
        except:
            statusDic["isLog"] = True
            return statusDic


# 座位数处理模块
class ModelAutoSeatNumberProcess():
    @staticmethod
    def process_filed(filed):
        statusDic = {
            "isLog": False,
            "filed": None
        }
        filed = filed.replace("、", "/")
        statusDic["filed"] = filed
        return statusDic


# 车型库字段管理模块
class ModelFieldProcessMange():

    @staticmethod
    @filterTable
    def process_data(data, filedNameList, logDriver, table, processFun):
        '''
        将字段的公共处理规则和私有处理规则分离
        todo 这个方法可以写成装饰器
        :param data:
        :param filedNameList:
        :param logDriver:
        :param table:
        :param processFun:
        :return:
        '''
        filedName = None
        for fn in filedNameList:
            if fn in data:
                filedName = fn
        if not filedName:
            return
        filed = data.get(filedName)
        if not filed:
            return
        # 字段处理规则
        statusDic = processFun(filed)
        print(statusDic)
        if statusDic.get("isLog"):
            logDriver.logger.warning("{}-->{}, source_table-->{}".format(filedName, data.get(filedName), table))
        elif statusDic.get("filed"):
            data[filedName] = statusDic.get("filed")


# 车型库处理模块
class ModelProcessManage():
    '''
    车型库处理模块
    加载和管理车型库各个字段处理模块
    '''
    filedProcessDic = {
        "年款": {"func": ModelYearProcess, "nameList": ["model_year"]},
        "变速箱": {"func": ModelGearboxProcess, "nameList": ["gearbox", "auto"]},
        "指导价": {"func": ModelPriceProcess, "nameList": ["model_process"]},
        "车型名称": {"func": ModelNameProcess, "nameList": ["model_name"]},
        "排放标准": {"func": ModelDischargeProcess, "nameList": ["discharge_standard"]},
        "车级别": {"func": ModelAutoCarLevelProcess, "nameList": ["car_level"]},
        "座位数": {"func": ModelAutoSeatNumberProcess, "nameList": ["seat_number"]},
    }

    @staticmethod
    def process_AutoModel_datas(dataDict, logDriver):
        dataList = dataDict.get("dataList")
        table = dataDict.get("table")
        for d in dataList:
            if "data" in d:
                data = d["data"]
            else:
                data = d
            for process in ModelProcessManage.filedProcessDic.values():
                nameList = process.get("nameList")
                processFun = process.get("func").process_filed
                ModelFieldProcessMange.process_data(data=data, filedNameList=nameList, logDriver=logDriver, table=table, processFun=processFun)


if __name__ == '__main__':
    # ret = ModelGearboxProcess.process_filed("序列变速箱")
    # ret = ModelpriceProcess.process_filed(8.02)
    # ret = ModelDischargeProcess.process_filed("国IV")
    ret = ModelNameProcess.process_filed("2008款 海 汽油系")
    print(ret)







