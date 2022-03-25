# -*- coding: utf-8 -*-

""" 
@author: Jin.Fish
@file: decorators.py
@version: 1.0
@time: 2021/05/03 23:21:24
@contact: jinxy@pku.edu.cn

decorators
"""

from functools import wraps
from flask import abort
from flask_login import current_user


def permission_required(permission):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.can(permission):
                abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator
