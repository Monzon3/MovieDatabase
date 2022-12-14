''' After the new database structure has been created and the reference tables populated, 
the real data from the Access database is imported into the new "Main" table. 

To do this, all reference tables should be looked up in order to exchange the values from
the original database for the new corresponding IDs.

After this is done, the tables Audio_in_file, Genre_in_file and Subs_in_file
are populated using the information from the original database and the reference tables.

Before running this script, copy the newly created '01_ImportDatabase.db' to keep a copy
and rename it /Test.db.'''

from configparser import ConfigParser
import common.dbConnector as dbConnector
import pandas as pd
import sqlite3 as sql


def import_df_to_db(dataFrame, connector, cursor):
    ''' After finding the new ID values for the fields 'Calidad', 'Disco' and 'Pais'
    the whole database from the Excel file is imported into the new SQL database.'''

    for i in range(dataFrame.shape[0]):
        # ' are replace by '' so SQL is able to process them properly
        tit = dataFrame.loc[i, 'Titulo'].replace("\'","\'\'")
        origTit = dataFrame.loc[i, 'TituloOriginal'].replace("\'","\'\'")
        disc = dataFrame.loc[i, 'Disco']
        qt = dataFrame.loc[i, 'Calidad']
        year = dataFrame.loc[i, 'Año']
        country = dataFrame.loc[i, 'Pais']
        dur = dataFrame.loc[i, 'Duracion']
        dir = dataFrame.loc[i, 'Director'].replace("\'","\'\'")
        script = dataFrame.loc[i, 'Guion'].replace("\'","\'\'")
        sql_query = f"""INSERT INTO Main (Titulo, TituloOriginal, DiscoID, CalidadID, Year,
                    PaisID, Duracion, Director, Guion) 
                    VALUES 
                    (\'{tit}\', \'{origTit}\', {disc}, {qt}, {year}, 
                    {country}, {dur}, \'{dir}\', \'{script}\')"""

        try:
            cursor.execute(sql_query)
            connector.commit()
        
        except sql.Error as error:
            print(f'Error during the execution of {sql_query}', error)


def import_genres(movie_id, value, connector, cursor):
    ''' This function will read all values from 'Genero' column
    in the Excel database, split them using the ',' character in the movies
    with more than one genre and then populate the table Genero_in_file with the genres found.'''
    
    # Obtain corresponding GeneroID from the new 'Genero' table for each genre in 'value'
    if value != '-':
        genres = value.split(',')[0:-1]    # value always ends with ',' so the last element is not needed

        for i in genres:
            # All genres have a category defined between brackets that is not needed for now
            pos1 = i.find('[')
            pos2 = i.find(']')
            category = i[(pos1 + 1):pos2]
            genre = i[(pos2 + 2):]

            # Some genres have changed in the new database, so to find them:
            if genre == 'Palma de Oro': genre = 'Cannes - Palma de Oro'
            if genre == 'Mejor película' and category == 'Premios - Goya': 
                genre = 'Goya - Mejor película'
            if genre == 'Mejor director': genre = 'Oscars - Mejor director'
            if genre == 'Mejor extranjera': genre = 'Oscars - Mejor extranjera'
            if genre == 'Mejor fotografía': genre = 'Oscars - Mejor fotografía'
            if genre == 'Mejor película' and category == 'Premios - Óscars':
                genre = 'Oscars - Mejor película'

            sql_query = f'SELECT id FROM Genero WHERE Nombre = \'{genre}\''
            res = db.execute(sql_query).fetchone()
            
            if res != None:
                sql_query = f'''INSERT INTO Genero_in_file (pelicula_id, genero_id) 
                            VALUES ({movie_id}, {res[0]})'''
                try:
                    cursor.execute(sql_query)
                    connector.commit()
                
                except sql.Error as error:
                    print(f'Error during the execution of {sql_query}', error)

            else:
                print(f'{sql_query} found nothing')


def import_languages(movie_id, category, value, connector, cursor):
    ''' This function will read all values from 'IdiomaAudio' and 'IdiomSubtitulos' columns
    in the Excel database, split them using the '-' character in the movies
    with two languages in 'Audio' or 'Subs' and then populate the tables 
    Audio_in_file and Subs_in_file with the languages found.'''

    id = []
    # To match the new values in the database these two have to be changed,
    # because in the original database they were 'May' and 'Var', instead of 'Maya' and 'Varios'
    # (see function 'get_individual_values' in /01_ImportDatabase/databaseImporter.py for reference)
    if value == 'Maya': 
        value = 'May'
    
    if value == 'Var':
        value = 'Varios'

    # Obtain corresponding LanguageID from the new 'Idioma' table for each language in 'value'
    if value != '-':
        if value.find('-') != -1:
            [lang1, lang2] = value.split('-')
            sql_query = f'SELECT id FROM Idioma WHERE IdiomaAbreviado = \'{lang1}\''
            id.append(db.execute(sql_query).fetchone()[0])

            sql_query = f'SELECT id FROM Idioma WHERE IdiomaAbreviado = \'{lang2}\''
            id.append(db.execute(sql_query).fetchone()[0])

        elif value.find('-') == -1:
            sql_query = f'SELECT id FROM Idioma WHERE IdiomaAbreviado = \'{value}\''
            id.append(db.execute(sql_query).fetchone()[0])

    # Populate Audio_in_file and Subs_in_file with the obtained values
    for i in id:
        if category == 'Audio':
            sql_query = f'INSERT INTO Audio_in_file (pelicula_id, idioma_id) VALUES ({movie_id}, {i})'

        elif category == 'Subs':
            sql_query = f'INSERT INTO Subs_in_file (pelicula_id, idioma_id) VALUES ({movie_id}, {i})'

        try:
            cursor.execute(sql_query)
            connector.commit()
        
        except sql.Error as error:
            print(f'Error during the execution of {sql_query}', error)


def obtainID(field, value):
    ''' Function to obtain the ID for a given 'value' in a given table.

    - field: Name of the table in which to look into (which is the same as the column's name within that table)
    - value: Value to look for in the database and obtain its ID.'''

    table = field
    sql_query = f'SELECT id FROM {table} WHERE {field} = \'{value}\''
    id = db.execute(sql_query).fetchone()

    return id[0]


if __name__ == '__main__':
    # Load the configuration.ini file
    config = ConfigParser()
    config.read('./config/configuration.ini')

    # Import data from Excel file (obtained from the original Access database)
    excel_path = config.get('Aux_files', 'excel_database')
    movie_database = pd.read_excel(excel_path)

    # # Connect with 'test_database' which is in [Paths] section from .ini file
    [conn, db] = dbConnector.connect_to_db('test_database')

    # Obtain IDs from database for old 'Pais', 'Disco' and 'Calidad' values
    # and update dataframe values
    for i in range(movie_database.shape[0]):
        movie_database.loc[i, 'Pais'] = obtainID('Pais', movie_database.loc[i, 'Pais'])
        movie_database.loc[i, 'Disco'] = obtainID('Disco', movie_database.loc[i, 'Disco'])
        movie_database.loc[i, 'Calidad'] = obtainID('Calidad', movie_database.loc[i, 'Calidad'])

    # Import dataFrame with updated 'Pais', 'Disco' and 'Calidad' values into SQL
    import_df_to_db(movie_database, conn, db)

    # After the old database is imported into the new one, the following can be done without breaking
    # any constraints related with FOREIGN KEYS.
    for i in range(movie_database.shape[0]):
        # Obtain Audios and Subs from 'movie_database' for each film 
        # and generate 'Audio_in_file' and 'Subs_in_file' tables
        import_languages(movie_database.loc[i, 'Id'], 'Audio', 
                            movie_database.loc[i, 'IdiomaAudio'], conn, db)

        import_languages(movie_database.loc[i, 'Id'], 'Subs', 
                            movie_database.loc[i, 'IdiomaSubtitulos'], conn, db)

        # Do the same with genres
        import_genres(movie_database.loc[i, 'Id'], movie_database.loc[i, 'Genero'], conn, db)

    print('All data imported into the new database')

    # Export values to Excel to be able to compare with the original ones to verify the process
    # See macro inside DataChecker.xlsm to verify that the imported data is the same as the original
    excel_newPath = config.get('Aux_files', 'excel_newDatabase')
    movie_database.to_excel(excel_newPath, index = False)

    db.close()
    conn.close()