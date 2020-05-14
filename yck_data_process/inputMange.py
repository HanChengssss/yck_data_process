from multiprocessing import Queue
from yck_data_process.settingsManage import SettingsManage, MODEL

class InputDataMange():
    @staticmethod
    def input_data(input_queue, sm_instance, dps_instance):
        input_func = dps_instance.get_input_func()
        input_func.input_data(input_queue, sm_instance, dps_instance)
        input_queue.put("end")
        print("input_queue have been finished !")


if __name__ == '__main__':
    q = Queue()
    sm = SettingsManage(MODEL)
    dps = sm.get_dsp_setting_instance("mysql")
    i = InputDataMange()
    i.input_data(q, sm, dps)
    print(q.qsize())

