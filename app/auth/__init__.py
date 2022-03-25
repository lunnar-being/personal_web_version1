# -*- coding: utf-8 -*-

""" 
@author: Jin.Fish
@file: __init__.py.py
@version: 1.0
@time: 2021/04/25 15:57:09
@contact: jinxy@pku.edu.cn

auth
"""

from flask import Blueprint

auth = Blueprint('auth', __name__)
from app.auth import views
