from pydantic import BaseModel, Field
from typing import Literal, Optional


#class AdminUpdatedUser(BaseModel):
#    username: Optional[str] = Field(description="The username cannot be empty", min_length=1, default=None)
#    email: Optional[str] = Field(example="valid_email@ficosa.com",
#                                 regex=r"^\w+([.-]?\w+)*@\w+([.-]?\w+)*(\.\w{2,3})+$", default=None)
#    full_name: Optional[str] = None
#    rank: Literal["user", "powerUser", "admin"] = None


class User(BaseModel):
    username: str = Field(description="The username cannot be empty", 
                          pattern=r"[0-9A-Za-z_]", 
                          min_length=1, max_length=20)
    email: Optional[str] = Field(example="valid_email@server.com",
                                 pattern=r"^\w+([.-]?\w+)*@\w+([.-]?\w+)*(\.\w{2,3})+$", default=None)
    user_rank: Literal["user", "admin"] = "user"
    disabled: Optional[bool] = False
    deleted: Optional[bool] = False


class NewUser(User):
    password: str = Field(description="The password cannot be empty", min_length=1)


#class UpdatedUser(BaseModel):
#    email: Optional[str] = Field(example="valid_email@ficosa.com",
#                                 regex=r"^\w+([.-]?\w+)*@\w+([.-]?\w+)*(\.\w{2,3})+$", default=None)
#    full_name: Optional[str] = None
#    password: Optional[str] = Field(description="The password cannot be empty", min_length=1, default=None)


class UserInDB(User):
    id: int