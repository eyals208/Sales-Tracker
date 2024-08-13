from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SubmitField, DateField
from wtforms.validators import InputRequired, NumberRange
import datetime

class SaleForm(FlaskForm):
    date = DateField("Date", validators=[InputRequired()], default= datetime.datetime.now())
    product = StringField("Product", validators=[InputRequired()])
    price = FloatField("Price", validators=[InputRequired(), NumberRange(0,1000000,message="Please enter a price between 0 and 1000000")])
    customer = StringField("Costumer", validators=[InputRequired()])
    details = StringField("details")
    submit = SubmitField("Add sale")
    