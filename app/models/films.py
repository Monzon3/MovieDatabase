from pydantic import BaseModel, Field
from typing import Optional


class Film(BaseModel):
    # Min and max values should match those in the definition of the database
    title: str = Field(min_length=1, max_length = 100)
    origTitle: str = Field(min_length=1, max_lenth=100)
    storage_device: str = Field(min_length=1, max_length=20)
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

class FilmInDB(Film):
    id: int