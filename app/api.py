from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
import functions.dbConnector as dbConnector
import os
from routes.users import usr

description = """
## This is an API to manage the Movie database 2024.

"""

app = FastAPI(
    title="Movie Database API",
    version=os.getenv("TAG").replace(":", ""),
    description=description,
)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(usr)

@app.get("/")
async def root():
    return {"Info": "Go to /docs URL for more info on the API"}

@app.get("/devices")
async def devices():
    return dbConnector.get_all('Storage')

@app.get("/qualities")
async def qualities():
    return dbConnector.get_all('Qualities')

@app.get("/countries")
async def countries():
    return dbConnector.get_all('Countries')

@app.get("/genres")
async def genres():
    return dbConnector.get_all_genres()

@app.get("/quality_in_device")
async def quality_in_device():
    return {'quality_in_device'}

@app.get("/country_in_device")
async def country_in_device():
    return {'country_in_device'}

@app.get("/device_in_country")
async def device_in_country():
    return {'device_in_country'}