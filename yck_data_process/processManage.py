from yck_data_process.logingDriver import Logger
from yck_data_process.process.autoModelProcess import ModelProcessManage
from yck_data_process.process.positionProcess import PositionProcessManage
from yck_data_process.settingsManage import SettingsManage, MODEL


class ProcessManage():
    '''
    管理和加载所有类型数据的处理类
    '''
    data_dic_process_dic = {
        "model": {"func": ModelProcessManage},
        "position": {"func": PositionProcessManage},
    }
    
    @staticmethod
    def process_data(input_queue, output_queue):
        '''
        :param input_queue:消费待处理队列的数据
        :param output_queue: 将处理完成的数据放入该队列
        :return:
        '''

        sm = SettingsManage(model=MODEL)
        log_dir_mange = sm.get_log_setting_instance()
        # 加载日志记录模块，记录处理过程中出现的异常
        log_driver = Logger("{}\modelProcess.log".format(log_dir_mange.get_logDirFullPath()), level='warning')
        while True:
            # print("process_Manage %s get_data" % (os.getpid()))
            data_dic = input_queue.get()
            data_type = data_dic.get("type")
            if data_dic == "end":
                # print("process_Manage is end")
                log_driver.logger.info("process_Manage is end")
                output_queue.put("end")
                break
            data_type_process_manage = ProcessManage.data_dic_process_dic.get(data_type).get("func")
            data_type_process_manage.process_data_dic(data_dic, log_driver)
            output_queue.put(data_dic)

