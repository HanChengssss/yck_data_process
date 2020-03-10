# !/usr/bin/env python
# -*-encoding: utf-8-*-
# author:LiYanwei
# version:0.1
from ModelProcess import GearboxProcess
import csv
import sys
sys.path.append("..")
from yck_data_process.input_data import GetTestData


class ModelTestDriver():
    with open('D:\yck_data_process\process_model\\table_name.csv', newline="") as csvfile:
        spamreader = csv.reader(csvfile, delimiter='\n')
        tables = []
        for row in spamreader:
            tables += row

    def get_test_data(self):
        g = GetTestData(tables=self.tables, filed="gearbox", query_all_data=True)
        datas = g.get_datas()
        return datas

    def test_process(self):
        m = GearboxProcess()
        test_datas = self.get_test_data()
        m.add_test_filed("gearbox")
        m.process_datas(test_datas)


if __name__ == '__main__':
    m = ModelTestDriver()
    textDatas = m.get_test_data()
    m.test_process()