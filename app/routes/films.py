from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder as json
import functions.dbConnector as dbConnector
from models.films import Film, FilmFull

flm = APIRouter(prefix="/films",
                tags=["Route for film entries management."],
                responses={404: {"description": "Not found"}})

# Get all films
@flm.get("/get_all_by_title", response_model=list[FilmFull])
async def get_full_list():
    return dbConnector.get_all_films('Title')

@flm.get("/get_all_by_year", response_model=list[FilmFull])
async def get_full_list():
    return dbConnector.get_all_films('Year')

@flm.get("/get_all_by_score", response_model=list[FilmFull])
async def get_full_list():
    return dbConnector.get_all_films('Score')

@flm.post("/")
async def get_film(film: Film):
    return dbConnector.get_film(json(film))