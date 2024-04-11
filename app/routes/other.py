from fastapi import APIRouter, HTTPException, status
from fastapi.encoders import jsonable_encoder as json
import functions.dbConnector as dbConnector
from models.other import (
    Country, CountryInDB,
    Device, DeviceInDB,
    Director, DirectorInDB, 
    Genre, GenreInDBFull,
    GenreCategory, GenreCategoryInDB, 
    Language, LanguageInDB, 
    Quality, QualityInDB)

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

@oth.post("/devices", response_model=DeviceInDB, status_code=status.HTTP_201_CREATED)
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

@oth.post("/genre_categories", response_model=GenreCategoryInDB, status_code=status.HTTP_201_CREATED)
async def add_genre_category(category: GenreCategory):
    return dbConnector.add_genre_category(json(category))

@oth.post("/genres", response_model=GenreInDBFull, status_code=status.HTTP_201_CREATED)
async def add_genre(genre: Genre):
    return dbConnector.add_genre(json(genre))

@oth.get("/languages", response_model=list[LanguageInDB], status_code=status.HTTP_200_OK)
async def languages():
    return dbConnector.get_all('Languages')

@oth.post("/languages", response_model=LanguageInDB, status_code=status.HTTP_201_CREATED)
async def add_language(language: Language):
    return dbConnector.add_language(json(language))

@oth.get("/qualities", response_model=list[QualityInDB], status_code=status.HTTP_200_OK)
async def qualities():
    return dbConnector.get_all('Qualities')

@oth.post("/qualities", response_model=QualityInDB, status_code=status.HTTP_201_CREATED)
async def add_quality(quality: Quality):
    return dbConnector.add_register('Qualities', 'Quality', quality.quality)

@oth.get("/country_in_device", response_model=list[CountryInDB], status_code=status.HTTP_200_OK)
async def country_in_device(device: Device):
    deviceID = dbConnector.get_object('Storage', 'Device', device.device)
    if deviceID:
        return dbConnector.get_combined('Countries', 'Country', 'DeviceID', deviceID)
    else: 
        raise HTTPException (status_code = 404, detail=f"Requested device is not in the database.")

@oth.get("/quality_in_device", response_model=list[QualityInDB], status_code=status.HTTP_200_OK)
async def quality_in_device(device: Device):
    deviceID = dbConnector.get_object('Storage', 'Device', device.device)
    if deviceID:
        return dbConnector.get_combined('Qualities', 'Quality', 'DeviceID', deviceID)
    else:
        raise HTTPException (status_code = 404, detail=f"Requested device is not in the database.")

@oth.get("/device_in_country", response_model=list[DeviceInDB], status_code=status.HTTP_200_OK)
async def device_in_country(country: Country):
    countryID = dbConnector.get_object('Countries', 'Country', country.country)
    if countryID:
        return dbConnector.get_combined('Storage', 'Device', 'CountryID', countryID)
    else:
        raise HTTPException (status_code = 404, detail=f"Requested country is not in the database.")