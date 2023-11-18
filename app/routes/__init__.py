from flask import Flask
from .main import view as main_view
from .api import api


def register_all_routes(app: Flask):
    app.register_blueprint(main_view)
    app.register_blueprint(api)
