# -*- coding: utf-8 -*-

"""
@author: Jin.Fish
@file: views.py
@version: 1.0
@time: 2021/04/25 15:58:12
@contact: jinxy@pku.edu.cn

views
"""
import json
import time
from collections import Counter
from datetime import datetime, timedelta

from flask import (render_template, redirect, request, send_file, url_for, flash)
from flask_login import login_required, current_user
from sqlalchemy import desc, text, func
from app import db, logging, Config
from app.models import File, PolicyText, User, Permissions, News, Event
from app.decorators import permission_required
from app.main import main
from util import get_md5_str, FileName, get_file, export_excel
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

    filter_args = [PolicyText.use]

    # 排序
    order = request.args.get('order', 'rank', str)
    logger.info(f'received order: {order}')

    # 领域分类
    field = request.args.get('field', '全部分类', str)
    logger.info(f'received field: {field}')
    if field != '全部分类':
        # filter_args.append(func.json_contains(PolicyText.norm_field, f'"{field}"') == 1)
        filter_args.append(PolicyText.correct_field == field)

    # 文档类型  todo file_type or doc_type
    doc_type = request.args.get('file_type', '全部文档类型', str)
    logger.info(f'received dic_type: {doc_type}')
    if doc_type != '全部文档类型':
        filter_args.append(PolicyText.doc_type == doc_type)

    # 国家
    country = request.args.get('country', '全部国家', str)
    logger.info(f'received country: {country}')
    if country != '全部国家':
        filter_args.append(PolicyText.nation == country)

    # 机构
    institute = request.args.get('institute', 'all', type=str)
    logger.info(f'received institute: {institute}')
    if institute != 'all':
        filter_args.append(PolicyText.institution == institute)

    # handle order
    if order == 'rank':
        rank_entity = PolicyText.rank
    else:
        rank_entity = PolicyText.release_time

    policy_text_pagination = PolicyText.query.filter(*filter_args).order_by(desc(rank_entity)).paginate(page=page,
                                                                                                        per_page=PER_PAGE)

    policy_text_list = policy_text_pagination.items
    for policy_text in policy_text_list:  # type: PolicyText
        # if policy_text.abstract:
        #     policy_text.abstract = bs(policy_text.abstract, 'lxml').text
        # else:
        #     policy_text.abstract = 'Sorry, there is no preview...'
        if not policy_text.translated_abstract:
            policy_text.translated_abstract = '该政策无摘要'

    field_list = PolicyText.query.with_entities(PolicyText.correct_field).filter(PolicyText.use,
                                                                                 PolicyText.correct_field != None)
    # field_list = list()
    # for field_tuple in field_tuple_list:
    #     field_list.extend(field_tuple)
    field_list = [f[0] for f in field_list]
    filed_count = dict(Counter(field_list))
    filed_count['全部分类'] = sum(filed_count.values())

    country_list = PolicyText.query.with_entities(PolicyText.nation).filter(PolicyText.use, PolicyText.correct_field != None)
    country_list = [c[0] for c in country_list]
    country_list = list(set(country_list))

    return render_template('index.html',
                           policy_text_list=policy_text_list,
                           pagination=policy_text_pagination,
                           filter={'order': order, 'field': field, 'file_type': doc_type, 'country': country},
                           filed_count_dict=filed_count,
                           country_list=country_list)


# 文章详情页面
@main.route('/article.html', methods=['GET', 'POST'])
@login_required
@permission_required(Permissions.READ)
def article():
    policy_text_id = int(request.args.get('id'))
    policy_text = PolicyText.query.get(policy_text_id)  # type: PolicyText
    original_file = File.query.get(policy_text.original_file)  # type: File
    format_file = File.query.get(policy_text.format_file)  # type: File
    trans_file = File.query.get(policy_text.translated_file) if policy_text.translated_file else None
    checked_file = File.query.get(policy_text.checked_file) if policy_text.checked_file else None
    return render_template('article.html',
                           policy_text=policy_text,
                           original_file=original_file,
                           format_file=format_file,
                           trans_file=trans_file,
                           checked_file=checked_file)


# 检索结果
@main.route('/search.html', methods=['GET'])
@login_required
@permission_required(Permissions.READ)
def search():
    PER_PAGE = 10
    logger = logging.getLogger('search')
    page = request.args.get('page', 1, int)
    filter_args = [PolicyText.use]

    # 排序
    order = request.args.get('order', 'rank', str)
    logger.info(f'received order: {order}')
    if order == 'rank':  # handle order
        rank_entity = PolicyText.rank
    else:
        rank_entity = PolicyText.release_time

    # 检索类型
    query_type = request.args.get('query-type')
    logger.info(f'received query type: {query_type}')

    # 检索词
    query_word = request.args.get('query')
    logger.info(f'received query word: {query_word}')
    if query_type == 'abstract':
        filter_args.append(PolicyText.translated_abstract.match(query_word))
    elif query_type == 'keyword':
        filter_args.append(PolicyText.translated_keywords.match(query_word))
    else:
        filter_args.append(PolicyText.translated_title.match(query_word))

    # 筛选
    query_country = request.args.get('country', '全部国家', str)
    logger.info(f'received query country: {query_country}')
    if query_country != '全部国家':
        filter_args.append(PolicyText.nation == query_country)

    query_field = request.args.get('field', '全部分类', str)
    logger.info(f'received query field: {query_field}')
    if query_field != '全部分类':
        # filter_args.append(func.json_contains(PolicyText.norm_field, f'"{query_field}"') == 1)
        filter_args.append(PolicyText.correct_field == query_field)

    policy_text_pagination = PolicyText.query.filter(*filter_args).order_by(rank_entity).paginate(page=page,
                                                                                                  per_page=PER_PAGE)

    policy_text_list = policy_text_pagination.items
    for policy_text in policy_text_list:
        if not policy_text.translated_abstract:
            policy_text.translated_abstract = '该政策无摘要'

    country_list = PolicyText.query.with_entities(PolicyText.nation).filter(PolicyText.use,
                                                                            PolicyText.correct_field != None)
    country_list = [c[0] for c in country_list]
    country_list = ['全部国家'] + list(set(country_list))

    return render_template('search.html',
                           query_word=query_word,
                           query_type=query_type,
                           query_country=query_country,
                           query_field=query_field,
                           order=order,
                           filter={'query': query_word, 'query-type': query_type},
                           pagination=policy_text_pagination,
                           policy_text_list=policy_text_list,
                           country_list=country_list)


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
    print(len(policy_text_list))
    policy_to_origin_file_dict = dict()
    for policy_text in policy_text_list:
        policy_to_origin_file_dict[policy_text.id] = File.query.get(
            policy_text.original_file)
    return render_template('old/management.html',
                           policy_text_list=policy_text_list,
                           policy_to_origin_file_dict=policy_to_origin_file_dict)


# 采集
@main.route('/collect.html', methods=['GET', 'POST'])
@login_required
@permission_required(Permissions.MANAGE_CONTENT)
def collect():
    return render_template('collect.html')


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
    policy_to_origin_file_dict = {policy_text.id: File.query.get(policy_text.original_file) for policy_text in
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
    original_file = File.query.get(policy_text.original_file)  # type: File
    format_file = File.query.get(
        policy_text.format_file) if policy_text.format_file else None
    trans_file = File.query.get(
        policy_text.translated_file) if policy_text.translated_file else None
    checked_file = File.query.get(
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

    if query_word:
        news_pagination = News.query.filter(News.time != None, News.translated_title.like('%' + query_word + '%'))\
                .order_by(desc('time')).paginate(page=page, per_page=PER_PAGE)
    else:
        news_pagination = News.query.filter_by(id=-1).paginate(page=page, per_page=PER_PAGE)

    news_list = news_pagination.items
    for news in news_list:
        news.time = news.time.strftime('%Y-%m-%d')

    return render_template('timeline.html',
                           query_word=query_word,
                           pagination=news_pagination,
                           news_list=news_list,
                           filter={'query' : query_word})

#默认的显示数量
entity_num = 10
institute_num = 10
link_num = 10
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
        print(num)
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

@main.route('/analysis_data', methods=['POST'])
@login_required
def get_analysis_data():
    chart = request.form.get('chart')
    if chart == 'country-year':
        sql = 'SELECT YEAR(release_time), nation, COUNT(nation) FROM policy_text WHERE `rank` > 6.7 GROUP BY YEAR(release_time), nation;'
        result = db.session.execute(sql)
        result = [list(row) for row in list(result)]
    elif chart == 'field-year':
        sql = 'SELECT norm_field, YEAR(release_time) FROM policy_text WHERE (`rank` > 6.7 AND YEAR(release_time) > 2011 AND YEAR(release_time) < 2021);'
        res = db.session.execute(sql)
        res = [list(row) for row in list(res)]
        year_count = {}
        for line in res:
            for field in json.loads(line[0]):
                if field != '无类别':
                    if field in year_count:
                        if line[1] in year_count[field]:
                            year_count[field][line[1]] += 1
                        else:
                            year_count[field][line[1]] = 1
                    else:
                        year_count[field] = {line[1]: 1}
        result = []
        for field in year_count:
            for year in year_count[field]:
                result.append([year, year_count[field][year], field])
    elif chart == 'country-field':
        sql = 'SELECT norm_field, nation FROM policy_text WHERE (`rank` > 6.7 AND YEAR(release_time) > 2011 AND YEAR(release_time) < 2021);'
        res = db.session.execute(sql)
        res = [list(row) for row in list(res)]
        nation_count = {}
        for line in res:
            for field in json.loads(line[0]):
                if field != '无类别':
                    if field in nation_count:
                        if line[1] in nation_count[field]:
                            nation_count[field][line[1]] += 1
                        else:
                            nation_count[field][line[1]] = 1
                    else:
                        nation_count[field] = {line[1]: 1}
        result = []
        for field in nation_count:
            for nation in nation_count[field]:
                result.append([nation, field, nation_count[field][nation]])
    elif chart == 'word-cloud':
        sql = 'SELECT tech_word FROM policy_text WHERE `rank` > 6.7;'
        result = db.session.execute(sql)
        result = [list(row) for row in list(result)]
    elif chart == 'key-word-cloud':
        sql = 'SELECT translated_keywords FROM policy_text WHERE `rank` > 6.7;'
        result = db.session.execute(sql)
        result = [list(row) for row in list(result)]
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
