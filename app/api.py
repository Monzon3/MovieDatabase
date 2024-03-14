from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
import functions.dbConnector as dbConnector
import os
from routes.info import info
from routes.movies import mov
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
app.include_router(info)
app.include_router(mov)

@app.get("/")
async def root():
    return {"Info": "Go to /docs URL for more info on the API"}