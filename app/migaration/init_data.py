# -*- coding: utf-8 -*-

""" 
@author: Jin.Fish
@file: init_data.py
@version: 1.0
@time: 2021/04/20 04:27:49
@contact: jinxy@pku.edu.cn

增加用户功能
"""

from app import db
from app.models import User
from disruptive import app
app.app_context().push()

u = User()
u.password = 'jxy1107'
u.username = 'jxy'
u.role_id = 2
print(u.verify_password('jxy1107'))
print(u.verify_password('jxy1109'))

db.session.add(u)
db.session.commit()
