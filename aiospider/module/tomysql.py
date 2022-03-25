import pymysql

"""
author : whg
time : 2021/12/25
"""


# 连接数据库
def connect():
    try:
        db = pymysql.connect(
            host="81.70.102.186",
            port=3306,
            user="root",
            password="YDH@henniu123",
            db='spider',
            charset='utf8'  # 字符编码
        )
        return db
    except Exception:
        raise Exception("连接失败")


# 获取id，文件名（带txt后缀），返回tuple
def get_file_name():
    sql = 'select id,original_file from t1'
    cur = connect().cursor()
    cur.execute(sql)
    data = cur.fetchall()
    # 返回id和file_name
    return data


# 获取id，文件名（带txt后缀），返回tuple
def get_file_field():
    sql = 'select id,original_file,field_main from t1 where field_main is null or field_main=""'
    cur = connect().cursor()
    cur.execute(sql)
    data = cur.fetchall()
    # 返回id和file_name
    return data


# 获取id，文件名（带txt后缀），涉华词频数量
def get_file_CHN():
    sql = 'select id,original_file,CHN,title from t1 where CHN is null'
    cur = connect().cursor()
    cur.execute(sql)
    data = cur.fetchall()
    # 返回id和file_name
    return data


# 获取id，url及其来源分类
def get_file_url():
    sql = 'select id,source_url,source_classification from t1 where source_classification is null or source_classification=""'
    cur = connect().cursor()
    cur.execute(sql)
    data = cur.fetchall()
    # 返回id和file_name
    return data


# 获取id，标题、摘要及主题分类
def get_file_topic():
    sql = 'select id,title,topic_classification,source_url from t1 where topic_classification is null or topic_classification=""'
    cur = connect().cursor()
    cur.execute(sql)
    data = cur.fetchall()
    # 返回id和file_name
    return data


# 获取id对应的摘要
def get_abstract(file_id):
    sql = f"select abstract from t1 where id={file_id}"
    cur = connect().cursor()
    cur.execute(sql)
    data = cur.fetchall()
    # 返回id和file_name
    return data


# 获取id对应的标题
def get_title(file_id):
    sql = f"select title from t1 where id={file_id}"
    cur = connect().cursor()
    cur.execute(sql)
    data = cur.fetchall()
    # 返回id和file_name
    return data


# 更新t1表，id，目标列，更新值
def update_t1(file_id, target_column, update_value):
    sql = f"update t1 SET {target_column}=%s where id=%s"
    mydb = pymysql.connect(
        host="81.70.102.186",
        port=3306,
        user="root",
        password="YDH@henniu123",
        db='spider'
    )
    mycursor = mydb.cursor()
    mycursor.execute(sql, (update_value, file_id))
    mydb.commit()
    print("\r 更新成功:%s" % file_id, end="")
