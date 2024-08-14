from flask import Blueprint, render_template, request, session
from sales_tracker.forms import SaleForm, RegisterForm, LoginForm

pages = Blueprint("pages", __name__, template_folder= "templates", static_folder= "static")


@pages.route("/")
def home():

    if 'email' in session:
        # get data for user from DB
        return render_template("personal_home.html", name = "Eyal.s")
    
    return render_template("home.html")

@pages.route("/register", methods=["GET","POST"])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        pass

    return render_template("register.html", form = form)

@pages.route("/login", methods=["GET","POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        pass

    return render_template("login.html", form = form)

@pages.route("/add_sale", methods=["GET","POST"])
def sales():
    form = SaleForm()

    if form.validate_on_submit():
        pass

    return render_template("add_sale.html", form = form)