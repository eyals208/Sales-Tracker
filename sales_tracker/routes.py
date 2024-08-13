from flask import Blueprint, render_template, request
from sales_tracker.forms import SaleForm

pages = Blueprint("pages", __name__, template_folder= "templates", static_folder= "static")


@pages.route("/")
def home():
    return render_template("home.html")

@pages.route("/register")
def register():
    return render_template("register.html")

@pages.route("/sales", methods=["GET","POST"])
def sales():
    form = SaleForm()

    if form.validate_on_submit():
        pass

    return render_template("sales.html", form = form)