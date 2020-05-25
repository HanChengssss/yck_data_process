# _*_ coding:utf-8_*_
# author: hancheng
# date: 2020/5/25 16:54


class Base(object):
    count = {"count": {"sub1": 0}}


class SubClass1(Base):

    def add_one(self):
        SubClass1.count["count"]["sub1"] += 1


def main():
    s = SubClass1()
    for i in range(10):
        s.add_one()

main()

print(Base.count)