# -*- coding: utf-8 -*-

""" 
@author: Jin.Fish
@file: views.py
@version: 1.0
@time: 2021/04/25 16:02:36
@contact: jinxy@pku.edu.cn

auth view
"""

from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from app.auth import auth
from app import db
from app.models import User

# 登陆
@auth.route('/login.html', methods=['GET', 'POST'])
def login():
    if request.form:
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user is not None and user.verify_password(password):
            login_user(user, False)
            next_url = request.args.get('next')
            if next_url is None or not next_url.startswith('/'):
                next_url = url_for('main.index')
            return redirect(next_url)
        flash('Invalid username or password.')
    return render_template('auth/login.html')


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.index'))
