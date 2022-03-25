# -*- coding: utf-8 -*-

""" 
@author: Jin.Fish
@file: util.py
@version: 1.0
@time: 2021/06/01 20:25:40
@contact: jinxy@pku.edu.cn

utils
"""

import os
import hashlib
import logging
import re
import threading
from bs4 import BeautifulSoup as bs
from config import Config
from flask import make_response

logging.basicConfig(format='%(asctime)s | %(levelname)s | %(filename)s | %(funcName)s | %(message)s',
                    level=logging.INFO, datefmt='%m-%d %H:%M:%S')


def get_md5_str(s_):
    """
    将字符串转换成md5
    所有文件的名称都用 文件链接的 md5
    """
    return hashlib.md5(s_.encode("utf-8")).hexdigest()


def pure_text(html_):
    if not html_:
        return ""
    return bs(html_, 'lxml').text


def check_path(path_):
    """
    check if path exist
    Args:
        path_ (str):
    Returns:
        bool
    """
    return os.path.exists(path_)


class FileNameNotMatchError(BaseException):
    def __init__(self, name):
        self.info = name


class FileName:
    md5_str: str
    origin_file_type: str
    origin_extension: str

    def __init__(self, file_url='', file_type='origin', extension='pdf'):
        """
        init filename
        Args:
            file_url (str): if intended to use set_by_name(), skip this
            file_type (str): origin | format | trans | check
            extension (str): pdf | txt | html
        """
        self.md5_str = get_md5_str(file_url)
        self.origin_file_type = file_type
        self.origin_extension = extension

    def set_by_name(self, save_name):
        # name_re = re.match(r"(origin|format|check|trans)_(\w*)\.(\w+)", save_name)
        # only support origin now
        name_re = re.match(r"(origin|format)_(\w*)\.(\w+)", save_name)
        if not name_re:
            raise FileNameNotMatchError(save_name)
        self.origin_file_type = name_re.group(1)
        self.md5_str = name_re.group(2)
        assert len(self.md5_str) == 32
        self.origin_extension = name_re.group(3)

    def gen_name(self, file_type):
        if file_type == 1:
            return f"origin_{self.md5_str}.{self.origin_extension}"
        if file_type == 2:
            return f"format_{self.md5_str}.txt"
        if file_type == 3:
            return f"trans_{self.md5_str}.txt"
        if file_type == 4:
            return f"check_{self.md5_str}.txt"

    def gen_path(self, file_type):
        dir_path = Config.BASE_DIR
        file_name = self.gen_name(file_type)
        if file_type == 1:
            return os.path.join(dir_path, 'app/data/origin', file_name)
        if file_type == 2:
            return os.path.join(dir_path, 'app/data/format', file_name)
        if file_type == 3:
            return os.path.join(dir_path, 'app/data/trans', file_name)
        if file_type == 4:
            return os.path.join(dir_path, 'app/data/check', file_name)


class MyThread(threading.Thread):
    def __init__(self, func, args):
        super(MyThread, self).__init__()
        self.func = func
        self.args = args

    def run(self):
        self.result = self.func(*self.args)

    def get_result(self):
        try:
            return self.result
        except Exception:
            return None

# import time
from io import BytesIO
import xlwt
from statistic import statistic
from flask import make_response
import pymysql

db = pymysql.connect(host="81.70.102.186", user="root", password="YDH@henniu123", database="spider", port=3306)
s = statistic(db)

def get_file(file):
    path = os.path.abspath(f"app/static/monitor/{file}.txt")
    with open(path, encoding='utf8') as f:
        entity = f.readlines()
        f.close()
    link2 = []
    for en in entity:
        link2.append(en.strip().split(','))
    return link2

#导出excel报表


def export_excel(num, type):
    """excel 报表导出"""
    type_ch = ''
    if type == 'ins':
        type = 'institute'
        type_ch = 'institute'
    elif type == 'entity':
        type_ch = 'entity'
    else:
        type_ch = 'link'
    results = entity2 = get_file(type)[:num]
    # 实例化，有encoding和style_compression参数
    new = xlwt.Workbook(encoding='utf-8')
    # Workbook的方法，生成.xls文件
    sheet = new.add_sheet('实体', cell_overwrite_ok=True)
    # 写上字段信息
    sheet.write(0, 0, type_ch)
    sheet.write(0, 1, '数量')

    for row in range(1, len(results) + 1):
        for col in range(0, 2):
            sheet.write(row, col, u'%s' % results[row - 1][col])

    sio = BytesIO()
    new.save(sio)  # 将数据存储为bytes
    sio.seek(0)
    response = make_response(sio.getvalue())
    response.headers['Content-type'] = 'application/vnd.ms-excel'  # 响应头告诉浏览器发送的文件类型为excel
    response.headers['Content-Disposition'] = f'attachment; filename={type_ch}.xls'  # 浏览器打开/保存的对话框，data.xlsx-设定的文件名
    return response

def get_statistic(db, name, num):
    res = db.query.order_by(db.rank).all()
    if name == 'keywords':
        res2 = [(i.keywords, i.keywords_number) for i in res]
        return res2[:num]
    return None

def export_excel2(db, name, num):
    """excel 报表导出"""
    # if name == 'keyword':
    #     results = s.count_keywords()[:num]
    # else:
    #     return
    res = db.query.order_by(db.rank).all()
    if name == 'keywords':
        res2 = [(i.keywords, i.keywords_number) for i in res]
        results = res2[:num]
    # 实例化，有encoding和style_compression参数
    new = xlwt.Workbook(encoding='utf-8')
    # Workbook的方法，生成.xls文件
    sheet = new.add_sheet('关键词', cell_overwrite_ok=True)
    # 写上字段信息
    sheet.write(0, 0, "关键词")
    sheet.write(0, 1, '数量')

    # 获取并写入数据段信息
    row = 1
    col = 0
    for row in range(1, len(results) + 1):
        for col in range(0, 2):
            sheet.write(row, col, u'%s' % results[row - 1][col])

    sio = BytesIO()
    new.save(sio)  # 将数据存储为bytes
    sio.seek(0)
    response = make_response(sio.getvalue())
    response.headers['Content-type'] = 'application/vnd.ms-excel'  # 响应头告诉浏览器发送的文件类型为excel
    response.headers['Content-Disposition'] = 'attachment; filename=keywords.xlsx'  # 浏览器打开/保存的对话框，data.xlsx-设定的文件名
    return response


# 判断检索类型：高级检索 或者 关键词检索
# 高级检索模块：逆波兰转化
def advanced_trans(query):
    flag_common = 0 #判断是否是普通检索
    for i in ['AND','OR','NOT']:
        if i not in query:
            flag_common +=1
    if flag_common == 3:
        return query
    # 转换成数学式形式（分词）
    query = query.replace('AND', '_*_')
    query = query.replace('OR', '_+_')
    query = query.replace('NOT', '_-_')
    query = query.replace(' ', '')
    query = query.replace('（', '_(_')
    query = query.replace('）', '_)_')
    query = query.replace('(', '_(_')  # 中英文括号都考虑
    query = query.replace(')', '_)_')

    query = re.split('_', query)

    while '' in query:
        query.remove('')

    # 开始逆波兰
    stack, result = [], []
    priority = {"*": 1, "+": 2, "-": 2}

    for i in query:
        if i == "(":
            stack.append(i)
        elif i == ")":
            while stack[-1] != "(":
                result.append(stack.pop())
            stack.pop()
        elif i in "*+-":
            while len(stack) >= 1 and stack[-1] != '(' and priority[stack[-1]] <= priority[i]:
                result.append(stack.pop())
            stack.append(i)
        else:
            result.append(i)

    while stack != []:
        result.append(stack.pop())

    return " ".join(result)


class Stack:

    def __init__(self):
        self.items = []

    def isEmpty(self):
        return self.items == []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        return self.items.pop()

    def peek(self):
        return self.items[len(self.items) - 1]

    def size(self):
        return len(self.items)

# def word2pla(i):#检索词i
#     pla=set()#空集合，最终输出
#
#     pla.add(i)
#     return pla
#
# def polishcal(i):
#     ope = ['+', '-', '*']
#     s = advanced_trans(i).split()
#     print(s)
#     stack = Stack()
#     for x in s:
#         if (x in ope) == False:
#             stack.push(word2pla(x))
#         elif x == "+":
#             a = stack.pop()
#             b = stack.pop()
#             print(a)
#             print(a | b)
#             stack.push(a | b)
#         elif x == "-":
#             a = stack.pop()
#             b = stack.pop()
#             stack.push(b - a)
#         elif x == "*":
#             a = stack.pop()
#             b = stack.pop()
#             stack.push(a & b)
#
#     return list(stack.peek())

if __name__ == '__main__':
    file = FileName(
        'https://assets.publishing.service.gov.uk/government/uploads/system/uploads/attachment_data/file/951739/Laptops_and_Tables_Data_as_of_12_January.pdf')
    for i in [1, 2, 3, 4]:
        print(file.gen_name(1))
        print(file.gen_path(1))
