# -*- coding: utf-8 -*-

""" 
@author: Jin.Fish
@file: mig_data.py
@version: 1.0
@time: 2021/04/19 21:09:30
@contact: jinxy@pku.edu.cn

从ali迁移数据到tx3
"""
import math
import os

import numpy as np
import pandas as pd
from app import db
from app.models import File, PolicyText
from disruptive import app
app.app_context().push()

pd.set_option('display.max_columns', None)


def get_path(path_):
    path_ = os.path.join(app.config['BASE_DIR'], path_)
    # print(path_)
    return path_


db_file_path = 'app/data/database/disruptive_technology_file.csv'
file_df = pd.read_csv(get_path(db_file_path), index_col='id')
db_policy_path = 'app/data/database/disruptive_technology_policy_text.csv'
policy_df = pd.read_csv(get_path(db_policy_path), index_col='id')

file_df = file_df.where(file_df.notnull(), None)
policy_df = policy_df.where(policy_df.notnull(), None)
# print(file_df.head(5))
# print(policy_df.head(5))
# print(policy_df.loc[20])

for idx, policy_rc in policy_df.iterrows():  # rc: record
    if idx % 100 == 0:
        print(idx)
    policy = PolicyText()
    same_name_list = ['source_url', 'nation', 'release_time', 'institution',
                      'field', 'language', 'keywords', 'original_title',
                      'translated_title', 'abstract']
    for same_name in same_name_list:
        setattr(policy, same_name, policy_rc[same_name])
    old_original_file_id = policy_rc['original_file']
    original_file = File()
    if old_original_file_id and not math.isnan(old_original_file_id):
        old_original_file = file_df.loc[old_original_file_id]
        policy.file_url = old_original_file.source_url
        original_file.filetype = 1
        original_file.name = old_original_file['name']
        original_file.extension = old_original_file['extension']
        original_file.savename = old_original_file['savename']
        db.session.add(original_file)
    old_trans_file_id = policy_rc['translated_file']
    trans_file = File()
    if old_trans_file_id and not math.isnan(old_trans_file_id):
        old_trans_file = file_df.loc[old_trans_file_id]
        trans_file.filetype = 3
        trans_file.name = old_trans_file['name']
        trans_file.extension = old_trans_file['extension']
        trans_file.savename = old_trans_file['savename']
        db.session.add(trans_file)
    db.session.commit()
    if old_original_file_id:
        policy.original_file = original_file.id
    if old_trans_file_id:
        policy.translated_file = trans_file.id
    db.session.add(policy)
    db.session.commit()


