from flask import Blueprint, render_template

from app.controllers.main import index, hourly


view = Blueprint("base", __name__, url_prefix='/')

view.route("/")(index)
view.route("/forecast")(index)
view.route("/hourly")(hourly)