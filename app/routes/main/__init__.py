from flask import Blueprint, render_template

from app.controllers.main import index, hourly, forecast


view = Blueprint("base", __name__, url_prefix="/")

view.route("/")(index)
view.route("/forecast")(forecast)
view.route("/hourly")(hourly)
