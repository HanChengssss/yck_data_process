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
class modelYearProcess():
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
    def process_filed(data, filed_name, logDriver, table):
        filed = data.get(filed_name)
        if not filed:
            return
        ret = modelYearProcess.standard_test(filed)
        if ret:
            data[filed_name] = filed
            return
        # Intpatter = re.compile(r'\d+')
        # Intret = Intpatter.search(str(filed)).group() if Intpatter.search(str(filed)) else None
        # if Intret:
        #     if len(Intret) == 4:
        #         filed = str(Intret) + "款"
        #         data[filed_name] = filed
        #         return
        logDriver.logger.warning("{}-->{}, source_table-->{}".format(filed_name, data.get(filed_name), table))


# 车型库变速箱字段处理模块
class GearboxProcess():
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
        :param filed:
        :return:
        '''
        standardList = ["电动", "自动", "手动"]
        standard_set = set(standardList)
        if filed not in standard_set:
            return False
        return True

    @staticmethod
    def process_filed(data, filed_name, logDriver, table):
        '''
        由于变速箱的字段名称有两个：gearbox,auto
        所以需要经过两次判断
        :param data:
        :param filed_name:
        :param logDriver:
        :param table:
        :return:
        '''
        filed = data.get(filed_name)
        if not filed:
            filed = data.get("auto")
        if not filed:
            return
        ret = GearboxProcess.standard_test(filed)
        if ret:
            data[filed_name] = filed
            return
        p1 = re.compile(r'自动|手动|电动')  # 标准
        p2 = re.compile(r'CVT无级变速|手自一体|机械自动|双离合|双离合\.*手自动一体|DSG双离合|双离合器|G-DCT|DCT|DSG|AT|AMT智能手动版|AMT智能手动|AMT|EMT|IMT')  # --> 自动
        p3 = re.compile(r'单速变速箱')  # -->电动
        p4 = re.compile(r'序列式')  # -->手动
        r1 = p1.search(filed)
        r1 = r1.group() if r1 else None
        if r1:
            data[filed_name] = r1
            return
        r2 = p2.search(filed)
        r2 = r2.group() if r2 else None
        if r2:
            data[filed_name] = "自动"
            return
        r3 = p3.search(filed)
        r3 = r3.group() if r3 else None
        if r3:
            data[filed_name] = "电动"
            return
        r4 = p4.search(filed)
        r4 = r4.group() if r4 else None
        if r4:
            data[filed_name] = "手动"
            return
        logDriver.logger.warning("{}-->{}, source_table-->{}".format(filed_name, data.get(filed_name), table))


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
    def process_filed(data, filed_name, logDriver, table):
        filed = data.get(filed_name)
        if not filed:
            return
        ret = ModelpriceProcess.standard_test(filed)
        if ret:
            data[filed_name] = filed
            return
        try:
            r1 = float(int(filed)/10000)
            data[filed_name] = r1
            return
        except:
            logDriver.logger.warning("{}-->{}, source_table-->{}".format(filed_name, data.get(filed_name), table))


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
    def process_filed(data, filed_name, logDriver, table):
        '''
        这个模块只检测车300的model_name
        '''
        if table == "config_che300_major_info":
            filed = data.get(filed_name)
            ret = ModelNameProcess.standard_test(filed)
            if ret:
                return
            logDriver.logger.warning("{}-->{}, source_table-->{}".format(filed_name, data.get(filed_name), table))


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
    def process_filed(data, filed_name, logDriver, table):
        # discharge_standard
        filed_name = "discharge_standard"
        filed = data.get(filed_name)
        if table == "config_che300_major_info":
            ret = ModelNameProcess.standard_test(filed)
            if ret:
                pattern = re.compile(r'国1|国2|国3|国4|国5|国6|京3|欧4')
                data[filed_name] = pattern.search(filed).group()
                return
            logDriver.logger.warning("{}-->{}, source_table-->{}".format(filed_name, data.get(filed_name), table))
        elif table == "config_firstauto_major_info":
            if not filed:
                return
            if isinstance(filed, str):
                try:
                    if len(filed) >= 2:
                        lomaDic = {"Ⅰ": 1, "Ⅱ": 2, "Ⅲ": 3, "Ⅳ": 4, "Ⅴ": 5}
                        new_filed = filed.replace(filed[1], str(lomaDic.get(filed[1])))
                        data[filed_name] = new_filed
                        return
                except:
                    logDriver.logger.warning("{}-->{}, source_table-->{}".format(filed_name, data.get(filed_name), table))


# 车型库处理模块
class AutoModelProcess():
    '''
    车型库处理模块
    加载和管理车型库各个字段处理模块
    model_year
    gearbox
    model_price
    '''
    # 标记没有目标字段的车型库，自动忽略。
    # ignoreDict = {
    #     "modelYear": ["config_autoowner_major_info_tmp", "config_wyauto_major_info"],
    #     "gearBox": [
    #         "config_autohome_major_info_tmp",
    #         "config_che300_major_info",
    #         "config_chezhibao_major_info",
    #         "config_souhu_major_info",
    #         "config_youxin_major_info_tmp",
    #         "config_firstauto_major_info",
    #         "config_xcar_major_info",
    #         "config_tc5u_major_info",
    #         "config_auto12365_major_info_tmp",
    #         "config_wyauto_major_info"
    #     ]
    # }

    @staticmethod
    def process_AutoModel_datas(dataDict, logDriver):
        dataList = dataDict.get("dataList")
        table = dataDict.get("table")
        for d in dataList:
            if "data" in d:
                data = d["data"]
            else:
                data = d
            modelYearProcess.process_filed(filed_name="model_year", data=data, logDriver=logDriver, table=table)
            GearboxProcess.process_filed(filed_name="gearbox", data=data, logDriver=logDriver, table=table)
            ModelpriceProcess.process_filed(filed_name="model_price", data=data, logDriver=logDriver, table=table)
            ModelNameProcess.process_filed(filed_name="model_name", data=data, logDriver=logDriver, table=table)


if __name__ == '__main__':
    log = ""
    data = dict(discharge_standard="国Ⅰ")
    ModelDischargeProcess.process_filed(data, filed_name="discharge_standard", logDriver=log, table="config_firstauto_major_info")
    print(data)






