from module.tomysql import *
from module.CHN import Cprocessing

"""
author : whg
time : 2021/12/25
"""


topic_dic = {
    "战略规划": ['strategic', 'plan', 'strategy', 'strategic guidance', 'executive order', 'blueprint', 'roadmap',
             'white paper', 'whitepaper', 'decade plan', 'basic plan'],
    "技术治理": ['regulatory', 'regulate', 'regulation', 'governance', 'governing', 'govern'],
    "技术项目": [],
    "研究报告": ["review", 'report', 'study', 'research', 'analysis', 'working paper', 'issue paper', 'consultation paper']
}

tech_project = ['arpa']


# 单条主题分类
def get_topic(origin_title, origin_url):
    for topic in topic_dic:
        try:
            tt = ' '.join(Cprocessing(origin_title)).lower()
        except:
            tt = origin_title
        finally:
            for keyword in topic_dic[topic]:
                if keyword in tt:
                    return topic
                else:
                    pass
    for part_url in tech_project:
        if part_url in origin_url:
            return "技术项目"
        else:
            return ''


# 全量更新
def update_topic():
    titles = get_file_topic()
    for i in titles:
        for topic in topic_dic:
            try:
                tt = ' '.join(Cprocessing(i[1])).lower()
            except:
                tt = i[1].lower()
            finally:
                for keyword in topic_dic[topic]:
                    if keyword in tt:
                        update_t1(i[0], 'topic_classification', topic)
                        continue
                    else:
                        pass
                pass
        for parturl in tech_project:
            if parturl in i[3]:
                update_t1(i[0], 'topic_classification', '技术项目')
            else:
                pass


if __name__ == '__main__':
    update_topic()
