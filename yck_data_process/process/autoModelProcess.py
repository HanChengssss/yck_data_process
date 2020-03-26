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

# 车型库年款字段处理处理模块
class ModelYearProcess():
    '''
    车型库年款字段处理处理模块
    '''
    @staticmethod
    def standard_test(filed):
        '''
        测试输入的字段是否符合标准
        符合返回True
        不符合返回False
        :param filed:
        :return:
        '''
        try:
            filed = str(int(filed))
            if len(filed) == 4:
                return True
            else:
                return False
        except:
            return False

    @staticmethod
    def process_filed(filed):
        statusDic = {
            "isLog": False,
            "filed": None
        }
        ret = ModelYearProcess.standard_test(filed)
        if ret:
            return statusDic
        # Intpatter = re.compile(r'\d+')
        # Intret = Intpatter.search(str(filed)).group() if Intpatter.search(str(filed)) else None
        # if Intret:
        #     if len(Intret) == 4:
        #         filed = str(Intret) + "款"
        #         data[filed_name] = filed
        #         return
        statusDic["isLog"] = True
        return statusDic



# 车型库变速箱字段处理模块
class ModelGearboxProcess():
    '''
    车型库变速箱字段处理模块
    '''
    @staticmethod
    def standard_test(filed):
        '''
        测试输入的字段是否符合标准
        符合返回True
        不符合返回False
        :param filed:
        :return:
        '''
        standardList = ["电动", "自动", "手动"]
        standard_set = set(standardList)
        if filed not in standard_set:
            return False
        return True

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
        ret = ModelGearboxProcess.standard_test(filed)
        if ret:
            return
        p1 = re.compile(r'自动|手动|电动')  # 标准
        p2 = re.compile(r'.*CVT|.*无级变速|手自一体|机械自动|双离合|双离合\.*手自动一体|DSG双离合|双离合器|G-DCT|DCT|DSG|AT|AMT智能手动版|AMT智能手动|AMT|EMT|IMT')  # --> 自动
        p3 = re.compile(r'单速变速箱')  # -->电动
        p4 = re.compile(r'序列式')  # -->手动
        r1 = p1.search(filed)
        r1 = r1.group() if r1 else None
        if r1:
            statusDic["isLog"] = False
            statusDic["filed"] = r1
            return statusDic
        r2 = p2.search(filed)
        r2 = r2.group() if r2 else None
        if r2:
            statusDic["isLog"] = False
            statusDic["filed"] = "自动"
            return statusDic
        r3 = p3.search(filed)
        r3 = r3.group() if r3 else None
        if r3:
            statusDic["isLog"] = False
            statusDic["filed"] = "电动"
            return statusDic
        r4 = p4.search(filed)
        r4 = r4.group() if r4 else None
        if r4:
            statusDic["isLog"] = False
            statusDic["filed"] = "手动"
            return statusDic


# 指导价处理模块
class ModelpriceProcess():
    '''
    指导价处理模块
    '''
    @staticmethod
    def standard_test(filed):
        '''
        测试输入的字段是否符合标准
        符合返回True
        不符合返回False
        :param filed:
        :return:
        :param filed:
        :return:
        '''
        try:
            if int(filed) < 10000:
                return True
            else:
                return False
        except:
            return False

    @staticmethod
    def process_filed(data, logDriver, table):
        filedNameList = ["model_price"]
        filedName = None
        for fn in filedNameList:
            if fn in data:
                filedName = fn
        if not filedName:
            return
        filed = data.get(filedName)
        if not filed:
            return
        ret = ModelpriceProcess.standard_test(filed)
        if ret:
            data[filedName] = filed
            return
        try:
            r1 = float(int(filed)/10000)
            data[filedName] = r1
            return
        except:
            logDriver.logger.warning("{}-->{}, source_table-->{}".format(filedName, data.get(filedName), table))


# 车型名称处理模块
class ModelNameProcess():
    @staticmethod
    def standard_test(filed):
        # 2008款 海狮 汽油系列三菱动力2.4(商务型)
        try:
            ret = re.search("\d+款", filed.split(" ")[0])
            if ret:
                return True
            else:
                return False
        except:
            return False

    @staticmethod
    def process_filed(data, logDriver, table):
        '''
        这个模块只检测车300的model_name
        '''
        filedNameList = ["model_name"]
        filedName = None
        for fn in filedNameList:
            if fn in data:
                filedName = fn
        if not filedName:
            return
        filed = data.get(filedName)
        if not filed:
            return
        if table in ["config_che300_major_info", "config_autohome_major_info_tmp"]:
            ret = ModelNameProcess.standard_test(filed)
            if ret:
                return
            logDriver.logger.warning("{}-->{}, source_table-->{}".format(filedName, data.get(filedName), table))


# 车型库排放标准处理模块
class ModelDischargeProcess():
    @staticmethod
    def standard_test(filed):
        pattern = re.compile(r'国1|国2|国3|国4|国5|国6|京3|欧4')
        try:
            ret = pattern.search(filed)
            if ret:
                return True
            else:
                return False
        except:
            return False


    @staticmethod
    def process_filed(data, logDriver, table):
        # discharge_standard
        filedNameList = ["discharge_standard"]
        filedName = None
        for fn in filedNameList:
            if fn in data:
                filedName = fn
        if not filedName:
            return
        filed = data.get(filedName)
        if not filed:
            return
        if table == "config_che300_major_info":
            ret = ModelDischargeProcess.standard_test(filed)
            if ret:
                pattern = re.compile(r'国1|国2|国3|国4|国5|国6|京3|欧4')
                data[filedName] = pattern.search(filed).group()
                return
            logDriver.logger.warning("{}-->{}, source_table-->{}".format(filedName, data.get(filedName), table))
        elif table == "config_firstauto_major_info":
            if not filed:
                return
            if isinstance(filed, str):
                try:
                    if len(filed) >= 2:
                        lomaDic = {"Ⅰ": 1, "Ⅱ": 2, "Ⅲ": 3, "Ⅳ": 4, "Ⅴ": 5}
                        new_filed = filed.replace(filed[1], str(lomaDic.get(filed[1])))
                        data[filedName] = new_filed
                        return
                except:
                    logDriver.logger.warning("{}-->{}, source_table-->{}".format(filedName, data.get(filedName), table))


# 车级别处理模块
class ModelAutoCarLevelProcess():
    @staticmethod
    def standard_test(filed):
        pattern = re.compile(r'微型车|小型车|紧凑型车|中型车|中大型车|豪华车|小型SUV|紧凑型SUV|中型SUV|中大型SUV|大型SUV|全尺寸SUV|跑车|MPV|客车|皮卡|微面|卡车|其它')
        try:
            ret = pattern.search(filed)
            if ret:
                return True
            else:
                return False
        except:
            return False

    @staticmethod
    def process_filed(data, logDriver, table):
        filedNameList = ["car_level"]
        filedName = None
        for fn in filedNameList:
            if fn in data:
                filedName = fn
        if not filedName:
            return
        filed = data.get(filedName)
        if not filed:
            return
        if table == "config_che300_major_info":
            ret = ModelAutoCarLevelProcess.standard_test(filed)
            if ret:
                pattern = re.compile(r'微型车|小型车|紧凑型车|中型车|中大型车|豪华车|小型SUV|紧凑型SUV|中型SUV|中大型SUV|大型SUV|全尺寸SUV|跑车|MPV|客车|皮卡|微面|卡车|其它')
                data[filedName] = pattern.search(filed).group()
                return
            logDriver.logger.warning("{}-->{}, source_table-->{}".format(filedName, data.get(filedName), table))


# 座位数处理模块
class ModelAutoSeatNumberProcess():
    @staticmethod
    def process_filed(data, logDriver, table):
        filedNameList = ["seat_number"]
        filedName = None
        for fn in filedNameList:
            if fn in data:
                filedName = fn
        if not filedName:
            return
        filed = data.get(filedName)
        if not filed:
            return
        if table == "config_che300_major_info":
            # 7、8、11
            filed = filed.replace("、", "/")
            data[filedName] = filed
            return

# 车型库字段管理模块
class ModelFieldProcessMange():

    @staticmethod
    def process_data(data, filedNameList, logDriver, table, processFun):
        '''
        将字段的公共处理规则和私有处理规则分离
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
        "年款": ModelYearProcess,  # ["model_year"]
        "变速箱": ModelGearboxProcess,  # ["gearbox", "auto"]
        "指导价": ModelpriceProcess,
        "车型名称": ModelNameProcess,
        "排放标准": ModelDischargeProcess,
        "车级别": ModelAutoCarLevelProcess,
        "座位数": ModelAutoSeatNumberProcess,
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
                process.process_filed(data=data, logDriver=logDriver, table=table)


if __name__ == '__main__':
    ModelFieldProcessMange.process_data(data={"model_year": "2998"}, filedNameList=["model_year"], logDriver="", table="xxx", processFun=ModelYearProcess.process_filed)






