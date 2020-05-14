from yck_data_process.logingDriver import Logger


class ProcessManage():
    '''
    管理和加载所有类型数据的处理类
    '''
    @staticmethod
    def process_data(input_queue, output_queue, sm_instance, dps_instance):
        '''
        :param input_queue:消费待处理队列的数据
        :param output_queue: 将处理完成的数据放入该队列
        :return:
        '''
        log_dir_mange = sm_instance.get_log_setting_instance()
        # 加载日志记录模块，记录处理过程中出现的异常
        log_driver = Logger("{}\modelProcess.log".format(log_dir_mange.get_log_dir_full_path()), level='warning')

        while True:
            data_dic = input_queue.get()
            # print(data_dic)
            if data_dic == "end":
                # print("process_Manage is end")
                log_driver.logger.info("process_Manage is end")
                output_queue.put("end")
                break
            coll = data_dic.get("coll_name")
            data_process_func = dps_instance.get_process_func(coll)
            data_process_func.process_data_dic(data_dic, log_driver)
            output_queue.put(data_dic)

