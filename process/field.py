# -*- coding: utf-8 -*-

""" 
@author: Jin.Fish
@file: field.py
@version: 1.0
@time: 2021/05/09 13:51:36
@contact: jinxy@pku.edu.cn

field classification
todo 逻辑比较难，建议进一步审核
"""
import csv
import json
import numpy as np
from sqlalchemy.orm.attributes import flag_modified

from process import PolicyText, logging, db, pure_text, tqdm, RANK_TH
from config import Config

from disruptive import app

app.app_context().push()
cls_lg = logging.getLogger("classification")
cls_lg.setLevel(logging.DEBUG)


class WordBag:
    """
    基于文章的标题和摘要
    生成一个词袋
    self.bag = dict()
    """

    def __init__(self, title, abstract, title_weight=5):
        """
        生成词袋
        只考虑2个词和1个词
        Args:
            title (str):
            abstract (str):
            title_weight (int):
        """
        self.bag = dict()
        # title
        title_word_list = title.split() * title_weight
        self.add_word_list(title_word_list)
        # abstract
        abs_word_list = abstract.split()
        self.add_word_list(abs_word_list)

    def add_word_list(self, word_list):
        """使用2-gram来生成词袋"""
        for idx, word in enumerate(word_list):
            # 考虑去停用值提高效率
            word = word.lower()
            word_list[idx] = word  # todo no sense
            self.update_bag(word)
            if idx == len(word_list) - 1: continue  # 最后一个
            self.update_bag(word + ' ' + word_list[idx + 1])

    def update_bag(self, word):
        """
        更新词袋
        Args:
            word (str): 新增的词
        Returns:
            int: 词数
        """
        if word in self.bag:
            self.bag[word] += 1
        else:
            self.bag[word] = 1
        return self.bag[word]


class BigField:
    """
    Field Manager
    """
    field_name: str
    has_extra: bool  # has extra supplement
    word2wc: dict  # {word: wc}
    word2val: dict  # {word: val}
    word2id: dict  # {word: id}
    vec: np.ndarray  # id -> val

    def __init__(self, field_name):
        self.field_name = field_name
        if field_name in ['Artificial Intelligence', 'Biotechnology', 'Intelligent manufacturing', 'new material technology']:
            self.has_extra = True
        else:
            self.has_extra = False

        # read word->word_count
        self.word2wc = dict()
        fpath = f'{Config.BASE_DIR}/process/field_data/{field_name}.txt'
        with open(fpath) as f:
            # read a txt file
            reader = csv.DictReader(f, fieldnames=['filed_word', 'word_count'], quotechar='\'')
            for row in reader:
                word = row['filed_word']
                try:
                    wc = int(row['word_count'])
                except ValueError:
                    cls_lg.debug(f"line_no: {reader.line_num}")
                else:
                    self.word2wc[word] = wc

        # normalize count to value
        self.word2val = self.normalize_wc_weight_by_segment(self.word2wc)

        # # read extra info
        # if self.has_extra:
        #     # has extra info supplement
        #     cls_lg.debug(f"extra: {field_name}")
        #     extra_info_path = f'{Config.BASE_DIR}/process/field_data/extra/{field_name}.json'
        #     with open(extra_info_path) as ef:
        #         extra_info = json.load(ef)
        #     for word, value in extra_info.items():
        #         norm_value = self.normalize_extra_value(value)
        #         if word in self.word2val:
        #             self.word2val[word] += norm_value
        #         else:
        #             self.word2val[word] = norm_value

        # vectorise
        self.word2id = dict()
        self.vec = np.zeros(len(self.word2val))
        for wid, w in enumerate(self.word2val):
            self.word2id[w] = wid
            self.vec[wid] = self.word2val[w]

    @staticmethod
    def normalize_wc_weight(word_wc_dict):
        """
        normalize a {word: wc} dict
        thinking: just get the most high freq word
        todo 这里的性能开销或许可以优化
        """
        FRONT_NUM = 1000
        cut_wc_weight = sorted(word_wc_dict.items(), key=lambda x: x[1], reverse=True)[:FRONT_NUM]
        tot_freq = sum([wc_item[1] for wc_item in cut_wc_weight])
        return {wc_item[0]: wc_item[1] / tot_freq for wc_item in cut_wc_weight}

    @staticmethod
    def normalize_wc_weight_by_order(word_wc_dict):
        """
        Args:
            word_wc_dict: {word: wc}
        Returns:
            {word: val}
        """
        FRONT_NUM = 1000
        cut_wc_weight = sorted(word_wc_dict.items(), key=lambda x: x[1], reverse=True)[:FRONT_NUM]
        cls_lg.debug(f"cut word weight before normalization: {cut_wc_weight[:5]} ... {cut_wc_weight[-5:]}, total len: {len(cut_wc_weight)}")
        # [(word, wc), ...]
        # [(word, 1000 - 0), ...]
        new_cut_wc_weight = [(i[0], FRONT_NUM - idx) for idx, i in enumerate(cut_wc_weight)]
        cls_lg.debug(f"cut word weight after normalization: {new_cut_wc_weight[:5]} ... {new_cut_wc_weight[-5:]}, total len: {len(new_cut_wc_weight)}")
        tot_freq = sum([wc_item[1] for wc_item in new_cut_wc_weight])
        return {wc_item[0]: wc_item[1] / tot_freq for wc_item in new_cut_wc_weight}

    @staticmethod
    def normalize_wc_weight_by_segment(word_wc_dict):
        """
        分段计算
        Args:
            word_wc_dict: {word: wc}
        Returns:
            {word: val}
        """
        FRONT_NUM = 1000
        cut_wc_weight = sorted(word_wc_dict.items(), key=lambda x: x[1], reverse=True)[:FRONT_NUM]
        cls_lg.debug(f"cut word weight before normalization: {cut_wc_weight[:5]} ... {cut_wc_weight[-5:]}, total len: {len(cut_wc_weight)}")
        # [(word, wc), ...]
        # [(word, 1000 - 0), ...]
        def seg(x):
            return int((x - 1) / 100 + 1) * 100
        new_cut_wc_weight = [(i[0], seg(FRONT_NUM - idx)) for idx, i in enumerate(cut_wc_weight)]
        cls_lg.debug(f"cut word weight after normalization: {new_cut_wc_weight[:5]} ... {new_cut_wc_weight[-5:]}, total len: {len(new_cut_wc_weight)}")
        tot_freq = sum([wc_item[1] for wc_item in new_cut_wc_weight])
        return {wc_item[0]: wc_item[1] / tot_freq for wc_item in new_cut_wc_weight}

    @staticmethod
    def normalize_extra_value(value):
        """
        normalize the extra weight from extra words
        5 -> 0.15
        """
        return 0.1 + value / 100


class FieldClassifier:
    """
    分类器
    初始化：加载领域词典
    逐个单词计算领域主题分布
    todo 应该单独把每个类别拿出来，然后做综合
    """
    BIG_FIELD_LIST = [
        'Artificial Intelligence',
        'Biotechnology',
        'Intelligent manufacturing',
        'Modern Transportation Technology',
        'aerospace technology',
        'big data technology',
        'gene technology',
        'marine technology',
        'new generation of information technology',
        'new material technology',
    ]
    en2cn = {
        'Artificial Intelligence': '人工智能技术',
        'Biotechnology': '生物技术',
        'Intelligent manufacturing': '智能制造',
        'Modern Transportation Technology': '现代交通技术',
        'aerospace technology': '空天技术',
        'big data technology': '大数据技术',
        'gene technology': '基因技术',
        'marine technology': '海洋技术',
        'new generation of information technology': '新代信息通信技术',
        'new material technology': '新材料技术'
    }
    threshold = {
        'Artificial Intelligence': 9,
        'Biotechnology': 8,
        'Intelligent manufacturing': 20,
        'Modern Transportation Technology': 7,
        'aerospace technology': 20,
        'big data technology': 6,
        'gene technology': 70,
        'marine technology': 25,
        'new generation of information technology': 25,
        'new material technology': 70
    }
    all_field = dict()  # {'Biotechnology': {'word 1': <freq 1>, 'word 2': <freq 2>, ...}, ...}

    def __init__(self):
        """
        初始化生成一个主题分布的词典 field_info
        每个 BigField 都封装成一个类
        {'Biotechnology': <BigField: Biotechnology>, ...}
        <BigField: Biotechnology>.field_info = {'word 1': <val 1>, 'word 2': <val 2>, ...}
        """
        for big_field in self.BIG_FIELD_LIST:
            self.all_field[big_field] = BigField(big_field)

    @staticmethod
    def cal_vec_sim(vec1, vec2, norm=False):
        """计算两个向量x和y的余弦相似度"""
        assert len(vec1) == len(vec2), "len(vec1) != len(vec2)"
        if np.all(vec1 == 0):
            return 0
        # other method is hidden in git history
        res = np.array([[vec1[i] * vec2[i], vec1[i] * vec1[i], vec2[i] * vec2[i]] for i in range(len(vec1))])
        cos = sum(res[:, 0]) / (np.sqrt(sum(res[:, 1])) * np.sqrt(sum(res[:, 2])))
        return 0.5 * cos + 0.5 if norm else cos  # 归一化到[0, 1]区间内

    def get_bag_hit_most_vec(self, word_bag, threshold=0.5):
        """
        generate vector at each big field for a word bag
        Args:
            word_bag (dict): {word1: count1, word2: count2}
            threshold (float): th
        """
        field_hit_res = dict()  # {bf1: score1, bf2: score2 ...}
        for bf_name, bf_info in self.all_field.items():  # type: str, BigField
            w2id = bf_info.word2id
            wb_vec = np.zeros(len(bf_info.vec))
            for w, freq in word_bag.items():
                if w in w2id:  # word in field dictionary
                    wb_vec[w2id[w]] = freq
            # got a word bag vector, compare (wb_vec, bf_vec)
            sim_score = self.cal_vec_sim(wb_vec, bf_info.vec)
            field_hit_res[bf_name] = sim_score
        # sort
        sorted_res = sorted(field_hit_res.items(), key=lambda kv: kv[1], reverse=True)
        return sorted_res


def run_filed_cls():
    cls = FieldClassifier()
    qres = PolicyText.query.filter(PolicyText.use,
                                   PolicyText.original_title != None,
                                   PolicyText.field == None,
                                   PolicyText.abstract != None).all()
    for policy in tqdm(qres):  # type: PolicyText
        title = policy.original_title
        abstract = pure_text(policy.abstract)
        wb = WordBag(title, abstract)
        cls_res = cls.get_bag_hit_most_vec(wb.bag)
        if not cls_res: continue
        policy.field = str(cls_res)
        db.session.add(policy)
        db.session.commit()
        # logging.info(f'id: {policy.id} | class res: {cls_res} | title: {title}\n')


def trim_norm_field(threshold=0.05):
    """根据field字段来生成可用的norm_field字段"""
    second_cnt = 0
    field_cnt = {
        '无类别': 0,
        '人工智能技术': 0,
        '生物技术': 0,
        '智能制造': 0,
        '现代交通技术': 0,
        '空天技术': 0,
        '大数据技术': 0,
        '基因技术': 0,
        '海洋技术': 0,
        '新代信息通信技术': 0,
        '新材料技术': 0
    }
    second_field_cnt = {
        '人工智能技术': 0,
        '生物技术': 0,
        '智能制造': 0,
        '现代交通技术': 0,
        '空天技术': 0,
        '大数据技术': 0,
        '基因技术': 0,
        '海洋技术': 0,
        '新代信息通信技术': 0,
        '新材料技术': 0
    }
    en2cn = {
        'Artificial Intelligence': '人工智能技术',
        'Biotechnology': '生物技术',
        'Intelligent manufacturing': '智能制造',
        'Modern Transportation Technology': '现代交通技术',
        'aerospace technology': '空天技术',
        'big data technology': '大数据技术',
        'gene technology': '基因技术',
        'marine technology': '海洋技术',
        'new generation of information technology': '新代信息通信技术',
        'new material technology': '新材料技术',
    }

    # loop all policy and get statistics
    qres = PolicyText.query.filter(PolicyText.use,
                                   PolicyText.correct_field == None,
                                   PolicyText.field != None,
                                   PolicyText.original_title != None,
                                   PolicyText.abstract != None)
    for policy in tqdm(qres):  # type: PolicyText
        field_info = eval(policy.field)
        cls_name_1, cls_val_1 = field_info[0]
        cls_name_2, cls_val_2 = field_info[1]
        cls_name_1 = en2cn[cls_name_1]
        cls_name_2 = en2cn[cls_name_2]
        policy.correct_field = cls_name_1
        if cls_val_1 < threshold:
            policy.norm_field = ['无类别']
            field_cnt['无类别'] += 1
        else:
            # 第一类特别大或者第二类没过阈值
            field_cnt[cls_name_1] += 1
            if cls_val_2 < threshold or (cls_val_1 - cls_val_2) / cls_val_2 > 2:
                policy.norm_field = [cls_name_1]
            else:
                policy.norm_field = [cls_name_1, cls_name_2]
                second_field_cnt[cls_name_2] += 1
                second_cnt += 1
        flag_modified(policy, 'norm_field')
        db.session.add(policy)
    db.session.commit()
    print(field_cnt)
    print(second_field_cnt)
    print(second_cnt)


def report_cls_info():
    cls = FieldClassifier()
    for bf, bf_info in cls.all_field.items():
        print(bf, '该领域的词数为：', len(bf_info.vec), 'SUM: ', sum(bf_info.vec))
        print(np.round(bf_info.vec[:10], 4))


if __name__ == '__main__':
    run_filed_cls()
    trim_norm_field()
    report_cls_info()
