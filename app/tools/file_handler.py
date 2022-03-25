# -*- coding: utf-8 -*-

""" 
@author: Jin.Fish
@file: file_handler.py
@version: 1.0
@time: 2021/06/26 15:54:11
@contact: jinxy@pku.edu.cn

file management
"""

import os
from app.models import File, PolicyText
from app import db
from disruptive import app

BASE_DIR = app.config['BASE_DIR']

class FileHandler:
    """
    handle a single file
    """
    file: File
    policy: PolicyText
    file_name: str
    file_type: int

    def __init__(self, file):
        """init"""
        self.file = file
        self.file_type = file.filetype
        self.file_ext = file.extension
        self.policy = PolicyText.query.filter(PolicyText.original_file == file.id).one()
        self.file_name = file.savename

    def get_file_abspath(self):
        """get absolute path"""
        return os.path.join(BASE_DIR, self.file_name)

    def get_file_content(self):
        with open(self.get_file_abspath()) as f:
            lines = f.readlines()
        content = list()
        for line in lines:
            content.append(line.strip())
        return ' '.join(content)
