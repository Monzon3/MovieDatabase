from pydantic import BaseModel, Field
from typing import Optional


class User(BaseModel):
    username: str = Field(description="The username cannot be empty", 
                          pattern=r"[0-9A-Za-z_]", 
                          min_length=1, max_length=20)
    password: str = Field(description="The password cannot be empty", min_length=1)
    email: str = Field(example="valid_email@server.com",
                       pattern=r"^\w+([.-]?\w+)*@\w+([.-]?\w+)*(\.\w{2,3})+$")
    user_rank: int
    disabled: Optional[bool] = False


class UserInDB(User):
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