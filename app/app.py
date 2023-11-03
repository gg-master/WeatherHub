import logging
from os import getenv
from flask import Flask

from app.routes import register_all_routes

# logging.basicConfig(
#     level=logging.DEBUG,
#     format='%(asctime)s %(levelname)s %(name)s %(message)s',
#     # filename=Config.APP_LOG,
#     # encoding='utf-8',
# )

def create_app() -> Flask:
    app = Flask(__name__)
    app.config["SECRET_KEY"] = getenv("SECRET_KEY")
    register_all_routes(app)
    return app
