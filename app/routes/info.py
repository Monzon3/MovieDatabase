from fastapi import APIRouter, HTTPException
import functions.dbConnector as dbConnector

info = APIRouter(prefix="/info",
                tags=["Route only to obtain info of specific fields from database"],
                responses={404: {"description": "Not found"}})

@info.get("/devices")
async def devices():
    return dbConnector.get_all('Storage')

@info.get("/qualities")
async def qualities():
    return dbConnector.get_all('Qualities')

@info.get("/countries")
async def countries():
    return dbConnector.get_all('Countries')

@info.get("/languages")
async def languages():
    return dbConnector.get_all('Languages')

@info.get("/genres")
async def genres():
    return dbConnector.get_all_genres()

@info.get("/quality_in_device")
async def quality_in_device(device_name:str):
    deviceID = dbConnector.get_object('Storage', 'Device', device_name)
    if deviceID:
        return dbConnector.get_combined('Qualities', 'Quality', 'StorageID', deviceID)
    else:
        raise HTTPException(status_code=403)

@info.get("/country_in_device")
async def country_in_device(device_name:str):
    deviceID = dbConnector.get_object('Storage', 'Device', device_name)
    if deviceID:
        return dbConnector.get_combined('Countries', 'Country', 'StorageID', deviceID)
    else: 
        raise HTTPException(status_code=403)

@info.get("/device_in_country")
async def device_in_country(country_name:str):
    countryID = dbConnector.get_object('Countries', 'Country', country_name)
    if countryID:
        return dbConnector.get_combined('Storage', 'Device', 'CountryID', countryID)
    else:
        raise HTTPException(status_code=403)