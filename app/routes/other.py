from fastapi import APIRouter, Depends, HTTPException, status
import functions.dbConnector as dbConnector
from models.other import *
from services.auth import check_admin, get_current_active_user

oth = APIRouter(prefix="/other",
                tags=["Route for secondary tables management"],
                responses={404: {"description": "Not found"}})

@oth.get("/countries", response_model=list[Country], dependencies=[Depends(get_current_active_user)],
         status_code=status.HTTP_200_OK)
async def countries():
    return dbConnector.get_all("Countries")

@oth.post("/countries", response_model=Country, dependencies=[Depends(check_admin)],
          status_code=status.HTTP_201_CREATED)
async def add_country(country: Country):
    return dbConnector.add_register("Countries", country.name)

@oth.get("/devices", response_model=list[Device], dependencies=[Depends(get_current_active_user)],
         status_code=status.HTTP_200_OK)
async def devices():
    return dbConnector.get_all("Storage")

@oth.post("/devices", response_model=Device, dependencies=[Depends(check_admin)],
          status_code=status.HTTP_201_CREATED)
async def add_device(device: Device):
    return dbConnector.add_register("Storage", device.name)

@oth.get("/directors", response_model=list[Director], dependencies=[Depends(get_current_active_user)],
         status_code=status.HTTP_200_OK)
async def directors():
    return dbConnector.get_all("Directors")

@oth.post("/directors", response_model=Director, dependencies=[Depends(check_admin)],
          status_code=status.HTTP_201_CREATED)
async def add_director(director: Director):
    [_, db] = dbConnector.connect_to_db()
    db.execute(f"SELECT Countries.id FROM Countries WHERE Countries.Name='{director.country}'")
    res = db.fetchone()
    if director.country == None:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, 
                            detail="'Country' cannot be empty.")    
    if res:
        return dbConnector.add_director(director.dict())
    else:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, 
                            detail=f"No country named '{director.country}' found in the database.")

@oth.get("/genres", response_model=list[Genre], dependencies=[Depends(get_current_active_user)],
         status_code=status.HTTP_200_OK)
async def genres():
    return dbConnector.get_all("Genres")

@oth.post("/genre_categories", response_model=GenreCategory, dependencies=[Depends(check_admin)],
          status_code=status.HTTP_201_CREATED)
async def add_genre_category(category: GenreCategory):
    return dbConnector.add_genre_category(category.dict())

@oth.post("/genres", response_model=Genre, dependencies=[Depends(check_admin)],
          status_code=status.HTTP_201_CREATED)
async def add_genre(genre: Genre):
    return dbConnector.add_genre(genre.dict())

@oth.get("/languages", response_model=list[Language], dependencies=[Depends(get_current_active_user)],
         status_code=status.HTTP_200_OK)
async def languages():
    return dbConnector.get_all('Languages')

@oth.post("/languages", response_model=Language, dependencies=[Depends(check_admin)],
          status_code=status.HTTP_201_CREATED)
async def add_language(language: Language):
    return dbConnector.add_language(language.dict())

@oth.get("/qualities", response_model=list[Quality], dependencies=[Depends(get_current_active_user)],
         status_code=status.HTTP_200_OK)
async def qualities():
    return dbConnector.get_all('Qualities')

@oth.post("/qualities", response_model=Quality, dependencies=[Depends(check_admin)],
          status_code=status.HTTP_201_CREATED)
async def add_quality(quality: Quality):
    return dbConnector.add_register('Qualities', quality.name)

@oth.post("/country_in_device", response_model=list[Country], dependencies=[Depends(get_current_active_user)],
         status_code=status.HTTP_200_OK)
async def country_in_device(device: Device):
    deviceID = dbConnector.get_object('Storage', device.name)
    if deviceID:
        return dbConnector.get_combined('Countries', 'StorageID', deviceID)
    else: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Requested device is not in the database.")

@oth.post("/quality_in_device", response_model=list[Quality], dependencies=[Depends(get_current_active_user)],
         status_code=status.HTTP_200_OK)
async def quality_in_device(device: Device):
    deviceID = dbConnector.get_object('Storage', device.name)
    if deviceID:
        return dbConnector.get_combined('Qualities', 'StorageID', deviceID)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Requested device is not in the database.")

@oth.post("/device_in_country", response_model=list[Device], dependencies=[Depends(get_current_active_user)],
         status_code=status.HTTP_200_OK)
async def device_in_country(country: Country):
    countryID = dbConnector.get_object('Countries', country.name)
    if countryID:
        return dbConnector.get_combined('Storage', 'CountryID', countryID)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Requested country is not in the database.")