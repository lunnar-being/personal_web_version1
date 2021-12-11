# -*- coding: utf-8 -*-

""" 
@author: Jin.Fish
@file: base_site.py
@version: 1.0
@time: 2021/07/23 14:32:19
@contact: jinxy@pku.edu.cn

base class for spider
implement:
    1. retrieve result (put into redis)
    2. record page parser (put into db)
"""
import json
import re
import fake_useragent
import requests_cache
import urllib.parse

from datetime import timedelta, datetime
from typing import List, Dict
from lxml import etree
from lxml.etree import tostring

from spider import PolicyText, File, logging, db, format_exc, FileName
from spider.redis_queue import RedisQueue
from spider.download import Downloader
from disruptive import app

app.app_context().push()


class ExtractError(BaseException):
    def __init__(self, info=''):
        self.info = info


class DomXpathError(BaseException):
    def __init__(self, item, info):
        self.item = item
        self.info = info


def strip_list(ele_list):
    """用来处理xpath抓取结果"""
    return [ele.strip() for ele in ele_list if ele]


def time_parser(str_time):
    """
    Args:
        str_time (str): July 1, 2010 | Monday, April 16, 2018 -
    Returns:
        datetime
    """
    try:
        return datetime.strptime(str_time, "%B %d, %Y")
    except ValueError:
        return datetime.strptime(str_time, "%A, %B %d, %Y -")


class DomHandler:
    def __init__(self, dom, xinfo):
        self.dom = dom
        self.xinfo = xinfo

    def __getitem__(self, item):
        try:
            res = self.dom.xpath(self.xinfo[item])
            if isinstance(res, list) and isinstance(res[0], str):
                res = list(map(lambda x: x.strip(), res))
            elif isinstance(res, str):
                res = res.strip()
            return res
        except Exception as e:
            if item == 'abstract':
                return ''
            else:
                raise DomXpathError(item, str(e))


class BaseSpider:
    # 内容相关
    spider_name: str
    domain: str
    query_keywords: List[str]
    query_pattern: str  # need implement & formatting
    lg: logging.Logger
    task_queue: RedisQueue
    downloader: Downloader
    xpath_dict: Dict  # need implement
    # 网络相关
    fake_ua = fake_useragent.UserAgent()  # 设置 useragent
    success_cnt: int

    def __init__(self, name, domain, cache_days=30):
        self.spider_name = name  # spider name
        self.lg = logging.getLogger(self.spider_name)  # init logger
        self.domain = domain  # it should starts with https
        self.query_keywords = [
            'disruptive technology',
            'Next Big Thing',
            'radical technology',
            'breakthrough technology',
            'game changer',
            'gaming changing technology',
            'emerging technology',
            'revolutionary technology',
            'transformative technology'
        ]  # query keywords
        requests_cache.install_cache(backend='sqlite', expires=timedelta(days=cache_days))  # init requests cache
        self.task_queue = RedisQueue(db=1, queue_name=self.spider_name)  # init redis crawl task queue
        self.downloader = Downloader(delay=5, user_agent=self.fake_ua['random'])

    def download_and_extract(self, url, xpath):
        """
        指定一个检索结果页面（链接）
        基于 xpath 解析信息
        Args:
            url (str): 检索结果页面链接
        """
        html = self.downloader(url, num_retries=3)
        if not html:
            raise ExtractError(f'Blank Content From URL: {url}')
        dom = etree.HTML(html)
        if isinstance(xpath, list):
            extract_res = [dom.xpath(x_item) for x_item in xpath]
        else:
            extract_res = dom.xpath(xpath)
        return extract_res

    def get_page_num(self, query_url):
        """
        检索结果一共有几页
        todo 这个函数需要单独定制
        """
        len_xpath = "//span[@class='results-number-info']/text()"
        len_info = self.download_and_extract(url=query_url, xpath=len_xpath)
        len_re = re.match(r"returned\s*(\d+)\s*results", len_info[0].strip())
        tot_len = int(len_re.group(1))
        return int(tot_len / 50) + 1

    def get_page_list(self, query_word, page_id):
        """
        获取 page list
        todo 这个函数需要单独定制
        Args:
            query_word:
            page_id:
        Returns:
            page_list
        """
        record_list = self.download_and_extract(url=self.query_pattern.format(query_word, page_id),
                                                xpath='//a[@class="documentDetailLink"]/@href')
        return record_list

    def retrieve_one(self, query_word):
        """
        处理一个检索词
        对每个检索页面都抓取链接放入redis
        """
        self.lg.info(f'Start Query Keyword: {query_word}')
        # 获取结果条数，用于翻页
        tot_len = self.get_page_num(self.query_pattern.format(query_word, 1))
        for page_id in range(1, tot_len + 1):  # 开始遍历
            record_list = self.get_page_list(query_word, page_id)
            self.lg.info(f'Handel Page: {page_id}, {len(record_list)} record_list got')  # 遍历完成 汇报情况
            self.task_queue.push(record_list)  # 加入任务列表

    def retrieve_all(self):
        """突然觉得这个函数有点鸡肋"""
        for query_word in self.query_keywords:
            self.retrieve_one(query_word)

    def policy_crawler(self):
        """
        批量下载html页面爬取一条政策
        具体的处理方式取决于输入的callback
        """
        # 不断循环任务队列
        self.success_cnt = 0
        while len(self.task_queue):
            url = self.task_queue.pop()  # type: str
            # url = 'https://itif.org/publications/2017/05/08/us-labor-market-experiencing-unprecedented-calm-new-analysis-census-data'
            if PolicyText.query.filter(PolicyText.source_url == url).first():
                self.lg.warning(f'Dup | {url} | Aborted')
                continue
            if not (url.startswith('https://') or url.startswith('http://')):
                url = urllib.parse.urljoin(self.domain, url)

            html_content = self.downloader(url, num_retries=3)
            try:
                self.parse_page(html_content, url)
            except DomXpathError as dom_error:
                self.lg.info(f"ParseError | {dom_error.item} | {dom_error.info}")
                self.task_queue.push(url, force=True)
            except Exception as e:
                self.lg.error(f'Unexpected | {e}')
                # logger.error(f'{e}:\n{format_exc()}')
                self.task_queue.push(url, force=True)
            else:
                self.success_cnt += 1
                self.lg.info(f'Done | success_cnt: {self.success_cnt}')

    def parse_page(self, html, url):
        """
        Args:
            html (str):
            url (str):
        Returns:
            db insert
        """
        ...
