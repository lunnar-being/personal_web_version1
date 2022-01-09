import os
import numpy as np
import pandas as pd
import tqdm
from tqdm import trange
import spacy
from spacy.lang.en.stop_words import STOP_WORDS
import string
import re
from flashtext import KeywordProcessor

"""
author : whg
time : 2021/12/25
"""


# txt文件地址 需要更改
path = r'module/file'

# 得到文件夹下的所有文件名称
files = os.listdir(path)


# 非结束符字符串
def puncs():
    # punc是一个全符号的字符串
    punc = string.punctuation
    punc = punc.replace('.', '')
    punc = punc.replace('?', '')
    punc = punc.replace('!', '')
    punc = punc.replace('。', '')
    punc = punc.replace('？', '')
    punc = punc.replace('！', '')
    # remove = str.maketrans('', '', punc)
    return punc


# flashtext去除停用词和符号
def get_stopwords_proc():
    # 停用词去除器
    stopword_processor = KeywordProcessor()
    # 加载停用词，不要字母
    for i in STOP_WORDS:
        if not i.isalpha():
            stopword_processor.add_keyword(i, ' ')
        elif len(i) >= 2:  # 此处的最短长度是否应当修改
            stopword_processor.add_keyword(i, ' ')
        else:
            pass
    # 如果有删除符号的必要，可以运行如下部分代码，将符号视作停用词加入
    # for i in puncs():
    #     stopword_processor.add_keyword(i, ' ')
    stopword_processor.add_keyword('↩', '.')
    stopword_processor.add_keyword('-', ' ')
    stopword_processor.add_keyword('“', ' ')
    stopword_processor.add_keyword('”', ' ')
    stopword_processor.add_keyword('\'s', ' ')
    stopword_processor.add_keyword('\nsec', ' ')
    stopword_processor.add_keyword('\n', ' ')
    stopword_processor.add_keyword('..', ' ')
    stopword_processor.add_keyword('...', ' ')
    # 缩略语，有待添加
    stopword_processor.add_keyword('U.S.', 'USA')
    return stopword_processor


# 读取文件
def readfile(file,file_path):
    with open("%s/%s" %(file_path,file), "r", encoding='utf-8') as f:  # 打开文件
        get_text = f.read()  # 读取文件
    f.close()
    return get_text


# 文本处理
def processing(file_content):
    file_content = file_content.strip()
    file_content = re.sub("\n|\d*", "", file_content)  # 清除数字，可更改
    stopword_processor = get_stopwords_proc()
    try:
        file_content = stopword_processor.replace_keywords(file_content)
        # 停用词删除 使用flashtext替换关键词会报错 也可以改用replace函数 缺点是速度慢
    except:
        pass
    # 一些没删掉的符号，可全部删除也可以自行控制
    for i in puncs():
        file_content = file_content.replace(i, "")
    file_content = file_content.replace('-', ' ')
    file_content = file_content.replace('“', ' ')
    file_content = file_content.replace('”', ' ')
    file_content = file_content.replace('–', ' ')
    file_content = file_content.replace('‘', ' ')
    file_content = file_content.replace('’', ' ')
    file_content = file_content.replace('#', ' ')
    file_content = file_content.replace('(', ' ')
    file_content = file_content.replace(')', ' ')
    file_content = file_content.replace('—', ' ')
    file_content = file_content.strip()
    # 单字符
    file_content = re.sub('\s[a-zA-Z]{1}\s', ' ', file_content)
    # 此处按照空格切分成列表，如果文本较短更加推荐nlp工具：spacy、nltk
    file_content = file_content.split()
    # 返回拼接起来的字符串
    return ' '.join(file_content)


# 单句合并，五个句子一个单位，可控制
def sent_clus(sentences):
    # 修改unit_num，控制将几个句子拼在一起
    unit_num = 5
    Res = []
    fRes = []

    temp = int(len(sentences) / unit_num)

    for i in range(temp):
        if (i + unit_num-1) < len(sentences):
            s = ''
            for j in range(i * unit_num, i * unit_num + unit_num):
                s += sentences[j]
            Res.append(s)
        else:
            pass
    if len(Res) > 10:  # 拼接后返回前五个后五个
        fRes = Res[:5] + Res[-5:]
    return fRes


# 句子切分
def cut_sentences(content):
    # 结束符号，包含中文和英文的
    end_flag = ['?', '!', '.', '？', '！', '。', '…']

    content_len = len(content)
    sentences = []
    tmp_char = ''
    for idx, char in enumerate(content):
        # 拼接字符
        tmp_char += char

        # 判断是否已经到了最后一位
        if (idx + 1) == content_len:
            sentences.append(tmp_char)
            break

        # 判断此字符是否为结束符号
        if char in end_flag:
            # 再判断下一个字符是否为结束符号，如果不是结束符号，则切分句子
            next_idx = idx + 1
            if not content[next_idx] in end_flag:
                # 在主函数中对整个文本进行清洗，此处不再对单个句子处理
                # tmp_char=processing(tmp_char)
                if tmp_char != None:
                    if (' ' in tmp_char) and (len(tmp_char) > 10):
                        sentences.append(tmp_char)
                tmp_char = ''
    res = sent_clus(sentences)
    return res

if __name__ == '__main__':
    # t = "I see -a girl %with the telephone. an important review will be"
    # print(processing(t))
    pass
