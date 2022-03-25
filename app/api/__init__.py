# -*- coding: utf-8 -*-

""" 
@author: Jin.Fish
@file: __init__.py.py
@version: 1.0
@time: 2021/05/08 20:23:25
@contact: jinxy@pku.edu.cn

file download and upload
"""

from flask import Blueprint

api = Blueprint('api', __name__)
from app.api import views
