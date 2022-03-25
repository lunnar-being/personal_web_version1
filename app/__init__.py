import os
import logging
from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user

db = SQLAlchemy(session_options={"autoflush": False})
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
from util import logging

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    login_manager.init_app(app)

    from app.main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from app.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    from app.models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from app.api import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api')

    return app
