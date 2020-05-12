from yck_data_process.testDriver.toolTestDriver import ToolTestDriver
from yck_data_process.process.autoModelProcess import ModelProcessManage
from yck_data_process.process.autoModelProcess import *
from yck_data_process.settingsManage import SettingsManage, MODEL
import pymongo
from yck_data_process.logingDriver import Logger
from queue import Queue
from yck_data_process.inputMange import InputDataMange
from datetime import datetime
'''
测试流程
从mongodb取出数据
放到AutoModelProcess中
'''

def parse_setting(auto_paramt, auto_config, name_chs, name_dict, autohome_id):
    item = dict()
    item["autohome_id"] = autohome_id
    paramt_result = get_json_list(auto_paramt)
    config_result = get_json_list(auto_config)
    parse_json_list(paramt_result, item, name_chs, name_dict)
    parse_json_list(config_result, item, name_chs, name_dict)
    # print(name_chs)
    if len(name_chs) > 0:
        for chs in name_chs:
            key = name_dict[chs]
            item[key] = '无'
    item["add_time"] = datetime.today()
    item["update_time"] = datetime.today()
    item['engine'] = item['emission']
    item['sub_air_bag'] = item['master_air_bag']
    item['rear_side_air_bag'] = item['front_side_air_bag']
    item['rear_head_air_bag'] = item['front_head_air_bag']
    item['rear_parking_radar'] = item['front_parking_radar']
    item['rear_seat_heating'] = item['front_seat_heating']
    item['rear_seat_ventilation'] = item['front_seat_ventilation']
    item['rear_electric_window'] = item['front_electric_window']
    item['url'] = ""
    print(item)
    return item


def get_json_list(json_dic):
    config_dic = json_dic.get("result")
    result = {}
    if "paramtypeitems" in config_dic:
        json_list = config_dic["paramtypeitems"]
        result["json_list"] = json_list
        result["key"] = "paramitems"
    elif "configtypeitems" in config_dic:
        json_list = config_dic["configtypeitems"]
        result["json_list"] = json_list
        result["key"] = "configitems"
    else:
        raise Exception("key not in json_dic")
    return result


def parse_json_list(result, item, name_chs, name_dict):
    json_list = result["json_list"]
    # print(json_list)
    data_body_key = result["key"]
    # print(key)
    for config_dic in json_list:
        # print(config_dic[data_body_key])
        for configitem in config_dic[data_body_key]:
            tag = configitem['name']
            config = configitem['value']
            if '&nbsp;/&nbsp;' in config:
                strinfo = re.compile(r'&nbsp;/&nbsp;')
                config = strinfo.sub('/', config)
            if '●' in config:
                strinfo = re.compile(r'●')
                config = strinfo.sub('标配', config)
            if '○' in config:
                strinfo = re.compile(r'○')
                config = strinfo.sub('选配', config)
            if '-' in config:
                strinfo = re.compile(r'-')
                config = strinfo.sub('无', config)
            if tag == '后悬架类型':
                config = config.replace('+', '').replace(',', '')
            if tag in '相关链接':
                pass
            if tag in name_chs:
                key = name_dict[tag]
                item[key] = config
                name_chs.remove(tag)


class settingFiledProcess():
    @staticmethod
    def process_data(data):
        name_chs = ['发动机', '级别', '发动机2', '变速箱', '长度(mm)', '宽度(mm)', '高度(mm)', '车身结构', '轴距(mm)', '整备质量(kg)', '行李厢容积(L)',
                    '进气形式', '气缸排列形式', '气缸数(个)', '配气机构', '最大马力(Ps)', '最大扭矩(N·m)', '燃料形式', '燃油标号', '供油方式', '环保标准', '驱动方式',
                    '前悬架类型', '后悬架类型', '助力类型', '车体结构', '前制动器类型', '后制动器类型', '驻车制动类型', '前轮胎规格', '后轮胎规格', '主/副驾驶座安全气囊',
                    '主/副驾驶座安全气囊2', '前/后排侧气囊', '前/后排侧气囊2', '前/后排头部气囊(气帘)', '前/后排头部气囊(气帘)2', '胎压监测装置', 'ISOFIX儿童座椅接口',
                    '车内中控锁', '无钥匙启动系统', 'ABS防抱死', '刹车辅助(EBA/BAS/BA等)', '车身稳定控制(ESC/ESP/DSC等)', '可变悬架', '电动天窗', '全景天窗',
                    '多功能方向盘', '定速巡航', '前/后驻车雷达', '前/后驻车雷达2', '倒车视频影像', '座椅材质', '电动座椅记忆', '前/后排座椅加热', '前/后排座椅加热2',
                    '前/后排座椅通风', '前/后排座椅通风2', 'GPS导航系统', '近光灯', 'LED日间行车灯', '自动头灯', '前雾灯', '前/后电动车窗', '前/后电动车窗2',
                    '后视镜电动调节', '后视镜加热', '空调控制方式', '外观颜色', '外观颜色码']
        name_dict = {'发动机': 'emission', '级别': 'level', '发动机2': 'engine', '变速箱': 'gear_box', '长度(mm)': 'length',
                     '宽度(mm)': 'width', '高度(mm)': 'height', '车身结构': 'body_structure', '轴距(mm)': 'wheelbase',
                     '整备质量(kg)': 'weight', '行李厢容积(L)': 'trunk_volume', '进气形式': 'intake',
                     '气缸排列形式': 'cylinder_arrangement', '气缸数(个)': 'cylinders', '配气机构': 'admission_gear',
                     '最大马力(Ps)': 'max_ps', '最大扭矩(N·m)': 'max_n_m', '燃料形式': 'fuel', '燃油标号': 'fuel_grade',
                     '供油方式': 'fuel_supply_system', '环保标准': 'environmental_standards_org', '驱动方式': 'drive_mode',
                     '前悬架类型': 'front_suspension_type', '后悬架类型': 'rear_suspension_type', '助力类型': 'power_type',
                     '车体结构': 'car_boty_type', '前制动器类型': 'front_brake_type', '后制动器类型': 'rear_brake_type',
                     '驻车制动类型': 'parking_brake_type', '前轮胎规格': 'front_tire_specifications',
                     '后轮胎规格': 'rear_tire_specifications', '主/副驾驶座安全气囊': 'master_air_bag', '主/副驾驶座安全气囊2': 'sub_air_bag',
                     '前/后排侧气囊': 'front_side_air_bag', '前/后排侧气囊2': 'rear_side_air_bag',
                     '前/后排头部气囊(气帘)': 'front_head_air_bag', '前/后排头部气囊(气帘)2': 'rear_head_air_bag',
                     '胎压监测装置': 'tire_pressure_monitoring', 'ISOFIX儿童座椅接口': 'ISOFIX_child_seat_interfaces',
                     '车内中控锁': 'car_internal_lock', '无钥匙启动系统': 'keyless_start_system', 'ABS防抱死': 'abs',
                     '刹车辅助(EBA/BAS/BA等)': 'brake_assist', '车身稳定控制(ESC/ESP/DSC等)': 'stability_control',
                     '可变悬架': 'variable_suspension', '电动天窗': 'electric_roof', '全景天窗': 'panoramic_roof',
                     '多功能方向盘': 'multifunction_steering_wheel', '定速巡航': 'cruise', '前/后驻车雷达': 'front_parking_radar',
                     '前/后驻车雷达2': 'rear_parking_radar', '倒车视频影像': 'reverse_video_image', '座椅材质': 'seat_material',
                     '电动座椅记忆': 'electric_seat_memory', '前/后排座椅加热': 'front_seat_heating',
                     '前/后排座椅加热2': 'rear_seat_heating', '前/后排座椅通风': 'front_seat_ventilation',
                     '前/后排座椅通风2': 'rear_seat_ventilation', 'GPS导航系统': 'gps', '近光灯': 'low_beam_lamp',
                     'LED日间行车灯': 'daytime_running_light', '自动头灯': 'automatic_headlights', '前雾灯': 'front_fog_lamp',
                     '前/后电动车窗': 'front_electric_window', '前/后电动车窗2': 'rear_electric_window',
                     '后视镜电动调节': 'mirror_electric_adjustment', '后视镜加热': 'mirror_heating',
                     '空调控制方式': 'air_conditioning_control_mode', '外观颜色': 'color_outside', '外观颜色码': 'color_outside_code'}
        auto_paramt = data["option"]
        auto_config = data["config"]
        autohome_id = data["autohome_id"]
        parse_setting(auto_paramt, auto_config, name_chs, name_dict, autohome_id)


def process_test_driver():
    q = Queue()
    i = InputDataMange()
    i.input_data(q)
    data_dic = q.get()
    data_list = data_dic.get("dataList")
    for data in data_list:
        settingFiledProcess.process_data(data)



if __name__ == '__main__':
    process_test_driver()