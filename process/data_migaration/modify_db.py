# -*- coding: utf-8 -*-

""" 
@author: Jin.Fish
@file: modify_db.py.py
@version: 1.0
@time: 2021/05/24 23:53:39
@contact: jinxy@pku.edu.cn

迁移数据后
同步修改数据库
"""
import re
import sqlalchemy
from process import (File, PolicyText, db, logging, os, PROCESS_BASE_DIR, BASE_DIR, path_join)
from disruptive import app
from spider.download_file import get_md5_str
from util import FileName, FileNameNotMatchError

app.app_context().push()


def file_existence():
    good_file_cnt = 0
    for file in File.query.filter(File.filetype == 1).all():
        # 遍历每一条
        try:
            policy = PolicyText.query.filter(
                PolicyText.original_file == file.id).one()  # type: PolicyText
        except sqlalchemy.exc.NoResultFound as e:
            logging.error(f'file_{file.id} does not belong to any policy')
            continue

        if file.savename:  # 数据库以为这个文件存在
            origin_file_path = path_join(f'app/data/origin/{file.savename}')
            if not os.path.exists(origin_file_path):  # 其实并不存在
                logging.warning(f'file_{file.id} not exist but in db')
            else:
                good_file_cnt += 1
        else:  # 数据库以为这个不文件存在
            assume_name = 'origin_' + get_md5_str(
                policy.file_url) + '.' + file.extension
            origin_file_path = path_join(f'app/data/origin/{assume_name}')
            if os.path.exists(origin_file_path):  # 结果这个文件存在
                logging.info(f'file_{file.id} exist but not in db')
    logging.info(f'good_file_cnt: {good_file_cnt}')


# one time function
def correct_db_savename():
    """
    @time: 20210622
    修复名称
    主要是由于扩展名导致的, 漏了一个点号
    """
    for file in File.query.filter(File.filetype == 1, File.savename != None).all():  # all origin file
        savename = file.savename  # if has savename, means it should exist
        policy = PolicyText.query.filter(PolicyText.original_file == file.id).one()
        try:
            gt_savename = f"origin_{get_md5_str(policy.file_url)}.{file.extension.lower()}"
        except AttributeError as e:
            logging.error(f"Null policy_file_url: {policy.id}, savename cleared")
            file.savename = None
            db.session.add(file)
        else:
            if savename != gt_savename:
                logging.info(f"{savename}->{gt_savename}")
                file.savename = gt_savename
    db.session.commit()


# one time function
def bad_name2good_name(bad_name):
    """
    todo only for origin and pdf now
    Args:
        bad_name: origin_9d31d0cf6486d1f252eed04730570f26pdf
    Returns:
        origin_9d31d0cf6486d1f252eed04730570f26.pdf
    """
    match = re.match(r"(origin_\w+)(pdf|odt|ods|html|txt)", bad_name)
    if match:
        return match.group(1) + '.' + match.group(2)
    else:
        logging.warning('bad name not recognized')


# one time function
def correct_os_savename():
    """
    找到错误命名的文件，删除（如果已经存在正确名称文件）或者重命名
    """
    # query os
    origin_data_dir = os.path.join(BASE_DIR, 'app/data/origin')
    file_origin_pdf_savename_indeed_list = os.listdir(origin_data_dir)
    # find bad name
    for file_path in file_origin_pdf_savename_indeed_list:
        if not re.match(r"origin_\w*\.\w{1,4}", file_path):  # 错误命名的文件，建议直接删除
            to_remove = os.path.join(origin_data_dir, file_path)
            # try to change bad 2 good
            bad2good_path = bad_name2good_name(file_path)
            if os.path.exists(os.path.join(origin_data_dir, bad2good_path)):
                # if related good exist
                logging.info(f"removing: {to_remove}")
                os.remove(to_remove)
            else:
                good_path = os.path.join(origin_data_dir, bad2good_path)
                logging.info(f"no good replace badname, renaming {to_remove} to {good_path}")
                os.rename(to_remove, good_path)


def check_file_consistency():
    """
    查看数据库里的文件名称和实际系统中的文件是否一致
    todo 关于名称，建议做一个 verify name 来确认没有问题
    """
    # query db
    file_origin_pdf_list = File.query.filter(File.filetype == 1).all()
    file_origin_pdf_savename_list = [file_origin_pdf.savename for file_origin_pdf in file_origin_pdf_list]  # type: list(str)
    # query os
    origin_data_dir = os.path.join(BASE_DIR, 'app/data/origin')
    file_origin_pdf_savename_indeed_list = os.listdir(origin_data_dir)

    os_ext_set = set([file.split('.')[1] for file in file_origin_pdf_savename_indeed_list])
    logging.info(f"os_ext_set: {os_ext_set}")

    # make set
    name_set = set(file_origin_pdf_savename_list)
    name_indeed_set = set(file_origin_pdf_savename_indeed_list)

    # check dup
    if len(file_origin_pdf_savename_list) != len(name_set):
        logging.warning("dup savename in db")
    if len(file_origin_pdf_savename_indeed_list) != len(name_indeed_set):
        logging.warning("dup savename indeed")

    logging.info(f"db redundant: {name_set - name_indeed_set}")
    logging.info(f"indeed redundant: {name_indeed_set - name_set}")


def replenish_db_from_os():
    """
    从os中找到数据中缺失的文件
    通过遍历数据库的方式
    """
    origin_data_dir = os.path.join(BASE_DIR, 'app/data/origin')

    for file in File.query.filter(File.filetype == 1, File.savename == None).all():  # all origin file
        try:
            policy = PolicyText.query.filter(PolicyText.original_file == file.id).one()  # type: PolicyText
        except sqlalchemy.exc.NoResultFound as e:
            logging.error(f"occur a file but it belong to no policy, file id: {file.id}")
            continue

        try:  # ensure file_url exist
            gt_savename = f"origin_{get_md5_str(policy.file_url)}.{file.extension.lower()}"
        except:
            logging.warning("null policy file_url")
        else:  # get gt_name and compare / replace
            if os.path.exists(os.path.join(origin_data_dir, gt_savename)):
                logging.info(f"find new file not in db: {gt_savename}, replenished")
                # origin_file_id = policy.original_file
                # ori_file = File.query.get(origin_file_id)  # type: File
                assert file.savename is None
                file.savename = gt_savename
                db.session.add(file)
    db.session.commit()


# 找到存在origin_file.savename但是文件并不存在
def clean_blank_dbsavename():
    for file in File.query.filter(File.filetype == 1, File.savename != None):
        file_name = FileName()
        try:
            file_name.set_by_name(file.savename)
        except FileNameNotMatchError as e:
            print(f"FileNameNotMatchError: {file.savename}")
        else:
            file_path = file_name.gen_path(1)
            if not os.path.exists(file_path):
                print('not exist: ', file_path)
                file.savename = None
                db.session.add(file)
    db.session.commit()


# 删除重复数据
def remove_dup():
    with open('dup_policy.csv') as f:
        lines = f.readlines()
    for line in lines:
        same_len, url, _ = line.split('\t')
        print(same_len, url)
        if not url: continue
        same_policy_list = PolicyText.query.filter(PolicyText.file_url == url).all()
        for idx, p_dup in enumerate(same_policy_list):  # type: (int, PolicyText)
            if idx < len(same_policy_list) - 1:  # 3 < 4 - 1
                print(f'handle file {idx}')
                File.query.filter(File.id == p_dup.original_file).delete()
                File.query.filter(File.id == p_dup.format_file).delete()
                File.query.filter(File.id == p_dup.translated_file).delete()
                File.query.filter(File.id == p_dup.checked_file).delete()
                db.session.delete(p_dup)
                db.session.commit()


if __name__ == '__main__':
    # file_existence()
    # print(bad_name2good_name('origin_492446f689885cd86314be6311139165odt'))
    # correct_db_savename()
    # correct_os_savename()
    # check_file_consistency()
    # replenish_db_from_os()
    clean_blank_dbsavename()
    # remove_dup()
