
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
            bank_code = data.get("bank_code")
            if bank_code is None:
                pass
            else:
                bank_code = bank_code.strip()
            if not bank_code:
               data["bank_code"] = "000000000000"
               data["bank_type"] = "000000000000"
               data["bank_province"] = "000000000000"
               data["bank_name"] = "000000000000"
               data["bank_city"] = "000000000000"
               data["isManual"] = "false"
               data["isSync"] = "false"
            else:
                data["isManual"] = "false"
                data["isSync"] = "false"
