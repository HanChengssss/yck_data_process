

# 车型库字段管理模块
class SettingFiledProcess():

    @staticmethod
    def process_data(data, filed_name_list, log_driver, table, process_fun):
        """
        将字段的公共处理规则和私有处理规则分离
        :param data:
        :param filed_name_list:
        :param log_driver:
        :param table:
        :param process_fun:
        :return:

        """



class SettingProcessManage():
    """
    车型配置处理模块
    加载和管理型配置各个字段处理模块
    """
    filed_process_dic = {
    }

    @staticmethod
    def process_data_dic(data_dict, log_driver):
        # data_list = data_dict.get("dataList")
        # table = data_dict.get("table")
        # for item in data_list:
        #     if "data" in item:
        #         data = item["data"]
        #     else:
        #         data = item
        #     model_id = item["model_id"]
        #     data["model_id"] = model_id
        pass