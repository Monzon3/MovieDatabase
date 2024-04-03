from pydantic import BaseModel, Field
from typing import Optional


class FilmFull(BaseModel):
    # Min and max values should match those in the definition of the database
    id: int
    title: str = Field(min_length=1, max_length = 100)
    origTitle: str = Field(min_length=1, max_lenth=100)
    storageDevice: str = Field(min_length=1, max_length=20)
    quality: str = Field(min_length=1, max_length=10)
    #audio: Optional[str] = Field(min_length=0, max_length=6)
    #subs: Optional[str] = Field(min_length=0, max_length=6)
    year: Optional[int] = Field(ge=1880, le=2100)
    country: str = Field(min_length=1, max_length=25)
    length: Optional[int] = Field(ge=0)
    #director: str = Field(min_length=1, max_lenght=200)
    screenplay: Optional[str] = Field(min_length=0, max_length=300)
    score: Optional[int] = Field(ge=0, le=10)
    #genre: Optional[str] = Field(min_length=0, max_length=300)
    img: Optional[str] = Field(min_length=0, max_length=120)

class Film(BaseModel):
    title: str = Field(max_length = 100, default="")
    origTitle: Optional[str] = Field(max_lenth=100, default="")
    storageDevice: Optional[str] = Field(max_length=20, default="")
    quality: Optional[str] = Field(max_length=10, default="")
    #audio: Optional[str] = Field(min_length=0, max_length=6, default="")
    #subs: Optional[str] = Field(min_length=0, max_length=6, default="")
    year1: Optional[int] = Field(ge=1880, le=2100, default = None)
    year2: Optional[int] = Field(ge=1880, le=2100, default = None)
    country: Optional[str] = Field(max_length=25, default="")
    length: Optional[str] = Field(default="")
    #director: Optional[str] = Field(min_length=1, max_lenght=200, default="")
    screenplay: Optional[str] = Field(max_length=300, default="")
    score1: Optional[int] = Field(ge=0, le=10, default=None)
    score2: Optional[int] = Field(ge=0, le=10, default=None)
    #genre: Optional[str] = Field(min_length=0, max_length=300, default="")

class FilmInDB(Film):
    id: int