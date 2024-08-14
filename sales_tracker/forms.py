from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SubmitField, DateField, EmailField,PasswordField
from wtforms.validators import InputRequired, NumberRange, Email, Length
import datetime

class SaleForm(FlaskForm):
    date = DateField("Date", validators=[InputRequired()], default= datetime.datetime.now())
    product = StringField("Product", validators=[InputRequired()])
    price = FloatField("Price", validators=[InputRequired(), NumberRange(0,1000000,message="Please enter a price between 0 and 1000000")])
    customer = StringField("Costumer", validators=[InputRequired()])
    details = StringField("details")
    submit = SubmitField("Add sale")

class RegisterForm(FlaskForm):
    email = EmailField("Email", validators = [InputRequired(), Email(message="Please enter a valid email address")])
    name = StringField("User name", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired(), Length(min=6,max=12,message="Password must have between 6 to 12 characters")])
    
    submit = SubmitField("Register")

class LoginForm(FlaskForm):
    email = EmailField("Email", validators = [InputRequired(), Email(message="Please enter a valid email address")])
    password = PasswordField("Password", validators=[InputRequired(), Length(min=6,max=12,message="Password must have between 6 to 12 characters")])
    
    submit = SubmitField("Login")
    