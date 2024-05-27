from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from routes.films import flm
from routes.other import oth
from routes.users import usr

description = """
## This is an API to manage the Movie database 2024."""

app = FastAPI(
    title="Movie Database API",
    version=os.getenv("TAG").replace(":", ""),
    description=description,
    contact={"name": "Sergio Monzón", "email": "sergio.monzon3@gmail.com"}
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
app.include_router(oth)
app.include_router(flm)

@app.get("/")
async def root():
    return {"Info": "Go to /docs URL for more info on the API"}