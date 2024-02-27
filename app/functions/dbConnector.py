''' Definition of the dbConnector class to connect with the MySQL database.
If there were more than one database, the connector can be updated to take arguments and 
connect to different databases.'''

#from bson.objectid import ObjectId
#from datetime import datetime
#from fastapi import HTTPException
from dotenv import load_dotenv
import os
import pymysql
#from pytz import timezone

load_dotenv()

def connect_to_db():
    MySQL_hostname = 'db'   # The name of the mysql Docker container
    sql_username = os.getenv("SQL_ADMIN_USERNAME")
    sql_password = os.getenv("SQL_ADMIN_PASSWORD")
    sql_database = os.getenv("MYSQL_DB")

    # Connect with the database
    connector = pymysql.connect(host=MySQL_hostname,
                        port=3306, 
                        user=sql_username,
                        passwd=sql_password, 
                        db=sql_database)

    cursor = connector.cursor()
    print(f'Connected to database \'{sql_database}\' \n')                                       

    return connector, cursor


def get_user(user):
    [conn, db] = dbConnector.connect_to_db()
    sql_query = '''SELECT Users.Name, Users.Password, Users.Email FROM MovieDB.Users
                WHERE Users.Name={user}'''

    db.execute(sql_query)
    return db.fetchone()


#    # General methods for objects
#    def check_and_createObj(self, collection: str, param:str, value: str, obj:dict):
#        '''
#        This is a generic function to check whether a new object is already in the database or not, 
#        before inserting it.
#
#        Currently it can only be used for cars and usages, since all other objects have more complex
#        checking methods and need a specific connector class of their own. 
#        
#        If the check is OK, the create_obj function is called.
#        '''
#        if self.get_object(collection, param, value) != None:
#            raise HTTPException(status_code=403, 
#                  detail=f"There is already a '{collection}' entry with '{param}' = '{value}' in the database")
#
#        else:
#            return self.create_obj(collection, param, obj)
#
#
#    def check_and_updateObj(self, collection: str, param: str, original_value: str, new_data: dict):
#        # First of all, check if the 'original_value' introduced by the user for the param 'param'
#        # is actually an object within 'collection' collection in the database
#        if self.get_object(collection, param, original_value) == None:
#            raise HTTPException(status_code=404,
#            detail=f"There is no object in '{collection}' collection with '{param}'='{original_value}'")
#
#        # Create a 'new_values' dict to filter those optional values left blank by the user.
#        # Otherwise, they would overwrite the real values in those fields, leaving them empty. 
#        new_values = {k:new_data[k] for k in new_data.keys() if new_data[k] != None}
#
#        # Check the 'param' is unique and if so, insert it into the database:
#        condition1 = param in new_values.keys()
#        condition2 = self.get_object(collection, param, new_data[param]) != None
#
#        if condition1 and condition2:
#            raise HTTPException(status_code=403,
#            detail=f"There is already a '{collection}' entry with '{param}'='{new_data[param]}' in the database")
#
#        return self.update_object(collection, param, original_value, new_values)
#
#    def create_obj(self, collection: str, param:str, obj:dict):
#        obj['date_created'] = datetime.now(timezone('Europe/Madrid'))
#        res = self.dbName[collection].insert_one(obj)
#
#        return f"""A new entry with '{param}' = '{obj[param]}' inserted in '{collection}' collection with _id '{res.inserted_id}'"""
#
#
#    # Instead of deleting an object, its field "deleted" is set to True.
#    def delete_object(self, obj: str, collection: str):
#        if collection == 'users':
#            new_values = {"$set": {"deleted": True, "disabled": True}}
#        else:
#            new_values = {"$set": {"deleted": True}}
#
#        query = {"_id": ObjectId(obj)}
#        if self.dbName[collection].find_one(query) == None:
#            raise HTTPException(status_code=404,
#            detail=f"There is no entry in '{collection}' collection with '_id' = '{obj}' in the database")
#
#        res = self.dbName[collection].update_one(query, new_values)
#        if res.modified_count != 0:
#            msg = f"Object {obj} has been deleted from '{collection}' collection."
#
#        else:
#            msg = f"Object {obj} could not be deleted from '{collection}' collection."
#
#        return {"result": msg}
#
#
#    def get_all_objects(self, collection: str, user_rank: str):
#        if user_rank != 'admin':
#            query = {'deleted': False}
#        else:
#            query = {}
#
#        all_objects = [i for i in self.dbName[collection].find(query)]
#        for obj in all_objects:
#            obj['id'] = str(obj['_id'])   # Converts ObjectId to str and changes name of key for model usage
#            del obj['_id']    
#
#        return all_objects
#
#
#    def get_object(self, collection: str, param: str, value: str):
#        if param == "_id":
#            value = ObjectId(value)
#
#        result = self.dbName[collection].find_one({param: value})
#        if result != None:
#            result['id'] = str(result['_id'])   # Converts ObjectId to str and changes name of key for model usage
#            del result['_id']
#
#            return result
#        else:
#            return None
#
#
#    def update_object(self, collection: str, param: str, original_value: str, new_data: dict):
#        res = self.dbName[collection].update_one({param: original_value}, {"$set": new_data})
#
#        if len(new_data.keys()) == 1:
#            aux1 = "Value"
#            aux2 = "has been"
#        else:
#            aux1 = "Values"
#            aux2 = "have been"
#
#        if res.modified_count != 0:
#            msg = f"{aux1} {new_data} {aux2} updated for entry '{original_value}' in collection '{collection}'."
#
#        else:
#            msg = f"{aux1} {new_data} could not be updated for entry '{original_value}' in collection '{collection}'."
#
#        return {'result': msg}