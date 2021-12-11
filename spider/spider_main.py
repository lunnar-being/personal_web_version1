# -*- coding: utf-8 -*-

"""
@author: Jin.Fish
@file: spider.py
@version: 1.0
@time: 2021/04/18 01:39:26
@contact: jinxy@pku.edu.cn

爬虫(检索界面，用于获取链接)

"""

import json
import re
from datetime import timedelta, datetime
from pprint import pprint

import urllib.parse as url_parser
from lxml import etree
import requests_cache
import fake_useragent

from spider import PolicyText, File, logging, format_exc
from download import Downloader
from download_file import save_html_file
from redis_queue import RedisQueue
from disruptive import app

app.app_context().push()
from app import db
logger = logging.getLogger('spider_main')

fake_ua = fake_useragent.UserAgent()  # 设置 useragent
keywords_list = [
    "disruptive technology",
    "disruptive innovation",
    "emerging technology",
    "discontinuous technology",
    "developing technology",
    "advanced technology",
    "integrated technology",
    "future technology",
    "promising technology",
    "next generation technology",
    "evolving technology",
    "radical technology",
    "diffusion of innovation",
    "technology diffusion",
    "national innovation system",
    "enabling technology"
]  # 检索关键词

# 建立缓存, 缓存保存时间设置为3天
requests_cache.install_cache(backend='sqlite', expires=timedelta(days=10))


def extract_page_by_xpath(url, xpath):
    """
    指定一个检索结果页面（链接）
    解析并获取若干条政策链接
    Args:
        url (str):      检索结果页面链接
        xpath (str):    每一条结果的URL对应的XPATH
    """
    downloader = Downloader(delay=3, user_agent=fake_ua['random'])
    html = downloader(url, num_retries=3)
    if not html:
        return
    dom = etree.HTML(html)
    extract_res = dom.xpath(xpath)
    return extract_res


def gen_opeu_tasks():
    """获取【出版物网站】所有政策链接"""
    crawl_queue = RedisQueue(db=1, queue_name='opeu_spider')
    # query_url = 'https://op.europa.eu/en/search-results?p_p_id=eu_europa_publications_portlet_search_executor_SearchExecutorPortlet_INSTANCE_q8EzsBteHybf&p_p_lifecycle=1&p_p_state=normal&queryText={}&facet.collection=EUPub&resultsPerPage=50&SEARCH_TYPE=SIMPLE&startRow={}'
    query_url = 'https://op.europa.eu/en/search-results?p_p_id=eu_europa_publications_portlet_search_executor_SearchExecutorPortlet_INSTANCE_q8EzsBteHybf&p_p_lifecycle=1&p_p_state=normal&queryText={}&facet.studies=&language=en&startRow=1&resultsPerPage=50&keywordOptions=EXACT&SEARCH_TYPE=ADVANCED&startRow={}'
    for query_word in keywords_list:
        logger.info(f'Start Query Keyword: {query_word}')
        item_num = 1
        # 以下用于获取 结果条数，用于翻页
        len_xpath = "//span[@class='results-number-info']/text()"
        url = query_url.format(query_word, item_num)
        len_info = extract_page_by_xpath(
            url=url, xpath=len_xpath)
        logger.info(f'query url: {url}')
        len_re = re.match(r"returned\s*(\d+)\s*results", len_info[0].strip())
        tot_len = int(len_re.group(1))
        logger.info(f'Query Result Len: {tot_len}')

        # 开始遍历
        while item_num < tot_len:
            page_list = extract_page_by_xpath(
                url=query_url.format(query_word, item_num),
                xpath='//a[@class="documentDetailLink"]/@href')
            logger.info(
                f'start_row: {item_num}, {len(page_list)} page_list got')
            crawl_queue.push(page_list)
            item_num += 50


def gen_csis_tasks():
    csis_crawl_queue = RedisQueue(db=1, queue_name='csis_spider')
    query_url = 'https://www.csis.org/search?search_api_views_fulltext={}&sort_by=search_api_relevance&type=publication&page={}'
    for query_word in keywords_list:
        logger.info(f'Start Query Keyword: {query_word}')

        len_info = extract_page_by_xpath(query_url.format(query_word, 0),
                                         "//li[@class='pager__item pager__item--last']//@href")
        len_re = re.search(r'&page=(\d{1,3})', len_info[0])
        tot_len = int(len_re.group(1))
        logger.info(f'Query Result Len: {tot_len}')

        for page_num in range(tot_len + 1):
            page_list = extract_page_by_xpath(
                url=query_url.format(query_word, page_num),
                xpath="//div[@class='teaser__title']//a/@href"
            )
            csis_crawl_queue.push(page_list)
            logger.info(f'Get {len(page_list)} url and pushed into {csis_crawl_queue.name}')


def policy_crawler(queue_name, delay=3, callback=None):
    """
    下载html页面，爬取一条政策
    具体的处理方式取决于输入的callback
    Args:
        queue_name(str): 队列名称
        delay (float): 延迟秒数 (default: 3)
        callback (function): 对下载内容进行处理的回调函数
    """
    crawl_queue = RedisQueue(db=1, queue_name=queue_name)
    downloader = Downloader(delay=delay, user_agent=fake_ua['random'])
    # 不断循环任务队列
    # todo 有个小问题，目前的逻辑是先把任务链接全爬下来，如果以后一边加任务一边执行任务，可能会因为任务断了而结束
    while len(crawl_queue):
        url = crawl_queue.pop()  # type: str
        if not (url.startswith('https://') or url.startswith('http://')):
            url = url_parser.urljoin('https://www.csis.org/', url)
        html = downloader(url, num_retries=3)
        if callback:
            try:
                callback(html, url)
                # crawl_queue.push(url, skip_seen=False)
            except Exception as e:
                logger.error(f'{e}')
                # logger.error(f'{e}:\n{format_exc()}')
                # crawl_queue.push(url, skip_seen=True)
        print()


def test_policy_crawler(url, callback=None):
    """用于测试数据抓取"""
    downloader = Downloader(delay=3, user_agent=fake_ua['random'])
    html = downloader(url, num_retries=3)
    callback(html, url)


def handle_policy_opeu(html, url):
    """
    处理欧盟出版物
    todo 语言和链接很难处理，目前统统drop掉
    Args:
        html (str):
        url (str):
    Returns:
        db input
    """
    logger = logging.getLogger('handle op_europa_eu policy')

    def strip_list(ele_list):
        """用来处理xpath抓取结果"""
        return [ele.strip() for ele in ele_list if ele]

    # 定义一堆xpath
    xpath_dict = {
        'publish_time': "//time[@itemprop='datePublished']/text()",
        'author': "//li[@class='list-item last']//a/text()",
        'themes': "//li[@class='list-item list-item-themes']//a[1]/text()",
        'keywords': "//li[contains(@class,'list-item last list-item-subject')]/a/text()",
        'file_url': "//a[@data-format='pdf']/@data-uri",
        'description': "//div[@itemprop='description']//span/text()",
        'bread': "//ol[@class='breadcrumb']/li//span/text()",
        'title': "//h1[@class='main-publication-title']/text()"
    }

    dom = etree.HTML(html)

    if PolicyText.query.filter(PolicyText.source_url == url).first():
        logger.warning(f'duplication, aborted: {url}')
        return

    policy_text = PolicyText()
    policy_text.site = 'op.europa.eu'
    policy_text.source_url = url
    policy_text.nation = '欧盟'
    policy_text.release_time = dom.xpath(xpath_dict['publish_time'])[0].strip()
    policy_text.language = '英语'

    policy_text.institution = json.dumps(strip_list(
        dom.xpath(xpath_dict['author'])))
    policy_text.field = json.dumps({
        'themes': strip_list(dom.xpath(xpath_dict['themes'])),
        'bread': strip_list(dom.xpath(xpath_dict['bread']))
        # fixme 爬取的网页没有第三个面包屑
    })
    policy_text.keywords = json.dumps(
        strip_list(dom.xpath(xpath_dict['keywords'])))
    policy_text.file_url = dom.xpath(xpath_dict['file_url'])[0].strip()
    policy_text.file_url = url_parser.urljoin(url, policy_text.file_url)
    policy_text.original_title = dom.xpath(xpath_dict['title'])[0].strip()
    try:
        policy_text.abstract = dom.xpath(xpath_dict['description'])[0].strip()
    except IndexError as e:
        logger.warning(f'{e}: blank abstract')

    # 创建文件
    file = File()
    file.name = policy_text.original_title
    file.filetype = 1
    file.extension = 'pdf'
    db.session.add(file)
    db.session.commit()

    policy_text.original_file = file.id
    db.session.add(policy_text)
    db.session.commit()


def handle_policy_csis(html, url):
    """
    处理欧盟出版物
    todo 语言和链接很难处理，目前统统drop掉
    Args:
        html (str):
        url (str):
    Returns:
        db input
    """
    xpath_dict = {
        'publish_time': "//div[@class='layout-detail-page__main']//p[1]/text()",  # July 1, 2010
        'author': "//div[@class='teaser__title']/text()",  # Abraham M. Denmark
        'themes': "",
        'keywords': "",
        'file_url': "//a[@class='file__link']/@href",  # 需要注意前面有没有域名
        # 'abstract': "//div[@class='purchase-info']/following-sibling::p[1]",
        'content': "//article",
        'bread': "",
        'original_title': "//div[@class='layout-detail-page__main']//h1[1]/text()"
    }

    #
    def time_parser(str_time):
        """
        Args:
            str_time (str): July 1, 2010
        Returns:
            datetime
        """
        return datetime.strptime(str_time, "%B %d, %Y")

    dom = etree.HTML(html)

    policy_text = PolicyText()
    file = File()

    if policy_text.query.filter(policy_text.source_url == url).first():
        logger.warning('duplicated policy, skip!')
        return
    policy_text.source_url = url
    policy_text.nation = '美国'
    policy_text.release_time = time_parser(dom.xpath(xpath_dict['publish_time'])[0].strip())
    policy_text.language = '英语'
    policy_text.institution = 'White House'
    policy_text.original_title = dom.xpath(xpath_dict['original_title'])[0].strip()
    policy_text.site = 'www.csis.org'

    file.name = policy_text.original_title
    file.filetype = 1

    try:  # 判断是不是pdf文件
        policy_text.file_url = dom.xpath(xpath_dict['file_url'])[0].strip()
    except IndexError as e:  # 不是 pdf 文件
        logger.info(f'{e}: no file url')
        file.extension = 'html'
        policy_text.spider_condition = 1
        # 如果不能成功提取的话，就放弃这个文件了
        try:
            html_content = etree.tostring(dom.xpath(xpath_dict['content'])[0]).decode()
        except IndexError as e:
            logger.error(f'Handle HTML File | no html_content, crawl give up')
            return
        else:
            file.savename = save_html_file(html_=html_content, file_url_=url)
    else:
        file.extension = 'pdf'
        logger.info(f'pdf file, url: {policy_text.file_url}')
        # try:
        #     policy_text.abstract = etree.tostring(dom.xpath(xpath_dict['content'])[0]).decode()
        # except IndexError as e:
        #     logger.warning(f'Handle PDF File Abstract: no abstract')
        policy_text.spider_condition = 0
        if not policy_text.file_url[-3:] in {'pdf', 'PDF'}:
            logger.warning('TYPE | not pdf')
            policy_text.spider_condition = 2

    db.session.add(file)
    db.session.commit()

    policy_text.original_file = file.id
    db.session.add(policy_text)
    db.session.commit()


if __name__ == '__main__':
    # gen_opeu_tasks()

    # policy_crawler('spider', delay=0.5, callback=handle_policy_op_europa_eu)
    # policy_crawler(queue_name='csis_spider', delay=0.5, callback=handle_policy_csis)
    policy_crawler(queue_name='opeu_spider', delay=0.5, callback=handle_policy_opeu)

    # opeu_demo_url = 'https://op.europa.eu/en/publication-detail/-/publication/bf587197-aeda-11eb-9767-01aa75ed71a1/language-en/format-PDF/source-209659206'
    # test_policy_crawler(opeu_demo_url, callback=handle_policy_op_europa_eu)

    # csis_demo_url = 'https://www.csis.org/analysis/twq-managing-global-commons-summer-2010'
    # csis_demo_url = 'https://www.csis.org/analysis/can-india-transition-looking-east-acting-east-aseans-help-commemorating-two-decades-asean'

    # test_policy_crawler(csis_demo_url, callback=handle_policy_csis)
