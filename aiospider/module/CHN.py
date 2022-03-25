from module.text_processing import *
from module.tomysql import *
import random

"""
author : whg
time : 2021/12/25
"""
Cwords = ['china', 'chinese', 'sino', 'sinae', 'serica', 'seres', 'chn', 'prc', 'beijing', 'peking',
          'chinamania', 'chinoiserie', 'confucianism', 'fohism', 'foism', 'maoism', 'mohism',
          'sinicism', 'sinology', 'cathay', 'manchuria', 'shanghai', 'xi', 'taiwan', 'tibet']


# 去除点号
def Cprocessing(origin_text):
    processor = get_stopwords_proc()
    processor.add_keyword('.', ' ')
    try:
        new_text = processor.replace_keywords(origin_text)  # 使用flashtext替换关键词会报错 也可以改用replace函数 缺点是速度慢
    except:
        new_text = origin_text
    for i in string.punctuation:
        new_text = new_text.replace(i, ' ')
    new_text = new_text.strip()
    return new_text.split()


# 传入原始文本,统计涉华词频,单条统计
def C_count(origin_text):
    sum = 0
    for i in Cprocessing(origin_text):
        if i.lower() in Cwords:
            sum += 1
    return sum


# 全量更新涉华词频
def update_CHN(file_path):
    names = get_file_CHN()  # 获取id，文档名

    for i in names:
        if i[1] in files:  # 更新未统计过的
            total = 0
            try:
                total += C_count(readfile(i[1],file_path))  # 正文涉华关键词
            except:
                pass
            finally:
                total += C_count(i[3])  # 标题涉华关键词
                update_t1(file_id=i[0], target_column='CHN', update_value=total)  # 按id更新数据库
        else:
            pass


if __name__ == '__main__':
    # Egtext = "President Joseph R. Biden, Jr. met virtually on November 15 with President Xi Jinping of the People’s " \
    #          "Republic of China (PRC). The two leaders discussed the complex nature of relations between our two " \
    #          "countries and the importance of managing competition responsibly. As in previous discussions, " \
    #          "the two leaders covered areas where our interests align, and areas where our interests, values, " \
    #          "and perspectives diverge. President Biden welcomed the opportunity to speak candidly and " \
    #          "straightforwardly to President Xi about our intentions and priorities across a range of issues. "
    # print(C_count(Egtext), '\n', processing(Egtext).split())
    update_CHN()
    pass
