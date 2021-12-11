# -*- coding: utf-8 -*-

""" 
@author: Jin.Fish
@file: techwords.py
@version: 1.0
@time: 2021/07/27 12:12:18
@contact: jinxy@pku.edu.cn

extracting tech words from policy
"""

# import pandas as pd
from flashtext import KeywordProcessor  # 分词抽取工具
# import spacy  # 引入spacy，后续进行名词单复数处理
from process import File, RANK_TH, FileName, db, tqdm
from process import PolicyText as Policy
from disruptive import app

app.app_context().push()


# nlp = spacy.load('en_core_web_sm')
# lemmatizer = nlp.get_pipe("lemmatizer")


class TechWordsFrenquency:
    def __init__(self, tech_keywords_path):
        self.tech_keywords_path = tech_keywords_path  # 具体词汇的关键词词表

        # 引入抽词工具
        self.kp = KeywordProcessor()
        self.kp.add_keywords_from_list(self._prepare_techwords())

    def _prepare_techwords(self):  # 准备需要的词表
        with open(self.tech_keywords_path, 'r', encoding='utf8') as f2:  # 直接读取处理好的词表
            res = f2.readlines()
            f2.close()
        res2 = []
        for i in res:
            if i == '\n':
                continue
            res2.append(i.strip())
        return res2

    # 统计词频
    def count_techwords(self, file_path):
        path = file_path
        with open(path, encoding='utf-8') as f:  # 设置文件对象
            doc = f.read()
            extract_res = (self.kp.extract_keywords(doc))

        def cal_num(x):
            temp = dict()
            words_dict = {'dna': 'DNA', 'nmr': 'nuclear magnetic resonance(NMR)',
                          'sem': 'scanning electron microscope(SEM）',
                          'rfid': 'radio frequency identification devices(RFID)',
                          'rna': 'RNA', 'genetically modified organism': 'genetically modified organism(GMO)',
                          'gmo': 'genetically modified organism(GMO)', 'uav': 'Unmanned Aerial Vehicle(UAV)',
                          'Unmanned Aerial Vehicle': 'Unmanned Aerial Vehicle(UAV)',
                          "iot": "internet of things(IOT)", "internet of things": "internet of things(IOT)",
                          "ai": "Artificial Intelligence(AI)", "artificial intelligence": "Artificial Intelligence(AI)",
                          "rs": 'remote sensing(RS)', "remote sensing": 'remote sensing(RS)',
                          "CNN": 'convolutional neural network(CNN)',
                          "convolutional neural network": 'convolutional neural network(CNN)',
                          "SVM": 'support vector machine(SVM)', "support vector machine": 'support vector machine(SVM)',
                          "vr": "virtual reality(VR)", "VR": "virtual reality(VR)",
                          'virtual reality': 'virtual reality(VR)', 'ml': 'Machine Learning(ML)',
                          'machine learning': 'Machine Learning(ML)',
                          "artificial neural network": 'Artificial Neural Network(ANN)',
                          "ANN": 'Artificial Neural Network(ANN)',
                          "information and communication technology": 'information and communication technology(ICT)',
                          "ict": 'information and communication technology(ICT)',
                          "nuclear magnetic resonance": "nuclear magnetic resonance(NMR)",
                          'nmr': "nuclear magnetic resonance(NMR)",
                          "battery electric vehicle": "battery electric vehicle(BEV)",
                          "bev": "battery electric vehicle(BEV)",
                          "micro and nano technology": "micro and nano technology(MNT)",
                          "mnt": "micro and nano technology(MNT)"}
            x2 = [words_dict[i] if i in words_dict else i for i in x]
            # 对词表中出现的缩略语进行统一表示
            for i in x2:
                if i in temp:
                    temp[i] += 1
                else:
                    temp[i] = 1

            b = sorted(temp.items(), key=lambda x: x[1], reverse=True)
            return b

        return cal_num(extract_res)


def run_tech_words():
    t = TechWordsFrenquency('./keywords/tech_keywords_all2.txt')  # 给出关键词文件路径
    p_list = Policy.query.filter(Policy.use,
                                 Policy.tech_word == None,
                                 Policy.format_file != None).all()
    for p in tqdm(p_list):  # type: Policy
        format_file = File.query.get(p.format_file)  # type: File
        name = FileName()
        name.set_by_name(format_file.savename)
        path = name.gen_path(file_type=2)
        res = t.count_techwords(path)
        if len(res) > 0:
            tech_word = res[0][0]
            p.tech_word = tech_word
            p.tech_word_list = [i[0] for i in res]
            db.session.add(p)
    db.session.commit()


if __name__ == '__main__':
    run_tech_words()
