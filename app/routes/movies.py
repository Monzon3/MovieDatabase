from fastapi import APIRouter
import functions.dbConnector as dbConnector
from models.movies import Movie

mov = APIRouter(prefix="/movies",
                tags=["Route for movie entries management."],
                responses={404: {"description": "Not found"}})

# Get all movies
@mov.get("/get_all_by_title", response_model=list[Movie])
async def get_full_list():
    return dbConnector.get_all_movies('Title')