''' The idea is to create the database using this file and leave it as a future reference
to look up which tables are in it, type of data within them, etc. 
The new empty database is created as 00_EmptyDatabase.db.'''
import common.dbConnector as dbConnector
import sqlite3 as sql

if __name__ == '__main__':
    # Connect with 'create_database' which is in [Paths] section from .ini file
    [conn, db] = dbConnector.connect_to_db('create_database')

    # Generate tables
    # Main table
    try:
        sql_query = '''CREATE TABLE Main (
                    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                    Titulo TEXT NOT NULL,
                    TituloOriginal TEXT NOT NULL,
                    DiscoID INTEGER NOT NULL,
                    CalidadID INTEGER NOT NULL, 
                    Year INTEGER NOT NULL CHECK(Year>1880),
                    PaisID INTEGER NOT NULL,
                    Duracion INTEGER NOT NULL CHECK(Duracion>=0),
                    Director TEXT NOT NULL,
                    Guion TEXT NOT NULL,
                    FOREIGN KEY (DiscoID) REFERENCES Disco(id)
                    ON DELETE SET NULL ON UPDATE CASCADE,
                    FOREIGN KEY (CalidadID) REFERENCES Calidad(id)
                    ON DELETE SET NULL ON UPDATE CASCADE,
                    FOREIGN KEY (PaisID) REFERENCES Pais(id)
                    ON DELETE SET NULL ON UPDATE CASCADE);'''

        db.execute(sql_query)
        conn.commit()
        print('\"Películas\" table has been created correctly')

    except sql.Error as error:
        print('Error while creating the table \"Películas\"', error)

    # Disco (this approach is called database normalization in sql)
    try:
        sql_query = '''CREATE TABLE Disco (
                    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                    Disco TEXT NOT NULL UNIQUE);'''

        db.execute(sql_query)
        conn.commit()
        print('\"Disco\" table has been created correctly')
    
    except sql.Error as error:
        print('Error while creating the table \"Disco\"', error)

    # Calidad
    try:
        sql_query = '''CREATE TABLE Calidad (
                    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                    Calidad TEXT NOT NULL UNIQUE);'''

        db.execute(sql_query)
        conn.commit()
        print('\"Calidad\" table has been created correctly')
    
    except sql.Error as error:
        print('Error while creating the table \"Calidad\"', error)

    # Idioma
    try:
        sql_query = '''CREATE TABLE Idioma (
                    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                    IdiomaAbreviado TEXT NOT NULL,
                    IdiomaCompleto TEXT NOT NULL);'''

        db.execute(sql_query)
        conn.commit()
        print('\"Idioma\" table has been created correctly')
    
    except sql.Error as error:
        print('Error while creating the table \"Idioma\"', error)

    # Audio_in_file
    try:
        sql_query = '''CREATE TABLE Audio_in_file (
                    pelicula_id INTEGER NOT NULL,
                    idioma_id INTEGER NOT NULL,
                    FOREIGN KEY (pelicula_id) REFERENCES Main(id)
                    ON DELETE CASCADE ON UPDATE CASCADE);'''

        db.execute(sql_query)
        conn.commit()
        print('\"Audio_in_file\" table has been created correctly')
    
    except sql.Error as error:
        print('Error while creating the table \"Audio_in_file\"', error)

    # Subs_in_file
    try:
        sql_query = '''CREATE TABLE Subs_in_file (
                    pelicula_id INTEGER NOT NULL,
                    idioma_id INTEGER NOT NULL,
                    FOREIGN KEY (pelicula_id) REFERENCES Main(id)
                    ON DELETE CASCADE ON UPDATE CASCADE);'''

        db.execute(sql_query)
        conn.commit()
        print('\"Subs_in_file\" table has been created correctly')
    
    except sql.Error as error:
        print('Error while creating the table \"Subs_in_file\"', error)

    # Pais
    try:
        sql_query = '''CREATE TABLE Pais (
                    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                    Pais INTEGER NOT NULL UNIQUE);'''

        db.execute(sql_query)
        conn.commit()
        print('\"Pais\" table has been created correctly')
    
    except sql.Error as error:
        print('Error while creating the table \"Pais\"', error)

    # Género - plantilla
    try:
        sql_query = '''CREATE TABLE Genero (
                    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                    Categoria TEXT NOT NULL,
                    Nombre TEXT NOT NULL);'''

        db.execute(sql_query)
        conn.commit()
        print('\"Genero\" table has been created correctly')
    
    except sql.Error as error:
        print('Error while creating the table \"Genero\"', error)

    # Género_in_file
    try:
        sql_query = '''CREATE TABLE Genero_in_file (
                    pelicula_id INTEGER NOT NULL,
                    genero_id INTEGER NOT NULL,
                    FOREIGN KEY (pelicula_id) REFERENCES Main(id)
                    ON DELETE CASCADE ON UPDATE CASCADE);'''

        db.execute(sql_query)
        conn.commit()
        print('\"Genero_in_file\" table has been created correctly')
    
    except sql.Error as error:
        print('Error while creating the table \"Genero_in_file\"', error)

    db.close()
    conn.close()