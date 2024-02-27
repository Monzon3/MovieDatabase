from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
import functions.dbConnector as dbConnector
import os

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

[conn, db] = dbConnector.connect_to_db()    # Object to connect with MySQL

@app.get("/")
async def root():
    return {"Info": "Go to /docs URL for more info on the API"}

@app.get("/test")
async def test():
    return {'a': 'b'}