import random
from yck_data_process.settings import auto_model_tables
import time
from functools import wraps
from copy import deepcopy
from queue import Queue
'''
本次测试目的：测试在各种情况下处理随机生成的100万条数据所花费的时间。
1. 测试1：统计随机生成100万条数据需要花费的时间。
结论:在测试过程中发现一个奇怪的现象，使用for循环每次生成一个新的字典对象，但是通过打印id发现，出现大量的重复。但是生成的数据却和预期的结果没有出入。
经测试随机生成100万条数据约1.4s
2. 单进程测试结果：生成+处理100万条数据大约11s,目前处理的过程比较简单，后续时间会有所增加。
3. 2进程：一条进程处理， 一条进程读取，用时约:11.6s
4. 4进程: 2条进程处理，二条进程读取，用时约：7s
5. 1进程：4线程处理，约10秒
6. 1进程：8线程处理，约8秒
'''


def fn_timer(function):
    @wraps(function)
    def function_timer(*args, **kwargs):
        t0 = time.time()
        result = function(*args, **kwargs)
        t1 = time.time()
        print("Total time running %s: %s seconds" %
              ("text_foo", str(t1 - t0))
              )
        return result

    return function_timer


@fn_timer
def randomProdictData(dataQuery, dataNum=1000):
    typeList = ["auto_model"]
    modelyearList = ["xx2012ss", "2098 n ", "2019", "1998 款x"]
    grarBoxList = ["xx自动ss", "半自动 n ", "全自动形式上", "电动sx马s达"]
    for i in range(dataNum):
        dataDict = dict()
        # dataDict = deepcopy(dataDict)
        dataDict["table"] = random.choice(auto_model_tables)
        dataDict["type"] = random.choice(typeList)
        dataDict["dataList"] = []
        for i in range(1000):
            dataDict["dataList"].append({"model_year": random.choice(modelyearList), "gearbox": random.choice(grarBoxList)})
        # print(id(dataDict))
        dataQuery.put(dataDict)
    dataQuery.put("end")
    print(dataQuery.get())


if __name__ == '__main__':
    q = Queue()
    randomProdictData(dataQuery=q)