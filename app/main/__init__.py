# -*- coding: utf-8 -*-

""" 
@author: Jin.Fish
@file: __init__.py.py
@version: 1.0
@time: 2021/04/25 15:56:58
@contact: jinxy@pku.edu.cn

main
"""

from flask import Blueprint

main = Blueprint('main', __name__)
from app.main import views
