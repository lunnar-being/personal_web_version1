# from transformers import pipeline
import time
from aiospider.module.entity import entity
from aiospider.module.utils import utils, globe
# import torch
# from aiospider.module.model.textteaser import TextTeaser


class Abstract:
    def __init__(self):
        self.model_path = "./module/model/distillbart"
        self.summarizer = pipeline("summarization", model=self.model_path)

    def generate(self, text):
        if len(text) > 5000:
            text = text[:5000]
        result_list = self.summarizer(text, max_length=256, min_length=30, do_sample=False)
        result = [i["summary_text"] for i in result_list]
        return result


class textteaser:
    def __init__(self):
        self.model = TextTeaser()

    def generate(self, title, text):
        sentences = self.model.summarize(title, text)
        result = "".join(sentences)
        return result


class upgrade_abs:
    def __init__(self, file_path):
        self.abstract_generator = Abstract()
        self.abstract_generator2 = textteaser()
        self.db = globe.db
        self.cur = self.db.cursor()
        self.id_name = utils.abs_null_id(self.db, self.cur)
        self.file_path = file_path

    def __call__(self):
        start_t = time.time()
        start_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        print("空摘要共有:%s" % len(self.id_name))
        count = 0
        for id, file_name, title in self.id_name:
            with open("%s/%s" %(self.file_path,file_name) , "r", encoding="utf8") as file:
                text = file.read()
                text = text.replace("\n", "").replace("\t", "").strip()
                try:
                    abst = self.abstract_generator.generate(text)[0]
                except:
                    count += 1
                    print("wrong id %s" % id)
                    abst = self.abstract_generator2.generate(title, text)
                    # print(text)
                    # print(abst)
                e = entity()
                e["id"] = id
                e["abstract"] = abst
                # print(abst)
                # print(e.sql_abs())

                utils.update_abstract(self.db, self.cur, e)
                count += 1
                print("count:%s id:%s" % (count, id))
        print("开始时间:%s" % start_time)
        print("结束时间:%s" % time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        print("总用时:%.2f" % (time.time() - start_t))


if __name__ == "__main__":
    if hasattr(torch.cuda, 'empty_cache'):
        torch.cuda.empty_cache()
    upgrade_abs()()

    # with open("file/00000ab0cdbbac96d12de12167b96e25.txt", encoding="utf8") as a:
    #     x = a.read()
    #
    # import os
    #
    # a = textteaser()
    # file_list = os.listdir("file")[:2]
    # for i in file_list:
    #     with open("file/%s" % i, 'r', encoding="utf8") as file:
    #         print(a.generate("thank you",file.read())[0])
    pass
