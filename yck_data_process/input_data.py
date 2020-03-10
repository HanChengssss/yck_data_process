# !/usr/bin/env python
# -*-encoding: utf-8-*-
# author:LiYanwei
# version:0.1
import pymysql
from yck_data_process.settings import *
from abc import ABCMeta, abstractmethod
from yck_data_process.logingDriver import *
from multiprocessing import Queue, Process
import time

class GetDataBase(metaclass=ABCMeta):
    pass
    # def __init__(self):
    #     '''
    #     加载数据库配置，连接数据库
    #     '''
    #     pass

    # def set_table(self, table):
    #     '''
    #     设置查询表名称
    #     :param table: String
    #     :return: None
    #     '''
    #     self.table = table
    #
    # def set_tables(self, tables):
    #     '''
    #     设置查询表名称列表
    #     :param tables: List
    #     :return: None
    #     '''
    #     self.tables = tables
    #
    # def set_filed(self, filed):
    #     self.filed = filed

    # @abstractmethod
    # def get_table_data(self, table=None):
    #     '''
    #     获取表数据
    #     :param table:String
    #     :return:dataList
    #     '''
    #     pass
    #
    # @abstractmethod
    # def get_tableList_data(self, tables=None):
    #     '''
    #     获取多表数据
    #     :param tables: List
    #     :return:dataList
    #     '''
    #     pass


class GetTestMysqlData():

    def get_table_data(self, table, conn, query_sql, filed):
        conn.ping()
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        cursor.execute(query_sql.format(filed=filed, table=table))
        records = cursor.fetchall()
        conn.close()
        datasDic = {}
        datasDic["table"] = table
        datasDic["dataList"] = records
        cursor.close()
        return datasDic

    def get_tableList_data(self, tables, dbparams, filed, query_all_data):
        conn = pymysql.connect(dbparams)
        if query_all_data:
            query_sql = "SELECT {filed} FROM {table};"
        else:
            query_sql = "SELECT {filed} FROM {table} ORDER BY RAND() LIMIT 1000;"
        conn.ping()
        datasDic = dict()
        # cursor = self.conn.cursor(cursor=pymysql.cursors.DictCursor)
        for table in tables:
            # print(table)
            try:
                # cursor.execute(self.query_sql.format(filed=self.filed, table=table))
                # records = cursor.fetchall()
                # datasDic[table] = records
                dDic = self.get_table_data(table=table, conn=conn, query_sql=query_sql, filed=filed)
                datasDic.update(dDic)
            except Exception as e:
                pass
                # self.logDriver.logger.error("from table {} raise error {}".format(table, str(e)))

        return datasDic

    def put_data_to_query(self, tables, dbparams, filed, query_all_data, q):
        logDriver = Logger("D:\YCK\代码\yck_data_process\yck_data_process\log_dir\GetTestMysqlData.log", level='warning')
        # cursor = self.conn.cursor(cursor=pymysql.cursors.DictCursor)
        conn = pymysql.connect(**dbparams)
        if query_all_data:
            query_sql = "SELECT {filed} FROM {table};"
        else:
            query_sql = "SELECT {filed} FROM {table} ORDER BY RAND() LIMIT 1000;"
        for table in tables:
            print(table)
            try:
                dDic = self.get_table_data(table=table, conn=conn, query_sql=query_sql, filed=filed)
                q.put(dDic)
                print("==========put data_query")
                # print(dDic)
            except Exception as e:
                print(e)
                logDriver.logger.error("from table {} raise error {}".format(table, str(e)))
        conn.close()
        q.put("end")
        print("p1 process end!")

def read_queue(q):
    while True:
        print(q.get())
        time.sleep(0.2)



if __name__ == '__main__':
    q = Queue()

    dbparams = dict(
                host="192.168.0.10",
                port=3306,
                user="root",
                passwd="000000",
                db="yck-data-center",
                charset="utf8",
            )

    g = GetTestMysqlData()
    # g.put_data_to_query()
    # print(g.data_query.get())
    p1 = Process(target=g.put_data_to_query, args=(auto_model_tables, dbparams, "gearbox", True, q,))
    r1 = Process(target=read_queue, args=(q,))
    r2 = Process(target=read_queue, args=(q,))
    p1.start()
    r1.start()
    r2.start()
    p1.join()
    r1.terminate()
    r2.terminate()

    print('Child process end.')



