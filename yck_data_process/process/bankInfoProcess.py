
class BankInfoProcessManage():
    '''
    银行信息
    '''
    @staticmethod
    def process_data_dic(data_dict, log_driver):
        data_list = data_dict.get("dataList")
        for d in data_list:
            if "data" in d:
                data = d["data"]
            else:
                data = d
            data["isManual"] = "false"
            data["isSync"] = "false"
