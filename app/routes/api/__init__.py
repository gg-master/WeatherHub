from flask import Blueprint

from app.controllers.api import suggest_geo


api = Blueprint("api", __name__, url_prefix='/api')

api.route("/suggest-geo")(suggest_geo)
