# -*- coding: utf-8 -*-

""" 
@author: Jin.Fish
@file: file_manager.py
@version: 1.0
@time: 2021/07/25 02:33:19
@contact: jinxy@pku.edu.cn

manage file
"""
import os

from process import PolicyText, File, db, BASE_DIR, FileName, tqdm, check_path
from disruptive import app
app.app_context().push()


def find_bad_file():
    origin_dir = os.path.join(BASE_DIR, 'app/data/origin')
    cnt = 0
    for file_name in os.listdir(origin_dir):
        if not file_name.endswith('.pdf'): continue
        file_path = os.path.join(origin_dir, file_name)
        size = os.path.getsize(file_path)
        if size < 500:
            print(size, '', file_path)
            os.remove(file_path)
            cnt += 1
    print('cnt: ', cnt)


def cal_len():
    """计算所有format的长度，放入size字段"""
    for file in tqdm(File.query.filter(File.filetype == 2, File.savename != None).all()):
        file_name = FileName()
        file_name.set_by_name(file.savename)
        file_path = file_name.gen_path(2)
        if not check_path(file_path): continue
        with open(file_path) as f:
            content = '\n'.join(f.readlines())
        file.size = len(content)
        db.session.add(file)
    db.session.commit()


if __name__ == '__main__':
    # find_bad_file()
    cal_len()
