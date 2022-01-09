import configparser
from aiospider.module import utils
from aiospider.module.spider_main import spider_main
# from aiospider.module.summarization import upgrade_abs
# from aiospider.module.score import submit_Score
# from aiospider.module.field import field_update
# from aiospider.module.source import update_source
# from aiospider.module.topic import update_topic
# from aiospider.module.CHN import update_CHN


class spider_pipline:
    def __init__(self):
        cf = configparser.RawConfigParser()
        cf.read(r"E:\research\technology\aiospider\config.ini")
        setting = cf["setting"]
        self.file = setting["file"]
        # self.model_bart = setting["model_bart"]
        # self.model_distillbart = setting["model_distillbart"]
        # self.model_textteaser = setting["model_textteaser"]
        # self.data_bm25 = setting["data_bm25"]
        # self.data_source = setting["data_source"]
        # self.data_whitehouse = setting["data_whitehouse"]

    def spider(self, name="all"):
        spider_main(self.file)(name)

    def abstract(self):
        upgrade_abs(self.file)()

    def score(self):
        submit_Score(self.file)()

    def source(self):
        update_source()

    def field(self):
        field_update(self.file)

    def topic(self):
        update_topic()

    def china(self):
        update_CHN(self.file)


if __name__ == "__main__":
    a = spider_pipline()
    a.spider("gov")
    # a.abstract()
    # a.score()
    # a.source()
    # a.field()
    # a.topic()
    # a.china()
