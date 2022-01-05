import pymysql


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


if __name__ == "__main__":
    db = pymysql.connect(host="81.70.102.186", user="root", password="YDH@henniu123", database="spider", port=3306)

    s = statistic(db)

    keywords = s.count_keywords()
    # print(keywords[:50])
    #
    institution = s.count_institution()
    # print(institution[:50])
    #
    location = s.count_location()
    # print(location[:50])
    #
    person = s.count_person()
    # print(person[:50])
    #
    other = s.count_other()
    # print(other[:50])
    #
    time = s.count_time()
    # print(time[:50])
    #
    policy = s.count_policy()
    # print(policy[:50])
