from flask import Blueprint, render_template


view = Blueprint("base", __name__, url_prefix='/')

@view.route("/")
def index():
    return render_template("index.html")