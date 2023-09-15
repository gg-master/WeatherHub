from flask import Flask
from os import getenv

from app.views import register_all_views


def create_app() -> Flask:
    app = Flask(__name__)
    app.config["SECRET_KEY"] = getenv("SECRET_KEY")
    register_all_views(app)
    return app