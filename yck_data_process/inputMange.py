from multiprocessing import Queue
from yck_data_process.input.mongoDB import MongodbSource
from yck_data_process.input.mysqlDB import MysqldbSource

class InputDataMange():
    SOURCE_FUNC_MAP = {
        "mongodb": MongodbSource,
        "mysql": MysqldbSource
    }

    @staticmethod
    def input_data(source_type, input_queue):
        input_func = InputDataMange.SOURCE_FUNC_MAP.get(source_type)
        input_func.input_data(input_queue)
        input_queue.put("end")
        print("input_queue have been finished !")


if __name__ == '__main__':
    q = Queue()
    i = InputDataMange()
    i.input_data('mysql', q)
    print(q.qsize())

