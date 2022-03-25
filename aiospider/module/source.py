import pandas as pd
from module.tomysql import *

"""
author : whg
time : 2021/12/25
"""


# url切分 一般不需改动
def url_split(origin_url):
    if 'http' in origin_url:
        url_part = origin_url.split('/')
        return url_part[2]
    else:
        return origin_url


# 加载本地url表格 不需改动
def get_web():
    inst = pd.read_csv('module/data/source.csv', encoding='utf-8')
    inst.columns = (['institution', 'web', 'score', 'cat', 'source'])
    return inst


# 单条来源分类
def get_source(origin_url):
    inst = get_web()
    for j in range(inst.shape[0]):
        if url_split(origin_url) == inst.loc[j, 'source']:
            return inst.loc[j, 'cat']


# 全量来源更新
def update_source():
    inst = get_web()
    urls = get_file_url()
    for i in urls:
        for j in range(inst.shape[0]):
            if url_split(i[1]) == inst.loc[j, 'source']:
                update_t1(i[0], 'source_classification', inst.loc[j, 'cat'])
            else:
                pass


if __name__ == '__main__':
    update_source()
