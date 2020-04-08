from yck_data_process.logingDriver import Logger
from yck_data_process.process.autoModelProcess import ModelProcessManage
from yck_data_process.settingsManage import SettingsManage, MODEL

class ProcessManage():
    '''
    管理和加载所有类型数据的处理类
    '''
    @staticmethod
    def process_data(inputQueue, outputQueue):
        '''
        :param inputQueue:消费待处理队列的数据
        :param outputQueue: 将处理完成的数据放入该队列
        :return:
        '''
        sm = SettingsManage(model=MODEL)
        logDirManage = sm.get_logSettingsInstance()
        # 加载日志记录模块，记录处理过程中出现的异常
        logDriver = Logger("{}\modelProcess.log".format(logDirManage.get_logDirFullPath()), level='warning')
        while True:
            # print("process_Manage %s get_data" % (os.getpid()))
            dataDic = inputQueue.get()
            # print(dataDic)
            if dataDic == "end":
                print("process_Manage is end")
                outputQueue.put("end")
                break
            elif dataDic.get("type") == "model":
                ModelProcessManage.process_AutoModel_datas(dataDict=dataDic, logDriver=logDriver)
            elif dataDic.get("type") == "settings":
                pass
            outputQueue.put(dataDic)

