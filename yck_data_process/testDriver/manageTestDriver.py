# coding=utf-8
from yck_data_process.testDriver.toolTestDriver import ToolTestDriver
from yck_data_process.process.positionProcess import PositionProcessManage
from yck_data_process.settingsManage import SettingsManage
from yck_data_process.logingDriver import Logger
import pymysql
'''
读取MySQL数据
处理数据
插入MySQL
'''
def create_update_sql(item, table, idField):
    if "data" in item:
        data = item["data"]
    else:
        data = item
    id = data.pop(idField)
    keys = "=%s,".join(data.keys()) + "=%s"
    sql = 'UPDATE {table} SET {keys} WHERE {idField} = "{filedId}"'.format(table=table, keys=keys, idField=idField, filedId=id)
    return sql, data

def update_mysql_one(mysqlConn, sql, data):
    '''
    更新车型库中有变化的一条数据
    :param mysqlConn: MySQL 连接
    :param item: 数据字典（可能有嵌套）
    :param table: Mysql table <String>
    :param idField: 该条数据的Id（唯一标识字段）名称<String>
    :return:
    '''

    cursor = mysqlConn.cursor()
    try:
        if cursor.execute(sql, tuple(data.values())):
            mysqlConn.commit()

    except Exception as e:
        mysqlConn.rollback()
        print(e)
        # ToolSave.log_error_data(item, table, str(e))
    finally:
        cursor.close()

mysql_conn_parms = dict(
    host="localhost",
    port=3306,
    user="root",
    passwd="123456",
    db="test2",
    charset="utf8",
    )
mysql_conn = pymysql.connect(**mysql_conn_parms)
query_position_data = "SELECT id, title from yck_zhaopin"

position_datas = ToolTestDriver.get_mysql_data(mysql_conn, query_position_data)

data_dic_list = ToolTestDriver.package_data_list(all_records=position_datas, table="yck_zhaopin", type="position_info")
sm = SettingsManage(model="test")
logDirManage = sm.get_log_setting_instance()
# 加载日志记录模块，记录处理过程中出现的异常
logDriver = Logger("{}\modelProcess.log".format(logDirManage.get_logDirFullPath()), level='warning')
table = "yck_zhaopin"
try:
    for data_dic in data_dic_list:
        PositionProcessManage.process_position_datas(data_dic, logDriver)
        print(data_dic)
        data_list = data_dic.get('dataList')
        for item in data_list:
            sql, data = create_update_sql(item, table=table, idField="id")
            update_mysql_one(mysql_conn, sql, data)
finally:
    mysql_conn.close()

# item = {'data': {'id': 43787, 'position': '区域经理'}}
# sql, data = create_update_sql(item, table="yck_zhaopin", idField="id")
# update_mysql_one(mysql_conn, sql, data)
# mysql_conn.close()




