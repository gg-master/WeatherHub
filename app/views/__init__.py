from flask import Flask
from .main import view as main_view


def register_all_views(app: Flask):
    app.register_blueprint(main_view)