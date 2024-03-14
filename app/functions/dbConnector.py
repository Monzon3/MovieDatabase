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

    db.execute(sql_query)
    res = db.fetchall()

    if table != 'Languages':
        obj_list = [res[i][1] for i in range(len(res))]
    elif table == 'Languages':
        obj_list = {res[i][2]:res[i][1] for i in range(len(res))}

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


def get_all_movies(order_by:str):
    [conn, db] = connect_to_db()
    if order_by == 'Title':
        sql_query = f'''SELECT Main.id, Main.Title, Main.OriginalTitle, Storage.Device, Qualities.Quality, 
                        Main.Year, Countries.Country, Main.Length, Main.Screenplay, Main.Score, Main.Image
                        FROM MovieDB.Main
                        INNER JOIN MovieDB.Storage ON Main.DeviceID = Storage.id
                        INNER JOIN MovieDB.Qualities ON Main.QualityID = Qualities.id
                        INNER JOIN MovieDB.Countries ON Main.CountryID = Countries.id
                        ORDER BY Main.Title;'''
    elif order_by == 'Year':
        sql_query = f'''SELECT Main.id, Main.Title, Main.OriginalTitle, Storage.Device, Qualities.Quality, 
                        Main.Year, Countries.Country, Main.Length, Main.Screenplay, Main.Score, Main.Image
                        FROM MovieDB.Main
                        INNER JOIN MovieDB.Storage ON Main.DeviceID = Storage.id
                        INNER JOIN MovieDB.Qualities ON Main.QualityID = Qualities.id
                        INNER JOIN MovieDB.Countries ON Main.CountryID = Countries.id
                        ORDER BY Main.Year DESC;'''
    elif order_by == 'Score':
        sql_query = f'''SELECT Main.id, Main.Title, Main.OriginalTitle, Storage.Device, Qualities.Quality, 
                        Main.Year, Countries.Country, Main.Length, Main.Screenplay, Main.Score, Main.Image
                        FROM MovieDB.Main
                        INNER JOIN MovieDB.Storage ON Main.DeviceID = Storage.id
                        INNER JOIN MovieDB.Qualities ON Main.QualityID = Qualities.id
                        INNER JOIN MovieDB.Countries ON Main.CountryID = Countries.id
                        ORDER BY Main.Score DESC;'''

    db.execute(sql_query)
    res = db.fetchall()

    movies = []
    for i in range(len(res)):
        new_movie = {'id': res[i][0],
                     'title': res[i][1],
                     'origTitle': res[i][2],
                     'storage_device': res[i][3],
                     'quality': res[i][4],
                     'year': res[i][5],
                     'country': res[i][6],
                     'length': res[i][7],
                     'screenplay': res[i][8],
                     'score': res[i][9],
                     'img': res[i][10]}

        movies.append(new_movie)

    db.close()
    conn.close()

    return movies


def get_combined(table, col, filter_col, value):
    '''get_combined will filter the Main table by a defined column and value, and from those filtered rows
    will return the distinct entries find in another desired column. It will return the names and not just IDs.
    For example, will get all different qualities found for a given Storage device, 
    or all countries found for a given quality. 

    - table: The table that contains the information to be retrieved
    - col: The name of the column to retrieved its distinct values
    - filter_col: The field to filter the Main table by
    - value: The value to filter by.'''

    [conn, db] = connect_to_db()
    sql_query = f'''SELECT DISTINCT {table}.{col}
                    FROM MovieDB.Main
                    INNER JOIN MovieDB.{table} ON Main.{col}ID={table}.id
                    WHERE Main.{filter_col} = {value}
                    ORDER BY {table}.{col};'''
    print(sql_query)

    db.execute(sql_query)
    res = db.fetchall()

    if res:
        obj_list = [res[i][0] for i in range(len(res))]

    db.close()
    conn.close()

    return obj_list


def get_object(table, field, value):
    [conn, db] = connect_to_db()
    sql_query = f'''SELECT {table}.id FROM MovieDB.{table} WHERE {table}.{field} = "{value}";'''
    
    db.execute(sql_query)
    res = db.fetchone()

    if res: data = res[0]
    else: data = ''

    db.close()
    conn.close()

    return data