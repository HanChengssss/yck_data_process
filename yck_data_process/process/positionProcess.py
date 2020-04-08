# coding=utf-8
import re


# 标准职位信息
class PositionProcess():
    @staticmethod
    def process_filed(filed):
        statusDic = {
            "isLog": False,
            "filed": None
        }
        position_pattern = '区域管理部总监|区域车源渠道经理|区域总监|分公司经理|区域经理|区域检测组长|区域主管|区域商务专员|区域车务专员|区域车贷经理|区域车贷销售|厂长|机电维修|油漆工|钣金工|美容工|仓库管理员|钣喷组长|内勤|线上拓展主管|线上拓展专员|整备经理|整备主管|整备专员|竞拍部经理|竞拍部主管|客服专员|技术架构|前端研发|拍卖服务|在线车商服务|大客户经理|大客户助理|业务总监|销售助理|加盟商务专员|线上售后客服|项目主管|内训师|营业部主管|渠道经理|资源拓展经理|资源拓展助理|资源拓展文员|售前支持经理|售前支持主管|售前支持专员|车源部经理|车源部主管|车源部专员|副总裁|定价经理|项目总监|项目经理|渠道主管|业务助理|渠道专员|检测经理|检测主管|检测专员|检测质监|检测评估师|车管部经理|车管部主管|车管部助理|车辆管理员|商务部经理/商务经理|定量项目主管|定量项目专员|售后商务主管|售后商务专员|售后车务主管|售后车务助理|物流部经理|物流部主管|发运经理|发运助理|物流专员|品牌经理|品牌主管|平面设计师|品牌执行专员|搜索推广专员|新媒体专员|文案策划|短视频编导|财务总监|财务副总监|资金结算部经理|融资专员|财务助理|会计核算部经理|核算主管|应收会计/会计|应付会计/会计|费用会计|子公司会计|预算分析部主管/预算主管|预算专员|金融事业部总监|风控经理|金融事业部主管|金融部助理|审核专员|运营专员|数据总监|数据经理|数据主管|数据主管（开发）|数据挖掘工程师|数据分析师|爬虫工程师|数据开发工程师|前端开发工程师|产品技术部总监|技术经理|技术主管|工程师|人资行政总监|人力资源经理|薪酬绩效主管|招聘培训主管|HRBP主管|HRBP|人事专员|行政主管|行政专员|部门总监|法务主管|知识产权|公共关系|部门助理|流程管控|文控专员|CEO|COO|助理'
        p1 = re.compile(position_pattern)
        try:
            ret = p1.search(str(filed))
            if ret:
                statusDic["filed"] = ret.group()
            else:
                statusDic["filed"] = "-"
                # statusDic["isLog"] = True
        except:
            # statusDic["isLog"] = True
            statusDic["filed"] = "-"
        finally:
            return statusDic

# re_pattern = '''
# 区域管理部总监
# 区域车源渠道经理
# 区域总监
# 分公司经理
# 区域经理
# 区域检测组长
# 区域主管
# 区域商务专员
# 区域车务专员
# 区域车贷经理
# 区域车贷销售
# 厂长
# 机电维修
# 油漆工
# 钣金工
# 美容工
# 仓库管理员
# 钣喷组长
# 内勤
# 线上拓展主管
# 线上拓展专员
# 整备经理
# 整备主管
# 整备专员
# 竞拍部经理
# 竞拍部主管
# 客服专员
# 技术架构
# 前端研发
# 拍卖服务
# 在线车商服务
# 大客户经理
# 大客户助理
# 业务总监
# 销售助理
# 加盟商务专员
# 线上售后客服
# 项目主管
# 内训师
# 营业部主管
# 渠道经理
# 资源拓展经理
# 资源拓展助理
# 资源拓展文员
# 售前支持经理
# 售前支持主管
# 售前支持专员
# 车源部经理
# 车源部主管
# 车源部专员
# 副总裁
# 定价经理
# 项目总监
# 项目经理
# 渠道主管
# 业务助理
# 渠道专员
# 检测经理
# 检测主管
# 检测专员
# 检测质监
# 检测评估师
# 车管部经理
# 车管部主管
# 车管部助理
# 车辆管理员
# 商务部经理/商务经理
# 定量项目主管
# 定量项目专员
# 售后商务主管
# 售后商务专员
# 售后车务主管
# 售后车务助理
# 物流部经理
# 物流部主管
# 发运经理
# 发运助理
# 物流专员
# 品牌经理
# 品牌主管
# 平面设计师
# 品牌执行专员
# 搜索推广专员
# 新媒体专员
# 文案策划
# 短视频编导
# 财务总监
# 财务副总监
# 资金结算部经理
# 融资专员
# 财务助理
# 会计核算部经理
# 核算主管
# 应收会计/会计
# 应付会计/会计
# 费用会计
# 子公司会计
# 预算分析部主管/预算主管
# 预算专员
# 金融事业部总监
# 风控经理
# 金融事业部主管
# 金融部助理
# 审核专员
# 运营专员
# 数据总监
# 数据经理
# 数据主管
# 数据主管（开发）
# 数据挖掘工程师
# 数据分析师
# 爬虫工程师
# 数据开发工程师
# 前端开发工程师
# 产品技术部总监
# 技术经理
# 技术主管
# 工程师
# 人资行政总监
# 人力资源经理
# 薪酬绩效主管
# 招聘培训主管
# HRBP主管
# HRBP
# 人事专员
# 行政主管
# 行政专员
# 部门总监
# 法务主管
# 知识产权
# 公共关系
# 部门助理
# 流程管控
# 文控专员
# CEO
# COO
# 助理
# '''
#
# re_pattern_list = re_pattern.split("\n")
# re_pattern = ""
# for p in re_pattern_list:
#     if p:
#         re_pattern += p + "|"
# print(re_pattern)
def replace_key_name(func):
    print("replace_key_name...")
    def new_func(data, filedNameList, logDriver, table, processFun):
        logDriver.logger.info("将字段名称title替换成position")
        data["position"] = data.pop("title")
        return func(data, filedNameList, logDriver, table, processFun)
    return new_func

class PositionFieldProcessMange():

    @staticmethod
    @replace_key_name
    def process_data(data, filedNameList, logDriver, table, processFun):
        '''
        将字段的公共处理规则和私有处理规则分离
        :param data:
        :param filedNameList:
        :param logDriver:
        :param table:
        :param processFun:
        :return:
        '''
        filedName = None
        for fn in filedNameList:
            if fn in data:
                filedName = fn
        if not filedName:
            return
        filed = data.get(filedName)
        if not filed:
            return
        # 字段处理规则
        statusDic = processFun(filed)
        print(statusDic)
        if statusDic.get("isLog"):
            logDriver.logger.warning("{}-->{}, source_table-->{}".format(filedName, data.get(filedName), table))
        elif statusDic.get("filed"):
            data[filedName] = statusDic.get("filed")

class PositionProcessManage():
    '''
    职位信息处理模块
    加载和管理车型库各个字段处理模块
    '''
    filedProcessDic = {
       "职位": {"func": PositionProcess, "name_list": ["position"]}
    }

    @staticmethod
    def process_position_datas(dataDict, logDriver):
        dataList = dataDict.get("dataList")
        table = dataDict.get("table")
        for d in dataList:
            if "data" in d:
                data = d["data"]
            else:
                data = d
            for process in PositionProcessManage.filedProcessDic.values():
                nameList = process.get("name_list")
                processFun = process.get("func").process_filed
                PositionFieldProcessMange.process_data(data=data, filedNameList=nameList, logDriver=logDriver, table=table, processFun=processFun)

if __name__ == '__main__':
    ret = PositionProcess.process_filed("**区域管理部总监xxxx")
    print(ret)