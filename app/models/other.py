from pydantic import BaseModel, Field
from typing import Optional

class Country(BaseModel):
    id: Optional[int] = None
    name: str = Field(max_length=25, description="Name of the country")

class Device(BaseModel):
    id: Optional[int] = None
    name: str = Field(max_length=20, description="Name of the storage device")

class Director(BaseModel):
    id: Optional[int] = None
    # Max values should match those in the definition of the database
    name: str = Field(max_length=200)
    country: Optional[str] = Field(max_length=25, default=None)

class Genre(BaseModel):
    id: Optional[int] = None
    name: str = Field(min_length=1, max_length=40)
    category: str = Field(min_length=1, max_length=15)

class GenreCategory(BaseModel):
    id: Optional[int] = None
    name: str = Field(min_length=1, max_length=15)

class Language(BaseModel):
    id: Optional[int] = None
    # Min and max values should match those in the definition of the database
    short: str = Field(min_length=3, max_length=6)
    complete: str = Field(max_length=15)

class Quality(BaseModel):
    id: Optional[int] = None
    name: str = Field(max_length=10, description="Quality description")