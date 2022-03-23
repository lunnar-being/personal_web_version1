# import time
from io import BytesIO
import xlwt
from flask import make_response
from statistic import statistic
import pymysql
db = pymysql.connect(host="81.70.102.186", user="root", password="YDH@henniu123", database="spider", port=3306)
s = statistic(db)

def get_file(file):
    path = rf"E:\research\technology\app\static\monitor\{file}.txt"
    with open(path, encoding='utf8') as f:
        entity = f.readlines()
        f.close()
    link2 = []
    for en in entity:
        link2.append(en.strip().split(','))
    return link2

#导出excel报表


def export_excel(num):
    """excel 报表导出"""
    results = entity2 = get_file('entity')[:num]
    # 实例化，有encoding和style_compression参数
    new = xlwt.Workbook(encoding='utf-8')
    # Workbook的方法，生成.xls文件
    sheet = new.add_sheet('实体', cell_overwrite_ok=True)
    # 写上字段信息
    for field in ['实体','数量']:
        sheet.write(0, field)

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
    response.headers['Content-Disposition'] = 'attachment; filename=newlist.xlsx'  # 浏览器打开/保存的对话框，data.xlsx-设定的文件名
    return response


def export_excel2(num,name):
    """excel 报表导出"""
    if name == 'keyword':
        results = s.count_keywords()[:num]
    else:
        return
    # 实例化，有encoding和style_compression参数
    new = xlwt.Workbook(encoding='utf-8')
    # Workbook的方法，生成.xls文件
    sheet = new.add_sheet('实体', cell_overwrite_ok=True)
    # 写上字段信息
    for field in ['实体','数量']:
        sheet.write(0, field)

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


# -*- coding: utf-8 -*-


# 判断检索类型：高级检索 或者 关键词检索
# 高级检索模块：逆波兰转化
def advanced_trans(query):
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


def polishcal(i):
    ope = ['+', '-', '*']
    s = advanced_trans(i).split()
    stack = Stack()
    for x in s:
        # if (x in ope) == False:
        #     stack.push(word2pla(x))
        if x == "+":
            a = stack.pop()
            b = stack.pop()
            stack.push(a | b)
        elif x == "-":
            a = stack.pop()
            b = stack.pop()
            stack.push(b - a)
        elif x == "*":
            a = stack.pop()
            b = stack.pop()
            stack.push(a & b)

    return list(stack.peek())