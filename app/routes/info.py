from fastapi.encoders import jsonable_encoder as json
from models.auxFields import (
    Director, DirectorInDBFull, 
    Genre, GenreInDBFull,
    GenreCategory, GenreCategoryInDB, 
    Language, LanguageInDB)
from fastapi import APIRouter
import functions.dbConnector as dbConnector

info = APIRouter(prefix="/info",
                tags=["Route only to obtain info of specific fields from database"],
                responses={404: {"description": "Not found"}})

@info.get("/countries")
async def countries():
    return dbConnector.get_all('Countries')

@info.post("/countries")
async def add_country(country_name: str):
    return dbConnector.add_register('Countries', 'Country', country_name)

@info.get("/devices")
async def devices():
    return dbConnector.get_all('Storage')

@info.post("/device")
async def add_device(device_name: str):
    return dbConnector.add_register('Storage', 'Device', device_name)

@info.get("/directors")
async def directors():
    return dbConnector.get_all('Directors')

@info.post("/directors", response_model=DirectorInDBFull)
async def add_director(director: Director):
    return dbConnector.add_director(json(director))

@info.get("/genres")
async def genres():
    return dbConnector.get_all_genres()

@info.post("/genre_categories", response_model=GenreCategoryInDB)
async def add_genre_category(category: GenreCategory):
    return dbConnector.add_genre_category(json(category))

@info.post("/genres", response_model=GenreInDBFull)
async def add_genre(genre: Genre):
    return dbConnector.add_genre(json(genre))

@info.get("/languages")
async def languages():
    return dbConnector.get_all('Languages')

@info.post("/languages", response_model=LanguageInDB)
async def add_language(language: Language):
    return dbConnector.add_language(json(language))

@info.get("/qualities")
async def qualities():
    return dbConnector.get_all('Qualities')

@info.post("/quality")
async def add_quality(quality_name: str):
    return dbConnector.add_register('Qualities', 'Quality', quality_name)

@info.get("/country_in_device")
async def country_in_device(device_name:str):
    deviceID = dbConnector.get_object('Storage', 'Device', device_name)
    if deviceID:
        return dbConnector.get_combined('Countries', 'Country', 'StorageID', deviceID)
    else: 
        return f"Device '{device_name}' not found"

@info.get("/quality_in_device")
async def quality_in_device(device_name:str):
    deviceID = dbConnector.get_object('Storage', 'Device', device_name)
    if deviceID:
        return dbConnector.get_combined('Qualities', 'Quality', 'StorageID', deviceID)
    else:
        return f"Device '{device_name}' not found"

@info.get("/device_in_country")
async def device_in_country(country_name:str):
    countryID = dbConnector.get_object('Countries', 'Country', country_name)
    if countryID:
        return dbConnector.get_combined('Storage', 'Device', 'CountryID', countryID)
    else:
        return f"Country '{country_name}' not found"