# -*- coding: utf-8 -*-

""" 
@author: Jin.Fish
@file: itif.py
@version: 1.0
@time: 2021/07/23 14:26:47
@contact: jinxy@pku.edu.cn

itif spider
"""

from spider.site_spider.base_site import *

class ItifSpider(BaseSpider):
    def __init__(self):
        super(ItifSpider, self).__init__(name='itif', domain='https://itif.org/')
        self.xpath_dict = {}
        self.query_pattern = "https://itif.org/search?keys={}&page={}"
        self.xpath_dict = {
            'publish_time': "//span[@class='date-display-single']/text()",
            'abstract': "//div[contains(@class, 'body')]//text()",
            'body': "//main[contains(@role, 'main')]",
            'title': "//*[@id='page-title']//text()",
        }

    def get_page_num(self, query_url):
        return 3

    def get_page_list(self, query_word, page_id):
        # todo 这里或者可以多搞一点东西下来，比如判断标题里面是否有关键词
        record_list, title_list, type_list = self.download_and_extract(
            url=self.query_pattern.format(query_word, page_id),
            xpath=["//div[@class='views-field views-field-title']/span[@class='field-content']//a/@href",
                   "//div[@class='views-field views-field-title']/span[@class='field-content']//a/text()",
                   "//div[@class='views-field views-field-type']/span[@class='field-content']/span/text()"])
        assert len(record_list) == len(title_list) and len(record_list) == len(type_list)
        return record_list

    def parse_page(self, html, url):
        domer = DomHandler(etree.HTML(html), self.xpath_dict)
        policy = PolicyText(site='itif.org', source_url=url, nation='美国', language='英语', file_url=url)
        policy.institution = 'ITIF'
        policy.release_time = time_parser(domer['publish_time'][0].strip())
        content_list = domer['abstract']
        content_list = strip_list(content_list)
        if len(content_list) > 1:  # has abstract
            policy.abstract = content_list[0]
        policy.original_title = domer['title'][0].strip()
        body = domer['body']

        # todo 如果是html的话，考虑直接写
        file = File(name=policy.original_title, filetype=1, extension='html')
        file_name = FileName(policy.file_url, extension='html')
        file.savename = file_name.gen_name(1)
        file_path = file_name.gen_path(1)
        self.lg.info(f"Write HTML | {file_path}")
        with open(file_path, 'w') as f:
            f.write(tostring(body[0], pretty_print=True, method='html').decode('utf-8'))
        db.session.add(file)
        db.session.commit()

        policy.original_file = file.id
        db.session.add(policy)
        db.session.commit()


if __name__ == '__main__':
    spider = ItifSpider()
    spider.retrieve_all()
    spider.policy_crawler()
