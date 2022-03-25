import pymysql
import time
from multiprocessing import Process

from utils import globe


class statistic:
    def __init__(self, db):
        self.db = db
        self.cur = self.db.cursor()

        self.keywords = "SELECT keywords FROM t1"
        self.institution = "SELECT entity_institution FROM t1"
        self.location = "SELECT entity_location FROM t1"
        self.person = "SELECT entity_person FROM t1"
        self.other = "SELECT entity_other FROM t1"
        self.time = "SELECT entity_time FROM t1"
        self.policy = "SELECT entity_policy FROM t1"

    def sql(self, s):
        flag = 1
        try:
            self.cur.execute(s)
        except:
            flag = 0
            print("wrong")
            print(self.keywords)

        if flag:
            return 1, self.cur.fetchall()
        else:
            return 0, 0

    def process_list(self, l):
        d = dict()
        for i in l:
            if i not in d:
                d[i] = l.count(i)
        d = sorted(d.items(), key=lambda x: x[1], reverse=True)
        return d

    def count_keywords(self):
        l = []
        flag, t = self.sql(self.keywords)

        if flag:
            for i in t:
                if i is not None:
                    if i[0] is not None:
                        if len(i[0]) > 0:
                            l += eval(i[0])
            return self.process_list(l)

    def ins_location_person(self, s):
        l = []
        flag, t = self.sql(s)
        if flag:
            for i in t:
                if i is not None:
                    if i[0] is not None:
                        spl = i[0].split(",")
                        for j in spl:
                            jj = j.strip()
                            if len(jj) > 1:
                                l.append(jj)
            return self.process_list(l)

    def count_institution(self):
        return self.ins_location_person(self.institution)

    def count_location(self):
        return self.ins_location_person(self.location)

    def count_person(self):
        return self.ins_location_person(self.person)

    def count_other(self):
        l = []
        flag, t = self.sql(self.other)
        if flag:
            for i in t:
                if i is not None:
                    if i[0] is not None and i[0] != '{}':
                        temp_d = eval(i[0])
                        for v in temp_d.values():
                            for va in v:
                                if not va.isnumeric():
                                    l.append(va)
            return self.process_list(l)

    def count_time(self):
        return self.ins_location_person(self.time)

    def count_policy(self):
        return self.ins_location_person(self.policy)

    def submit(self, lis, name):
        l = lis[:1000]
        for i in range(len(l)):
            content, number = "\"%s\"" % l[i][0].replace("\"", ""), l[i][1]
            sql = "UPDATE statistics SET `%s` = %s,`%s_number` = %s WHERE `rank` = %s" % (
                name, content, name, number, i + 1)
            # sql = "REPLACE INTO statistics (`rank`,`%s`,`%s_number`) VALUES (%s, %s, %s);" % (name, name, i + 1, content, number)
            try:
                self.cur.execute(sql)
                self.db.commit()
            except:
                print("update wrong")
                print(sql)
        print(name, "over")

    def upgrade(self, name):
        p = eval("self.count_%s()" % name)
        self.submit(p, name)


def k1():
    statistic(globe.db).upgrade("keywords")


def k2():
    statistic(globe.db).upgrade("institution")


def k3():
    statistic(globe.db).upgrade("location")


def k4():
    statistic(globe.db).upgrade("person")


def k5():
    statistic(globe.db).upgrade("other")


def k6():
    statistic(globe.db).upgrade("time")


def k7():
    statistic(globe.db).upgrade("policy")


if __name__ == "__main__":
    start_t = time.time()
    start_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    p1 = Process(target=k1, args=())
    p2 = Process(target=k2, args=())
    p3 = Process(target=k3, args=())
    p4 = Process(target=k4, args=())
    p5 = Process(target=k5, args=())
    p6 = Process(target=k6, args=())
    p7 = Process(target=k7, args=())

    multi = [p1, p2, p3, p4, p5, p6, p7]

    for p in multi:
        p.start()
    for p in multi:
        p.join()

    print("开始时间:%s" % start_time)
    print("结束时间:%s" % time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    print("总用时:%.2f" % (time.time() - start_t))
