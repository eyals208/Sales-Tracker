from flask import Blueprint, render_template

pages = Blueprint("pages", __name__, template_folder= "templates", static_folder= "static")


@pages.route("/")
def home():
    return render_template("home.html")