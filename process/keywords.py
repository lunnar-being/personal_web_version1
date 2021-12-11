# -*- coding: utf-8 -*-

""" 
@author: Chang AoFei
@file: keywords.py
@version: 1.0
@time: 2021/07/26 09:21:16
@contact:

extract keywords
"""

import pandas as pd
import os
import math

# nlp = spacy.load('en_core_web_sm')

from tqdm import tqdm

from process import BASE_DIR, File, db, Config
from process import PolicyText as Policy
from flashtext import KeywordProcessor
from disruptive import app

app.app_context().push()


# 生成当前已有的文件列表，用于传给
def gen_rank_file_list():
    name_list = File.query.with_entities(File.savename).join(Policy, Policy.format_file == File.id).filter(
        File.savename != None,
        Policy.rank > Config.RANK_TH)
    path_list = list(map(lambda x: os.path.join(BASE_DIR, 'app/data/format', x[0]) + '\n', name_list))
    print(f'totally {len(path_list)} file')
    with open(os.path.join(BASE_DIR, 'process/keywords/files_path_list.txt'), 'w') as f:
        f.writelines(path_list)


class ExtractKeywords:
    def __init__(self, files_path_list_path, record_save_path, most_important_words, important_words_path,
                 keywords_list_path, file_list_path):
        self.files_path_list_path = files_path_list_path  # 所有文本所在的路径
        self.record_save_path = record_save_path  # 存储计算结果的txt的路径
        self.most_important_words = most_important_words  # 核心关键词列表
        self.important_words_path = important_words_path  # 重要关键词txt路径
        self.keywords_list_path = keywords_list_path  # WOS关键词txt文档路径
        self.file_list_path = file_list_path
        # 缩略语对照词典，用于替换抽词之后的结果
        self.words_dict = {"iot": "internet of things(iot)", "internet of things": "internet of things(iot)",
                           "ai": "artificial intelligence(ai)",
                           "artificial intelligence": "artificial intelligence(ai)",
                           "rs": 'remote sensing(rs)', "remote sensing": 'remote sensing(rs)',
                           "CNN": 'convolutional neural network(CNN)',
                           "convolutional neural network": 'convolutional neural network(CNN)',
                           "SVM": 'support vector machine(SVM)',
                           "support vector machine": 'support vector machine(SVM)',
                           "vr": "virtual reality(VR)", "VR": "virtual reality(VR)",
                           'virtual reality': 'virtual reality(VR)', 'ml': 'machine learning(ML)',
                           'machine learning': 'machine learning(ML)',
                           "artificial neural network": 'artificial neural network(ANN)',
                           "ANN": 'artificial neural network(ANN)',
                           "information and communication technology": 'information and communication technology(ict)',
                           "ict": 'information and communication technology(ict)',
                           "nuclear magnetic resonance": "nuclear magnetic resonance(nmr)",
                           'nmr': "nuclear magnetic resonance(nmr)",
                           "battery electric vehicle": "battery electric vehicle(bev)",
                           "bev": "battery electric vehicle(bev)",
                           "micro and nano technology": "micro and nano technology(mnt)",
                           "mnt": "micro and nano technology(mnt)"}

    def _read_keywords_list(self):
        tech_keywords1 = pd.read_csv(self.keywords_list_path, header=None, names=['words'])
        keywords_all = []
        for i in tech_keywords1['words'].to_list():
            if ':' in i:
                j = i.index(':')
                keywords_all.append(i[:j])
            else:
                keywords_all.append(i[1:-1])
        keywords_all = list(set(keywords_all))
        return keywords_all

    def _define_important_words(self):
        tech_keywords1 = pd.read_csv(self.important_words_path, header=None, names=['words'])
        tech_keywords_all = []
        for i in tech_keywords1['words'].to_list():
            if ':' in i:
                j = i.index(':')
                tech_keywords_all.append(i[:j])
            else:
                tech_keywords_all.append(i[1:-1])
        return list(set(tech_keywords_all))

    # 依次处理文件
    def process_files(self):
        print('run process files')
        # 读取服务器绝对路径
        with open(self.files_path_list_path) as f:
            file_path_list = f.readlines()
        kp = KeywordProcessor()
        keywords_all = self._read_keywords_list()
        kp.add_keywords_from_list(keywords_all)
        extract_res = []
        file_list = []
        for i in tqdm(list(map(str.strip, file_path_list)), desc='loop: file_path_list'):
            with open(i, encoding='utf-8') as f:  # 设置文件对象
                doc = f.read()
            file_list.append(i)
            extract_res.append(kp.extract_keywords(doc))

        def cal_num(x):
            temp = dict()
            for i in x:
                if i in temp:
                    temp[i] += 1
                else:
                    temp[i] = 1
            return temp

        # 进行名词单复数的统一
        cal_num_res = []
        for res in tqdm(extract_res, desc='extract_res'):
            # after_stem = []
            # for i in res:
            #     i = nlp(i)
            #     temp = []
            #     for token in i:
            #         if token.pos_ == 'NOUN':
            #             temp.append(str(token.lemma_))  # 名词统一为单数形式
            #         else:
            #             temp.append(str(token))
            #     res2 = ' '.join(temp)
            #     if ' - ' in res2:
            #         res2 = res2.replace(' - ', '-')  # 一些特殊格式的处理，小问题
            #     after_stem.append(res2)
            res3 = [self.words_dict[i] if i in self.words_dict else i for i in res]
            cal_num_res.append(cal_num(res3))

        phrases_set = set()
        for c in cal_num_res:
            for i in c.keys():
                phrases_set.add(i)
        self.phrases_set = phrases_set
        self.file_list = file_list
        self.cal_num_res = cal_num_res
        # 保存TF-IDF矩阵之后就没必要保存这些抽词结果了
        # with open(self.file_list_path, 'w', encoding='utf8') as f:  # 保存抽词结果
        #     f.write(str(file_list))
        #     f.close()
        # with open('phrases_list.txt','w',encoding='utf8') as f:
        #   f.write(str(list(phrases_set)))
        #  f.close()

    # 尝试读取之前的结果，如果已经有就不再计算，直接返回存储的结果
    def cal_result(self):
        print('run cal_result')
        # if os.path.exists(self.record_save_path):
        #     with open(self.record_save_path, 'r') as f:
        #         res = eval(f.read())
        #         f.close()
        #         if len(res) != 0:
        #             self.dict_res = res
        #             return
        self.process_files()
        print(f'process done')
        file_length = len(self.file_list)
        important_keywords = self._define_important_words()
        pre_list = list(self.phrases_set)
        len_unique_items = len(self.phrases_set)
        zeros = [0] * len_unique_items
        empty_dict = list(zip(pre_list, zeros))
        empty_dict2 = dict(empty_dict)
        df_data = []
        for i in tqdm(self.cal_num_res, desc='loop: self.cal_num_res'):
            temp = empty_dict2.copy()
            for j in i.keys():
                # 关键短语的权重提高
                if j in self.most_important_words:
                    temp[j] = 30 * i[j]
                elif j in important_keywords:
                    temp[j] = 10 * i[j]
                else:
                    temp[j] = i[j]
            df_data.append(temp)
        df_items = []
        for dic in tqdm(df_data, desc='loop: df_data'):
            tmp = []
            for j in list(dic.items()):
                tmp.append(j[1])
            df_items.append(tmp)
        print(f'tf_idf caled')
        df1 = pd.DataFrame(df_items)
        df1.columns = list(self.phrases_set)
        df1.index = self.file_list
        # 此处计算出了TF/IDF所需要的矩阵，可以存储为csv格式
        martrix_path = 'tf_idf.csv'
        df1.to_csv(martrix_path, encoding='utf8', index=False)
        print("tf_idf文件存储完成")

    # 这个函数读取存储的tf_idf文件到内存，以备计算tf_idf使用，所以在抽取每一个文件的关键词的时候都应该提前运行这个（如果是内存中已经有tf_idf也可不必）
    def read_tf_idf(self):
        if os.path.exists("tf_idf.csv"):
            tf_idf_matrix = pd.read_csv('tf_idf.csv', encoding='utf-8')
            if tf_idf_matrix.shape[0] != 0:
                self.tf_idf_matrix = tf_idf_matrix
                print("读取tf_idf文件完成")

    def get_result(self, file_path):  # 这里的file_path是最后一级路径的文件名
        tf_idf = self.tf_idf_matrix  # 存储时索引变成了列，这里需要设置索引
        print(tf_idf.index)
        file_length, len_unique_items = tf_idf.shape[0], tf_idf.shape[1]
        # 分别是tf_idf的行的数量、列的数量，即这些文档集合的长度、所有文档中出现的所有词的集合的长度
        temp = []
        s = tf_idf.loc[file_path]
        m = max(s)
        for j in range(len_unique_items):
            tf = s.iloc[j] / m  # 计算tf
            if tf == 0:
                continue
            idf = math.log(file_length / sum(tf_idf.iloc[:, j] != 0))  # 计算idf
            temp.append((j, tf * idf))
        res = temp
        phrases_list = list(self.phrases_set)

        def get_tfidf_word(res1):
            res1 = sorted(res1, key=lambda x: x[1], reverse=True)
            res_indexes1 = [i[0] for i in res1[:10]]
            res_items1 = [phrases_list[i] for i in res_indexes1]
            return res_items1

        res2 = get_tfidf_word(res)
        print(1)
        return res2

    # 增量的程序，输入一个文件的路径,直接返回抽词结果
    # 增量操作之前需要read_tf_idf()操作，读取之前的TF_IDF表到程序缓存
    def increment(self, incr_file_path):  # 大部分操作是之前的重复，但是不便修改为共同的函数
        # 1,对新加入的文章进行抽词处理
        kp = KeywordProcessor()
        keywords_all = self._read_keywords_list()
        kp.add_keywords_from_list(keywords_all)
        with open(incr_file_path, encoding='utf-8') as f:  # 设置文件对象
            doc = f.read()
        incre_words_list = kp.extract_keywords(doc)

        def cal_num(x):
            temp = dict()
            for i in x:
                if i in temp:
                    temp[i] += 1
                else:
                    temp[i] = 1
            return temp

        res3 = [self.words_dict[i] if i in self.words_dict else i for i in incre_words_list]
        incre_words_freq = cal_num(res3)
        # 2，下面根据新加一行的tf_idf矩阵计算新的文档的tf*idf值
        tf_idf = self.tf_idf_matrix
        important_keywords = self._define_important_words()
        pre_list = tf_idf.columns
        len_unique_items = tf_idf.shape[1]
        zeros = [0] * len_unique_items
        empty_dict = list(zip(pre_list, zeros))
        empty_dict2 = dict(empty_dict)
        for j in incre_words_freq.keys():
            # 关键短语的权重提高
            if j in self.most_important_words:
                empty_dict2[j] = 30 * incre_words_freq[j]
            elif j in important_keywords:
                empty_dict2[j] = 10 * incre_words_freq[j]
            elif j in pre_list:
                empty_dict2[j] = incre_words_freq[j]
        incre_df_item = [i[1] for i in empty_dict2.items()]
        assert len(incre_df_item) == len_unique_items, f"列的数量不匹配: incre_df_item({len(incre_df_item)}) != len_unique_items({len_unique_items})"
        tf_idf.loc[incr_file_path] = incre_df_item  # 把新的文章加入到tf_idf
        m = max(incre_df_item)
        if m == 0:
            return 'null'
        file_length = tf_idf.shape[0]  # 即所有文档的数量
        temp = []
        for j in range(len_unique_items):
            tf = incre_df_item[j] / m  # 计算tf
            if tf == 0:
                continue
            idf = math.log(file_length / sum(tf_idf.iloc[:, j] != 0))  # 计算idf
            temp.append((j, tf * idf))
        res = temp
        phrases_list = pre_list

        # 该函数将tf*idf的结果排序后映射到对应的词汇，即抽取出对应的关键词
        def get_tfidf_word(res1):
            res1 = sorted(res1, key=lambda x: x[1], reverse=True)
            res_indexes1 = [i[0] for i in res1[:10]]
            res_items1 = [phrases_list[i] for i in res_indexes1]
            return res_items1

        res2 = get_tfidf_word(res)
        return res2
    # 返回抽词结果


def main():
    most_important_words = ['disruptive innovation', 'radical innovation', 'innovation', 'disruptive technology',
                            'incremental innovation', 'open innovation', 'new product development', 'business model',
                            'absorptive capacity', 'technological innovation', 'developing technology',
                            'advanced technology', 'integrated technology', 'future technology', 'promising technology',
                            'next generation technology', 'evolving technology', 'radical technology', 'Next Big Thing',
                            'radical technology', 'breakthrough technology', 'game changer',
                            'gaming changing technology',
                            'emerging technology', 'revolutionary technology', 'transformative technology']
    files_path_list_path = os.path.join(BASE_DIR, 'process/keywords/files_path_list.txt')
    record_save_path = os.path.join(BASE_DIR, 'process/keywords/cal_result.txt')
    important_words_path = os.path.join(BASE_DIR, 'process/keywords/tech_keywords_all.txt')
    keywords_list_path = os.path.join(BASE_DIR, 'process/keywords/keywords_v3.txt')
    file_list_path = os.path.join(BASE_DIR, 'process/keywords/file_list.txt')
    # print(files_path_list_path, record_save_path, important_words_path, keywords_list_path)
    t = ExtractKeywords(files_path_list_path=files_path_list_path,
                        record_save_path=record_save_path,
                        most_important_words=most_important_words,
                        important_words_path=important_words_path,
                        file_list_path=file_list_path,
                        keywords_list_path=keywords_list_path)
    t.cal_result()  # 如果是增量就不需要这一步了，因为cal_result的结果已经存起来了
    # 增量的逻辑代码
    # t.read_tf_idf()
    # for file in increment_filelist:
    #    increment_result=t.increment(file)
    # 上面那个函数抽取了部分文章的路径，这里就把这些文章的关键词写进数据库
    flist = File.query.join(Policy, Policy.format_file == File.id).filter(File.savename != None,
                                                                          Policy.use == True,
                                                                          Policy.keywords == None
                                                                          ).all()
    print(f'run keyword extracting, total task: {len(flist)}')
    t.read_tf_idf()
    for file in tqdm(flist):
        policy = Policy.query.filter(Policy.format_file == file.id).one()  # type: Policy
        file_path = os.path.join(BASE_DIR, 'app/data/format', file.savename)
        kw_res = t.get_result(file_path)
        print(file, policy, kw_res)
        if not kw_res: continue
        policy.keywords = ', '.join(kw_res)
        db.session.add(policy)
    db.session.commit()


def run_keywords():
    most_important_words = ['disruptive innovation', 'radical innovation', 'innovation', 'disruptive technology',
                            'incremental innovation', 'open innovation', 'new product development', 'business model',
                            'absorptive capacity', 'technological innovation', 'developing technology',
                            'advanced technology', 'integrated technology', 'future technology', 'promising technology',
                            'next generation technology', 'evolving technology', 'radical technology', 'Next Big Thing',
                            'radical technology', 'breakthrough technology', 'game changer',
                            'gaming changing technology',
                            'emerging technology', 'revolutionary technology', 'transformative technology']
    files_path_list_path = os.path.join(BASE_DIR, 'process/keywords/files_path_list.txt')
    record_save_path = os.path.join(BASE_DIR, 'process/keywords/cal_result.txt')
    important_words_path = os.path.join(BASE_DIR, 'process/keywords/tech_keywords_all.txt')
    keywords_list_path = os.path.join(BASE_DIR, 'process/keywords/keywords_v3.txt')
    file_list_path = os.path.join(BASE_DIR, 'process/keywords/file_list.txt')
    print(files_path_list_path, record_save_path, important_words_path, keywords_list_path)
    t = ExtractKeywords(files_path_list_path=files_path_list_path,
                        record_save_path=record_save_path,
                        most_important_words=most_important_words,
                        important_words_path=important_words_path,
                        file_list_path=file_list_path,
                        keywords_list_path=keywords_list_path)
    t.read_tf_idf()
    print(t.tf_idf_matrix.head())
    flist = File.query.join(Policy, Policy.format_file == File.id).filter(Policy.use == True,
                                                                          File.savename != None,
                                                                          Policy.keywords == None
                                                                          ).all()

    print(f'run increment keyword extracting, total task: {len(flist)}')
    # loop through all the policy file
    for f in flist:  # type: File
        p = Policy.query.filter(Policy.format_file == f.id).one()  # type: Policy
        f_path = os.path.join(BASE_DIR, 'app/data/format', f.savename)
        kw_res = t.increment(f_path)
        print(f, p, kw_res)
        if not kw_res: continue
        p.keywords = ', '.join(kw_res)
        db.session.add(p)
    db.session.commit()


if __name__ == '__main__':
    # gen_rank_file_list()
    # main()
    run_keywords()
