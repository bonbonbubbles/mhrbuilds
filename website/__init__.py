from flask_pymongo import PyMongo
from flask import Flask
from flask import session
from flask_wtf import CSRFProtect
import os
from dotenv import load_dotenv

def create_app():
    app = Flask(__name__)
    app.config['SESSION_TYPE'] = 'filesystem'
    SECRET_KEY = os.urandom(32)
    app.config['SECRET_KEY'] = SECRET_KEY

    load_dotenv()

    csrf = CSRFProtect()
    csrf.init_app(app)

    with app.app_context():
        from .database import db
        from .view_gear import view_gear
        from .auth import auth
        from .view import view
        from .gearsets import gearsets

        app.register_blueprint(view_gear, url_prefix='/')
        app.register_blueprint(auth, url_prefix='/')
        app.register_blueprint(view, url_prefix='/')
        app.register_blueprint(gearsets, url_prefix='/')

    return app