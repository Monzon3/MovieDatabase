from pydantic import BaseModel, Field


class Director(BaseModel):
    # Min and max values should match those in the definition of the database
    name: str = Field(min_length=1, max_length=200)
    country: str = Field(min_length=1, max_length=25)

class DirectorInDBFull(Director):
    id: int

class Genre(BaseModel):
    name: str = Field(min_length=1, max_length=40)
    category: str = Field(min_length=1, max_length=15)

class GenreInDBFull(Genre):
    id: int

class GenreCategory(BaseModel):
    name: str = Field(min_length=1, max_length=15)

class GenreCategoryInDB(GenreCategory):
    id: int

class Language(BaseModel):
    # Min and max values should match those in the definition of the database
    short: str = Field(min_length=3, max_length=6)
    complete: str = Field(min_length=1, max_length=15)

class LanguageInDB(Language):
    id: int