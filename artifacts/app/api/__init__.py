# app/api/__init__.py

from flask import Flask
from flask_restx import Api
from app.routes import register_routes  #  dynamically registers all routes


def init_api(app: Flask) -> Api:
    api = Api(
        app,
        title=app.config["API_TITLE"],  # dynamic title from config
        version=app.config["API_VERSION"],  # dynamic version
        description=app.config["API_DESCRIPTION"],  # doc description
        authorizations=app.config[
            "API_AUTHORIZATIONS"
        ],  # auth schemes (JWT, basic, etc.)
    )

    register_routes(api)  #  Auto-register routes from app/api/routes

    return api
