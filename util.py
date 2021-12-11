# -*- coding: utf-8 -*-

""" 
@author: Jin.Fish
@file: util.py
@version: 1.0
@time: 2021/06/01 20:25:40
@contact: jinxy@pku.edu.cn

utils
"""

import os
import hashlib
import logging
import re
import threading
from bs4 import BeautifulSoup as bs
from config import Config

logging.basicConfig(format='%(asctime)s | %(levelname)s | %(filename)s | %(funcName)s | %(message)s',
                    level=logging.INFO, datefmt='%m-%d %H:%M:%S')


def get_md5_str(s_):
    """
    将字符串转换成md5
    所有文件的名称都用 文件链接的 md5
    """
    return hashlib.md5(s_.encode("utf-8")).hexdigest()


def pure_text(html_):
    if not html_:
        return ""
    return bs(html_, 'lxml').text


def check_path(path_):
    """
    check if path exist
    Args:
        path_ (str):
    Returns:
        bool
    """
    return os.path.exists(path_)


class FileNameNotMatchError(BaseException):
    def __init__(self, name):
        self.info = name


class FileName:
    md5_str: str
    origin_file_type: str
    origin_extension: str

    def __init__(self, file_url='', file_type='origin', extension='pdf'):
        """
        init filename
        Args:
            file_url (str): if intended to use set_by_name(), skip this
            file_type (str): origin | format | trans | check
            extension (str): pdf | txt | html
        """
        self.md5_str = get_md5_str(file_url)
        self.origin_file_type = file_type
        self.origin_extension = extension

    def set_by_name(self, save_name):
        # name_re = re.match(r"(origin|format|check|trans)_(\w*)\.(\w+)", save_name)
        # only support origin now
        name_re = re.match(r"(origin|format)_(\w*)\.(\w+)", save_name)
        if not name_re:
            raise FileNameNotMatchError(save_name)
        self.origin_file_type = name_re.group(1)
        self.md5_str = name_re.group(2)
        assert len(self.md5_str) == 32
        self.origin_extension = name_re.group(3)

    def gen_name(self, file_type):
        if file_type == 1:
            return f"origin_{self.md5_str}.{self.origin_extension}"
        if file_type == 2:
            return f"format_{self.md5_str}.txt"
        if file_type == 3:
            return f"trans_{self.md5_str}.txt"
        if file_type == 4:
            return f"check_{self.md5_str}.txt"

    def gen_path(self, file_type):
        dir_path = Config.BASE_DIR
        file_name = self.gen_name(file_type)
        if file_type == 1:
            return os.path.join(dir_path, 'app/data/origin', file_name)
        if file_type == 2:
            return os.path.join(dir_path, 'app/data/format', file_name)
        if file_type == 3:
            return os.path.join(dir_path, 'app/data/trans', file_name)
        if file_type == 4:
            return os.path.join(dir_path, 'app/data/check', file_name)


class MyThread(threading.Thread):
    def __init__(self, func, args):
        super(MyThread, self).__init__()
        self.func = func
        self.args = args

    def run(self):
        self.result = self.func(*self.args)

    def get_result(self):
        try:
            return self.result
        except Exception:
            return None


if __name__ == '__main__':
    file = FileName(
        'https://assets.publishing.service.gov.uk/government/uploads/system/uploads/attachment_data/file/951739/Laptops_and_Tables_Data_as_of_12_January.pdf')
    for i in [1, 2, 3, 4]:
        print(file.gen_name(1))
        print(file.gen_path(1))
