# app/__init__.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.schemas import init_api
from app.models import bind_app
from app.config import config_by_name

db = SQLAlchemy()


def create_app(config_name="dev"):
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])

    bind_app(app)
    init_api(app)

    return app
