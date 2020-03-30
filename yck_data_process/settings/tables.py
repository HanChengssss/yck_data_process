auto_model_tables = [
    "config_autohome_major_info_tmp",
    "config_che300_major_info",
    "config_chezhibao_major_info",
    "config_autoowner_major_info_tmp",
    "config_souhu_major_info",
    "config_yiche_major_info",
    "config_youxin_major_info_tmp",
    "config_firstauto_major_info",
    "config_xcar_major_info",
    "config_tc5u_major_info",
    "config_auto12365_major_info_tmp",
    "config_wyauto_major_info"
]


class TablesManage():
    @staticmethod
    def get_tables(type):
        if type == "model":
            return auto_model_tables