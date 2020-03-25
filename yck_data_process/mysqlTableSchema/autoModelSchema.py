import pymysql
from yck_data_process import settings
import simplejson


class MysqlTableSchema():
    basePath = "D:\YCK\代码\yck_data_process\yck_data_process\mysqlTableSchema\\{}"

    @staticmethod
    def get_table_schema(mysqlConn, tableNameList, dbName):
        cursor = mysqlConn.cursor()
        tableSchemaDicList = []
        for table in tableNameList:
            schemaSql = "select COLUMN_NAME, COLUMN_COMMENT from information_schema.columns where table_schema ='{db}'  and table_name = '{table}';".format(db=dbName, table=table)
            cursor.execute(schemaSql)
            records = cursor.fetchall()
            print(records)
            tableShcemaDic = MysqlTableSchema.package_data(records, table)
            tableSchemaDicList.append(tableShcemaDic)
        return tableSchemaDicList

    @staticmethod
    def save_to_json(tableSchemaDicList, jsonPath):
        with open(MysqlTableSchema.basePath.format(jsonPath), 'w', encoding='utf8') as f:
            for tableSchemaDic in tableSchemaDicList:
                f.write(simplejson.dumps(tableSchemaDic, ensure_ascii=False, encoding='utf8') + "\n")

    @staticmethod
    def get_table_name_list(dataType):
        if dataType == "auto_model":
            table_name_list = settings.auto_model_tables
            table_name_list.append("config_vdatabase_yck_major_info")
        return table_name_list

    @staticmethod
    def package_data(records, table):
        tableScemaDic = dict()
        tableScemaDic["table"] = table
        tableScemaDic["COLUMN"] = []
        tableScemaDic["COLUMN_COMMENT"] = []
        for r in records:
            tableScemaDic["COLUMN"].append(r[0])
            tableScemaDic["COLUMN_COMMENT"].append(r[1])
        sorted(tableScemaDic["COLUMN"])
        sorted(tableScemaDic["COLUMN_COMMENT"])
        return tableScemaDic

    @staticmethod
    def manage():
        mysqlConn = pymysql.connect(**settings.mysqlSchemaParams)
        table_name_list = MysqlTableSchema.get_table_name_list(dataType="auto_model")
        dbName = "yck-data-center"
        tableSchemaDicList = MysqlTableSchema.get_table_schema(mysqlConn, table_name_list, dbName)
        MysqlTableSchema.save_to_json(tableSchemaDicList, "autoModelSchemaInfo.json")

if __name__ == '__main__':
    MysqlTableSchema.manage()






