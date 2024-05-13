from pydantic import BaseModel, Field
from typing import Literal, Optional

class UpdatedUser(BaseModel):
    Name: Optional[str] = Field(description="The username cannot be empty", 
                          pattern=r"[0-9A-Za-z_]", 
                          min_length=1, max_length=20, default=None)
    Email: Optional[str] = Field(example="valid_email@server.com",
                       pattern=r"^\w+([.-]?\w+)*@\w+([.-]?\w+)*(\.\w{2,3})+$",
                       default=None)
    Password: Optional[str] = Field(description="The password cannot be empty", min_length=1,
                                    default=None)
    RankID: Literal[1, 2, 3] = None
    Disabled: Optional[bool] = False

class UserSecure(BaseModel):
    username: str = Field(description="The username cannot be empty", 
                          pattern=r"[0-9A-Za-z_]", 
                          min_length=1, max_length=20)
    email: str = Field(example="valid_email@server.com",
                       pattern=r"^\w+([.-]?\w+)*@\w+([.-]?\w+)*(\.\w{2,3})+$")
    user_rank: Literal["admin", "powerUser", "user"]
    disabled: Optional[bool] = False

class User(UserSecure):
    password: str = Field(description="The password cannot be empty", min_length=1)

class UserInDB(UserSecure):
    id: int


# Token-related classes
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None


#class UpdatedUser(BaseModel):
#    email: Optional[str] = Field(example="valid_email@ficosa.com",
#                                 regex=r"^\w+([.-]?\w+)*@\w+([.-]?\w+)*(\.\w{2,3})+$", default=None)
#    full_name: Optional[str] = None
#    password: Optional[str] = Field(description="The password cannot be empty", min_length=1, default=None)


#class AdminUpdatedUser(BaseModel):
#    username: Optional[str] = Field(description="The username cannot be empty", min_length=1, default=None)
#    email: Optional[str] = Field(example="valid_email@ficosa.com",
#                                 regex=r"^\w+([.-]?\w+)*@\w+([.-]?\w+)*(\.\w{2,3})+$", default=None)
#    full_name: Optional[str] = None
#    rank: Literal["user", "powerUser", "admin"] = None