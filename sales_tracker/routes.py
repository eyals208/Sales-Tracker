from dataclasses import asdict
import uuid
from flask import(
    Blueprint, 
    render_template, 
    current_app,
    request, 
    session, 
    redirect, 
    url_for, 
    flash
)
from passlib.hash import pbkdf2_sha256
from sales_tracker.forms import SaleForm, RegisterForm, LoginForm
from sales_tracker.models import user_data

pages = Blueprint("pages", __name__, template_folder= "templates", static_folder= "static")


@pages.route("/")
def home():

    if 'email' in session:
        # get data for user from DB
        return render_template("personal_home.html", name = "Eyal.s")
    
    return render_template("home.html")

@pages.route("/register", methods=["GET","POST"])
def register():
    #redirect to home page if logged in
    if session.get('email'): 
        return redirect(url_for(".home"))

    form = RegisterForm()

    if form.validate_on_submit():
        user = user_data(
            _id = uuid.uuid4().hex,
            email= form.email.data,
            name= form.name.data,
            password= pbkdf2_sha256.hash(form.password.data)
        )
        
        current_app.db.user.insert_one(asdict(user))
        flash("Successfully registered","success")

        return redirect(url_for(".home"))

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