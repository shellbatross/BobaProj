# 3rd-party packages
from flask import Flask, render_template, request, redirect, url_for
from flask_mongoengine import MongoEngine
from flask_login import (
    LoginManager,
    current_user,
    login_user,
    logout_user,
    login_required,
)
from flask_bcrypt import Bcrypt
from werkzeug.utils import secure_filename
from flask_mail import Mail, Message

# stdlib
from datetime import datetime
import os

# local
from .client import MovieClient


db = MongoEngine()
login_manager = LoginManager()
bcrypt = Bcrypt()
mail = Mail()
movie_client = MovieClient()

from .users.routes import users
from .boba.routes import bobas


def page_not_found(e):
    return render_template("404.html"), 404


def create_app(test_config=None):
    app = Flask(__name__)

    app.config.from_pyfile("config.py", silent=False)
    if test_config is not None:
        app.config.update(test_config)

    app.config['MAIL_SERVER']='smtp.gmail.com'
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USERNAME'] = 'bobatea.shop1@gmail.com'
    app.config['MAIL_PASSWORD'] = 'urvktqbhbwssrjuz'
    app.config['MAIL_USE_TLS'] = False
    app.config['MAIL_USE_SSL'] = True

    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)
    mail.init_app(app)

    app.register_blueprint(users)
    app.register_blueprint(bobas)
    app.register_error_handler(404, page_not_found)



    login_manager.login_view = "users.login"

    return app
