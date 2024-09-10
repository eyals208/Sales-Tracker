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
import sales_tracker.mongo as mongo

pages = Blueprint("pages", __name__, template_folder= "templates", static_folder= "static")

MAX_RECENT_SALES = 7

@pages.route("/")
def home():

    if 'email' in session:
        # get data for user from DB
        user = user_data(**mongo.get_user(current_app.db, user_id = session['user_id']))
        user_sales = mongo.get_user_sales(current_app.db, user.sales, max_sales = MAX_RECENT_SALES)

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
        
        mongo.add_new_user(current_app.db, user)
        flash("Successfully registered","success")

        return redirect(url_for(".home"))

    return render_template("register.html", form = form)

@pages.route("/login", methods=["GET","POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        email = form.email.data
        user = mongo.get_user(current_app.db, email = email)
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
        
        mongo.add_sale(current_app.db, sale, session['user_id'])
        
        form_new = SaleForm(formdata = None)
        flash("Added successfully","success")
        return render_template("add_sale.html", form = form_new)

    return render_template("add_sale.html", form = form)


@pages.route("/sales_view", methods = ["GET","POST"])
def sales_view():

    month = request.args.get('month')
    year = request.args.get('year')
    if year and month:
        year = int(year)
        month = int(month)
        if year < 1990 or year > 2050 or month < 1 or month > 12:
            year = datetime.now().year
            month = datetime.now().month
    else:
        year = datetime.now().year
        month = datetime.now().month

    year = int(year)
    month = int(month)
    start_date = datetime(year,month,1)
    end_date = datetime(year,month+1,1) if month < 12 else datetime(year+1,1,1)
    user = user_data(**mongo.get_user(current_app.db, user_id =  session['user_id']))
    sales = mongo.get_user_sales(current_app.db, user.sales, start_date = start_date, end_date = end_date)
    
    return render_template("sales_view.html", month = start_date.strftime("%B"), sales = sales,date = {'month': month, 'year':year})