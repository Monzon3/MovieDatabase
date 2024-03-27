from fastapi import APIRouter
import functions.dbConnector as dbConnector
from models.films import Film

flm = APIRouter(prefix="/films",
                tags=["Route for film entries management."],
                responses={404: {"description": "Not found"}})

# Get all films
@flm.get("/get_all_by_title", response_model=list[Film])
async def get_full_list():
    return dbConnector.get_all_films('Title')