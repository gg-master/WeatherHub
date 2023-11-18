from flask import Blueprint

from app.controllers.api import location_search


api = Blueprint("api", __name__, url_prefix='/api')

api.route("/findLocation")(location_search)
