from flask import Blueprint, render_template

from app.controllers.main import index


view = Blueprint("base", __name__, url_prefix='/')

view.route("/")(index)
