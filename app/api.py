from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from routes.cars import car
from routes.configs import cfg
from routes.projects import prj
from routes.usages import usg
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

@app.get("/")
async def root():
    return {"Info": "Go to /docs URL for more info on the API"}