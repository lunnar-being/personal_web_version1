# -*- coding: utf-8 -*-

""" 
@author: Jin.Fish
@file: download_file.py
@version: 1.0
@time: 2021/04/20 17:55:37
@contact: jinxy@pku.edu.cn

下载文件
"""
import hashlib
from time import sleep
import requests
import wget
from shutil import copyfile
from pyaria2 import Aria2RPC

from spider import File, PolicyText, check_path, os, db, get_md5_str, logging, BASE_DIR, FileName
from disruptive import app
from spider.thread_download import Download, show_process

# use app
app.app_context().push()
fd_logger = logging.getLogger('download_file')


def get_file_thread(url_, save_path_file_, thread_num=5):
    dl = Download(url_, save_path_file_, thread_num)
    dl.download()
    show_process(dl)
    fd_logger.info(f"thread_dl | url: {url_} | saved")
    return os.path.getsize(save_path_file_) / 1024  # KB


def get_file_aria(url_, save_path_file_):
    jsonrpc = Aria2RPC()
    dir, name = os.path.split(save_path_file_)
    options = {"dir": dir, "out": name, }
    jsonrpc.addUri([url_], options=options)
    return os.path.getsize(save_path_file_) / 1024  # KB


def get_file_cmd(url_, save_path_file_):
    fd_logger.info(f"wget cmd | url: {url_} | saved to {save_path_file_}")
    os.system(f"wget '{url_}' -O {save_path_file_}")
    return os.path.getsize(save_path_file_) / 1024  # KB

def get_pdf_file(url_, save_path_file_):
    """
    通过链接获取并存储pdf报告到服务器文件夹
    通用，就是一个二进制文件存储器
    :param url_:
    :param save_path_file_:
    :return:
    """
    fd_logger.info(f"downloading: {url_}")
    # 因为要下载的是二进制流文件，将stream参数置为True
    response_ = requests.get(url_, stream="TRUE")
    with open(save_path_file_, 'wb') as f:
        for data in response_.iter_content():
            f.write(data)
    return os.path.getsize(save_path_file_) / 1024  # KB


def get_pdf_file_wget(url_, save_path_file_):
    """use wget"""
    file_name = wget.download(url=url_, out=save_path_file_)
    fd_logger.info(f"wget | url: {url_} | save to: {file_name}")
    return os.path.getsize(save_path_file_) / 1024  # KB


def save_html_file(html_, file_url_, file_type_='origin'):
    """
    写 HTML 文件
    todo 这种写工作总觉得不安全
    Args:
        html_: 内容
        file_url_: 链接名称（用来生成 md5）
        file_type_: 文件类型
    Returns:
        md5_name
    """
    md5_name = get_md5_str(file_url_)
    save_path = f'{BASE_DIR}/app/data/origin/{file_type_}_{md5_name}.html'
    fd_logger.debug(f'content | {html_}')
    if check_path(save_path):
        fd_logger.warning(f'file already exist and is covered | {save_path}')
    else:
        fd_logger.info(f'file saved | {save_path}')
    with open(save_path, 'w') as f:
        f.write(html_)
    return md5_name


def run_all_raw_file():
    done_cnt = 0
    # 遍历所有的 origin file，savename 为 null 就说明还咩有下载，目前考虑31805之后，也就是屏蔽旧的出版物
    for file in File.query.join(PolicyText, PolicyText.original_file == File.id).filter(File.filetype == 1,
                                                                                        # PolicyText.id > 31805,
                                                                                        # PolicyText.site != 'www.govinfo.gov',
                                                                                        File.savename == None):  # not saved origin file
        policy = PolicyText.query.filter(PolicyText.original_file == file.id).one()

        fd_logger.info(f"Handle | policy_id: {policy.id} | file_savename: {file.savename} | {policy.file_url}")
        if not policy.file_url:
            fd_logger.error(f'no url')
            continue

        # 还没有下载，开干
        file_url = policy.file_url
        save_name = 'origin_' + get_md5_str(file_url) + '.' + file.extension.lower()
        if File.query.filter(File.savename == save_name).all():  # save name already exist
            fd_logger.warning(f"Dup |{file.id}: {file.savename} | id {policy.id} | savename already exist")
            file.savename = save_name
            db.session.add(file)
            db.session.commit()
            continue

        file.savename = save_name
        save_path = f"{BASE_DIR}/app/data/origin/"
        assert check_path(save_path)
        fpath = os.path.join(save_path, file.savename)
        if check_path(fpath):  # file already exist
            fd_logger.info(f"Dup | {file.savename} | id {policy.id} | file already exist in {fpath}")
            db.session.add(file)
            db.session.commit()
            continue

        try:  # call wget and download file
            file_size_kb = get_file_cmd(file_url, fpath)
        except Exception as e:
            fd_logger.error(f'downloading error {e} | aborted')
        else:
            db.session.add(file)
            db.session.commit()
            done_cnt += 1
            # download success and report
            fd_logger.info(f"Done {file.savename} | size {round(file_size_kb / 1024, 2)}MB | id {policy.id} | already down {done_cnt}")
            # sleep(1)


def gen_task():
    f = open('./task.txt', 'w')
    for file in File.query.join(PolicyText, PolicyText.original_file == File.id).filter(File.filetype == 1,
                                                                                        File.extension == 'pdf',
                                                                                        # PolicyText.id > 31805,
                                                                                        # PolicyText.site != 'www.govinfo.gov',
                                                                                        File.savename == None):  # not saved origin file
        policy = PolicyText.query.filter(PolicyText.original_file == file.id).one()
        # fd_logger.info(f"Handle | policy_id: {policy.id} | file_savename: {file.savename} | {policy.file_url}")
        if not policy.file_url:
            fd_logger.error(f'no url')
            continue
        f.write(f"{policy.file_url}\n")
    f.close()


def load_task():
    with open('./task.txt') as f:
        url_list = f.readlines()
    for url in map(str.strip, url_list):
        # url to name
        file_list = PolicyText.query.filter(PolicyText.file_url == url).all()
        file_old_name = os.path.split(url)[1]
        file_old_path = os.path.join('/Users/leverest/Downloads/wget/', file_old_name)
        # make new name
        file_name = FileName(url)
        file_new_path = file_name.gen_path(1)
        file_new_name = file_name.gen_name(1)
        # 如果两个地方都不在就跳过
        if not os.path.exists(file_old_path) and not check_path(file_new_path):
            print(f'not exist {file_old_path} | {url}')
            continue
        # 如果新的地方不在
        if not check_path(file_new_path):
            # move file
            print(file_old_path, '->', file_new_path)
            copyfile(file_old_path, file_new_path)
        # 旧的删了
        if check_path(file_old_path):
            os.remove(file_old_path)
        for file in file_list:
            file.savename = file_new_name
            db.session.add(file)
        db.session.commit()


if __name__ == '__main__':
    run_all_raw_file()
    # gen_task()
    # load_task()
