import pymongo
from pymongo.database import Database
from dataclasses import asdict

#from sales_tracker.models import user_data, Sale

def add_new_user(mongo_client : Database, user ):
    '''
        Registers the user to the database
    '''
    mongo_client.user.insert_one(asdict(user))

def get_user(mongo_client : Database, **kwargs):
    '''
        finds a user in the database.
        
        Key word arguments (choose one):
        * 'user_id' - find user by id
        * 'email' - find user by email
    '''
    
    if 'user_id' in kwargs:
        user = mongo_client.user.find_one({"_id" : kwargs['user_id']})
        return user
    
    if 'email' in kwargs:
        return mongo_client.user.find_one({"email" : kwargs['email']})


def delete_user(mongo_client : Database, user_id):
    '''
        Delete the user from the database and all of its sales
    '''
    user = get_user(mongo_client, user_id = user_id)
    if not user:
        raise Exception(f"user not found (id = {user_id})")
    
    sales_list = user['sales']
    delete_sales(mongo_client, sales_list, user_id)
    result = mongo_client.user.delete_one({"_id" : user_id})
    if result.deleted_count != 1:
        raise Exception(f"Failed to delete user (id = {user_id})")    


def get_user_sales(mongo_client : Database, sales_ids, **kwargs):
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


def add_sale(mongo_client : Database, sale , user_id):
    '''
        Adds a sale to the sales collection, and writes the id of the sale into the list of sales of the user
        
        Parameters:
        * mongo_client - MongoDB client
        * sale - the sale to be save
        * user_id - the id of the user who made the sale
    '''
    mongo_client.sales.insert_one(asdict(sale))
    mongo_client.user.update_one({"_id" : user_id}, {"$push" : {"sales" : sale._id}})

def delete_sale(mongo_client : Database, sale_id, user_id):
    '''
        Deletes the sale from the database and removes it from the list of sales of the user specified by user_id
    '''
    result = mongo_client.sales.delete_one({"_id" : sale_id})
    if result.deleted_count != 1:
        raise Exception(f'sale_id: {sale_id} not found')
    
    result = mongo_client.user.update_one({"_id" : user_id}, {"$pull" : {"sales" : sale_id}} )
    if result.modified_count != 1:
        raise Exception(f'Document not found (id: {user_id}) or sale not deleted (id: {sale_id})')
    

def delete_sales(mongo_client : Database, sales_ids, user_id):
    '''
        Deletes the sales from the database and removes them from the list of sales of the user specified by user_id
    '''
    result = mongo_client.sales.delete_many({"_id" : {"$in" :sales_ids}})
    
    result = mongo_client.user.update_one({"_id" : user_id}, {"$pull" : {"sales" : {"$in" :sales_ids}}} )
    if result.modified_count != 1:
        raise Exception(f'Document not found (id: {user_id}) or sale not deleted (ids: {sales_ids})')