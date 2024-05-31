""" Definition of the dbConnector class to connect with the MySQL database.
If there were more than one database, the connector can be updated to take arguments and 
connect to different databases."""

from fastapi import HTTPException, status
from dotenv import load_dotenv
import os
import pymysql as sql
from services.auth import crypt

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

    return connector, cursor


def disconnect_from_db(connector, cursor):
    cursor.close()
    connector.close()


 ###################
 ## USERS METHODS ##
 ###################
def create_user(user: dict):
    [conn, db] = connect_to_db()
    # Query to convert User_rank into its id
    sel_query = f"""SELECT User_ranks.id FROM MovieDB.User_ranks
                    WHERE User_ranks.Name = '{user['user_rank']}'"""
    
    # Hashed password to store in the database for better security
    hashed_password = crypt.hash(user['password'])

    # Full query
    try:
        sql_query = f"""INSERT INTO MovieDB.Users (Name, Password, Email, 
                        RankID, Disabled) VALUES 
                        ('{user['username']}', '{hashed_password}', 
                        '{user['email']}', ({sel_query}), 
                        {user['disabled']});"""

        db.execute(sql_query)
        conn.commit()
    
    except sql.Error as error:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, 
                            detail=f'{error.args[0]}: {error.args[1]}')

    finally:
        disconnect_from_db(conn, db)

    return get_user(user['username'])


def delete_user(user_id: int):
    [conn, db] = connect_to_db()
    
    try:
        sql_query = f"DELETE FROM MovieDB.Users WHERE Users.id={user_id};"

        db.execute(sql_query)
        conn.commit()

    except sql.Error as error:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, 
                            detail=f'{error.args[0]}: {error.args[1]}')
        
    disconnect_from_db(conn, db)

    return f"User with id = {user_id} has been deleted."


def get_all_users():
    [conn, db] = connect_to_db()
    sql_query = f"""SELECT Users.id, Users.Name, Users.Email, 
                User_ranks.Name, Users.Password, Users.Disabled 
                FROM MovieDB.Users 
                INNER JOIN User_ranks ON User_ranks.id = Users.RankID;"""

    db.execute(sql_query)
    res = db.fetchall()

    users_list = [{"id": res[i][0], "username": res[i][1], "email": res[i][2], "user_rank": res[i][3],
                   "password": res[i][4], "disabled": res[i][5]} for i in range(len(res))]

    disconnect_from_db(conn, db)

    return users_list


def get_user(username: str):
    [conn, db] = connect_to_db()
    sql_query = f"""SELECT Users.id, Users.Name, Users.Email, User_ranks.Name, 
                Users.Password, Users.Disabled 
                FROM MovieDB.Users 
                INNER JOIN User_ranks ON User_ranks.id = Users.RankID
                WHERE Users.Name='{username}';"""

    db.execute(sql_query)
    res = db.fetchone()

    if res:
        user = {"id": res[0], "username": res[1], "email": res[2],
                "user_rank": res[3], "password": res[4], "disabled": res[5]}

        disconnect_from_db(conn, db)

        return user
    else:
        disconnect_from_db(conn, db)

        return None


def get_user_by_id(user_id: int):
    [conn, db] = connect_to_db()
    sql_query = f"""SELECT Users.id, Users.Name, Users.Email, User_ranks.Name, 
                Users.Password, Users.Disabled 
                FROM MovieDB.Users 
                INNER JOIN User_ranks ON User_ranks.id = Users.RankID
                WHERE Users.id={user_id};"""

    db.execute(sql_query)
    res = db.fetchone()

    if res:
        user = {"id": res[0], "username": res[1], "email": res[2],
                "user_rank": res[3], "password": res[4], "disabled": res[5]}

        disconnect_from_db(conn, db)

        return user
    else:
        disconnect_from_db(conn, db)

        return None


def update_user(user_id: int, user_mod: dict):
    # Create a 'new_values' dict to filter those optional values left blank by the user.
    # Otherwise, they would overwrite the real values in those fields, leaving them empty. 
    new_values = {k:user_mod[k] for k in user_mod.keys() if user_mod[k] != None}

    [conn, db] = connect_to_db()
    
    # Hashed password to store in the database for better security
    if "Password" in new_values.keys():
        new_values['Password'] = crypt.hash(new_values['Password'])

    set_str = ", ".join([f"Users.{k}='{new_values[k]}'" for k in new_values.keys()])
    set_str = set_str.replace("'True'", "TRUE")
    set_str = set_str.replace("'False'", "FALSE")
    # Full query
    try:
        sql_query = f"UPDATE MovieDB.Users SET {set_str} WHERE Users.id = {user_id};"

        db.execute(sql_query)
        conn.commit()

    except sql.Error as error:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, 
                            detail=f'{error.args[0]}: {error.args[1]}')

    finally:
        disconnect_from_db(conn, db)
 
    return get_user_by_id(user_id)
    

#####################
## GENERAL METHODS ##
#####################
def add_director(director: dict):
    [conn, db] = connect_to_db()

    try:
        sql_query = f"""INSERT INTO MovieDB.Directors (Name, CountryID) 
                        VALUES ('{director['name']}', 
                        (SELECT Countries.id FROM Countries 
                        WHERE Countries.Name = '{director['country']}'));"""
        db.execute(sql_query)
        conn.commit()
    
    except sql.Error as error:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, 
                            detail=f'{error.args[0]}: {error.args[1]}')

    else:
        sql_query = f"""SELECT Directors.id, Directors.Name, Countries.Name FROM MovieDB.Directors
                        INNER JOIN MovieDB.Countries ON Directors.CountryID = Countries.id 
                        WHERE Directors.Name = '{director['name']}';"""

        db.execute(sql_query)
        res = db.fetchone()

        new_director = {"id": res[0], "name": res[1], "country": res[2]}

        return new_director

    finally:
        disconnect_from_db(conn, db)

def add_genre(genre: dict):
    [conn, db] = connect_to_db()
    
    try:
        sql_query = f"""INSERT INTO MovieDB.Genres (Name, CategoryID) 
                    VALUES ('{genre['name']}', 
                    (SELECT Genre_Categories.id FROM MovieDB.Genre_Categories 
                    WHERE Genre_Categories.Name = '{genre['category']}'));"""
        db.execute(sql_query)
        conn.commit()
    
    except sql.Error as error:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, 
                            detail=f'{error.args[0]}: {error.args[1]}')

    else:
        sql_query = f"""SELECT Genres.id, Genres.Name, Genre_Categories.Name 
                        FROM MovieDB.Genres 
                        INNER JOIN Genre_Categories ON Genres.CategoryID = Genre_Categories.id
                        WHERE Genres.Name = '{genre['name']}';"""

        db.execute(sql_query)
        res = db.fetchone()

        new_genre = {"id": res[0], "name": res[1], "category": res[2]}

        return new_genre

    finally:
        disconnect_from_db(conn, db)        


def add_genre_category(category: dict):
    [conn, db] = connect_to_db()

    try:
        sql_query = f"INSERT INTO MovieDB.Genre_Categories (Name) VALUES ('{category['name']}');"
        db.execute(sql_query)
        conn.commit()
    
    except sql.Error as error:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, 
                            detail=f'{error.args[0]}: {error.args[1]}')

    else:
        sql_query = f"""SELECT * FROM MovieDB.Genre_Categories 
                      WHERE Genre_Categories.Name = '{category['name']}';"""
        db.execute(sql_query)
        res = db.fetchone()

        new_category = {"id": res[0], "name": res[1]}

        return new_category

    finally:
        disconnect_from_db(conn, db)


def add_language(language: dict):
    [conn, db] = connect_to_db()

    try:
        sql_query = f"""INSERT INTO MovieDB.Languages (LangShort, LangComplete) 
                    VALUES ('{language['short']}', '{language['complete']}');"""
        db.execute(sql_query)
        conn.commit()
    
    except sql.Error as error:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, 
                            detail=f'{error.args[0]}: {error.args[1]}')

    else:
        sql_query = f"""SELECT * FROM MovieDB.Languages 
                      WHERE Languages.LangShort = '{language['short']}';"""
        db.execute(sql_query)
        res = db.fetchone()

        new_language = {"id": res[0], "short": res[1], "complete": res[2]}

        return new_language

    finally:
        disconnect_from_db(conn, db)


def add_register(table, value):
    [conn, db] = connect_to_db()

    try:
        sql_query = f"INSERT INTO MovieDB.{table} (Name) VALUES ('{value}');"
        db.execute(sql_query)
        conn.commit()
    
    except sql.Error as error:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, 
                            detail=f'{error.args[0]}: {error.args[1]}')
    
    else:
        sql_query = f"SELECT {table}.id, {table}.Name FROM MovieDB.{table} WHERE Name = '{value}';"
        db.execute(sql_query)
        res = db.fetchone()

        new_obj = {"id": res[0], "name": res[1]}

        return new_obj
    
    finally:
        disconnect_from_db(conn, db)


def get_all(table: str):
    [conn, db] = connect_to_db()

    if table == "Genres":
       sql_query = """SELECT Genres.id, Genres.Name, Genre_Categories.Name 
                      FROM MovieDB.Genres
                      INNER JOIN MovieDB.Genre_Categories 
                      ON Genres.CategoryID = Genre_Categories.id;""" 
    elif table == "Directors":      # LEFT JOIN because some Directors have CountryID = None
        sql_query = f"""SELECT Directors.id, Directors.Name,
                        Countries.Name FROM MovieDB.Directors
                        LEFT JOIN MovieDB.Countries ON Directors.CountryID = Countries.id;"""
    else:
        sql_query =f"SELECT * FROM MovieDB.{table};"

    db.execute(sql_query)
    res = db.fetchall()

    if table == "Countries" or table == "Storage" or table == "Qualities":
        obj_list = [{"id":res[i][0], "name":res[i][1]} for i in range(len(res))]
    elif table == "Directors":
        obj_list = [{"id":res[i][0], "name":res[i][1], "country":res[i][2]} for i in range(len(res))]
    elif table == "Genres":
        obj_list = [{"id": res[i][0], "name":res[i][1], "category":res[i][2]} for i in range(len(res))]
    elif table == "Languages":
        obj_list = [{"id": res[i][0], "short": res[i][1], "complete": res[i][2]} for i in range(len(res))]

    disconnect_from_db(conn, db)

    return obj_list


def get_all_films(field: str, order_by: str):
    [conn, db] = connect_to_db()

    sql_query = f"""SELECT Main.id, Main.Title, Main.OriginalTitle, Storage.Name, Qualities.Name, 
                    Main.Year, Countries.Name, Main.Length, Main.Screenplay, Main.Score, Main.Image
                    FROM MovieDB.Main
                    INNER JOIN MovieDB.Storage ON Main.StorageID = Storage.id
                    INNER JOIN MovieDB.Qualities ON Main.QualityID = Qualities.id
                    INNER JOIN MovieDB.Countries ON Main.CountryID = Countries.id
                    ORDER BY Main.{field} {order_by};"""

    db.execute(sql_query)
    res = db.fetchall()

    films = [{"id": res[i][0], "title": res[i][1], "origTitle": res[i][2],
              "storageDevice": res[i][3], "quality": res[i][4], "year": res[i][5],
              "country": res[i][6], "length": res[i][7], "screenplay": res[i][8],
              "score": res[i][9], "img": res[i][10]} for i in range(len(res))]

    disconnect_from_db(conn, db)

    return films


def get_combined(table, filter_col, value):
    '''get_combined will filter the Main table by a defined column and value, and from those filtered rows
    will return the distinct entries find in another desired column. It will return the names and not just IDs.
    For example, will get all different qualities found for a given Storage device, 
    or all countries found for a given quality. 

    - table: The table that contains the information to be retrieved
    - filter_col: The field to filter the Main table by
    - value: The value to filter by.'''

    if table == "Countries":
        col = "CountryID"
    elif table == "Qualities":
        col = "QualityID"
    elif table == "Storage":
        col = "StorageID"

    [conn, db] = connect_to_db()
    sql_query = f"""SELECT DISTINCT {table}.id, {table}.Name
                    FROM MovieDB.Main
                    INNER JOIN MovieDB.{table} ON Main.{col}={table}.id
                    WHERE Main.{filter_col} = {value}
                    ORDER BY {table}.Name;"""

    db.execute(sql_query)
    res = db.fetchall()

    obj_list = [{"id": res[i][0], "name": res[i][1]} for i in range(len(res))]

    disconnect_from_db(conn, db)

    return obj_list


def get_film(film: dict):
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
        storageAux = f" AND Storage.Name = '{film['storageDevice']}'"
        
    elif film['storageDevice'] != "" and flag == 0:
        storageAux = f"Storage.Name = '{film['storageDevice']}'"
        flag = 1

    if film['quality'] != "" and flag == 1:
        qualityAux = f" AND Qualities.Name = '{film['quality']}'"
        
    elif film['quality'] != "" and flag == 0:
        qualityAux = f"Qualities.Name = '{film['quality']}'"
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
        countryAux = f" AND Countries.Name = '{film['country']}'"
        
    elif film['country'] != "" and flag == 0:
        countryAux = f"Countries.Name = '{film['country']}'"
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
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                            detail="You have not filled anything to look for.")

    fields = """Main.id, Main.Title, Main.OriginalTitle, Storage.Name, Qualities.Name, 
                Main.Year, Countries.Name, Main.Length, Main.Screenplay, Main.Score, Main.Image """

    join_str = """INNER JOIN MovieDB.Storage ON Main.StorageID = Storage.id
                  INNER JOIN MovieDB.Qualities ON Main.QualityID = Qualities.id
                  INNER JOIN MovieDB.Countries ON Main.CountryID = Countries.id"""

    condition = titleAux + origTitleAux + storageAux + qualityAux + yearAux + countryAux + \
                lengthAux + screenplayAux + scoreAux

    sql_query = f"SELECT {fields} FROM MovieDB.Main {join_str} WHERE {condition};"
    
    [conn, db] = connect_to_db()
    db.execute(sql_query)
    res = db.fetchall()

    films = [{"id": res[i][0], "title": res[i][1], "origTitle": res[i][2],
              "storageDevice": res[i][3], "quality": res[i][4], "year": res[i][5],
              "country": res[i][6], "length": res[i][7], "screenplay": res[i][8],
              "score": res[i][9], "img": res[i][10]} for i in range(len(res))]
    
    disconnect_from_db(conn, db)

    return films


def get_object(table, value):
    [conn, db] = connect_to_db()
    sql_query = f"SELECT {table}.id FROM MovieDB.{table} WHERE {table}.Name = '{value}';"
    
    db.execute(sql_query)
    res = db.fetchone()

    if res: 
        data = res[0]
    else: 
        data = ""

    disconnect_from_db(conn, db)

    return data