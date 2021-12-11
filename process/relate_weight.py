# -*- coding: utf-8 -*-

""" 
@author: Yu DaHai
@file: relate_weight.py
@version: 1.0
@time: 2021/04/20 19:19:45
@contact: jinxy@pku.edu.cn

计算政策的颠覆性相关程度
"""
import logging

from process import *
import nltk
import nltk.data
import math

from disruptive import app

app.app_context().push()


def split_sentence(whole_passage):
    """
    分句
    Args:
        whole_passage (str):
    Returns:
        list of sentences
    """
    t = nltk.data.load('tokenizers/punkt/english.pickle')
    result = t.tokenize(whole_passage)
    return result


def weight_calculate2(policy_title, policy_abs, policy_body):
    """
    计算权重
    Args:
        policy_title (str): 标题
        policy_abs (str): 摘要
        policy_body (str): 正文

    Returns:
        score (float)
    在yudahai版本基础上改了以下输入参数结构
    """
    len_title = len(split_sentence(policy_title)) + 1
    len_abs = len(split_sentence(policy_abs)) + 1
    len_body = math.log(2 + len(split_sentence(policy_body)), 2)

    text_list = [
        [split_sentence(policy_title), 3 / len_title],
        [split_sentence(policy_abs), 1 / len_abs],
        [split_sentence(policy_body), 2 / len_body]
    ]

    dic = [
        ['disrupt', 'tech', 10],
        ['disrupt', 'inno', 10],
        ['emerging', 'tech', 5],
        ['developing', 'tech', 1],
        ['advanced', 'tech', 1],
        ['integrated', 'tech', 1],
        ['future', 'tech', 1],
        ['promising', 'tech', 1],
        ['evolving', 'tech', 1],
        ['radical', 'tech', 5],
    ]
    v = 0
    s = 0
    for i in text_list:
        for k in i[0]:
            for j in dic:
                if j[0] in k and j[1] in k:
                    v += j[-1]
        s += v * i[1]
        v = 0
    return s


def run_weight():
    weight_logger = logging.getLogger("weight")
    weight_cnt = 0
    # 设置 nltk 读取路径
    nltk.data.path.append(os.path.expanduser('~/repos/nltk_data'))
    # nltk.download('punkt', download_dir=os.path.expanduser('~/repos/nltk_data'))

    plist = PolicyText.query.filter(PolicyText.use,
                                    PolicyText.format_file != None,
                                    PolicyText.rank == None).all()
    for policy in tqdm(plist):  # type: PolicyText
        format_file = File.query.get(policy.format_file)  # type: File
        if format_file and format_file.savename:
            real_path = path_join('app/data/format/' + format_file.savename)
            if not os.path.exists(real_path):
                weight_logger.error(f"file not exist: {real_path}, policy id: {policy.id}")
                continue
            with open(real_path) as f:
                content = ''.join(f.readlines())
                content = bs(content, 'lxml').text
            # 调用计算权重的函数
            rank = weight_calculate2(policy.original_title, pure_text(policy.abstract), content)
            if rank > 28:
                weight_logger.debug(f"high rank: {rank}")
            policy.rank = rank
            db.session.add(policy)
            weight_cnt += 1
    db.session.commit()
    return weight_cnt


if __name__ == '__main__':
    cnt = run_weight()
    print(f"[INFO] Compute weight success count: {cnt}")
