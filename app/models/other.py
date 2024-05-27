from pydantic import BaseModel, Field
from typing import Optional

class Country(BaseModel):
    name: str = Field(max_length=25, description="Name of the country")

class CountryInDB(Country):
    id: int

class Device(BaseModel):
    name: str = Field(max_length=20, description="Name of the storage device")

class DeviceInDB(Device):
    id: int

class Director(BaseModel):
    # Max values should match those in the definition of the database
    name: str = Field(max_length=200)
    country: str = Field(max_length=25)

class DirectorInDB(Director):
    id: int

class Genre(BaseModel):
    name: str = Field(min_length=1, max_length=40)
    category: str = Field(min_length=1, max_length=15)

class GenreInDB(Genre):
    id: int

class GenreCategory(BaseModel):
    name: str = Field(min_length=1, max_length=15)

class GenreCategoryInDB(GenreCategory):
    id: int

class Language(BaseModel):
    # Min and max values should match those in the definition of the database
    short: str = Field(min_length=3, max_length=6)
    complete: str = Field(max_length=15)

class LanguageInDB(Language):
    id: int

class Quality(BaseModel):
    name: str = Field(max_length=10, description="Quality description")

class QualityInDB(Quality):
    id: int