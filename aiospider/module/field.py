import random
from transformers import pipeline
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from module.text_processing import *
from module.tomysql import *

"""
author : whg
time : 2021/12/25
"""

# 领域标签
candidate_labels = ['energy | environment',
                    'medicine | biology | health | gene',
                    'material & nano',
                    'food & agriculture',
                    'space & cosmos',
                    'defense & army & military',
                    'manufacture',
                    'signal & wireless & electronics',
                    'AI | big data',
                    'traffic']

# 英文标签转中文
transform_label_dic = {
    "energy | environment": "能源环境科技",
    'medicine | biology | health | gene': "医药健康科技",
    'material & nano': "新材料科技",
    'food & agriculture': "食品农业科技",
    'space & cosmos': "空天科技",
    'defense & army & military': "国防安全",
    'manufacture': "智能制造",
    "signal & wireless & electronics": "新代信息通信科技",
    "AI | big data": "大数据与人工智能",
    "traffic": "现代交通科技",
    "others": "其他"}


# 领域分类可视化
def vs(content):
    res = bart(content, candidate_labels, multi_label=True, hypothesis_template=hypothesis_template)
    print(content)
    print(np.var(res['scores']))
    if (res['scores'][0] >= 0.4) and (np.var(res['scores']) >= 0.02) and (res['scores'][0] * 0.8 >= res['scores'][2]):
        print('accepted1')
    else:
        print('reject')
    plt.barh(res['labels'], res['scores'])
    plt.show()


# 分类函数，content为原始未经处理的长文本字符串，id为数据库对应id， 单条分类
def class_result(origin_text, file_id, bart, hypothesis_template):
    # 最终结果列表
    main_result = []
    sub_result = []

    sent_list = cut_sentences(processing(origin_text))

    # 标题*5
    # -------------------------------------------------------------------------------------------------------------------------
    file_title = get_title(file_id)

    if len(file_title) > 0:
        tt = file_title[0][0]
        res = bart(tt, candidate_labels, multi_label=True, hypothesis_template=hypothesis_template)
        if (res['scores'][0] >= 0.4) and (np.var(res['scores']) >= 0.02) and (
                res['scores'][0] * 0.8 >= res['scores'][2]):
            for j in range(5):
                main_result.append(res['labels'][0])
            if res['scores'][1] >= res['scores'][0] * 0.6:
                for j in range(5):
                    sub_result.append(res['labels'][1])
            else:
                pass
        else:
            pass

    # 摘要*3
    # ---------------------------------------------------------------------------------------------------------------------
    file_abstract = get_abstract(file_id)

    if (file_abstract != None) and (len(file_abstract) > 0):
        ab = file_abstract[0][0]
        res = bart(ab, candidate_labels, multi_label=True, hypothesis_template=hypothesis_template)
        if (res['scores'][0] >= 0.4) and (np.var(res['scores']) >= 0.02) and (
                res['scores'][0] * 0.8 >= res['scores'][2]):
            for j in range(3):
                main_result.append(res['labels'][0])
            if res['scores'][1] >= res['scores'][0] * 0.6:
                for j in range(3):
                    sub_result.append(res['labels'][1])
            else:
                pass
        else:
            pass
    # 文本子句*2
    # -----------------------------------------------------------------------------------------------------------------------
    for s in sent_list:
        res = bart(s, candidate_labels, multi_label=True, hypothesis_template=hypothesis_template)
        if (res['scores'][0] >= 0.4) and (np.var(res['scores']) >= 0.02) and (
                res['scores'][0] * 0.8 >= res['scores'][2]):
            for j in range(2):
                main_result.append(res['labels'][0])
            if res['scores'][1] >= res['scores'][0] * 0.6:
                for j in range(2):
                    sub_result.append(res['labels'][1])
            else:
                pass
        else:
            pass
    # 投票
    if len(main_result) > 0:
        main_label = max(main_result, key=main_result.count)
        if len(sub_result) > 0:
            sub_label = max(sub_result, key=sub_result.count)
            return [transform_label_dic[main_label], transform_label_dic[sub_label]]
        else:
            return [transform_label_dic[main_label], '其他']
    else:
        return ['其他', '其他']


# 全量更新
def field_cla(bart, hypothesis_template,file_path):
    names = get_file_field()
    for i in names:
        if i[1] in files:  # 重置条件
            final_labels = class_result(readfile(i[1],file_path), i[0], bart, hypothesis_template)
            # 更新函数
            update_t1(file_id=i[0], target_column='field_main', update_value=final_labels[0])
            update_t1(file_id=i[0], target_column='field_sub', update_value=final_labels[1])


def field_update(file_path):
    model_path = r"./module/model/bart"
    bart = pipeline("zero-shot-classification", model=model_path, device=0)
    hypothesis_template = "This text is about {}."
    field_cla(bart, hypothesis_template,file_path)
    pass


if __name__ == '__main__':
    model_path = r"./bart"  # 需要下载到本地
    """
    model url:
    https://huggingface.co/joeddav/bart-large-mnli-yahoo-answers/tree/main
    """
    bart = pipeline("zero-shot-classification", model=model_path, device=0)
    hypothesis_template = "This text is about {}."
    field_cla()  # 全量更新
    pass
