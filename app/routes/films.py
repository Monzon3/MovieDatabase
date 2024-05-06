from fastapi import APIRouter, Depends, status
from fastapi.encoders import jsonable_encoder as json
import functions.dbConnector as dbConnector
from models.films import Film, FilmFull
from services.auth import get_current_active_user

flm = APIRouter(prefix="/films",
                tags=["Route for film entries management."],
                responses={404: {"description": "Not found"}})

# Get all films
@flm.get("/get_all_by_title", response_model=list[FilmFull], 
         dependencies=[Depends(get_current_active_user)],
         status_code = status.HTTP_200_OK)
async def get_full_list():
    return dbConnector.get_all_films("Title", "ASC")

@flm.get("/get_all_by_year", response_model=list[FilmFull], 
         dependencies=[Depends(get_current_active_user)],
         status_code = status.HTTP_200_OK)
async def get_full_list():
    return dbConnector.get_all_films("Year", "DESC")

@flm.get("/get_all_by_score", response_model=list[FilmFull], 
         dependencies=[Depends(get_current_active_user)],
         status_code = status.HTTP_200_OK)
async def get_full_list():
    return dbConnector.get_all_films("Score", "DESC")

@flm.post("/", response_model=list[FilmFull], 
          dependencies=[Depends(get_current_active_user)],
          status_code = status.HTTP_200_OK)
async def get_film(film: Film):
    return dbConnector.get_film(json(film))