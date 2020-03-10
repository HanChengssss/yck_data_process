# !/usr/bin/env python
# -*-encoding: utf-8-*-
# author:HanCheng
# version:0.1
import re
from abc import ABCMeta, abstractmethod
from yck_data_process.logingDriver import Logger
import os
from multiprocessing import Queue, Process



# 单个字段处理基类
class ModelProcessBase(metaclass=ABCMeta):
    '''
    单个字段处理基类
    '''
    @abstractmethod
    def _process_filed(self, filed):
        pass

    @abstractmethod
    def standard_test(self, filed):
        pass


    def process_datas(self, dataList, filed_name, logDriver, table):
        for d in dataList:
            ret = self._process_filed(d.get(filed_name))
            if not ret:
                logDriver.logger.warning("{}-->{}, source_table-->{}".format(filed_name, d.get(filed_name), table))
            else:
                d[filed_name] = ret
                # dataList.append(d)
        return dataList

# 车型库年款字段处理处理模块
class modelYearProcess(ModelProcessBase):
    '''
    车型库年款字段处理处理模块
    '''
    def standard_test(self, filed):
        filed = str(filed)
        standardPattern = re.compile(r'\d+款')
        ret =standardPattern.search(filed)
        if ret:
            return True
        else:
            return False

    def _process_filed(self, filed):
        if not filed:
            return
        ret = self.standard_test(filed)
        if ret:
            return filed
        Intpatter = re.compile(r'\d+')
        Intret = Intpatter.match(str(filed)).group() if Intpatter.match(str(filed)) else None
        if Intret:
            if len(Intret) == 4:
                filed = str(Intret) + "款"
                return filed
        return None

# 车型库变速箱字段处理模块
class GearboxProcess(ModelProcessBase):
    '''
    车型库变速箱字段处理模块
    '''
    def standard_test(self, filed):
        standardList = ["电动", "自动", "手动"]
        standard_set = set(standardList)
        if filed not in standard_set:
            return False
        return True

    def _process_filed(self, filed):
        if not filed:
            return None
        ret = self.standard_test(filed)
        p1 = re.compile(r'自动|手动|电动')  # 标准
        # 单速变速箱

        p2 = re.compile(r'CVT无级变速|手自一体|机械自动|双离合|双离合\.*手自动一体|DSG双离合|双离合器|G-DCT|DCT|DSG|AT|AMT智能手动版|AMT智能手动|AMT|EMT|IMT')  # --> 自动
        p3 = re.compile(r'单速变速箱')  # -->电动
        p4 = re.compile(r'序列式')  # -->手动

        if ret:
            return filed
        r1 = p1.search(filed)
        r1 = r1.group() if r1 else None
        if r1:
            return r1
        r2 = p2.search(filed)
        r2 = r2.group() if r2 else None
        if r2:
            r2 = "自动"
            return r2
        r3 = p3.search(filed)
        r3 = r3.group() if r3 else None
        if r3:
            r3 = "电动"
            return r3
        r4 = p4.search(filed)
        r4 = r4.group() if r4 else None
        if r4:
            r4 = "手动"
            return r4
        return None

# 车型库处理模块
class AutoModelProcess():
    '''
    车型库处理模块
    加载和管理车型库各个字段处理模块
    '''
    @staticmethod
    def process_AutoModel_datas(dataDicts, logDriver):
        dataList = dataDicts.get("dataList")
        table = dataDicts.get("table")
        modelYearProcess().process_datas(dataList=dataList, filed_name="model_name", logDriver=logDriver, table=table)
        GearboxProcess().process_datas(dataList=dataList, filed_name="gearbox", logDriver=logDriver, table=table)

# 管理和加载所有类型数据的处理方法
class ProcessManage():

    @staticmethod
    def process_data(inputQueue, outputQueue):
        '''
        管理和加载所有类型数据的处理方法
        :param inputQueue:消费待处理队列的数据
        :param outputQueue: 将处理完成的数据放入该队列
        :return:
        '''
        # 加载日志记录模块，记录处理过程中出现的异常
        logDriver = Logger("D:\YCK\代码\yck_data_process\yck_data_process\log_dir\modelProcess.log", level='warning')
        while True:
            print("process_Manage %s get_data" % (os.getpid()))
            dataDic = inputQueue.get()
            if dataDic == "end":
                print("process_Manage is end")
                outputQueue.put("end")
                break
            elif dataDic.get("type") == "auto_model":
                AutoModelProcess.process_AutoModel_datas(dataDicts=dataDic, logDriver=logDriver)
            elif dataDic.get("type") == "settings":
                pass
            outputQueue.put(dataDic)




if __name__ == '__main__':
    q1 = Queue()
    q2 = Queue()
    dataDict = {
        "table": "xxx",
        "type": "auto_model",
        "dataList": [
            {
                "model_name": None,
                "gearbox": None,
            }
        ]
    }
    q1.put(dataDict)
    q1.put("end")
    p1 = Process(target=ProcessManage.process_data, args=((q1, q2)))
    p1.start()
    p1.join()
    print(dataDict)







