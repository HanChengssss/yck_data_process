from yck_data_process.pipelines.Tools import ToolSave
from tqdm import tqdm
# config_autohome_major_info_tmp


class AutoModelPipeline(object):
    id_set_dic = {}  # 存放各个车型库的去重集合
    @staticmethod
    def process_item(item, updateList, insertList, idFieldSet, mysqlConn, table):
        '''
        车型库更新逻辑
        只负责把不同存储逻辑的数据进行
        分类不作任何修改数据库的操作。
        --------------------------
        分类逻辑：
        首先判断该条数据是否已存在
        如果不存在加入到insertList
        否则，判断数据是否出现变化
        如果有变化：将数据加入到
        updateList
        如果没变化：抛弃
        :param item: 一条车型数据
        :param updateList:待更新列表
        :param insertList:待插入列表
        :param idFieldSet:过滤集合
        :param mysqlConn:数据库连接
        :return:
        '''
        if "data" in item:
            data = item["data"]
        else:
            data = item
        model_id = data.get("model_id")
        ret = ToolSave.test_exist(idField=model_id, idFieldSet=idFieldSet)
        if ret:
            # todo 此处的执行效率待优化
            data.pop("add_time")
            update_time = data.pop("update_time")
            new_data = ToolSave.sort_item(data)
            old_data = ToolSave.get_old_data(new_data=data, table_name=table, mysqlConn=mysqlConn, idField="model_id")
            old_data = ToolSave.sort_item(old_data)
            compare_ret = ToolSave.compare_data(new_data=new_data, old_data=old_data)
            if not compare_ret:
                data["update_time"] = update_time
                item["idField"] = "model_id"
                updateList.append(item)
            else:
                pass
                # print("数据无变化！")
        else:
            insertList.append(item)

    @staticmethod
    def process_dataDic(dataDic, mysqlConn):
        '''
        将dataDic中数据进行分类
        不同存储逻辑的数据分别放到不同的列表中
        最后再统一处理，将存逻辑和数据存储操作分离
        # todo 新旧对比需要优化，初步决定先统一将已有数据全字段取出，加密后放到集合中
        :param dataDic:
        :param mysqlConn:
        :return:
        '''
        table = dataDic.get("table")
        dataList = dataDic.get("dataList")
        updateList = []
        insertList = []
        idField = "model_id"
        idFieldSet = ToolSave.get_filter_set(mysqlConn=mysqlConn, idField=idField, table=table)
        # 将数据进行分类
        print("==========", table)
        for item in dataList:
            AutoModelPipeline.process_item(item=item, updateList=updateList, insertList=insertList, idFieldSet=idFieldSet, mysqlConn=mysqlConn, table=table)
        # 将分类后的数据进行批存储操作
        ToolSave.update_mysql_many(mysqlConn=mysqlConn, dataList=updateList, table=table, idField=idField)
        ToolSave.insert_mysql_many(mysqlConn=mysqlConn, dataList=insertList, table=table, hp=False)



