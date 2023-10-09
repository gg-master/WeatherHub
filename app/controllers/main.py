from flask import render_template


async def index():
    return render_template("index.html")
