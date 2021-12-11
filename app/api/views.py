# -*- coding: utf-8 -*-

""" 
@author: Jin.Fish
@file: views.py
@version: 1.0
@time: 2021/05/08 20:24:01
@contact: jinxy@pku.edu.cn

apis:
file download and upload
user management todo requirements
"""
import random
import re
import os
import time

from flask import send_file, request

from config import Config
from app.api import api
from app.models import File, PolicyText, User, Roles
from app import db


# download
@api.route('/download', methods=['GET'])
def download():
    """
    下载文件
    """
    file_name = request.args.get('file_name', type=str)
    # todo check file_name safety
    file_type_re = re.match(r'^(.*)_', file_name)
    file_type = file_type_re.group(1)
    file_path = f'{Config.BASE_DIR}/app/data/{file_type}/{file_name}'
    print(file_path)
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    else:
        return 'no such file', 404


@api.route('/upload', methods=['POST'])
def upload():
    """upload proofread file"""
    # todo 需要进行一些上传的检查
    # print(request.form)
    policy_id = request.form.get('id', type=int)
    upload_file = request.files.get('checked_file')
    print(policy_id, upload_file)

    policy_text = PolicyText.query.get(policy_id)
    origin_file = File.query.get(policy_text.original_file)

    # 如果是第一次上传
    checked_file = File()
    checked_file.filetype = 4
    checked_file.name = origin_file.name

    common_name = re.match(r'^\w_(\w)\.\w')

    checked_file.extension = "txt"
    checked_file.savename = ('check_' + common_name.group(1) + '.txt')
    savepath = f'{Config.BASE_DIR}/app/data/check/{checked_file.savename}'
    upload_file.save(savepath)

    db.session.add(checked_file)
    db.session.commit()
    policy_text.checked_file = checked_file.id
    db.session.add(policy_text)
    db.session.commit()
    return 'success', 204


@api.route('/add_user', methods=['POST'])
def add_user():
    user_name = request.form.get('user_name')
    password = request.form.get('password')
    role = request.form.get('role')
    assert role in ['common', 'admin']
    # todo name/password validation needed
    new_user = User()
    new_user.username = user_name
    new_user.password = password
    new_user.role_id = Roles().get_role_id(role)
    db.session.add(new_user)
    db.session.commit()
    return {'user_id', new_user.id}, 204


@api.route('/change_password', methods=['POST'])
def change_password():
    user_id = request.form.get('user_id')
    new_password = request.form.get('new_password')
    # todo password validation needed
    user = User.query.get(user_id)
    user.password = new_password
    db.session.add(user)
    db.session.commit()
    return 'success', 204


@api.route('/delete_user', methods=['GET'])
def delete_user():
    user_id = request.form.get('user_id')
    user = User.query.get(user_id)
    # todo can't delete super
    db.session.delete(user)
    db.session.commit()
    return 'success', 204


@api.route('/collect', methods=['POST'])
def collect():
    site_name = request.form.get('site_name')
    print(f"received site name: {site_name}")
    site_info = {
        'govuk': '英国政府网',
        'opeu': '欧盟出版物',
        'csis': '美国战略与国际研究中心',
        'itif': '美国信息技术与创新基金会'
    }
    msg = f"{site_info[site_name]} 暂无更新"
    sleep_gap = random.randint(1, 10)
    print(f"sleep: {sleep_gap}")
    time.sleep(sleep_gap)
    return msg, 200