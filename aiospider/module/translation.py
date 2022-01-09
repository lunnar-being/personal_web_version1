# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import mysql.connector
import requests
import random
import json
import time
from hashlib import md5

"""
author : whg
time : 2021/12/25
"""


def trans(query):
    # Set your own appid/appkey.
    appid = '20211018000976129'
    appkey = 'juwaIxXExoFqPWKuDbgX'

    # For list of language codes, please refer to `https://api.fanyi.baidu.com/doc/21`
    from_lang = 'en'
    to_lang = 'zh'

    endpoint = 'http://api.fanyi.baidu.com'
    path = '/api/trans/vip/translate'
    url = endpoint + path

    # Generate salt and sign
    def make_md5(s, encoding='utf-8'):
        return md5(s.encode(encoding)).hexdigest()

    salt = random.randint(32768, 65536)
    sign = make_md5(appid + query + str(salt) + appkey)

    # Build request
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    payload = {'appid': appid, 'q': query, 'from': from_lang, 'to': to_lang, 'salt': salt, 'sign': sign}

    # Send request
    r = requests.post(url, params=payload, headers=headers)
    result = r.json()

    # Show response
    return (json.loads(json.dumps(result, indent=4, ensure_ascii=False)))


# ------------------------------------------------------------------------------------------------
"""
需要修改的部分
"""
host, user, password, database = '175.24.114.16', 'caf', 'tech2021', 'tech_pro'
table = 'event'
source_col = 'title'
target_col = 'title_zh'


# -------------------------------------------------------------------------------------------------

def connect():
    mydb = mysql.connector.connect(
        host=host,
        user=user,
        passwd=password,
        database=database
    )
    return mydb


def select():
    mydb = connect()
    mycursor = mydb.cursor()
    sql = f"SELECT * FROM {table}"  # select 语句 可编辑
    mycursor.execute(sql)  # 执行
    myresult = mycursor.fetchall()  # fetchall() 获取所有记录
    # print(myresult)#list,每个元素是一个元组
    # print(type(myresult))
    for x in myresult:
        print(x)
    # return myresult


def update_translation():
    mydb = connect()
    mycursor = mydb.cursor()
    sql_1 = f'select id from {table} where {source_col} is not null and {target_col} is null '
    mycursor.execute(sql_1)  # 执行
    trans_id = mycursor.fetchall()  # fetchall() 获取需要翻译的id列表
    for i in trans_id:
        print(i[0])
        sql_2 = f'select {source_col} from {table} where id = {i[0]}'
        mycursor.execute(sql_2)  # 执行
        cont = mycursor.fetchall()  # fetchall() 获取需要翻译的content
        # print(cont,type(cont))
        if cont[0][0] != '':
            cont_zh = trans(cont[0][0])
            time.sleep(1)
            if ('from' in cont_zh):
                Towrite = cont_zh['trans_result'][0]['dst']
                # print((Towrite))
                sql_3 = f'update {table} set {target_col} = %s where id = %s'
                mycursor.execute(sql_3, (Towrite, i[0]))
                mydb.commit()
        else:
            pass

    print('finish')


if __name__ == '__main__':
    # sentence = 'I saw a girl. '
    # res = trans(sentence)
    # # class dict
    # print(res)
    # print(type(res))
    # # class list
    # print(res['trans_result'])
    # print(type(res['trans_result']))
    # #class str
    # print(res['trans_result'][0]['dst'])
    # print(type(res['trans_result'][0]['dst']))
    # print(trans('Senate Panel Approves NOAA Nominee on Party-Line Vote'))
    update_translation()
    # select()
