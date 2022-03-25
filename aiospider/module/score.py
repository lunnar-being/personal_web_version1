from aiospider.module.utils import *
import time
from aiospider.module.entity import entity
import nltk
import json


class bm25:
    def __init__(self, file_path):
        self.sentence_tokenize = nltk.data.load('tokenizers/punkt/english.pickle')
        self.file_path = file_path
        with open("module/data/bm25.json", "r") as f:
            self.dic = json.load(f)
            # print(self.dic)

    def split_sentence(self, text):
        return self.sentence_tokenize.tokenize(text)

    def generate_list(self, title, abstract, file_name):
        l = [self.split_sentence(title), self.split_sentence(abstract)]
        with open("%s/%s" % (self.file_path, file_name), "r", encoding="utf8") as file:
            text = file.read()
            l.append(self.split_sentence(text))
        return l

    def score(self, title, abstract, file_name):
        l = self.generate_list(title, abstract, file_name)
        result = 0
        for seg in [0, 1, 2]:
            length = len(l[seg])
            for sentence in l[seg]:
                for keyword in self.dic:
                    if keyword in sentence:
                        result += (3 * self.dic[keyword]) / (2 * (0.25 + 0.75 * length / 100) + self.dic[keyword])
        return round(result, 2)

    def __call__(self, title, abstract, file_name):
        return self.score(title, abstract, file_name)


class obwtccm:
    def __init__(self):
        pass

    def __call__(self):
        pass


class submit_Score:
    def __init__(self, file_path):
        self.db = globe.db
        self.cur = self.db.cursor()
        self.id_name = utils.score_null_id(self.cur)
        self.file_path = file_path
        self.scorer = bm25(self.file_path)

    def __call__(self):
        start_t = time.time()
        start_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        print("空分数共有:%s" % len(self.id_name))

        count = 0
        for id, title, abstract, file_name in self.id_name:
            point = self.scorer(title, abstract, file_name)
            # print(id, point)
            e = entity()
            e["id"] = id
            e["score"] = point

            utils.upgrade_score(self.db, self.cur, e)
            count += 1
            print("\rcount:%s id:%s score:%s" % (count, id, point), end="")

        print()
        print("开始时间:%s" % start_time)
        print("结束时间:%s" % time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        print("总用时:%.2f" % (time.time() - start_t))


if __name__ == "__main__":
    submit_Score(globe.db)()
    pass
