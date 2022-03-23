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
# import pymysql
# db = pymysql.connect(host='175.24.114.16',
#                      user='caf',
#                      password='tech2021',
#                      database='tech_pro')
# # print(db)
# cursor = db.cursor()
# cursor.execute("SELECT title FROM news_aip")
# title = cursor.fetchall()
# print(len(set(title)))
# d = dict()
# d['sda'] = 1
# print(list(d.items()))
class Father(object):
    def __init__(self, name):
        self.name = name





if __name__ == '__main__':
    print("dsd".startswith())
    # q={1,2,3}
    # u={3,4}
    # print(q-u)
    # print(type(f))
    #
    # class Son(f):
    #     def __init__(self,age):
    #         super(Son,self).__init__()
    #         self.age = age
    # son = Son('23')
    # print(type(son))

# print(len("http://127.0.0.1:5000/search.html?query-type=%E6%A0%87%E9%A2%98&query=%E6%8B%9C%E7%99%BB&query-bool-1=OR&query-type-1=%E6%A0%87%E9%A2%98&query-1=%E4%B8%AD%E5%9B%BD&query-bool-1=AND&query-type-1=%E6%A0%87%E9%A2%98&query-1=%E4%B8%AD%E5%9B%BD&field=%E5%85%A8%E9%83%A8%E5%88%86%E7%B1%BB&order=star"))