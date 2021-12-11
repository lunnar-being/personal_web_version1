# -*- coding: utf-8 -*-

""" 
@author: Jin.Fish
@file: data_import.py
@version: 1.0
@time: 2021/07/03 11:00:40
@contact: jinxy@pku.edu.cn

import data from outside source
"""
import logging
import os

import numpy as np
import pandas as pd
import re

from spider import File, PolicyText, get_md5_str, db, BASE_DIR
from disruptive import app

app.app_context().push()


def import_us():
    imp_lg = logging.getLogger('us_importer')
    df = pd.read_csv('./wyz-us-all.csv')
    for rid, record in df.iterrows():
        policy = PolicyText()
        policy.source_url = record['detailsLink']

        # handle nan source_url
        if pd.isna(policy.source_url):
            imp_lg.error('no source_url')
            break

        # handle duplicate
        if PolicyText.query.filter(PolicyText.source_url == policy.source_url).first():
            continue
        policy.nation = '美国'
        if record['publishdate'] == 'publishdate':
            imp_lg.error('publishdate')
            continue
        policy.release_time = record['publishdate']
        policy.institution = record['collection']
        policy.language = '英语'

        # handle nan title
        if pd.isna(record['title']):
            # if no title: don't need it
            imp_lg.warning('no title, dropped')
            continue

        policy.original_title = record['title']
        policy.abstract = record['teaser']
        policy.site = 'www.govinfo.gov'
        if not pd.isna(record['htmlLink']):
            # html spider
            policy.spider_condition = 1
            policy.file_url = record['htmlLink']
            file = File()
            file.filetype = 1
            # if not downloaded, no name
            # file.savename = f"origin_{get_md5_str(policy.file_url)}.html"
            file.extension = 'html'
            db.session.add(file)
            db.session.commit()
            policy.original_file = file.id
        elif not pd.isna(record['pdfLink']):
            # pdf spider
            policy.spider_condition = 0
            policy.file_url = record['pdfLink']
            file = File()
            file.filetype = 1
            # if not downloaded, no name
            # file.savename = f"origin_{get_md5_str(policy.file_url)}.pdf"
            file.extension = 'pdf'
            db.session.add(file)
            db.session.commit()
            policy.original_file = file.id
        else:
            imp_lg.warning('no pdf or html')
        db.session.add(policy)
        db.session.commit()


def find_match():
    cnt = 0
    us_data_dir = os.path.join(BASE_DIR, 'app/data/us-data')
    us_file_name_list = os.listdir(us_data_dir)
    print(us_file_name_list[0])
    target_policies = PolicyText.query.filter(PolicyText.site == 'www.govinfo.gov').all()
    # print(len(target_policies))
    for policy in target_policies:
        for name in us_file_name_list:
            if policy.original_title.lower() in name:
                logging.info(f'matched: {policy.id}, {policy.original_title}')
                cnt += 1
    logging.info(f"cnt: {cnt}")


def import_manual():
    df_p = pd.read_excel('./manual-0724.xlsx', sheet_name='policy_text')
    df_f = pd.read_excel('./manual-0724.xlsx', sheet_name='file')
    df_p['release_time'] = df_p['release_time'].astype('str')
    df_p = df_p.where(pd.notnull(df_p), None)
    for i in range(df_p.shape[0]):
        p = df_p.iloc[i]
        f = df_f.iloc[i]
        policy = PolicyText()
        policy.source_url = p['source_url']
        if PolicyText.query.filter(PolicyText.source_url == p['source_url']).first():
            logging.info(f"Dup | {p['source_url']} | row {i}")
            if not p['source_url'] in ['https://www8.cao.go.jp/cstp/sentan/about-kakushin.html',
                                       'https://www8.cao.go.jp/cstp/moonshot/index.html']:
                continue
        policy.file_url = p['source_url']
        site_re = re.match(r"https?:\/\/([\w\.]+)\/.*", p['source_url'])
        if site_re:
            policy.site = site_re.group(1)
        else:
            print('no site')
        policy.nation = p['nation']
        policy.release_time = p['release_time'] if p['release_time'] != 'NaT' else '1970-01-01'
        policy.institution = p['institution']
        policy.language = p['language']
        policy.original_title = p['original_title']
        policy.abstract = p['abstract']
        policy.spider_condition = 299

        file = File()
        file.filetype = 1
        ext_re = re.match(r"\w*\.(\w+)$", p['original_file'])
        file.extension = ext_re.group(1)
        file.savename = f"origin_{p['original_file']}"
        assert os.path.exists(os.path.join(BASE_DIR, 'app/data/origin/', file.savename))
        file.name = f['name']

        db.session.add(file)
        db.session.commit()
        policy.original_file = file.id
        db.session.add(policy)
        db.session.commit()
        logging.info(f"insert success | {policy}")


def import_doctype():
    """
    zzx version 0807
    """
    doc_type_map = {
        'tech_reg': '技术治理',
        'tech_rev': '研究报告',
        'tech_prog': '技术项目',
        'tech_plan': '战略规划'
    }
    df = pd.read_csv('./doc_type_0807.csv')
    for i in range(df.shape[0]):
        row = df.iloc[i]
        p = PolicyText.query.get(int(row['pf_id']))  # type: PolicyText
        p.doc_type = doc_type_map[row['doc_type']]
        db.session.add(p)
    db.session.commit()

if __name__ == '__main__':
    # import_us()
    # find_match()
    # import_manual()
    import_doctype()

