from dataclasses import asdict
import uuid
import pymongo
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
from datetime import datetime, time
from passlib.hash import pbkdf2_sha256
from sales_tracker.forms import SaleForm, RegisterForm, LoginForm
from sales_tracker.models import user_data, Sale

pages = Blueprint("pages", __name__, template_folder= "templates", static_folder= "static")

MAX_RECENT_SALES = 5

@pages.route("/")
def home():

    if 'email' in session:
        # get data for user from DB
        user = user_data(**current_app.db.user.find_one({"_id" : session['user_id']}))
        user_sales = current_app.db.sales.find({"_id" : {"$in" : user.sales}}, limit = MAX_RECENT_SALES, sort = {"date" : pymongo.DESCENDING})

        return render_template("personal_home.html", name = session['user_name'], sales = user_sales )
    
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
        email = form.email.data
        user = current_app.db.user.find_one({"email" : email})
        if not user:
            flash("Incorrect user credentails", category= "danger")
            return redirect(url_for(".login"))
        user = user_data(**user)

        if user and pbkdf2_sha256.verify(form.password.data , user.password):
            session['email'] = user.email
            session['user_name'] = user.name
            session['user_id'] = user._id
            return redirect(url_for(".home"))
        
        flash("Incorrect user credentails", category= "danger")

    return render_template("login.html", form = form)

@pages.route("/logout")
def logout():
    session.clear()
    return redirect(url_for(".home"))


@pages.route("/add_sale", methods=["GET","POST"])
def sales():
    form = SaleForm()

    if form.validate_on_submit():
        sale = Sale(
            _id = uuid.uuid4().hex,
            product= form.product.data,
            cost= form.price.data,
            date= datetime.combine(form.date.data, time.min),
            upload_time= datetime.now(),
            customer= form.customer.data
        )
        
        current_app.db.sales.insert_one(asdict(sale))
        current_app.db.user.update_one({"_id" : session["user_id"]}, {"$push" : {"sales" : sale._id}})
        
        form_new = SaleForm(formdata = None)
        flash("Added successfully","success")
        return render_template("add_sale.html", form = form_new)

    return render_template("add_sale.html", form = form)

@pages.route("/sales_view")
def sales_view():
    
	return render_template("sales_view.html")