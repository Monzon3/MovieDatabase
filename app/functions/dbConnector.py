''' Definition of the dbConnector class to connect with the MySQL database.
If there were more than one database, the connector can be updated to take arguments and 
connect to different databases.'''

#from bson.objectid import ObjectId
#from datetime import datetime
from fastapi import HTTPException
from dotenv import load_dotenv
import os
import pymysql as sql
#from pytz import timezone

load_dotenv()

def connect_to_db():
    MySQL_hostname = 'db'   # The name of the mysql Docker container
    sql_username = os.getenv("MYSQL_USER")
    sql_password = os.getenv("MYSQL_PASSWORD")
    sql_database = os.getenv("MYSQL_DATABASE")

    # Connect with the database
    connector = sql.connect(host=MySQL_hostname,
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
def add_director(director:dict):
    [conn, db] = connect_to_db()

    sql_query = f'''INSERT INTO MovieDB.Directors (Name, CountryID) 
                    VALUES ('{director['name']}', 
                           (SELECT Countries.id FROM Countries 
                           WHERE Countries.Country = '{director['country']}'));'''
    try:
        db.execute(sql_query)
    
    except sql.Error as error:
        raise HTTPException (status_code = 403, detail=f'{error.args[0]}: {error.args[1]}')

    sql_query = f"""SELECT Directors.id, Directors.Name, Countries.Country FROM MovieDB.Directors
                    INNER JOIN MovieDB.Countries ON Directors.CountryID = Countries.id 
                    WHERE Directors.Name = '{director['name']}';"""
    db.execute(sql_query)
    res = db.fetchone()
    directorInDBFull = {}
    directorInDBFull['id'] = res[0]
    directorInDBFull['name'] = res[1]
    directorInDBFull['country'] = res[2]

    conn.commit()

    db.close()
    conn.close()

    return directorInDBFull

def add_genre(genre:dict):
    [conn, db] = connect_to_db()

    sql_query = f"""INSERT INTO MovieDB.Genres (Name, CategoryID) 
                    VALUES ('{genre['name']}', 
                    (SELECT Genre_Categories.id FROM MovieDB.Genre_Categories 
                    WHERE Genre_Categories.Category = '{genre['category']}'));"""
    print(sql_query)
    try:
        db.execute(sql_query)
    
    except sql.Error as error:
        raise HTTPException (status_code = 403, detail=f'{error.args[0]}: {error.args[1]}')

    sql_query = f"""SELECT Genres.id, Genres.Name, Genre_Categories.Category 
                    FROM MovieDB.Genres 
                    INNER JOIN Genre_Categories ON Genres.CategoryID = Genre_Categories.id
                    WHERE Genres.Name = '{genre['name']}';"""
    print(sql_query)
    db.execute(sql_query)
    res = db.fetchone()
    genreInDBFull = {}
    genreInDBFull['id'] = res[0]
    genreInDBFull['name'] = res[1]
    genreInDBFull['category'] = res[2]

    conn.commit()

    db.close()
    conn.close()

    return genreInDBFull

def add_genre_category(category:dict):
    [conn, db] = connect_to_db()

    sql_query = f"""INSERT INTO MovieDB.Genre_Categories (Category) 
                    VALUES ('{category['name']}');"""
    try:
        db.execute(sql_query)
    
    except sql.Error as error:
        raise HTTPException (status_code = 403, detail=f'{error.args[0]}: {error.args[1]}')

    sql_query = f"""SELECT * FROM MovieDB.Genre_Categories 
                  WHERE Genre_Categories.Category = '{category['name']}';"""
    db.execute(sql_query)
    res = db.fetchone()
    categoryInDB = {}
    categoryInDB['id'] = res[0]
    categoryInDB['name'] = res[1]

    conn.commit()

    db.close()
    conn.close()

    return categoryInDB

def add_language(language:dict):
    [conn, db] = connect_to_db()

    sql_query = f"""INSERT INTO MovieDB.Languages (LangShort, LangComplete) 
                    VALUES ('{language['short']}', '{language['complete']}');"""
    try:
        db.execute(sql_query)
    
    except sql.Error as error:
        raise HTTPException (status_code = 403, detail=f'{error.args[0]}: {error.args[1]}')

    sql_query = f"""SELECT * FROM MovieDB.Languages 
                  WHERE Languages.LangShort = '{language['short']}';"""
    db.execute(sql_query)
    res = db.fetchone()
    languageInDB = {}
    languageInDB['id'] = res[0]
    languageInDB['short'] = res[1]
    languageInDB['complete'] = res[2]

    conn.commit()

    db.close()
    conn.close()

    return languageInDB

def add_register(table, field, value):
    [conn, db] = connect_to_db()

    sql_query = f'''INSERT INTO MovieDB.{table} ({field}) VALUES ('{value}');'''
    try:
        db.execute(sql_query)
    
    except sql.Error as error:
        raise HTTPException (status_code = 403, detail=f'{error.args[0]}: {error.args[1]}')

    sql_query = f"SELECT {table}.id, {table}.{field} FROM MovieDB.{table} WHERE {field} = '{value}';"
    db.execute(sql_query)
    res = db.fetchone()

    conn.commit()

    db.close()
    conn.close()

    return f"{field} '{res[1]}' inserted into '{table}' table with id = {res[0]}"


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


def get_all_films(order_by:str):
    [conn, db] = connect_to_db()
    if order_by == 'Title':
        sql_query = f"""SELECT Main.id, Main.Title, Main.OriginalTitle, Storage.Device, Qualities.Quality, 
                        Main.Year, Countries.Country, Main.Length, Main.Screenplay, Main.Score, Main.Image
                        FROM MovieDB.Main
                        INNER JOIN MovieDB.Storage ON Main.DeviceID = Storage.id
                        INNER JOIN MovieDB.Qualities ON Main.QualityID = Qualities.id
                        INNER JOIN MovieDB.Countries ON Main.CountryID = Countries.id
                        ORDER BY Main.Title;"""
    elif order_by == 'Year':
        sql_query = f"""SELECT Main.id, Main.Title, Main.OriginalTitle, Storage.Device, Qualities.Quality, 
                        Main.Year, Countries.Country, Main.Length, Main.Screenplay, Main.Score, Main.Image
                        FROM MovieDB.Main
                        INNER JOIN MovieDB.Storage ON Main.DeviceID = Storage.id
                        INNER JOIN MovieDB.Qualities ON Main.QualityID = Qualities.id
                        INNER JOIN MovieDB.Countries ON Main.CountryID = Countries.id
                        ORDER BY Main.Year DESC;"""
    elif order_by == 'Score':
        sql_query = f"""SELECT Main.id, Main.Title, Main.OriginalTitle, Storage.Device, Qualities.Quality, 
                        Main.Year, Countries.Country, Main.Length, Main.Screenplay, Main.Score, Main.Image
                        FROM MovieDB.Main
                        INNER JOIN MovieDB.Storage ON Main.DeviceID = Storage.id
                        INNER JOIN MovieDB.Qualities ON Main.QualityID = Qualities.id
                        INNER JOIN MovieDB.Countries ON Main.CountryID = Countries.id
                        ORDER BY Main.Score DESC;"""

    db.execute(sql_query)
    res = db.fetchall()

    films = []
    for i in range(len(res)):
        new_film = {'id': res[i][0],
                    'title': res[i][1],
                    'origTitle': res[i][2],
                    'storageDevice': res[i][3],
                    'quality': res[i][4],
                    'year': res[i][5],
                    'country': res[i][6],
                    'length': res[i][7],
                    'screenplay': res[i][8],
                    'score': res[i][9],
                    'img': res[i][10]}

        films.append(new_film)

    db.close()
    conn.close()

    return films

def get_film(film:dict):
    # First of all, define SQL query depending on filled fields
    flag = 0
    titleAux = ""
    origTitleAux = ""
    storageAux = ""
    qualityAux = ""
    yearAux = ""
    countryAux = ""
    lengthAux = ""
    screenplayAux = ""
    scoreAux = ""

    if film['title'] != "":
        titleAux = f"Title LIKE '%{film['title']}%'"
        flag = 1
    
    if film['origTitle'] != "" and flag == 1:
        origTitleAux = f" AND OriginalTitle LIKE '%{film['origTitle']}%'"
    elif  film['origTitle'] != "" and flag == 0:
        origTitleAux = f"OriginalTitle LIKE '%{film['origTitle']}%'"
        flag = 1

    if film['storageDevice'] != "" and flag == 1:
        storageAux = f" AND Storage.Device = '{film['storageDevice']}'"
        
    elif film['storageDevice'] != "" and flag == 0:
        storageAux = f"Storage.Device = '{film['storageDevice']}'"
        flag = 1

    if film['quality'] != "" and flag == 1:
        qualityAux = f" AND Qualities.Quality = '{film['quality']}'"
        
    elif film['quality'] != "" and flag == 0:
        qualityAux = f"Qualities.Quality = '{film['quality']}'"
        flag = 1

    if film['year1'] != None and film['year2'] == None and flag == 1:
        yearAux = f" AND Year = {film['year1']}"
    elif  film['year1'] != None and film['year2'] == None and flag == 0:
        yearAux = f"Year = {film['year1']}"
        flag = 1
    elif film['year1'] != None and film['year2'] != None and flag == 1:
        yearAux = f" AND Year BETWEEN {film['year1']} AND {film['year2']}"
    elif film['year1'] != None and film['year2'] != None and flag == 0:
        yearAux = f"Year BETWEEN {film['year1']} AND {film['year2']}"
        flag = 1

    if film['country'] != "" and flag == 1:
        countryAux = f" AND Countries.Country = '{film['country']}'"
        
    elif film['country'] != "" and flag == 0:
        countryAux = f"Countries.Country = '{film['country']}'"
        flag = 1

    if film['length'] != "":
        if film['length'] == "Cortos":
            lengthAux = f"Main.Length BETWEEN 0 AND 30"
        elif film['length'] == "Menos de 80 minutos":
            lengthAux = f"Main.Length BETWEEN 31 AND 80"
        elif film['length'] == "90 minutos":
            lengthAux = f"Main.Length BETWEEN 81 AND 105"
        elif film['length'] == "120 minutos":
            lengthAux = f"Main.Length BETWEEN 106 AND 135"
        elif film['length'] == "Entre 120 y 180 minutos":
            lengthAux = f"Main.Length BETWEEN 121 AND 180"
        elif film['length'] == "Más de 180 minutos":
            lengthAux = f"Main.Length > 181" 

        if flag == 1:
            lengthAux = " AND " + lengthAux 
        else:
            flag = 0

    if film['screenplay'] != "" and flag == 1:
        screenplayAux = f" AND Screenplay LIKE '%{film['screenplay']}%'"
    elif  film['screenplay'] != "" and flag == 0:
        screenplayAux = f"screenplay LIKE '%{film['screenplay']}%'"
        flag = 1

    if film['score1'] != None and film['score2'] == None and flag == 1:
        scoreAux = f" AND Score = {film['score1']}"
    elif  film['score1'] != None and film['score2'] == None and flag == 0:
        scoreAux = f"Score = {film['score1']}"
        flag = 1
    elif film['score1'] != None and film['score2'] != None and flag == 1:
        scoreAux = f" AND Score BETWEEN {film['score1']} AND {film['score2']}"
        flag = 1
    elif film['score1'] != None and film['score2'] != None and flag == 0:
        scoreAux = f"Score BETWEEN {film['score1']} AND {film['score2']}"

    if titleAux == "" and origTitleAux == "" and storageAux == "" and qualityAux == "" and \
       yearAux == "" and countryAux == "" and lengthAux == "" and scoreAux == "" \
       and screenplayAux == "": 
        raise HTTPException (status_code = 403, detail="You have not filled anything to look for.")

    fields = """Main.id, Main.Title, Main.OriginalTitle, Storage.Device, Qualities.Quality, 
                Main.Year, Countries.Country, Main.Length, Main.Screenplay, Main.Score, Main.Image """

    join_str = """INNER JOIN MovieDB.Storage ON Main.DeviceID = Storage.id
                  INNER JOIN MovieDB.Qualities ON Main.QualityID = Qualities.id
                  INNER JOIN MovieDB.Countries ON Main.CountryID = Countries.id"""

    sql_query = f"SELECT {fields} FROM MovieDB.Main {join_str} WHERE " + titleAux + origTitleAux + \
                storageAux + qualityAux + yearAux + countryAux + lengthAux + screenplayAux + \
                scoreAux + (";")
    print(sql_query)
    [conn, db] = connect_to_db()
    db.execute(sql_query)
    res = db.fetchall()

    films = []
    for i in range(len(res)):
        new_film = {'id': res[i][0],
                    'title': res[i][1],
                    'origTitle': res[i][2],
                    'storageDevice': res[i][3],
                    'quality': res[i][4],
                    'year': res[i][5],
                    'country': res[i][6],
                    'length': res[i][7],
                    'screenplay': res[i][8],
                    'score': res[i][9],
                    'img': res[i][10]}
        films.append(new_film)
    
    db.close()
    conn.close()

    return films

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