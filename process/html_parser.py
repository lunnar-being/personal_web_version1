# -*- coding: utf-8 -*-

""" 
@author: Jin.Fish
@file: html.py.py
@version: 1.0
@time: 2021/04/20 02:37:44
@contact: jinxy@pku.edu.cn

处理html文件
"""

import re
from process import File, PolicyText, logging, BASE_DIR, bs, db
import os.path as op

from disruptive import app
app.app_context().push()


def html2txt(file_path, save_path):
    with open(file_path, 'r', errors='ignore') as f_in:
        content = ''.join(f_in.readlines())
        norm_content = bs(content, 'lxml')
    with open(save_path, 'w') as f_out:
        f_out.write(norm_content.text)


def run_html_parser():
    cnt = 0
    for file in File.query.filter(File.filetype == 1, File.savename != None, File.extension == 'txt').all():
        format_name = file.savename.replace('origin_', 'format_')
        format_name = re.sub(r'\.(pdf|html)$', '.txt', format_name)
        format_path = op.join(BASE_DIR, 'app/data/format/', format_name)

        origin_path = op.join(BASE_DIR, 'app/data/origin/', file.savename)
        if not op.exists(origin_path):
            print('origin not exist, aborted')
            continue

        if not op.exists(format_path):
            format_file = File()
            format_file.filetype = 2
            format_file.name = file.name
            format_file.savename = format_name
            format_file.extension = 'txt'

            logging.info(f"id: {file.id}, {origin_path} -> {format_path}")
            html2txt(origin_path, format_path)

            db.session.add(format_file)
            db.session.add(file)
            db.session.commit()
            policy_text = PolicyText.query.filter_by(original_file=file.id).one()
            policy_text.format_file = format_file.id
            db.session.add(policy_text)
            db.session.commit()
            cnt += 1
    return cnt


if __name__ == '__main__':
    cnt = run_html_parser()
    print(cnt)
