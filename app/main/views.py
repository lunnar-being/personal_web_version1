# -*- coding: utf-8 -*-

"""
@author: caf
@file: views.py
@version: 1.0
@time: 2021/1/31 15:58:12
@contact: chaf@pku.edu.cn

views
"""
import json
import time
import re
from collections import Counter
from datetime import datetime, timedelta

from flask import (render_template, redirect, request, send_file, url_for, flash)
from flask_login import login_required, current_user
from sqlalchemy import desc, text, func, or_, and_
import shutil
from app import db, logging, Config
from app.models import PolicyText, User, Permissions, News, Event, Statistic, Collect
from app.decorators import permission_required
from app.main import main
from config import Config
from util import get_md5_str, FileName, get_file, export_excel, export_excel2, advanced_trans, Stack
# from utils import export_excel2
import os

logger = logging.getLogger('main view')
logger.setLevel(logging.DEBUG)


# 主页
@main.route('/', methods=['GET', 'POST'])
@main.route('/index.html', methods=['GET', 'POST'])
@login_required
@permission_required(Permissions.READ)
def index():
    """
    主页
    /index.html?page=2
    Returns:
        分页模块
    """
    PER_PAGE = 10
    page = request.args.get('page', 1, int)

    filter_args = []

    # 排序
    order = request.args.get('order', 'rank', str)
    logger.info(f'received order: {order}')

    # 领域分类
    field = request.args.get('field', 'All', str)
    # print(field)
    logger.info(f'received source field: {field}')
    if field != 'All':
        # filter_args.append(func.json_contains(PolicyText.norm_field, f'"{field}"') == 1)
        filter_args.append(PolicyText.source_classification == field)
        # filter_args.append(PolicyText.field_sub == field)
    # print('dad',filter_args)
    # 文档类型  todo file_type or doc_type
    doc_type = request.args.get('file_type', '全部文档类型', str)
    logger.info(f'received dic_type: {doc_type}')
    if doc_type != '全部文档类型':
        filter_args.append(PolicyText.topic_classification == doc_type)

    # 国家
    country = request.args.get('country', '全部国家', str)
    logger.info(f'received country: {country}')
    if country != '全部国家':
        filter_args.append(PolicyText.nation == country)

    # 机构
    # institute = request.args.get('institute', 'all', type=str)
    # logger.info(f'received institute: {institute}')
    # if institute != 'all':
    #     filter_args.append(PolicyText.institution == institute)

    # handle order
    if order == 'rank':
        rank_entity = PolicyText.score
    elif order == 'star':
        rank_entity = PolicyText.recommend
    else:
        rank_entity = PolicyText.time

    policy_text_pagination = PolicyText.query.filter(*filter_args).order_by(desc(rank_entity)).paginate(page=page,
                                                                                                        per_page=PER_PAGE)

    policy_text_list = policy_text_pagination.items
    i=page*10+1-10
    for policy_text in policy_text_list:
        policy_text.id2 = i
        i+=1
        if not policy_text.recommend:
            policy_text.recommend="0"
        else:
            policy_text.recommend = str(policy_text.recommend)
        if policy_text.time:
            policy_text.time = str(policy_text.time)[:-8]
        if not policy_text.abstract:
            policy_text.translated_abstract = '该政策无摘要'

    field_list = PolicyText.query.with_entities(PolicyText.source_classification).filter(PolicyText.source_classification != None)
    # field_list = list()
    # for field_tuple in field_tuple_list:
    #     field_list.extend(field_tuple)
    # print('22122',field_list)
    field_list = [f[0] for f in field_list]
    # print(field_list)
    filed_count = dict(Counter(field_list))
    filed_count['All'] = sum(filed_count.values())
    type_list = PolicyText.query.with_entities(PolicyText.topic_classification).filter(
        PolicyText.topic_classification != None)
    type_list = [f[0] for f in type_list]
    # print(field_list)
    type_count = dict(Counter(type_list))
    type_count['全部文档类型'] = sum(type_count.values())
    # country_list = PolicyText.query.with_entities(PolicyText.nation).filter(PolicyText.use, PolicyText.correct_field != None)
    # country_list = [c[0] for c in country_list]
    # country_list = list(set(country_list))
    # print(policy_text_list)
    username = current_user.username
    user = User.query.filter_by(username=username).first()
    #处理收藏显示
    favors = user.favor
    favor_list = list(map(int,favors.split(',')))
    favor_policy = []
    policy_favor_dict = dict()
    policies = [i.id for i in policy_text_list]
    for p in policies:
        policy_favor_dict[p] = 0
    for f in favor_list:
        policy_favor_dict[f] = 1
    def inherit(policy,favor_flag):
        policy.favor = favor_flag
        return policy
        # class Policy(policy):
        #     def __init__(self,favor):
        #         self.favor = favor
        # policy_class = Policy()
        # return policy_class(favor_flag)
    policy_text_list2 = []
    for policy in policy_text_list:
        item = inherit(policy, policy_favor_dict[policy.id])
        # print(item.favor)
        policy_text_list2.append(item)
    return render_template('index.html',
                           policy_text_list = policy_text_list2,
                           # policy_text_nofavor=policy_text_nofavor,
                           # policy_text_favor = favor_policy,
                           pagination=policy_text_pagination,
                           filter={'order': order, 'field': field, 'file_type': doc_type,'country':country},
                           filed_count_dict=filed_count,
                           type_count_dict=type_count,
                           country_list = ["全部国家",'美国','英国',"日本","加拿大"]
                           )


# 我的收藏
@main.route('/', methods=['GET', 'POST'])
@main.route('/my_favor.html', methods=['GET', 'POST'])
@login_required
@permission_required(Permissions.READ)
def my_favor():
    PER_PAGE = 10
    page = request.args.get('page', 1, int)

    filter_args = []
    username = current_user.username
    user = User.query.filter_by(username=username).first()
    # 处理收藏显示
    favors = user.favor
    favor_list = list(map(int, favors.split(',')))
    filter_args.append(PolicyText.id.in_(favor_list))
    policy_text_pagination = PolicyText.query.filter(*filter_args).paginate(page=page,
                                                                                per_page=PER_PAGE)

    policy_text_list = policy_text_pagination.items
    i=page*10+1-10
    for policy_text in policy_text_list:
        policy_text.id2 = i
        i+=1
        if not policy_text.recommend:
            policy_text.recommend="0"
        else:
            policy_text.recommend = str(policy_text.recommend)
        if policy_text.time:
            policy_text.time = str(policy_text.time)[:-8]
        if not policy_text.abstract:
            policy_text.translated_abstract = '该政策无摘要'
    favor_policy = []
    policy_favor_dict = dict()
    policies = [i.id for i in policy_text_list]
    for p in policies:
        policy_favor_dict[p] = 0
    for f in favor_list:
        policy_favor_dict[f] = 1
    def inherit(policy,favor_flag):
        policy.favor = favor_flag
        return policy
        # class Policy(policy):
        #     def __init__(self,favor):
        #         self.favor = favor
        # policy_class = Policy()
        # return policy_class(favor_flag)
    policy_text_list2 = []
    for policy in policy_text_list:
        item = inherit(policy, policy_favor_dict[policy.id])
        if item.favor:
            policy_text_list2.append(item)
    return render_template('my_favor.html',
                           policy_text_list = policy_text_list2,
                           # policy_text_nofavor=policy_text_nofavor,
                           # policy_text_favor = favor_policy,
                           pagination=policy_text_pagination
                           )

# 文章详情页面
@main.route('/article.html', methods=['GET', 'POST'])
@login_required
@permission_required(Permissions.READ)
def article():
    policy_text_id = int(request.args.get('id', '', str))
    policy_text = PolicyText.query.get(policy_text_id)  # type: PolicyText
    # keywords = [', '.join(eval(i.keywords)) for i in policy_text]
    if policy_text.keywords:
        policy_text.keywords = ', '.join(eval(policy_text.keywords))
    original_file = PolicyText.query.get(policy_text.original_file)  # type: File
    format_file = PolicyText.query.get(policy_text.format_file)  # type: File
    trans_file = PolicyText.query.get(policy_text.translated_file) if policy_text.translated_file else None
    checked_file = PolicyText.query.get(policy_text.checked_file) if policy_text.checked_file else None
    return render_template('article.html',
                           policy_text=policy_text,
                           original_file=original_file,
                           format_file=format_file,
                           trans_file=trans_file,
                           checked_file=checked_file)


# 检索结果
@main.route('/search.html', methods=['GET','POST'])
@login_required
@permission_required(Permissions.READ)
def search():
    i=0
    query_list = []
    type_list = []
    bool_list = []
    args = dict(request.args)
    keys = args.keys()
    for i in keys:
        if i.startswith("query-type"):
            type_list.append(args[i])
        elif i.startswith("query-bool"):
            bool_list.append(args[i])
        elif i.startswith("query"):
            query_list.append(args[i])
    box_num = len(query_list)
    #获取所有的检索词和布尔逻辑符等
    # while True:
    #     if i>0:
    #         try:
    #             query = request.args.get('query-' + str(i))
    #             if not query:
    #                break
    #             query_list.append(query)
    #             type_list.append(request.args.get('query-type-' + str(i)))
    #             bool_list.append(request.args.get('query-bool-' + str(i)))
    #             i += 1
    #         except:
    #             break
    #     else:
    #         query_list.append(request.args.get('query'))
    #         type_list.append(request.args.get('query-type'))
    #         # bool_list.append(request.args.get('query-bool'))
    #         i += 1
    # box_num = i
    PER_PAGE = 10
    logger = logging.getLogger('search')
    page = request.args.get('page', 1, int)
    filter_args = [PolicyText.id==000]
    policy_text_pagination = None
    policy_text_pagination = PolicyText.query.filter(*filter_args).paginate(
        page=page,
        per_page=PER_PAGE)
    filter_args=[]
    # 排序
    order = request.args.get('order', 'rank', str)
    logger.info(f'received order: {order}')

    if order == 'rank':  # handle order
        rank_entity = PolicyText.score
    elif order == 'star':
        rank_entity = PolicyText.recommend
    else:
        rank_entity = PolicyText.time

    # 检索类型

    logger.info(f'received query type: {type_list}')

    # 检索词
    # query_word = request.args.get('query')
    logger.info(f'received query word: {query_list}')
    # if query_type == 'abstract':
    #     filter_args.append(PolicyText.translated_abstract.match(query_word))
    # elif query_type == 'keyword':
    #     filter_args.append(PolicyText.translated_keywords.match(query_word))
    # else:
    #     filter_args.append(PolicyText.title.match(query_word))
    # 筛选
    # query_country = request.args.get('country', '全部国家', str)
    # logger.info(f'received query country: {query_country}')
    # if query_country != '全部国家':
    #     filter_args.append(PolicyText.nation == query_country)
    #分类的筛选条件
    query_field = request.args.get('field', '全部分类', str)
    logger.info(f'received query field: {query_field}')
    if query_field != '全部分类':
        # filter_args.append(func.json_contains(PolicyText.norm_field, f'"{query_field}"') == 1)
        filter_args.append(PolicyText.field_main == query_field)

    def construct_query(x, query_type):
        filter_args_temp = filter_args.copy()
        if query_type == '摘要':
            filter_args_temp.append(PolicyText.translated_abstract.like(f"%{x}%"))
            policy_text_filter = PolicyText.query.filter(*filter_args_temp)
            items = policy_text_filter.all()
            ids = [i.id for i in items]
            return set(ids)

        elif query_type == '关键词':
            filter_args_temp.append(PolicyText.translated_keywords.like(f"%{x}%"))
            policy_text_filter = PolicyText.query.filter(*filter_args_temp)
            items = policy_text_filter.all()
            ids = [i.id for i in items]
            return set(ids)
        else:
            filter_args_temp.append(PolicyText.translated_title.like(f"%{x}%"))
            policy_text_filter = PolicyText.query.filter(*filter_args_temp)
            items = policy_text_filter.all()
            ids = [i.id for i in items]
            return set(ids)
    # def polishcal(i):
    #     ope = ['+', '-', '*']
    #     s = advanced_trans(i).split()
    #     stack = Stack()
    #     for x in s:
    #         if (x in ope) == False:
    #             a = construct_query(x,query_type)
    #             stack.push(a)
    #         elif x == "+":
    #             a = stack.pop()
    #             b = stack.pop()
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
    policy_text_list = []

    if query_list:
        # if 'NOT' in query_word or "AND" in query_word or "OR" in query_word:
        if box_num>1:
            filter_args = []
            ids_list = []
            for i in range(box_num):
                # ids = polishcal(query_word)
                ids = construct_query(query_list[i],query_type=type_list[i])
                ids_list.append(ids)
            ids_list_reverse = ids_list
            i = 0 #循环bool检索逻辑符
            while len(ids_list_reverse) > 1:
                ids1 = ids_list_reverse.pop()
                ids2 = ids_list_reverse.pop()
                if bool_list[i] == 'AND':
                    ids_list_reverse.append(ids1 & ids2)
                elif bool_list[i] == 'OR':
                    ids_list_reverse.append(ids1 | ids2)
                elif bool_list[i] == 'NOT':
                    ids_list_reverse.append(ids2 - ids1)
            ids_final = ids_list_reverse[0]
            ids = ids_final
            policy_text_pagination = PolicyText.query.filter(PolicyText.id.in_(ids)).order_by(desc(rank_entity)).paginate(
                page=page,
                per_page=PER_PAGE)
            policy_text_list = policy_text_pagination.items
        elif box_num<=1:
            query_word = query_list[0]
            if type_list[0] == '摘要':
                filter_args.append(PolicyText.translated_abstract.like(f"%{query_word}%"))
            elif type_list[0] == '关键词':
                filter_args.append(PolicyText.translated_keywords.like(f"%{query_word}%"))
            else:
                filter_args.append(PolicyText.translated_title.like(f"%{query_word}%"))
            policy_text_pagination = PolicyText.query.filter(*filter_args).order_by(desc(rank_entity)).paginate(
                page=page,
                per_page=PER_PAGE)
            policy_text_list = policy_text_pagination.items
    # print(policy_text_list)

    i = page * 10 + 1 - 10
    for policy_text in policy_text_list:
        policy_text.id2 = i
        i += 1
        if not policy_text.recommend:
            policy_text.recommend = "0"
        else:
            policy_text.recommend = str(policy_text.recommend)
        if policy_text.time:
            policy_text.time = str(policy_text.time)[:-8]
        if not policy_text.abstract:
            policy_text.translated_abstract = '该政策无摘要'

    # country_list = PolicyText.query.with_entities().filter(PolicyText.field_main != None)
    # country_list = [c[0] for c in country_list]
    # country_list = ['全部国家'] + list(set(country_list))
    filter = dict()
    if query_list:
        filter['query'] = query_list[0]
        filter['query-type'] = type_list[0]
    if box_num>1:
        for i in range(1,box_num):
            filter['query-'+str(i)] = query_list[i]
            filter['query-type-'+str(i)] = type_list[i]
            if i<=box_num-1:
                filter['query-bool-'+str(i)] = bool_list[i-1]
    # print(filter)
    query_word = ""

    if query_list:
        query_word = query_list[0]
    return render_template('search.html',
                           query_word=query_word,
                           query_type=type_list,
                           # query_country=query_country,
                           query_field=query_field,
                           order=order,
                           filter=filter,
                           pagination=policy_text_pagination,
                           policy_text_list=policy_text_list,
                           query_list = query_list,
                           box_num = box_num,
                           query_boolean = bool_list,
                           query_types = type_list,
                           query_length = [i+1 for i in range(box_num-1)]
                           )


# 数据分析
@main.route('/analysis.html', methods=['GET'])
@login_required
@permission_required(Permissions.READ)
def analysis():
    return render_template('analysis.html')


# 用户管理
@main.route('/user_manage.html', methods=['GET'])
@permission_required(Permissions.MANAGE_USER)
def user_manage():
    users = User.query.all()
    ...


# 管理
@main.route('/management.html', methods=['GET', 'POST'])
@login_required
@permission_required(Permissions.MANAGE_CONTENT)
def management():
    policy_text_list = PolicyText.query.limit(10).offset(10).all()
    # print(len(policy_text_list))
    policy_to_origin_file_dict = dict()
    for policy_text in policy_text_list:
        policy_to_origin_file_dict[policy_text.id] = PolicyText.query.get(
            policy_text.original_file)
    return render_template('old/management.html',
                           policy_text_list=policy_text_list,
                           policy_to_origin_file_dict=policy_to_origin_file_dict)


# 采集
@main.route('/collect.html', methods=['GET', 'POST'])
@login_required
@permission_required(Permissions.MANAGE_CONTENT)
def collect():
    collect = Collect
    collect.name = 'user_select'
    record = Collect.query.filter_by(id=9).first()
    # print(record.name)
    # record = Collect.query.get(collect.name)
    # print(record.new_title)
    time_select, day_select = record.new_title.split()

    sql = 'SELECT * FROM collect WHERE id < 9;'
    result = db.session.execute(sql)
    result = [list(row) for row in list(result)]
    result2 = [result[-1]]
    result2+=result[:-1]
    result3 = []
    for i in result2:
        i[1] = str(i[1])
        result3.append(i)
    # all_record = Collect.
    # print(result3)
    data = [
                ('白宫','https://www.whitehouse.gov/','whitehouse'),
                ('英国政府网', 'https://www.gov.uk', 'gov'),
                ('美国能源局', 'https://www.energy.gov/', 'energy'),
                ('麦肯锡公司', 'https://www.mckinsey.com/', 'mckinsey'),
                ('兰德公司', 'https://www.rand.org/', 'rand'),
                ('哈佛大学贝尔福研究中心', 'https://www.belfercenter.org', 'belfercenter'),
                ('众议院军事委员会', 'https://armedservices.house.gov/', 'armedservices'),
                ('美国国防部', 'https://www.defense.gov/', 'defense'),

                ]
    for i in range(8):
        data[i] = list(data[i])
        data[i].append(result3[i][1])
        data[i].append(result3[i][2])
    # print(data)
    return render_template('collect.html', day_select=int(day_select), time_select=int(time_select), result = data)


# 审校
@main.route('/proofread.html', methods=['GET', 'POST'])
@login_required
@permission_required(Permissions.MANAGE_CONTENT)
def proofread():
    PER_PAGE = 10
    logger = logging.getLogger('proofread')
    page = request.args.get('page', 1, int)
    policy_text_pagination = PolicyText.query.filter(PolicyText.use).order_by().paginate(page=page, per_page=PER_PAGE)
    policy_text_list = policy_text_pagination.items
    policy_to_origin_file_dict = {policy_text.id: PolicyText.query.get(policy_text.original_file) for policy_text in
                                  policy_text_list}
    return render_template('proofread.html',
                           policy_text_list=policy_text_list,
                           pagination=policy_text_pagination,
                           policy_to_origin_file_dict=policy_to_origin_file_dict)


# 修改内容
@main.route('/edit-details.html', methods=['GET'])
@login_required
@permission_required(Permissions.READ)
def details():
    policy_text_id = request.args.get('id', type=int)
    policy_text = PolicyText.query.get(policy_text_id)  # type: PolicyText
    original_file = PolicyText.query.get(policy_text.original_file)  # type: File
    format_file = PolicyText.query.get(
        policy_text.format_file) if policy_text.format_file else None
    trans_file = PolicyText.query.get(
        policy_text.translated_file) if policy_text.translated_file else None
    checked_file = PolicyText.query.get(
        policy_text.checked_file) if policy_text.checked_file else None
    return render_template('edit-details.html',
                           policy_text=policy_text,
                           original_file=original_file,
                           format_file=format_file,
                           trans_file=trans_file,
                           checked_file=checked_file)


# 用户
@main.route('/users.html', methods=['GET', 'POST'])
@login_required
@permission_required(Permissions.MANAGE_USER)
def users():
    users_info = User.query.order_by(User.role_id).all()
    return render_template('users.html', users_info=users_info)


# 导入
@main.route('/add-policy.html', methods=['GET', 'POST'])
@login_required
@permission_required(Permissions.MANAGE_CONTENT)
def add_policy():
    return render_template('add-policy.html')


# 新闻动态
@main.route('/', methods=['GET', 'POST'])
@main.route('/news.html', methods=['GET', 'POST'])
@login_required
@permission_required(Permissions.READ)
def news():
    """
    新闻动态
    /news.html?week=2
    Returns:
        当周的新闻
    """
    week = request.args.get('week', 1, int)

    date = News.query.with_entities(News.time).order_by(desc('time')).group_by('time').offset(week-1).first()[0]
    news_list = News.query.filter_by(time=date).all()

    this_week_news_list = []
    last_week_news_list = []
    for news in news_list:
        if news.period_sign == 'ahead':
            this_week_news_list.append(news)
        elif news.period_sign == 'missed':
            last_week_news_list.append(news)

    week_start = date.strftime('%Y-%m-%d')
    end_date = date + timedelta(days=6)
    week_end = end_date.strftime('%Y-%m-%d')

    return render_template('news.html',
                           this_week_news_list=this_week_news_list,
                           last_week_news_list=last_week_news_list,
                           week_start=week_start,
                           week_end=week_end,
                           week=week)


# 重要事件
@main.route('/', methods=['GET', 'POST'])
@main.route('/events.html', methods=['GET', 'POST'])
@login_required
@permission_required(Permissions.READ)
def events():
    """
    重要事件
    /events.html?page=2
    Returns:
        分页模块
    """
    PER_PAGE = 10
    page = request.args.get('page', 1, int)

    events_pagination = Event.query.order_by(desc('date')).paginate(page=page, per_page=PER_PAGE)

    events_list = events_pagination.items
    for event in events_list:
        event.date = event.date.strftime('%Y-%m-%d')

    return render_template('events.html',
                           pagination=events_pagination,
                           events_list=events_list)


# 新闻时间线
import pymysql

@main.route('/search_topic',methods = ['POST','GET'])
@login_required
@permission_required(Permissions.READ)
def search_topic():
    query = request.args.get('query', '', str)
    logger.info(f'received query word: {query}')
    # query = request.form['input_search_topic']
    conn = pymysql.connect(host='81.70.102.186', user='root', password='YDH@henniu123', db='spider', charset='utf8')
    cur = conn.cursor()
    sql = "SELECT `id`,`object`, `trigger`, `subject`, `normal_time`,`organization`,`policy`,`translated_content`,`organization_class`,`policy_class` FROM news WHERE object LIKE '%" + query + "%' OR subject LIKE '%" + query + "%' OR translated_content LIKE '%" + query + "%' ORDER BY `normal_time` desc"
    cur.execute(sql)
    result = cur.fetchall()
    conn.close()
    return(render_template('timeline2.html',result = result))


@main.route('/timeline.html', methods=['GET'])
@login_required
@permission_required(Permissions.READ)
def timeline():
    PER_PAGE = 10
    logger = logging.getLogger('timeline')
    page = request.args.get('page', 1, int)

    # 检索词
    query_word = request.args.get('query', '', str)
    logger.info(f'received query word: {query_word}')
    import pymysql
    query = query_word
    conn = pymysql.connect(host='81.70.102.186', user='root', password='YDH@henniu123', db='spider', charset='utf8')
    cur = conn.cursor()
    sql = "SELECT `id`,`object`, `trigger`, `subject`, `normal_time`,`organization`,`policy`,`translated_content`,`organization_class`,`policy_class` FROM news WHERE object LIKE '%" + query + "%' OR subject LIKE '%" + query + "%' OR translated_content LIKE '%" + query + "%' ORDER BY `normal_time` desc"
    if query:
        cur.execute(sql)
        result = cur.fetchall()
        conn.close()
    else:
        result = []
    return render_template('timeline2.html',
                           query_word=query_word,
                           result = result,
                           filter={'query' : query_word})

#默认的显示数量
entity_num = 10
institute_num = 10
link_num = 10
kw_num = 10
import os
# pwd = os.path.dirname(os.getcwd())


@main.route('/', methods=['GET', 'POST'])
@main.route('/aip_monitor.html', methods=['GET', 'POST'])
@login_required
@permission_required(Permissions.READ)
def aip_monitor():
    global entity_num
    entity2 = get_file('entity')[:entity_num]
    return render_template('aip_monitor.html', entity=entity2, entity_num=entity_num)


@main.route('/', methods=['GET', 'POST'])
@main.route('/aip_institute.html', methods=['GET', 'POST'])
@login_required
@permission_required(Permissions.READ)
def aip_institute():
    institute2 = get_file('institute')[:institute_num]
    return render_template('aip_institute.html', institute=institute2, institute_num=institute_num)


@main.route('/', methods=['GET', 'POST'])
@main.route('/aip_link.html', methods=['GET', 'POST'])
@login_required
@permission_required(Permissions.READ)
def aip_link():
    superlink2 = get_file('link')[:link_num]
    return render_template('aip_link.html', superlink=superlink2, link_num=link_num)


@main.route('/', methods=['GET', 'POST'])
@main.route('/china_topic.html', methods=['GET', 'POST'])
@login_required
@permission_required(Permissions.READ)
def china_topic():
    PER_PAGE = 10
    page = request.args.get('page', 1, int)

    filter_args = []

    # 排序
    order = request.args.get('order', 'rank', str)
    logger.info(f'received order: {order}')

    # 领域分类
    field = request.args.get('field', 'All', str)
    # print(field)
    logger.info(f'received source field: {field}')
    if field != 'All':
        # filter_args.append(func.json_contains(PolicyText.norm_field, f'"{field}"') == 1)
        filter_args.append(PolicyText.field_main == field)
        # filter_args.append(PolicyText.field_sub == field)
    # print('dad',filter_args)
    # 文档类型  todo file_type or doc_type
    # doc_type = request.args.get('file_type', '全部文档类型', str)
    # logger.info(f'received dic_type: {doc_type}')
    # if doc_type != '全部文档类型':
    #     filter_args.append(PolicyText.doc_type == doc_type)

    # 国家
    # country = request.args.get('country', '全部国家', str)
    # logger.info(f'received country: {country}')
    # if country != '全部国家':
    #     filter_args.append(PolicyText.nation == country)

    # 机构
    # institute = request.args.get('institute', 'all', type=str)
    # logger.info(f'received institute: {institute}')
    # if institute != 'all':
    #     filter_args.append(PolicyText.institution == institute)

    # handle order
    if order == 'rank':
        rank_entity = PolicyText.CHN
    elif order == 'star':
        rank_entity = PolicyText.recommend
    else:
        rank_entity = PolicyText.time
    filter_args.append(PolicyText.CHN>0)
    policy_text_pagination = PolicyText.query.filter(*filter_args).order_by(desc(rank_entity)).paginate(page=page,
                                                                                                        per_page=PER_PAGE)

    policy_text_list = policy_text_pagination.items
    policy_text_list_temp = []
    i = page * 10 + 1 - 10
    for policy_text in policy_text_list:
        policy_text.id2 = i
        i += 1
        if not policy_text.recommend:
            policy_text.recommend = "0"
        else:
            policy_text.recommend = str(policy_text.recommend)
        if policy_text.time:
            policy_text.time = str(policy_text.time)[:-8]
        if not policy_text.abstract:
            policy_text.translated_abstract = '该政策无摘要'
    for policy_text in policy_text_list:
        if policy_text.CHN > 0:
            # print()
            policy_text_list_temp.append(policy_text)
    policy_text_list = policy_text_list_temp
    filter_args2 = []
    filter_args2.append(PolicyText.CHN > 0)
    field_list = PolicyText.query.filter(*filter_args2).with_entities(PolicyText.field_main).filter(
        PolicyText.field_main != None)
    # field_list = list()
    # for field_tuple in field_tuple_list:
    #     field_list.extend(field_tuple)
    # print('22122',field_list)
    field_list = [f[0] for f in field_list]
    # print(field_list)
    filed_count = dict(Counter(field_list))
    filed_count['All'] = sum(filed_count.values())

    # country_list = PolicyText.query.with_entities(PolicyText.nation).filter(PolicyText.use, PolicyText.correct_field != None)
    # country_list = [c[0] for c in country_list]
    # country_list = list(set(country_list))
    # print(policy_text_list)
    username = current_user.username
    user = User.query.filter_by(username=username).first()
    # 处理收藏显示
    favors = user.favor
    favor_list = list(map(int, favors.split(',')))
    favor_policy = []
    policy_favor_dict = dict()
    policies = [i.id for i in policy_text_list]
    for p in policies:
        policy_favor_dict[p] = 0
    for f in favor_list:
        policy_favor_dict[f] = 1

    def inherit(policy, favor_flag):
        policy.favor = favor_flag
        return policy
        # class Policy(policy):
        #     def __init__(self,favor):
        #         self.favor = favor
        # policy_class = Policy()
        # return policy_class(favor_flag)

    policy_text_list2 = []
    for policy in policy_text_list:
        item = inherit(policy, policy_favor_dict[policy.id])
        # print(item.favor)
        policy_text_list2.append(item)
    return render_template('china_topic.html',
                           policy_text_list=policy_text_list2,
                           pagination=policy_text_pagination,
                           filter={'order': order, 'field': field},
                           filed_count_dict=filed_count,
                           )

#引入统计工具
from util import get_statistic


@main.route('/', methods=['GET', 'POST'])
@main.route('/analysis_keywords.html', methods=['GET', 'POST'])
@login_required
@permission_required(Permissions.READ)
def tech_keywords():
    keywords = get_statistic(Statistic, 'keywords', kw_num)
    return render_template('analysis_keywords.html', keywords=keywords, kw_num=kw_num)


# --------------------------------以下是api-------------------------------- #
# todo 迁移到api的blueprint

@main.route('/aip_monitor_entity', methods=['POST'])
@login_required
def get_AIPentity_num():
    global entity_num
    num = request.form.get('num')
    num = int(num)
    if 0<num and num<=100:
        entity_num = num
        # print(num)
        # render_template('aip_monitor.html',entity = entity2[:num])
        return json.dumps({'status':"ok"}), 200
    else:
        return "wrong number"


@main.route('/aip_monitor_ins', methods=['POST'])
@login_required
def get_AIPins_num():
    global institute_num
    num = request.form.get('num')
    num = int(num)
    if 0<num and num<=100:
        institute_num = num
        return json.dumps({'status':"ok"}), 200
    else:
        return "wrong number"


@main.route('/aip_monitor_link', methods=['POST'])
@login_required
def get_AIPlink_num():
    global link_num
    num = request.form.get('num')
    num = int(num)
    if 0<num and num<=100:
        link_num = num
        return json.dumps({'status':"ok"}), 200
    else:
        return "wrong number"


@main.route('/ana_keyword', methods=['POST'])
@login_required
def get_keyword_num():
    global kw_num
    num = request.form.get('num')
    num = int(num)
    # print(num)
    if 0<num and num<=100:
        kw_num = num
        return json.dumps({'status':"ok"}), 200
    else:
        return "wrong number"


@main.route('/export_keyword', methods=['GET'])
@login_required
def export_keyword():
    num = int(request.args.get('num'))
    if num>0 and num<=100:
        entity_num = num
        res = export_excel2(Statistic, 'keyword', num)
        return res
    else:
        return "导出失败"

@main.route('/export_entity', methods=['GET'])
@login_required
def export_entity():
    num = int(request.args.get('num'))
    if num>0 and num<=100:
        entity_num = num
        res = export_excel(entity_num, 'entity')
        return res
    else:
        return "导出失败"


@main.route('/export_ins', methods=['GET'])
@login_required
def export_ins():
    num = int(request.args.get('num'))
    if num>0 and num<=100:
        entity_num = num
        res = export_excel(entity_num, 'ins')
        return res
    else:
        return "导出失败"

@main.route('/export_link', methods=['GET'])
@login_required
def export_link():
    num = int(request.args.get('num'))
    if num>0 and num<=100:
        entity_num = num
        res = export_excel(entity_num, 'link')
        return res
    else:
        return "导出失败"

from aiospider.main import spider_pipline
a = spider_pipline()


@main.route('/collect_web', methods=['POST'])
@login_required
def collect_web():
    site_name = request.form.get('site_name')
    print(site_name)
    filter_args = []
    filter_args.append(Collect.name == site_name)
    res = Collect.query.filter(*filter_args)
    a.spider(site_name)
    # print(res)
    # record = res[0]
    # print(record.name)
    return f'{site_name}采集完毕!'


@main.route('/select_day', methods=['POST'])
@login_required
def select_day():
    day = request.form.get('day')
    record = Collect.query.filter_by(id=9).first()
    time_select, day_select = record.new_title.split()
    record.new_title = time_select + ' '+str(day)
    db.session.commit()
    return 'ok'


@main.route('/select_time', methods=['POST'])
@login_required
def select_time():
    time = request.form.get('time')
    record = Collect.query.filter_by(id=9).first()
    time_select, day_select = record.new_title.split()
    record.new_title = str(time) + ' ' + day_select
    db.session.commit()
    return 'ok'

#收藏功能
@main.route('/favor_operate', methods=['POST'])
@login_required
def favor_operate():
    favor = request.form.get('favor')
    id = request.form.get('id')
    if id[0] == 'n':
        id = id[15:]
    elif id[0] == 'f':
        id = id[11:]
    else:
        return "error"
    # print(id)
    username = current_user.username
    user = User.query.filter_by(username=username).first()
    # 处理收藏显示
    favors = user.favor
    favor_list = list(map(int, favors.split(',')))
    favor_list = list(set(favor_list))
    # print(favor)
    if favor=='1':
        favor_list.append(id)
    else:
        # try:
        index = favor_list.index(int(id))
        # print(index)
        favor_list.pop(index)
        # except:
        #     pass
    user.favor = ",".join(map(str, favor_list))
    db.session.commit()
    return 'ok',200


#打分功能
@main.route('/rate_star', methods=['POST'])
@login_required
def rate_star():
    # global time_select
    star = request.form.get('star')
    id = request.form.get('id')
    id = int(id[7:])
    # print(id)
    record = PolicyText.query.filter_by(id=id).first()
    record.recommend = float(star)
    db.session.commit()
    # print(star)

    # time_select = time
    return 'ok'

#计算关键词出现次数
from collections import Counter
def keywords_number(li,num_get):
    count = dict(Counter(li))
    items = list(count.items())
    items.sort(key = lambda x: x[1])
    items = items[::-1]
    res = items[:num_get]
    res_2 = []
    for i in res:
        res_2.append({'name':i[0], 'value':i[1]})
    # print(res_2)
    return res_2


@main.route('/analysis_data', methods=['POST'])
@login_required
def get_analysis_data():
    chart = request.form.get('chart')
    if chart == 'country-year':
        sql = 'SELECT YEAR(release_time), nation, COUNT(nation) FROM policy_text WHERE `rank` > 6.7 GROUP BY YEAR(release_time), nation;'
        result = db.session.execute(sql)
        result = [list(row) for row in list(result)]
    elif chart == 'china-field':
        sql = 'SELECT count(*), YEAR(time), MONTH(time), field_main FROM t1 WHERE (`CHN` > 0 AND YEAR(time) > 2019 AND YEAR(time) < 2022) GROUP BY YEAR(time), MONTH(time), field_main  ;'
        res = db.session.execute(sql)
        res = [list(row) for row in list(res)]
        fields = list(set([i[3] for i in res if i[3] and i[3]!='其他']))
        res.sort(key = lambda x:(x[1],x[2]))
        #按照季度分类汇总
        quaters = [[] for _ in range(8)]
        for i in res:
            if i[1] == 2020:
                quaters[(i[2]-1) // 3].append(i)
            else:
                quaters[((i[2]-1) // 3) + 4].append(i)
        res2 = []
        for quater in quaters:
            fields_num = [0 for _ in range(len(fields))]
            for i in quater:
                for j in range(len(fields)):
                    if i[3] == fields[j]:
                        fields_num[j]+=i[0]
                        break
            res2.append(fields_num)
        total_num = [sum(i) for i in res2]
        # print(len(total_num))
        fields_res = [[i[j] for i in res2] for j in range(10)]
        result = [fields, fields_res, total_num]

    elif chart == 'china-num':
        sql = 'SELECT count(*),YEAR(time), MONTH(time) as m FROM t1 WHERE (`CHN` > 0 AND YEAR(time) > 2019 AND YEAR(time) < 2022) GROUP BY YEAR(time), MONTH(time)  ;'
        res = db.session.execute(sql)
        res = [list(row) for row in list(res)]
        # print(res)
        res.sort(key = lambda x:(x[1],x[2]))
        # print(res)
        num = [i[0] for i in res]
        time = ['.'.join([str(i[1]),str(i[2])]) for i in res]
        result = [num,time]
    elif chart == 'institution-num':
        sql = 'SELECT count(*),translated_institution, MONTH(time) FROM t1 WHERE (`CHN` > 0 AND YEAR(time) > 2020 AND MONTH(time) > 4) GROUP BY MONTH(time), translated_institution;'
        res = db.session.execute(sql)
        res = [list(row) for row in list(res)]
        # print(res)
        institutions = list(set([i[1] for i in res if i[1]]))
        insti_num = [[0 for _ in range(8)] for _ in range(len(institutions))]
        # print(institutions)
        for i in res:
            if i[1]:
                j = institutions.index(i[1])
                insti_num[j][i[2]-5] = i[0]
        institutions_mt2 = []
        institute_num_res = []
        for i in range(len(institutions)):
            if sum(insti_num[i])>=3:
                institutions_mt2.append(institutions[i])
                institute_num_res.append(insti_num[i])
        # print(institutions_mt2)
        # print(institute_num_res)
        result = [institutions_mt2, institute_num_res]
    elif chart == 'china-keyword-cloud':
        sql = 'SELECT translated_keywords FROM t1 WHERE `CHN` > 0;'
        result = db.session.execute(sql)
        result = [list(row) for row in list(result) if row.translated_keywords]
        result_processed = []
        # print(result[0])
        for row in result:
            k = row[0].replace('、',',')
            k2 = k.replace('“',"'")
            k3 = k2.replace('”', "'")
            k4 = k3.replace('’', "'")
            k5 = k4.replace('‘', "'")
            k6 = k5.replace('，',',')
            try:
                keywords = ', '.join(eval(k6))
            except:
                pass
            row = [keywords]
            result_processed.append(row)
        result = result_processed
    elif chart == 'china-keyword-pie':
        sql = 'SELECT keywords, YEAR(time) FROM t1 WHERE `CHN` > 0;'
        result = db.session.execute(sql)
        result = [list(row) for row in list(result) if row.keywords]
        result_processed = []
        # print(result[0])
        # print(result)
        years_num = [[],[]]
        for row in result:
            keywords = eval(row[0])
            if row[1] == 2020:
                years_num[0] += keywords
            else:
                years_num[1] += keywords

        res2020 = keywords_number(years_num[0],10)
        res2021 = keywords_number(years_num[1],10)
        # res2020 = [i for i in result if i[0]==2020]
        # res2021 = [i for i in result if i[0] == 2021]
        result = [res2020,res2021]

    elif chart == 'state-message-tree':
        pa = os.path.abspath("app/static/monitor/state_message.txt")
        with open(pa) as f:
            keywords = eval(f.read())
            f.close()
        # print(keywords)
        keywords2 = []
        for i in keywords:
            k = []
            for j in i:
                k.append({'name':j.title(),'value':1})
            keywords2.append(k[:4])
        # print(keywords2)
        result = {
            'name':'国情咨文关键词',
            'children':
                [
                    {
                        'name': '2015',
                        'children': keywords2[0]
                },
                    {
                        'name': '2016',
                        'children': keywords2[1]
                    },
                    {
                        'name': '2017',
                        'children': keywords2[2]
                    },
                    {
                        'name': '2018',
                        'children': keywords2[3]
                    },
                    {
                        'name': '2019',
                        'children': keywords2[4]
                    },
                    {
                        'name': '2020',
                        'children': keywords2[5]
                    }
                ]

        }
    elif chart == 'key-word-cloud':
        sql = 'SELECT translated_keywords FROM t1 WHERE `rank` > 6.7;'
        result = db.session.execute(sql)
        result = [list(row) for row in list(result) if row.keywords]
    elif chart == 'customizedAna':
        type = request.form.get('type')
        domain = request.form.get('domain')
        keyword = request.form.get('keyword')
        print(type)
        if type == "number_change":
            if domain=='All' and keyword=="任意关键词" or keyword == "":
                sql = 'SELECT count(*),YEAR(time), MONTH(time) as m FROM t1 WHERE (YEAR(time) > 2020 AND MONTH(time) > 4) GROUP BY YEAR(time), MONTH(time)  ;'
            elif domain!='All' and keyword=="任意关键词" or keyword == "":
                sql = f'SELECT count(*),YEAR(time), MONTH(time) as m FROM t1 WHERE (YEAR(time) > 2020 AND MONTH(time) > 4 AND `field_main`="{domain}") GROUP BY YEAR(time), MONTH(time)  ;'
            elif domain=='All' and keyword!="任意关键词" and keyword!="":
                sql = f'SELECT count(*),YEAR(time), MONTH(time) as m FROM t1 WHERE (YEAR(time) > 2020 AND MONTH(time) > 4 AND `translated_keywords` LIKE "%{keyword}%" OR `translated_title` LIKE "%{keyword}%") GROUP BY YEAR(time), MONTH(time)  ;'
            elif domain!='All' and keyword!="任意关键词" and keyword!="":
                sql = f'SELECT count(*),YEAR(time), MONTH(time) as m FROM t1 WHERE (YEAR(time) > 2020 AND MONTH(time) > 4 AND `translated_keywords` LIKE "%{keyword}%" OR `translated_title` LIKE "%{keyword}%" AND `field_main`="{domain}") GROUP BY YEAR(time), MONTH(time)  ;'
            res = db.session.execute(sql)
            res = [list(row) for row in list(res) if row[1]]
            print(res)
            res.sort(key=lambda x: (x[1], x[2]))
            print(res)
            num = [i[0] for i in res]
            time = ['.'.join([str(i[1]), str(i[2])]) for i in res]
            result = [num, time]
        elif type == "number_institute":
            if domain == 'All' and keyword == "任意关键词" or keyword == "":
                sql = 'SELECT count(*),translated_institution FROM t1 WHERE (YEAR(time) >= 2020 AND `translated_institution` is not null ) GROUP BY translated_institution;'
            elif domain != 'All' and keyword == "任意关键词" or keyword == "":
                sql = f'SELECT count(*),translated_institution FROM t1 WHERE (YEAR(time) >= 2020 AND `field_main`="{domain}" AND `translated_institution` is not null) GROUP BY translated_institution;'
            elif domain == 'All' and keyword != "任意关键词" and keyword!="":
                sql = f'SELECT count(*),translated_institution FROM t1 WHERE (YEAR(time) >= 2020 AND `translated_institution` is not null AND `translated_keywords` LIKE "%{keyword}%" OR `translated_title` LIKE "%{keyword}%") GROUP BY translated_institution;'
            elif domain != 'All' and keyword != "任意关键词" and keyword!="":
                sql = f'SELECT count(*),translated_institution FROM t1 WHERE (YEAR(time) >= 2020 AND `translated_institution` is not null AND `translated_keywords` LIKE "%{keyword}%" OR `translated_title` LIKE "%{keyword}%" AND `field_main`="{domain}") GROUP BY translated_institution;'

            res = db.session.execute(sql)
            res = [list(row) for row in list(res)]
            # print(res)
            res = [i for i in res if i[0]]
            if len(res)>=10:
                res.sort(key=lambda x:x[0],reverse=True)
                institute_top10 = res[:10]
            else:
                institute_top10 = res
            # print(len(institute_mt10))
            institute_num = [i[0] for i in institute_top10]
            institutes = [i[1] for i in institute_top10]
            # print(institutes)
            # print(institute_num)
            result = [dict([("name",institutes[i]),("value",institute_num[i])]) for i in range(len(institutes)) if institutes[i]]
            # print(result)
    return json.dumps(result)


@main.route('/submit_details', methods=['POST'])
@login_required
def submit_details():
    # get submit data
    logger.info("submit_details called")
    policy_id = request.form.get('id', type=int)
    logger.info(f"submit id get: {policy_id}")
    title = request.form.get('title')
    logger.debug(f"submit title get: {title}")
    institution = request.form.get('institution')
    logger.debug(f"submit institution get: {institution}")
    abstract = request.form.get('abstract')
    logger.debug(f"submit abstract get: {abstract}")
    keywords = request.form.get('keywords')
    logger.debug(f"submit keywords get: {keywords}")
    doc_type = request.form.get('doc_type')
    logger.debug(f"submit doc_type get: {doc_type}")
    field = request.form.get('field')
    logger.debug(f"submit field get: {field}")
    use = True if request.form.get('use') == "1" else False
    logger.debug(f"submit use get: {use}")
    recommend = True if request.form.get('recommend') == "1" else False
    logger.debug(f"submit recommend get: {recommend}")
    logger.info(f"uploaded by user: {current_user.username}")

    # upload
    p = PolicyText.query.get(policy_id)  # type: PolicyText
    p.translated_title = title
    p.translated_abstract = abstract
    p.translated_keywords = keywords
    p.doc_type = doc_type
    p.correct_field = field
    p.use = use
    p.recommend = recommend
    p.modified_by = current_user.username
    try:
        db.session.add(p)
        db.session.commit()
    except Exception as e:
        logger.error(f"Fail to commit | {e}")
        return 'fail', 200
    else:
        logger.debug('edit success')
        return 'success', 200


@main.route('/add_user', methods=['POST'])
@login_required
def add_user():
    username = request.form.get('username')
    password = request.form.get('password')
    role_id = request.form.get('role')
    u = User()
    u.username = username
    u.password = password
    u.role_id = role_id
    db.session.add(u)
    db.session.commit()
    return 'success', 200


@main.route('/del_user', methods=['POST'])
@login_required
def del_user():
    usernames = request.form.get('usernames')
    usernames = usernames.split()
    usernames = ["'" + name + "'" for name in usernames]
    print(usernames)
    sql = "DELETE FROM user WHERE username in ({});".format(", ".join(usernames))
    db.session.execute(sql)
    db.session.commit()
    return 'success', 204


@main.route('/add_one_policy', methods=['POST'])
@login_required
def add_one_policy():
    """
    add new policy manually
    todo there should be more safety check and field examination before save the file
    todo further process need to be launched
    """
    logger.info(f"add_one_policy called")
    logger.debug(f"received form: {request.form}")

    # receive data (handle file)
    uploaded_file = request.files.get('file')
    logger.debug(f"received file: {uploaded_file}")
    # check file validation
    if uploaded_file.mimetype == 'application/pdf':
        extension = 'pdf'
    elif uploaded_file.mimetype == 'text/plain':
        extension = 'txt'
    else:
        return '错误的文件格式', 200

    # receive data (handle text)
    original_title = request.form.get('original-title')
    translated_title = request.form.get('translated-title')
    nation = request.form.get('nation')
    lang = request.form.get('lang')
    source_url = request.form.get('source-url', type=str)  # need more process
    field = request.form.get('field')
    doc_type = request.form.get('doc-type')
    institution = request.form.get('institution')
    keywords = request.form.get('keywords')
    abstract = request.form.get('abstract')

    # generate new policy
    p = PolicyText(original_title=original_title,
                   translated_title=translated_title,
                   nation=nation,
                   language=lang,
                   source_url=source_url,
                   correct_field=field,
                   doc_type=doc_type,
                   institution=institution,
                   translated_abstract=abstract,
                   keywords=keywords,
                   spider_condition=99)  # 99: manual
    p.release_time = datetime.now()

    # generate new file
    file_name = f"origin_{get_md5_str(source_url)}.{extension}"
    f = File(savename=file_name)
    fname = FileName(file_name)
    opath = fname.gen_path(file_type=1)
    uploaded_file.save(opath)
    logger.debug(f"savepath: {opath}")
    db.session.add(f)
    db.session.commit()

    # complete policy
    p.original_file = f.id
    db.session.add(p)
    db.session.commit()
    return '上传成功', 200

import xlrd
@main.route('/add_batch_policy', methods=['POST'])
@login_required
def add_batch_policy():
    zip_path = Config.BASE_DIR
    logger.info(f"add_batch_policy called")
    logger.debug(f"received form: {request.form}")

    # receive data (handle file)
    print(request.files)
    uploaded_file = request.files.get('excel_file')
    zip_file = request.files.get("zip_file")
    logger.debug(f"received file: {uploaded_file}")
    # check file validation
    if uploaded_file.mimetype == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet':
        extension = 'excel'
    else:
        return '错误的文件格式', 200

    if zip_file.mimetype == 'application/x-zip-compressed':
        extension2 = 'zip'
    else:
        return '错误的文件格式', 200
    import zipfile
    target_path_zip = os.path.join(zip_path, r'aiospider\file')
    file_like_obj = zip_file.stream._file
    zipfile_ob = zipfile.ZipFile(file_like_obj)
    file_names = zipfile_ob.namelist()
    for fname in file_names:
        file_path = os.path.join(target_path_zip,fname)
        print(file_path)
        with open(file_path,'wb') as f2:
            f2.write(zipfile_ob.open(fname).read())
        f2.close()
    f = uploaded_file.read()
    data = xlrd.open_workbook(file_contents=f)
    table = data.sheets()[0]
    names = data.sheet_names()  # 返回book中所有工作表的名字
    status = data.sheet_loaded(names[0])  # 检查sheet1是否导入完毕
    nrows = table.nrows  # 获取该sheet中的有效行数
    ncols = table.ncols  # 获取该sheet中的有效列数
    s = table.col_values(0)
    policy_list = []
    for i in range(1,nrows):
        columns = table.row_values(i)
        p = {"title":columns[0],
                       "translated_title":columns[1],
                       "nation":columns[2],
                       "source_url":columns[3],
                       "field_main":columns[4],
                       "topic_classification":columns[5],
                       "institution":columns[6],
                       "time":columns[7],
                       "keywords":columns[8],
                       "abstract":columns[9],
                       "original_file":columns[10]}
        policy_list.append(p)
    db.session.execute(
        PolicyText.__table__.insert(policy_list)
    )
    db.session.commit()
    return '上传成功', 200


