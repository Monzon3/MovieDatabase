from fastapi import APIRouter, status
from fastapi.encoders import jsonable_encoder as json
import functions.dbConnector as dbConnector
from models.other import (
    Country, CountryInDB,
    Device, DeviceInDB,
    Director, DirectorInDB, 
    Genre, GenreInDBFull,
    GenreCategory, GenreCategoryInDB, 
    Language, LanguageInDB)

oth = APIRouter(prefix="/other",
                tags=["Route for secondary tables management"],
                responses={404: {"description": "Not found"}})

@oth.get("/countries", response_model=list[CountryInDB], status_code=status.HTTP_200_OK)
async def countries():
    return dbConnector.get_all("Countries")

@oth.post("/countries", response_model=CountryInDB, status_code=status.HTTP_201_CREATED)
async def add_country(country: Country):
    return dbConnector.add_register("Countries", "Country", country.country)

@oth.get("/devices", response_model=list[DeviceInDB], status_code=status.HTTP_200_OK)
async def devices():
    return dbConnector.get_all("Storage")

@oth.post("/device", response_model=DeviceInDB, status_code=status.HTTP_201_CREATED)
async def add_device(device: Device):
    return dbConnector.add_register("Storage", "Device", device.device)

@oth.get("/directors", response_model=list[DirectorInDB], status_code=status.HTTP_200_OK)
async def directors():
    return dbConnector.get_all("Directors")

@oth.post("/directors", response_model=DirectorInDB, status_code=status.HTTP_201_CREATED)
async def add_director(director: Director):
    return dbConnector.add_director(json(director))

@oth.get("/genres", response_model=list[GenreInDBFull], status_code=status.HTTP_200_OK)
async def genres():
    return dbConnector.get_all("Genres")

@oth.post("/genre_categories", response_model=GenreCategoryInDB)
async def add_genre_category(category: GenreCategory):
    return dbConnector.add_genre_category(json(category))

@oth.post("/genres", response_model=GenreInDBFull)
async def add_genre(genre: Genre):
    return dbConnector.add_genre(json(genre))

@oth.get("/languages")
async def languages():
    return dbConnector.get_all('Languages')

@oth.post("/languages", response_model=LanguageInDB)
async def add_language(language: Language):
    return dbConnector.add_language(json(language))

@oth.get("/qualities")
async def qualities():
    return dbConnector.get_all('Qualities')

@oth.post("/quality")
async def add_quality(quality_name: str):
    return dbConnector.add_register('Qualities', 'Quality', quality_name)

@oth.get("/country_in_device")
async def country_in_device(device_name:str):
    deviceID = dbConnector.get_object('Storage', 'Device', device_name)
    if deviceID:
        return dbConnector.get_combined('Countries', 'Country', 'StorageID', deviceID)
    else: 
        return f"Device '{device_name}' not found"

@oth.get("/quality_in_device")
async def quality_in_device(device_name:str):
    deviceID = dbConnector.get_object('Storage', 'Device', device_name)
    if deviceID:
        return dbConnector.get_combined('Qualities', 'Quality', 'StorageID', deviceID)
    else:
        return f"Device '{device_name}' not found"

@oth.get("/device_in_country")
async def device_in_country(country_name:str):
    countryID = dbConnector.get_object('Countries', 'Country', country_name)
    if countryID:
        return dbConnector.get_combined('Storage', 'Device', 'CountryID', countryID)
    else:
        return f"Country '{country_name}' not found"