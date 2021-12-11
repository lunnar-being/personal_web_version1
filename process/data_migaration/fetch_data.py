# -*- coding: utf-8 -*-

""" 
@author: Jin.Fish
@file: fetch_data.py
@version: 1.0
@time: 2021/08/17 00:53:42
@contact: jinxy@pku.edu.cn

fetch data with database
"""

import shutil

from process import db, File, Config, logging, os
from process import PolicyText as Policy
from disruptive import app
app.app_context().push()


def pull_out():
    """把要翻译的文件拎出来"""
    dest_dir = os.path.join(Config.BASE_DIR, 'process/data_migaration/keyword_debug')
    if not os.path.exists(dest_dir):
        os.mkdir(dest_dir)
        print(f'created dir: {dest_dir}')

    # 遍历所有的format文件对象
    savename_list = File.query.with_entities(File.savename).join(Policy, Policy.format_file == File.id).filter(
        Policy.use == True,
        File.savename != None,
        Policy.keywords == None).all()

    for savename in savename_list:
        savename = savename[0]
        old_path = f'/root/repos/disruptive/app/data/format/{savename}'
        new_path = os.path.join(dest_dir, savename)
        print(old_path, ' -> ', new_path)
        shutil.copyfile(old_path, new_path)


def move_back():
    """把翻译好的送回去"""
    src_dir = os.path.join(Config.BASE_DIR, 'process/data_migaration/trans_res')
    dest_dir = os.path.join(Config.BASE_DIR, 'app/data/format/')
    for file in os.listdir(src_dir):
        old_path = os.path.join(src_dir, file)
        new_path = os.path.join(dest_dir, file)
        print(old_path, ' -> ', new_path)
        shutil.copy(old_path, new_path)


if __name__ == '__main__':
    pull_out()
    # move_back()
