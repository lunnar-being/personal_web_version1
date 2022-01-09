import hashlib
from aiospider.module.rediscache import RedisCache
import pymysql


class globe:
    db = pymysql.connect(host="81.70.102.186", user="root", password="YDH@henniu123", database="spider", port=3306)
    cur = db.cursor()
    red = RedisCache()


class utils:
    @staticmethod
    def file_write(title, content, file_path):
        hash_title = hashlib.md5(title.encode("utf-8")).hexdigest()
        f = open("%s/%s.txt" % (file_path, hash_title), 'w', encoding='UTF-8')
        f.write(content)
        f.close()

    @staticmethod
    def submit(db, cur, e):
        sql1 = e.sql1()
        # sql2 = e.sql2()
        try:
            cur.execute(sql1)
            db.commit()
            # cur.execute(sql2)
            # db.commit()
        except:
            print("insert wrong")
            print(sql1)
            # print(sql2)

    @staticmethod
    def abs_null_id(db, cur):
        # sql_abs = "SELECT id,original_file FROM t1 WHERE LENGTH(abstract)<=200"
        sql_abs = "SELECT id,original_file,title FROM t1 WHERE abstract is NULL"
        # sql_abs = "SELECT id,original_file FROM t1 ORDER BY score DESC limit 300,1000"
        try:
            cur.execute(sql_abs)
            result = cur.fetchall()
            return result
        except:
            print("get null abs wrong")
            print(sql_abs)

    @staticmethod
    def update_abstract(db, cur, e):
        sql_abs = e.sql_abs()
        try:
            cur.execute(sql_abs)
            db.commit()
        except:
            print("update abs wrong")
            print(sql_abs)
            # print(sql2)

    @staticmethod
    def load_database_to_redis(db, red):
        # db = pymysql.connect(host="10.1.38.243", user="root", password="123456", database="spider", port=3306)
        # db = pymysql.connect(host="81.70.102.186", user="root", password="YDH@henniu123", database="spider", port=3306)
        cur = db.cursor()
        sql = "select source_url from t1"
        cur.execute(sql)
        res = cur.fetchall()
        for i in res:
            red[i[0]] = "a"
        print("加载完毕")
        # cur.close()
        # db.close()

    @staticmethod
    def score_null_id(cur):
        ids = "SELECT id,title,abstract,original_file FROM t1 WHERE score is NULL"
        id_list = []
        try:
            cur.execute(ids)
            res = cur.fetchall()
            for i in res:
                id_list.append(i)

            return id_list
        except:
            print("id wrong")

    @staticmethod
    def upgrade_score(db, cur, e):
        sql_score = e.sql_score()
        try:
            cur.execute(sql_score)
            db.commit()
        except:
            print("update score wrong")
            print(sql_score)
            # print(sql2)

    @staticmethod
    def upgrade_collect(db, cur, e):
        sql_score = e.sql()
        try:
            cur.execute(sql_score)
            db.commit()
        except:
            print("update collect wrong")
            print(sql_score)
            # print(sql2)


if __name__ == "__main__":
    db = globe.db
    cur = db.cursor()
    l = utils.get_sql(db, cur)
