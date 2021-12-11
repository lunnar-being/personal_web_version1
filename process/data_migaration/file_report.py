# -*- coding: utf-8 -*-

""" 
@author: Jin.Fish
@file: file_report.py
@version: 1.0
@time: 2021/06/25 16:37:04
@contact: jinxy@pku.edu.cn

报告文件情况
"""

import os
import re
from pprint import pprint
from collections import Counter
from process import BASE_DIR, logging


data_dir = os.path.join(BASE_DIR, "app/data/")
origin_dir = os.path.join(data_dir, "origin")
format_dir = os.path.join(data_dir, "format")


def get_ext(file_name_, file_type_='origin'):
    """
    Args:
        file_name_: xxxx.pdf
        file_type_: origin or format?
    Returns:
    """
    ext_match = re.match(file_type_ + r"_\w{32}.(\w+)", file_name_)
    if ext_match:
        return ext_match.group(1)
    else:
        logging.error("not matched file ext")


def report_ext():
    origin_file_list = os.listdir(origin_dir)
    ext_list = list(map(get_ext, origin_file_list))
    print(f"tot file count: {len(ext_list)}")
    ext_counter = Counter(ext_list)
    print("ext distribution is:")
    pprint(ext_counter)
