import pymongo
import os
from pymongo import MongoClient
from dotenv import load_dotenv
import sys
from datetime import datetime

sys.path.append('sales_tracker')
'''
mongo = importlib.import_module("mongo")

print(sys.path)
'''
import mongo
from models import user_data, Sale

load_dotenv()

user_id = "10"
user_email = "an email"

sale_id1 = "0101"
sale_id2 = "0102"

db = MongoClient(os.environ.get("MONGODB_URI")).get_database('sales')
try:
    mongo.delete_user(db, user_id)
except Exception as e:
    print(e)
    pass

user = user_data(user_id, "eyal_yo", "123456789", user_email)

mongo.add_new_user(db, user)
result = mongo.get_user(db, user_id = user_id)

if not result:
    print("failed to retrive user by id")

_user = user_data(**result)
if not (_user._id == user_id and _user.name == "eyal_yo" and _user.password == "123456789"):
    print('Read wrong user from DB')

else:
    result = mongo.get_user(db, email = user_email)
    if not result:
        print("failed to retrive user by email")
    else:
        print("successful read/write user to DB")


for i in range(1,10,1):
    s = Sale(str(i), f'product_{i}',200 * i, datetime(2022,i,5,0,0,0) , datetime.now(), f'customer_{i}')
    mongo.add_sale(db,s, user_id)

result = mongo.get_user(db, user_id = user_id)
user = user_data(**result)
sales_list = user.sales
print(f'sales list: {sales_list}')
sales = mongo.get_user_sales(db,sales_list,max_sales = 5)
print('last 5 sales:')
for sale in sales:
    print(sale)

print('sales between fab - may:')
sales = mongo.get_user_sales(db,sales_list,start_date = datetime(2022,2,5,0,0,0), end_date = datetime(2022,5,5,0,0,0))
for sale in sales:
    print(sale)


mongo.delete_user(db, user_id)
result = mongo.get_user(db, user_id = user_id)
if result:
    print('Failed to delete user')
else:
    print('Successful delete user')

db.client.close()


