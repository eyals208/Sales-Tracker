import pymongo
from dataclasses import asdict
from flask import current_app

from sales_tracker.models import user_data, Sale

def add_new_user(mongo_client, user : user_data):
    '''
        Registers the user to the database
    '''
    mongo_client.user.insert_one(asdict(user))

def get_user(mongo_client, **kwargs):
    '''
        finds a user in the database.
        
        Key word arguments (choose one):
        * 'user_id' - find user by id
        * 'email' - find user by email
    '''
    
    if 'user_id' in kwargs:
        return user_data(**mongo_client.user.find_one({"_id" : kwargs['user_id']}))
    
    if 'email' in kwargs:
        return mongo_client.user.find_one({"email" : kwargs['email']})


def get_user_sales(mongo_client, sales_ids, **kwargs):
    '''
        returns the sales of the given sales IDs list.
        
        Key word arguments:
            Get last X sales:
        * 'max_sales' - the number of sales to return

            Get sales between 2 dates:
        * 'start_date' - the returned sales will be after this date
        * 'end_date' - the returned sales will be before this date
    '''
    if 'max_sales' in kwargs:
        return mongo_client.sales.find({"_id" : {"$in" : sales_ids}}, limit = kwargs['max_sales'], sort = {"date" : pymongo.DESCENDING})
    
    if 'start_date' in kwargs and 'end_date' in kwargs:
        query = {"_id" : {"$in" : sales_ids}, "date" : {"$gte" : kwargs['start_date'], "$lte" : kwargs['end_date']}}
        return mongo_client.sales.find(query, sort = {"date" : pymongo.DESCENDING})


def add_sale(mongo_client , sale : Sale, user_id):
    '''
        Adds a sale to the sales collection, and writes the id of the sale into the list of sales of the user
        
        Parameters:
        * mongo_client - MongoDB client
        * sale - the sale to be save
        * user_id - the id of the user who made the sale
    '''
    mongo_client.sales.insert_one(asdict(sale))
    mongo_client.user.update_one({"_id" : user_id}, {"$push" : {"sales" : sale._id}})