

dataDict = {
    "table": "xxx",
    "type": "xxx",
    "dataList": [
        {
            "model_name": None,
            "gearbox": None,
        }
    ]
}

print("globals id: {}".format(id(dataDict)))

def p1(dataList, filed, new_filed):
    for data in dataList:
        data[filed] = new_filed
    # return dataList

def p2(dataDict):
    dataList = dataDict.get("dataList")
    p1(dataList, "model_name", "2007")
    print("p1 id: {}".format(id(dataDict)))
    print(dataDict)
    p1(dataList, "gearbox", "自动")
    print("p2 id: {}".format(id(dataDict)))
    print(dataDict)
    # return dataDict

def p3(dataDict):
    p2(dataDict)
    print("p3 id: {}".format(id(dataDict)))
    print(dataDict)

if __name__ == '__main__':
    p3(dataDict)

'''
globals id: 2680558357168
p1 id: 2680558357168
{'table': 'xxx', 'type': 'xxx', 'dataList': [{'model_name': '2007', 'gearbox': None}]}
p2 id: 2680558357168
{'table': 'xxx', 'type': 'xxx', 'dataList': [{'model_name': '2007', 'gearbox': '自动'}]}
p3 id: 2680558357168
{'table': 'xxx', 'type': 'xxx', 'dataList': [{'model_name': '2007', 'gearbox': '自动'}]}
------------------------------------
结论：将全局变量dataDict传入函数中进行修改，无论有没有重新赋值给新的变量名，都没有改变其原来的内存地址
'''