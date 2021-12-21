# import os
# fa_path = os.path.dirname(os.getcwd())
# print(fa_path+'\static\monitor\entity.txt')
# # path = os.path.join(fa_path)
# path = fa_path+'\static\monitor\entity.txt'
# with open(path,encoding='utf8') as f:
#     entity = f.readlines()
#     f.close()
#
# entity2 = []
#
# for en in entity:
#     entity2.append(en.strip().split(','))
# print('fwengfj'[-2:])
import pymysql
db = pymysql.connect(host='175.24.114.16',
                     user='caf',
                     password='tech2021',
                     database='tech_pro')
# print(db)
cursor = db.cursor()
cursor.execute("SELECT title FROM news_aip")
title = cursor.fetchall()
print(len(set(title)))