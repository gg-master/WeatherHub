from os import getenv
from flask import Flask
from flask_moment import Moment

from app.routes import register_all_routes
from app.utils.logging import setup_logging_queue


def create_app() -> Flask:
    setup_logging_queue()

    app = Flask(__name__, static_url_path="/")
    app.config["SECRET_KEY"] = getenv("SECRET_KEY")
    moment = Moment(app)
    register_all_routes(app)
    return app
