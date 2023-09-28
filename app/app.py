from os import getenv
from flask import Flask

from app.routes import register_all_routes


def create_app() -> Flask:
    app = Flask(__name__)
    app.config["SECRET_KEY"] = getenv("SECRET_KEY")
    register_all_routes(app)
    return app
