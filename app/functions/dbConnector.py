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
    sql_username = os.getenv("MYSQL_USER")
    sql_password = os.getenv("MYSQL_PASSWORD")
    sql_database = os.getenv("MYSQL_DATABASE")

    # Connect with the database
    connector = pymysql.connect(host=MySQL_hostname,
                        port=3306, 
                        user=sql_username,
                        passwd=sql_password, 
                        db=sql_database)

    cursor = connector.cursor()
    print(f'Connected to database \'{sql_database}\' \n')                                       

    return connector, cursor

 ###################
 ## USERS METHODS ##
 ###################
def create_user(user:dict):
    [conn, db] = connect_to_db()
    sql_query = f'''INSERT INTO MovieDB.Users (Name, Password, Email, 
                    User_rank, Disabled, Deleted) VALUES 
                    ("{user['username']}", "{user['password']}", 
                    "{user['email']}", "{user['user_rank']}", 
                    {user['disabled']}, {user['deleted']});'''

    db.execute(sql_query)
    conn.commit()

    db.close()
    conn.close()

    return get_user(user['username'])

def get_user(user:str):
    [conn, db] = connect_to_db()
    sql_query = f'''SELECT Name, Email, User_rank, 
                Disabled, Deleted FROM MovieDB.Users
                WHERE Name="{user}";'''

    db.execute(sql_query)
    res = db.fetchone()

    if res:
        user = {'username': res[0],
                'email': res[1],
                'user_rank': res[2],
                'disabled': res[3],
                'deleted': res[4]}

    db.close()
    conn.close()

    return user


def get_all_users():
    [conn, db] = connect_to_db()
    sql_query =f'''SELECT id, Name, Email, User_rank, 
                Disabled, Deleted FROM MovieDB.Users;'''

    db.execute(sql_query)
    res = db.fetchall()

    users_list = []
    for i in range(len(res)):
        users_list.append(
            {'id': res[i][0],
             'username': res[i][1],
             'email': res[i][2],
             'user_rank': res[i][3],
             'disabled': res[i][4],
             'deleted': res[i][5]})

    db.close()
    conn.close()

    return users_list

#####################
## GENERAL METHODS ##
#####################
def delete_register(id:int, table:str):
    [conn, db] = connect_to_db()

    # Get info of the user to delete
    db.execute(f'''SELECT Name FROM MovieDB.Users WHERE id="{id}";''')
    deleted_user = get_user(db.fetchone()[0])

    db.execute(f'''DELETE FROM {table} WHERE id={id};''')
    conn.commit()

    db.close()
    conn.close()

    return deleted_user

def get_all(table:str):
    [conn, db] = connect_to_db()
    sql_query =f'''SELECT * FROM MovieDB.{table};'''
    print(sql_query)

    db.execute(sql_query)
    res = db.fetchall()

    obj_list = [res[i][1] for i in range(len(res))]

    db.close()
    conn.close()

    return obj_list

def get_all_genres():
    [conn, db] = connect_to_db()
    sql_query = '''SELECT MovieDB.Genres.Name, MovieDB.Genre_Categories.Category 
                   FROM MovieDB.Genres
                   INNER JOIN MovieDB.Genre_Categories 
                   ON MovieDB.Genres.CategoryID = MovieDB.Genre_Categories.id;'''

    db.execute(sql_query)
    res = db.fetchall()
    
    genres_list = [('[' + str(res[i][1]) + '] ' + str(res[i][0])) for i in range(len(res))]

    db.close()
    conn.close()

    return genres_list