import hashlib
import time


class entity:
    def __init__(self):
        self.dic = {
            "id": "null",
            "source_url": "null",
            "time": "null",
            "institution": "null",
            "translated_institution": "null",
            "field_main": "null",
            "field_sub": "null",
            "keywords": "null",
            "translated_keywords": "null",
            "title": "null",
            "abstract": "null",
            "translated_abstract": "null",
            "original_file": "null",
            "format_file": "null",
            "translated_file": "null",
            "checked_file": "null",
            "entity_institution": "null",
            "entity_location": "null",
            "entity_person": "null",
            "entity_other": "null",
            "entity_time": "null",
            "entity_policy": "null",
            "score": "null",
            "source_classification": "null",
            "topic_classification": "null",
            "CHN": "null",
            "recommend": "null",

        }

    def __setitem__(self, key, value):
        if value is not None:
            if type(value) == str:
                if len(value) > 0:
                    value = value.replace("\"", "").replace("\'", "").strip()
                    self.dic[key] = "\"%s\"" % value

            if type(value) == int or type(value) == float:
                self.dic[key] = "%s" % value

    def __getitem__(self, key):
        return self.dic.get(key)

    def sql1(self):
        self.dic["original_file"] = "\"%s.txt\"" % hashlib.md5(self.dic["title"].encode("utf-8")).hexdigest()
        sql1 = "INSERT INTO t1 VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s," \
               "%s)" % (
                   self.dic["id"],
                   self.dic["source_url"],
                   self.dic["time"],
                   self.dic["institution"],
                   self.dic["translated_institution"],
                   self.dic["field_main"],
                   self.dic["field_sub"],
                   self.dic["keywords"],
                   self.dic["translated_keywords"],
                   self.dic["title"],
                   self.dic["abstract"],
                   self.dic["translated_abstract"],
                   self.dic["original_file"],
                   self.dic["format_file"],
                   self.dic["translated_file"],
                   self.dic["checked_file"],
                   self.dic["entity_institution"],
                   self.dic["entity_location"],
                   self.dic["entity_person"],
                   self.dic["entity_other"],
                   self.dic["entity_time"],
                   self.dic["entity_policy"],
                   self.dic["score"],

                   self.dic["source_classification"],
                   self.dic["topic_classification"],
                   self.dic["CHN"],
                   self.dic["recommend"],

               )
        return sql1

    def sql_abs(self):
        update = "UPDATE t1 SET abstract = %s WHERE id = %s" % (self.dic["abstract"], self.dic["id"])
        return update

    def sql_score(self):
        update = "UPDATE t1 SET score = %s WHERE id = %s" % (self.dic["score"], self.dic["id"])
        return update


class entity_collect:
    def __init__(self, name):
        self.dic = {
            "name": "\"%s\"" % name,
            "last_time": "null",
            "new_title": [],
        }

    def __setitem__(self, key, value):
        self.dic["new_title"].append(value)

    def __getitem__(self, key):
        return self.dic.get(key)

    def sql(self):
        self.dic["last_time"] = "\"%s\"" % time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.dic["new_title"] = "\"%s\"" % str(self.dic["new_title"])
        sql = "UPDATE collect SET last_time = %s,new_title=%s WHERE name = %s" % (
            self.dic["last_time"], self.dic["new_title"], self.dic["name"])
        # print(sql)
        return sql


if __name__ == '__main__':
    e = entity()
    e[
        "source_url"] = 'https://www.whitehouse.gov/ostp/news-updates/2021/12/15/white-house-office-of-science-and-technology-policy-announces-a-bold-strategy-to-understand-a-changing-arctic/'
    print(e["source_url"])
